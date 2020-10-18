#Copy this script into directory where personal GDB is located
import arcpy, Tkinter, tkFileDialog, os
timestamp = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
print "Started @ " + timestamp

# Use Tkinter to get file path for mdb
root = Tkinter.Tk()
root.withdraw()
root.attributes('-topmost', True)
getMDBLoc = tkFileDialog.askopenfilename(parent=root, initialdir=sys.path[0], title='Select the MDB to convert')
root.attributes('-topmost', False)
mdbPath = os.path.dirname(getMDBLoc)
mdbFile = os.path.basename(getMDBLoc)
mdbLoc = os.path.abspath(os.path.join(mdbPath, mdbFile))
installationName = os.path.splitext((os.path.split(mdbLoc)[1]))[0]
if len(mdbLoc) > 0:
    print("MDB selected: %s" % os.path.abspath(mdbLoc))
root.destroy()

arcpy.env.workspace = mdbPath

print "Creating FGDB Shell with same name as input Personal GDB"
arcpy.CreateFileGDB_management(mdbPath, installationName)
print "Exporting XML with GDB structure and data from MDB"
arcpy.ExportXMLWorkspaceDocument_management(mdbFile, installationName + ".xml", "DATA", "BINARY", "METADATA")
print "Importing XML into FGDB Shell"
arcpy.ImportXMLWorkspaceDocument_management(installationName + ".gdb", installationName + ".xml", "DATA", "DEFAULTS")

timestamp_end = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
print "Finished @ " + timestamp_end