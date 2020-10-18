""" ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
Description: This Script audits all of the Items within a Geodatabase.

Beginning with: GeodatabaseAudit.py

Created on: 9/2/2017

Purpose: This Script audits all of the Items within a Geodatabase.
    The first step of the process is to accesses the GDB_ITEMS table, and
    export the table to a scratch gdb. Then Definition and Documentation
    fields are deleted because excel does not like them. The the proces
    accesses the GDB_ITEMTYPES table, and export the table to a scratch gdb.
    Then Join Field Management Geoprocessing tool is run to bring the two
    tables together then exported to excel.

Authored by:


### ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

# Import modules
import arcpy, time, sys, string, os, traceback, datetime, shutil, httplib, urllib, json, getpass, arcserver, subprocess
import xml.dom.minidom as DOM
import xml.etree.ElementTree as ET
from subprocess import Popen
import smtplib
from email.MIMEText import MIMEText
# End Import

# Setting the arc py environment
ENV= arcpy.env
# End Arcpy Environment

# Setting the overwrite of existing features
ENV.overwriteOutput = True
# End Overwrite Setting

# Set Email List
SetEmail([])
# End Set Email List

# Write Log code
logFile, root = setLog(sys.argv[0], False) #True=Time stamp in log file name; False=No time stamp in log file name

'''
---  These are log examples  ---
message += "Write log message here" + "\n"
exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
formatted_lines = traceback.format_exc().splitlines()
writelog(logFile,message + "\n" + formatted_lines[-1])
writelog(logFile, "Write log message here" + "\n")
---  End log examples  ---
'''
# End Write Log code


# Functions
message = ""
scriptName = ""
logFile = ""
EmailList = ['jsguzi@starkcountyohio.gov', 'bwlongenberger@starkcountyohio.gov', 'jmreese@starkcountyohio.gov']

def setLog(SysArgv, Timestamp):
    global scriptName, logFile
    dateTimeStamp = time.strftime('%Y%m%d%H%M%S')
    root = os.path.dirname(SysArgv) #"C:\\Users\\jsguzi\\Desktop"
    if not os.path.exists(root + "\\log"): # Check existence of a log folder within the root, if it does not exist it creates one.
        os.mkdir(root + "\\log")
    scriptName = SysArgv.split("\\")[len(SysArgv.split("\\")) - 1][0:-3] #Gets the name of the script without the .py extension

    if Timestamp == True:
        logFile = root + "\\log\\" + scriptName + "_" + dateTimeStamp[:14] + ".log" #Creates the logFile variable
    elif Timestamp == False:
        logFile = root + "\\log\\" + scriptName + ".log" #Creates the logFile variable

    if os.path.exists(logFile):
        os.remove(logFile)
    return logFile, root

def SetEmail(AdditionalEmailList):
    global EmailList
    EmailList = EmailList + AdditionalEmailList

def writelog(logfile,msg):
    global message
    message += msg
    print msg
    f = open(logfile,'a')
    f.write(msg)
    f.close()

def sendEmail(subject, emailMessage):
    #This function is for general success or error emails, sent to SCGIS
    global message, scriptName, EmailList, logFile
    message += emailMessage
    messages = arcpy.GetMessages()
    message += messages
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    formatted_lines = traceback.format_exc().splitlines()
    writelog(logFile, formatted_lines[-1] + "\n")
    # Send Email
    # This is the email notification piece [%]
    #email error notification
    smtpserver = 'mailrelay.co.stark.oh.us'
    AUTHREQUIRED = 0 # if you need to use SMTP AUTH set to 1
    smtpuser = ''  # for SMTP AUTH, set SMTP username here
    smtppass = ''  # for SMTP AUTH, set SMTP password here

    RECIPIENTS = EmailList
    SENDER = 'gissas@starkcountyohio.gov'
    msg = MIMEText(message) #***i pointed this mime thing at the message
    msg['Subject'] = subject + ' with Script: ' + str(scriptName) ### this is the subject line of the email
    # Following headers are useful to show the email correctly
    # in your recipient's email box, and to avoid being marked
    # as spam. They are NOT essential to the sendmail call later
    msg['From'] = "ArcGIS on GISSAS "
    msg['Reply-to'] = "Joe Guzi "
    msg['To'] = "jsguzi@starkcountyohio.gov"

    session = smtplib.SMTP(smtpserver)
    if AUTHREQUIRED:
        session.login(smtpuser, smtppass)
    session.sendmail(SENDER, RECIPIENTS, msg.as_string())
    session.close()

def readTextFile(File, Time):
    DayAgo = datetime.timedelta(days = 1)
    DayAgoDateTime = Time - DayAgo
    PreviousDateTime = str(DayAgoDateTime)[0:19]
    if not os.path.exists(File):
        TextFile = open(File, "w")
        TextFile.write("")
        TextFile.close()
    else:
        TextFile = open(File, "r")
        Lines = TextFile.read()
        if Lines == "":
            pass
        else:
            PreviousDateTime = Lines
        TextFile.close()
    return PreviousDateTime

def writeTextFile(File, Time):
    ShortTime = str(Time)[0:19]
    TextFile = open(File, "w")
    TextFile.write(ShortTime)
    TextFile.close()

def GDBAudit(GDBItems, GDBItemType, OutputLocation):

    # GDB Items to scratch table
    writelog(logFile, "Process: GDB Items to scratch table" + "\n")
    GDB_ITEMSTable = arcpy.TableToTable_conversion(GDBItems, arcpy.env.scratchGDB, "GDB_ITEMSTable", "", "", "")
    writelog(logFile, "Process: GDB Items to scratch table Complete!" + "\n")

    # Delete Fields
    writelog(logFile, "Process: Delete Fields" + "\n")
    GDB_ITEMSTable = arcpy.DeleteField_management(GDB_ITEMSTable, "Definition;Documentation")
    writelog(logFile, "Process: Delete Fields Complete!" + "\n")

    # GDB ITem Type to Scratch Table
    writelog(logFile, "Process: GDB ITem Type to Scratch Table" + "\n")
    GDB_ITEMTPYESTable = arcpy.TableToTable_conversion(GDBItemType, arcpy.env.scratchGDB, "GDB_ITEMTPYESTable", "", "", "") #arcpy.env.scratchGDB
    writelog(logFile, "Process: GDB ITem Type to Scratch Table Complete!" + "\n")

    # Run Join Field GDP tool to put the GDB_ITEMS table and the GDB_ITEMTYPES table together
    writelog(logFile, "Process: Run Join Field GDP tool to put the GDB_ITEMS table and the GDB_ITEMTYPES table together" + "\n")
    GDB_ITEMSTable = arcpy.JoinField_management(GDB_ITEMSTable, "Type", GDB_ITEMTPYESTable, "UUID", "Name;ParentTypeID")
    writelog(logFile, "Process: Run Join Field GDP tool to put the GDB_ITEMS table and the GDB_ITEMTYPES table together Complete!" + "\n")

    # Table to Excel Conversion tool
    writelog(logFile, "Table to Excel Conversion tool" + "\n")
    arcpy.TableToExcel_conversion(GDB_ITEMSTable, OutputLocation, "NAME", "CODE")
    writelog(logFile, "Table to Excel Conversion tool Complete!" + "\n")
    writelog(logFile, "Table Located: " + str(OutputLocation) + "\n")
# End Function Section

# Variables
GISGDB = root + "\\Connection Files\\ConnectionFile.sde" # Change ConnectionFile to name of the Connection File
GISGDBItems = GISGDB + "\\***.dbo.GDB_ITEMS" # Change the *** to the Geodatabase name
GISGDBItemType = GISGDB + "\\***.dbo.GDB_ITEMTYPES" # Change the *** to the Geodatabase name
Excel = root + "\\Audits\\GDBName_GDBAudit.xls" # Name the File whatever you would like
# End Variable Section

try:
    # Process
    writelog(logFile, "Process:" + "\n")
    writelog(logFile, "STARTING TIME: " + str(datetime.datetime.now()) + "\n")

    writelog(logFile, "Process: GDB Audit" + "\n")
    GDBAudit(GISGDBItems, GISGDBItemType, Excel)
    writelog(logFile, "Process: GDB Audit Complete!" + "\n")

    writelog(logFile, "ENDING TIME: " + str(datetime.datetime.now()) + "\n")
    writelog(logFile, "Success!" + "\n")
except:
    writelog(logFile, "Error:" + "\n")
    writelog(logFile, "ERROR TIME: " + str(datetime.datetime.now()) + "\n")
    #sendEmail("Error", "Error" + "\n")