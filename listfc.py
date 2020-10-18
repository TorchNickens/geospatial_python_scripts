import arcpy  
from arcpy import env  
env.workspace = r"C:\Users\nickens\OneDrive - Woolpert, Inc\JIRA PROJECTS\Enterprise Diff Analysis Project Data\ULS Data 3.12.2019\ULS_Cannon_20170314.gdb\ULS_Cannon_20170314.gdb"  
  
for dataset in arcpy.ListDatasets("*"):  
    print dataset  
    for fc in arcpy.ListFeatureClasses("*", "", dataset):  
        count = arcpy.GetCount_management(fc).getOutput(0)  
        print "\t" + fc + ": " + str(count)  
  
for fc in arcpy.ListFeatureClasses("*"):  
        count = arcpy.GetCount_management(fc).getOutput(0)  
        print fc + ": " + str(count) 