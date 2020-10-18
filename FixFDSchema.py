import arcpy, os

shell = arcpy.GetParameterAsText(0)
myGDB = arcpy.GetParameterAsText(1)

arcpy.env.workspace = shell

inTable = "ReportTable"
OutLocation = myGDB
OutputTable = "ReportTable"


FCShell = arcpy.ListFeatureClasses('*', '', 'utilitiesWater')

for fcs in FCShell:
    if not arcpy.Exists(os.path.join(myGDB, fcs)):
        arcpy.FeatureClassToFeatureClass_conversion(fcs, os.path.join(myGDB, 'utilitiesWater'), fcs)

if not arcpy.Exists(os.path.join(myGDB, inTable)):
    arcpy.TableToTable_conversion(inTable, os.path.join(myGDB), OutputTable)

