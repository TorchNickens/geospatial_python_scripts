import arcpy
import os
import getpass
import Tkinter, tkFileDialog
from Tkinter import *

username = getpass.getuser()
mainDir = os.chdir("C:\\Users\\" + username + "\\Desktop")

# Use Tkinter file dialog ask directory to get file path for installation geodatabase being compared
root = Tkinter.Tk()
root.withdraw()
root.attributes('-topmost', True)
path_sGDB = tkFileDialog.askdirectory(parent=root, initialdir=mainDir, title='Directory to folder directory with loose feature class installation data')
if len(path_sGDB) > 0:
    print("Folder selected: %s" % os.path.abspath(path_sGDB))
path_gdb = tkFileDialog.askdirectory(parent=root, initialdir=mainDir, title='Directory to GDB Shell')
if len(path_gdb) > 0:
    print("GDB Shell locaiton: %s" % os.path.abspath(path_gdb))
root.destroy()

timestamp = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
print "Started @ " + timestamp

arcpy.env.workspace = path_sGDB
fclist = arcpy.ListFeatureClasses()
for fc in fclist:
    in_name = os.path.basename(fc)
    arcpy.MakeFeatureLayer_management(path_sGDB + "/" + in_name, in_name + "_lyr")
    count = int(arcpy.GetCount_management(in_name + "_lyr").getOutput(0))
    if count == 0:
        print "No features exist for " + in_name
        pass
    else:
        arcpy.env.workspace = path_gdb
        target_ds = arcpy.ListDatasets()
        for ds in target_ds:
            ds_name = os.path.basename(ds)
            target_fc = arcpy.ListFeatureClasses("*", "All", ds_name)
            for fc in target_fc:
                fc_name = os.path.basename(fc)
                if fc_name == in_name:
                    print "Appending " + str(count) + " features from " + in_name + " to the " + fc_name + " feature class in the " + ds_name + " dataset in the GeoBASE_3101_Shell.gdb"
                    arcpy.Append_management(in_name + "_lyr", path_gdb + "/" + ds_name + "/" + fc_name, "NO_TEST","","")
                else:
                    pass

timestamp_end = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
print "Ended @ " + timestamp_end

raw_input("Press enter to exit")