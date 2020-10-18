import os, arcpy

spang = r"C:/Users/1528874122E/Desktop/vyhk31n_2018-07-06_Spangdahlem_311_AF_GeoBase_Shell_2018.gdb"
arcpy.env.workspace = spang
for fd in arcpy.ListDatasets():
    print str(fd).upper()
    for fc in arcpy.ListFeatureClasses("*","",fd):
        print "  {}".format(fc)
        if int(arcpy.GetCount_management(fc)[0]) == 0:
            print "  >> Deleting"
            arcpy.Delete_management(fc)
