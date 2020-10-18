
# Import modules
import arcpy, time, os, sys, getpass
from datetime import datetime

# Start time
startT = datetime.now()
print(startT)

# Get username
username = getpass.getuser()

theGDB = "C:\\Users\\" + username + "\\Desktop\\to_gdb\\GeoBASE_3101_Shell_CIP.gdb"
arcpy.env.workspace = theGDB

##def listFcsInGDB():
##    ''' set your arcpy.env.workspace to viewer minimum attribution gdb before calling '''
##    for fds in arcpy.ListDatasets('','feature') + ['']:
##        for fc in arcpy.ListFeatureClasses('','',fds):
##            minFields = (fld.name for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
##            reqDomains = (fld.domain for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
##            for f, d in zip(minFields, reqDomains):
##                yield os.path.join(fds, fc, f, d) # add arcpy.env.workspace at beginning of join if want to keep the viewer workspace in the file path
##vwrDataList = list(listFcsInGDB())

def listFcsInGDB_minusDomains():
    ''' set your arcpy.env.workspace to viewer minimum attribution gdb before calling '''
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            minFields = (fld.name for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
            for f in minFields:
                yield os.path.join(fds, fc, f) # add arcpy.env.workspace at beginning of join if want to keep the viewer workspace in the file path
vwrDataList = list(listFcsInGDB())

strList = []
for item in vwrDataList:
    strList.append(str(item))
print strList

# End time
endT = datetime.now()
print(endT)