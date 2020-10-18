#-------------------------------------------------------------------------------
# Name:        Hurricane Michael/Tyndall Feature Class Appending by Shape Type
# Author:      Marie Cline Delgado
# Created:     02 NOV 2018
#-------------------------------------------------------------------------------

import arcpy, os

inWork = r"C:\Users\1528874122E\Desktop\ScriptProjects\HurricaneMichael\Tyndall_Export_Aug2018_311_AF_GeoBase_2018.gdb".replace("\\", "/")
outWork = r"C:\Users\1528874122E\Desktop\ScriptProjects\HurricaneMichael\TyndalHurricaneMichaelcombinedFCs.gdb".replace("\\", "/")

polygonFC=[]
pointFC=[]
lineFC=[]
arcpy.env.workspace = inWork
for dataset in arcpy.ListDatasets():
    for fc in arcpy.ListFeatureClasses('*','',dataset):
        for fld in arcpy.ListFields(fc):
            if "realPropertyUnique" in fld.name:
                #featureClassesList.append((os.path.join(arcpy.env.workspace, dataset, fc)).replace("\\", "/"))
                shpType = arcpy.Describe(fc).shapeType
                print("{} : {}".format(fc, shpType))
                if shpType == 'Polygon':
                    polygonFC.append(fc)

                elif shpType == 'Point':
                    pointFC.append(fc)

                elif shpType == 'Polyline':
                    lineFC.append(fc)

print("Appending Polygons")
arcpy.Append_management(polygonFC, os.path.join(outWork,"PolygonFeatures").replace("\\", "/"), "NO_TEST")
print("Appending Points")
arcpy.Append_management(pointFC, os.path.join(outWork,"PointFeatures").replace("\\", "/"), "NO_TEST")
print("Appending Lines")
arcpy.Append_management(lineFC, os.path.join(outWork,"LineFeatures").replace("\\", "/"), "NO_TEST")


