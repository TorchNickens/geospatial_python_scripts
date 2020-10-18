#-------------------------------------------------------------------------------
# Name:        ZIP GDBs
# Author:      Marie Cline Delgado
# Created:     02 NOV 2018
# Description:
#    Zips the contents of a geodatabase.
# Parameters:
#   0 - Input folder.
#-------------------------------------------------------------------------------

import sys, zipfile, os, traceback, Tkinter, tkFileDialog

# Function for zipping geodatabases.  If keep is true, the folder, along with  all its contents, will be written to the zip file.
#  If false, only the contents of the input folder will be written to the zip file - the input folder name will not appear in the zip file.
def zipws(path, zip, keep):
    path = os.path.normpath(path)
    print("Zipping {}...".format(path))

    for (dirpath, dirnames, filenames) in os.walk(path):

        for file in filenames:

            # Ignore .lock files
            if not file.endswith('.lock'):
                try:
                    if keep:
                        zip.write(os.path.join(dirpath, file),
                        os.path.join(os.path.basename(path), os.path.join(dirpath, file)[len(path)+len(os.sep):]))
                    else:
                        zip.write(os.path.join(dirpath, file),
                        os.path.join(dirpath[len(path):], file))

                except Exception, e:
                    print("    Error adding {}: {}".format(file, e))

    return None

try:
    root = Tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    getGDBLoc = tkFileDialog.askdirectory(parent=root, initialdir="C:", title='Select the folder which contains the GDBs to be zipped')
    root.attributes('-topmost', False)
    wkPath = os.path.abspath(getGDBLoc).replace("\\","/")
    root.destroy()

    # Create the zip file for writing compressed data. In some rare instances, the ZIP_DEFLATED constant may be unavailable and the
    #  ZIP_STORED constant is used instead.  When ZIP_STORED is used, the zip file does not contain compressed data, resulting in large zip files.
    for fldr in os.listdir(wkPath):
        if fldr.endswith('.gdb'):
            outfile = fldr+".zip"
            try:
                    zip = zipfile.ZipFile(os.path.join(wkPath,outfile), 'w', zipfile.ZIP_DEFLATED)
                    zipws(os.path.join(wkPath,fldr), zip, False)
                    zip.close()
                    print("  >> {} zipped successfully".format(outfile))

            except RuntimeError:
                    # Delete zip file if it exists
                    if os.path.exists(os.path.join(wkPath,outfile)):
                            os.unlink(os.path.join(wkPath,outfile))
                    zip = zipfile.ZipFile(os.path.join(wkPath,outfile), 'w', zipfile.ZIP_STORED)
                    zipws(os.path.join(wkPath,fldr), zip, False)
                    zip.close()
                    print("  >> {} zipped, however unable to compress zip file contents.".format(outfile))

except:

    # Return any Python specific errors
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print("PYTHON ERRORS:\nTraceback Info:\n{}\nError Info:\n    {}: {}\n".format(tbinfo, sys.exc_type, sys.exc_value))

raw_input("Press Enter To Close")
