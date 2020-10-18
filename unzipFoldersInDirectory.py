#-------------------------------------------------------------------------------
# Name:        unZIP Folders
# Author:      Marie Cline Delgado
# Created:     11 DEC 2018
# Description:
#    Unzips the contents of a folder.
# Parameters:
#   0 - Input folder.
#-------------------------------------------------------------------------------

import sys, zipfile, os, traceback, Tkinter, tkFileDialog

# Function for unzipping folders in a directory.  If keep is true, the original zipped folder will be kept in the directory.
#  If false, the original zipped folder will be deleted from the input directory.
def unzip(inpath, outpath, keep=True):
    os.chdir(inpath) # change directory from working dir to dir with files
    for item in os.listdir(inpath): # loop through items in dir
        if item.endswith('.zip'): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zipdFldr_name = os.path.basename(file_name.rstrip('.zip'))
            print (" > Unzipping {}".format(file_name))
            with zipfile.ZipFile(file_name) as zip_ref: # create zipfile object
                zip_ref.extractall(outpath) #(os.path.join(outpath,zipdFldr_name)) # extract file to dir
                zip_ref.close() # close file
            if not keep:
                os.remove(file_name) # delete zipped file
    return None

try:
    root = Tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    getDirLoc = tkFileDialog.askdirectory(parent=root, initialdir="C:", title='Select the folder which contains the zipped folders to be unzipped')
    outLoc = tkFileDialog.askdirectory(parent=root, initialdir="C:", title='Select a location to place unzipped folders')
    root.attributes('-topmost', False)
    wkPath = os.path.abspath(getDirLoc).replace("\\","/")
    outPath = os.path.abspath(outLoc).replace("\\","/")
    root.destroy()

    unzip(wkPath, outPath)

except:

    # Return any Python specific errors
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print("PYTHON ERRORS:\nTraceback Info:\n{}\nError Info:\n    {}: {}\n".format(tbinfo, sys.exc_type, sys.exc_value))

raw_input("Press Enter To Close")