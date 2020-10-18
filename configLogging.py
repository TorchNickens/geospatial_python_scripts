#-------------------------------------------------------------------------------
# Name:         Configure Logging
# Purpose:      Create a log file to save message from script
# Author:       Marie Cline Delgado
# Last Updated: 09 AUG 2018
#-------------------------------------------------------------------------------

import os, sys, logging, logging.config
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

# Print messages and log messages
print("Start time: " + str(t))
logger.info("Start time: " + str(t))


