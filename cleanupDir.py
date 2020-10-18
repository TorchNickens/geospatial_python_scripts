import os, time

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

cleanupdir(r"C:\Users\1528874122E\Desktop\test\JBMDL.gdb")