#-------------------------------------------------------------------------------
# Name:         Compact GDBs
# Purpose:      Compact GDBs and log results in log file for user inspection
# Author:       Marie Cline Delgado
# Last Updated: 09 AUG 2018
#-------------------------------------------------------------------------------

import arcpy, os, sys, time, logging, logging.config
from datetime import datetime

pyScriptLoc = os.path.dirname(sys.argv[0])
pyScriptName = os.path.basename(sys.argv[0]).split(".")[0]

# Check for log files folder
logFolder = os.path.join(pyScriptLoc, "_LogFiles")
if not os.path.exists(logFolder):
    os.makedirs(logFolder)

# Set up the logfile name
t = datetime.now()
logFile = os.path.join(logFolder, pyScriptName+"_")
logName = logFile + t.strftime("%y%m%d") + ".log"

# Set up logging
logger = logging.getLogger(pyScriptName)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(logName)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s : line %(lineno)d - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def compactGDBs(aFolder):
    for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype="Container"):
        for dirname in dirnames:
            if dirname.endswith(".gdb") and arcpy.Describe(os.path.join(dirpath,dirname)).dataElementType == "DEWorkspace":
                try:
                    arcpy.Compact_management(os.path.join(dirpath, dirname))
                    print("Successfully compacted " + dirname)
                    logger.info("Successfully compacted " + dirname)
                except:
                    print("ERROR: " + str(os.path.join(dirpath, dirname)))
                    logger.info("ERROR: " + str(os.path.join(dirpath, dirname)))

def cleanupdir(path):
    """
    Removes any log files in the given directory that are older than 32 days.
    """
    now = time.time()
    for logs in os.listdir(path):
        fullpath = os.path.join(path, logs)
        if os.stat(fullpath).st_ctime < (now - 2765000): # seconds in 32 days
            if os.path.isfile(fullpath):
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                cleanupdir(fullpath)


workspace = r"C:\Users\1528874122E\Desktop\test"

compactGDBs(workspace)

cleanupdir(logFolder)
