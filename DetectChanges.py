# ---------------------------------------------------------------------------------------------------------------------
# Name:        DetectChanges.py  
# Purpose:      detect and report changes in feature services
#
# Notes:        Uses python 3.x but should work with 2.x (not tested) *IF* requests module is installed
#
# Author:       ESRI Applications Prototype Lab
#
# Created:      7/26/2017
#               Change to send an email for each update
# 10/27/2017    Correct token errors
#               Correct for multiple email recipients
#               Change referrer to machine ip address
# 11/28/2017    Add function to print errors to log file
#               Remove messagefile.txt from config file
#               Check for valid user/pw
#               Update statuslist for completion
# ---------------------------------------------------------------------------------------------------------------------
import os
import socket
import datetime
import smtplib
from email.message import EmailMessage
import requests
import json
import sys


def main(cfile):
    starttime = gettime()

    # completion status list
    statuslist = ['Completed', 'Failed']

    # Build some paths
    scriptpath = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    messagepath = os.path.join(scriptpath, 'generations')

    # check for existence of 'generations' folder
    if not os.path.exists(messagepath):
        os.mkdir(messagepath)

    # Change modes include ANY, UPDATE and ADD
    changemode = 'ANY'

    # Get the configuration information
    cfg = json.load(open(cfile))
    fsurl = cfg['service']['fsURL'].replace('http:','https')
    viewerurl = cfg['service']['viewerURL']
    mapViewerLevel= cfg['service']['viewerMapLevel']

    # URL information
    sharingurl = 'https://www.arcgis.com/sharing/rest'
    mapurl = '{}?url={}&level={}&center='.format(viewerurl, fsurl, mapViewerLevel)

    # Get a token
    referingclient = socket.gethostbyname(socket.gethostname())
    servicetoken = getToken(sharingurl, cfg['service']['serviceuser'],
                            cfg['service']['servicepw'], referingclient)

    # Check url and get service info
    urlLyr = '{}/{}'.format(fsurl, cfg['service']['fsLayerNum'])
    serviceinfo = requests.request('GET', '{}?f=pjson&token={}'.format(urlLyr, servicetoken))
    si = serviceinfo.json()

    try:
        capabilities = si['capabilities']
    except:
        errlogname = generrlogname()
        emsg = 'Cannot access Capabilities ({}) \nPlease enable Change Tracking capabilities in the Feature Service\n{}'.format(si['error']['message'],fsurl)
        print(emsg)
        writeerror(errlogname, emsg)
        return

    if capabilities.find('ChangeTracking') < 0:
        errlogname = generrlogname()
        emsg = 'Change Tracking not enabled in the Feature Service\nPlease enable Change Tracking capabilities in the Feature Service\n{}'.format(fsurl)
        print(emsg)
        writeerror(errlogname, emsg)
        return

    # Get the editor fields and all fields
    edfieldsDict = si['editFieldsInfo']
    fieldsList = si['fields']
    fieldsDict = {}
    for f in fieldsList:
        fieldsDict[f['name']] = f

    # Read the previous layer server gens file if it exists
    layergensname = cfg['filenames']['layergens']
    if os.path.exists(os.path.join(messagepath, layergensname)):
        changetrackinfo = readcachefile(os.path.join(messagepath, layergensname))
    else:
        # Get layer gens from the service and date
        changetrackinfo = returnupdates(fsurl,servicetoken)

    # Extract changes
    result = extractchanges(fsurl, cfg['service']['fsLayerNum'], changemode, changetrackinfo['layerServerGens'], servicetoken)
    code = result.status_code
    if code != 200:
        errlogname = generrlogname()
        emsg = result.reason
        print('Extract Changes request failed: {}'.format(emsg))
        writeerror(errlogname, emsg)
        return

    # Result is async so stay here until it is complete
    resultjson = result.json()
    resurl = resultjson['statusUrl']
    resurl = '{}?token={}'.format(resurl, servicetoken)
    done = False
    while not done:
        result = requests.get(resurl, params='f=json')
        resultjs = result.json()
        if 'status' in resultjs:
            if resultjs['status'] in statuslist:
                done = True
                print('Status = {}'.format(resultjs['status']))
        else:
            # an error occurred
            errlogname = generrlogname()
            if 'error' in resultjs:
                emsg = resultjs['error']['message']
                print('Error: {}'.format(emsg))
                writeerror(errlogname, emsg)
                return 'Operation failed . . . returning'
            else:
                emsg = resultjs
                print(emsg)
                writeerror(errlogname, emsg)
                return 'Operation failed . . . returning'

    # Are there changes?
    print('Checking the result')
    changetype = resultjs['responseType']
    resultjson = getresult('{}?token={}'.format(resultjs['resultUrl'], servicetoken))
    newlayergens = {'layerServerGens': resultjson['layerServerGens']}

    if changetype == 'esriDataChangesResponseTypeNoEdits':
        print('\tThere have been no changes to the service')
        # write the servergens file
        writecachefile(newlayergens, os.path.join(messagepath, layergensname))
        return
    else:
        print('\tThere were edits to the service')

    edits = resultjson['edits'][0]
    features = edits['features']

    # Send an email for each add or update
    writemessages(features, cfg, mapurl, fieldsDict, edfieldsDict)

    # Write the lyrgens object to disk in the tools folder -
    writecachefile(newlayergens, os.path.join(messagepath, layergensname))

    printelapsedtime(starttime, gettime())

    return


def getToken(baseURL, username, password, referrer):
    url = baseURL + '/generateToken'
    postData = {
        'username': username,
        'password': password,
        'client': 'referer',
        'referer': referrer,
        'expiration': 60,
        'f': 'json'}
    r = requests.post(url, verify=True, data=postData)
    rjson = r.json()
    if 'token' in rjson:
        return rjson['token']
    elif 'error' in rjson:
        errlogname = generrlogname()
        emsg = '{}\n{}\n\n(in getToken)'.format(rjson['error']['message'], rjson['error']['details'][0])
        writeerror(errlogname, emsg)
        sys.exit('1 {}'.format(rjson['error']['message']))


def returnupdates(theurl,token):
    r = requests.post('{}?f=json&token={}&returnUpdates=true'.format(theurl,token))
    rjson = r.json()
    try:
        changetrackinfo = rjson['changeTrackingInfo']
        return changetrackinfo
    except:
        errlogname = generrlogname()
        emsg = 'Error in return updates'
        writeerror(errlogname, emsg)
        sys.exit('Error in returnupdates')


def extractchanges(theurl, lyrnum, mode, layergens, token):
    exturl = '{}/extractChanges?token={}'.format(theurl, token)
    if mode == 'ADD':
        data = {'layers': lyrnum,
                'returnInserts': 'true',
                'returnUpdates': 'false',
                'returnDeletes': 'false',
                'layerServerGens': json.dumps(layergens),
                'dataFormat': 'json',
                'f': 'json',
                'returnAttachments': 'false',
                'returnAttachmentsByUrl': 'false'}
    elif mode == 'ANY':
        data = {'layers': lyrnum,
                'returnInserts': True,
                'returnUpdates': True,
                'returnDeletes': True,
                'layerServerGens': json.dumps(layergens),
                'dataFormat': 'json',
                'f': 'json',
                'returnAttachments': False,
                'returnAttachmentsByUrl': False}
    elif mode == 'UPDATE':
        data = {'layers': lyrnum,
                'returnInserts': 'false',
                'returnUpdates': 'true',
                'returnDeletes': 'false',
                'layerServerGens': json.dumps(layergens),
                'dataFormat': 'json',
                'f': 'json',
                'returnAttachments': 'false',
                'returnAttachmentsByUrl': 'false'}
    r = requests.post(exturl, data=data)
    return r


def writemessages(feats, cfg, msgurl, fDict, eDict):
    # Get the features that have been modified, deleted or added
    adds = feats['adds']
    deletes = feats['deleteIds']
    updates = feats['updates']

    if len(adds) > 0:
        themsg = 'The following new incident has been added:'
        parseattributes(adds, cfg, fDict, msgurl, themsg)

    if len(updates) > 0:
        themsg = 'The following incident has been updated:'
        parseattributes(updates, cfg, fDict, msgurl, themsg)

    if len(deletes) > 0:
        # Get a new message
        msg = returnmessage(cfg)
        msg = msg + '{} incidents have been deleted.\n'.format(len(deletes))
        for f in deletes:
            msg = msg + '\t{}\n'.format(f)

        sendMail(cfg['email']['server'], msg, cfg['email']['recipients'], cfg['email']['from'],
                 cfg['email']['subject'])

    return


def parseattributes(feats, cfg, fDict, msgurl,  message):
    for i in feats:
        # Get a new message
        msg = returnmessage(cfg)
        msg = msg + '{}\n'.format(message)

        atts = i['attributes']
        geom = i['geometry']
        newx = geom['x']
        newy = geom['y']

        # write additions
        for f in atts.keys():  # this is a dictionary so it will be atts[f]
            if f not in ['objectid', 'globalid']:
                falias = fDict[f]['alias']
                val = ''
                if fDict[f]['type'] == 'esriFieldTypeDate':
                    if atts[f]:
                        val = datetime.datetime.fromtimestamp(atts[f] / 1000.).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    val = atts[f]
                msg = msg + '\t{}: {}\n'.format(falias, val)
        msg = msg + '\tIncident Location: {}{},{}\n'.format(msgurl, newx, newy)
        msg = msg + '\n'
        sendMail(cfg['email']['server'], msg, cfg['email']['recipients'], cfg['email']['from'],
                 cfg['email']['subject'])
    return


def sendMail(srvrInfo, messagetext, eMailTo, eMailFrom, eMailSubject):
    servername = srvrInfo[0].lower()
    try:
            
        if eMailTo[0].index("@") > 0:

                        
            msg = EmailMessage()
            server = smtplib.SMTP(servername,srvrInfo[1])
            server.ehlo()
            server.starttls()
            if servername=="smtp.gmail.com":
                server.login(srvrInfo[2],srvrInfo[3])

            msg['From'] = eMailFrom
            msg['To'] = eMailTo
            msg['Subject'] = eMailSubject

            msg.set_content(messagetext)

            # send it
            server.sendmail(eMailFrom, eMailTo, msg.as_string())
            server.close()
    except:
        errlogname = generrlogname()
        emsg = 'An email error occurred (in sendMail) while attempting to connect to: {} \nPlease ensure your Mail Server Host and port are set correctly in your Init.json file'.format(servername)
        writeerror(errlogname, emsg)
        pass

def generrlogname ():
    errlogname = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__))),
                              'Error{}.txt'.format(datetime.datetime.strftime(datetime.datetime.now(),
                                                                              '%Y%m%d_%H_%M_%S')))
    return errlogname


def returnmessage(thecfg):
    msg = thecfg['email']['text']
    msg = msg + '\t{}\n'.format(thecfg['service']['fsURL']).replace('http:','https:')
    msg = msg + '\n'
    return msg


def getresult(theurl):
    try:
        r = requests.get(theurl)
        rj = r.json()
    except:
        errlogname = generrlogname()
        emsg = 'An error occurred retrieving the result (in getresult)\ntheurl={}'.format(theurl)
        print(emsg)
        writeerror(errlogname, emsg)
        sys.exit('3 An error with the result URL occurred')
    return rj


def writecachefile(data, filename):
    with open(filename, 'w') as out:
        json.dump(data, out)


def readcachefile(filename):
    with open(filename, 'r') as out:
        lines = json.load(out)
    return lines


def parsefile(infile):
    with open(infile, 'r') as myfile:
        data = myfile.read()
    return data

def timediff(stime, etime):
    return etime - stime


def printelapsedtime(stime, etime):
    print('\n\nElapsed time: {}'.format(etime - stime))


def writeerror(errfile, msg):
    with open(errfile, 'w') as outfile:
        outfile.write(msg)
    return


def gettime():
    return datetime.datetime.now()


if __name__ == '__main__':

    configfilename = 'init.json'

    main(configfilename)
    print('\nProcess Complete')
