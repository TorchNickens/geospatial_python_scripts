# ---------------------------------------------------------------------------
# CheckExists.py
# Created on: Wed Jan 3 2008
# Updated on: Wed Dec 27 2011
#
# 0 - Name of Feature Dataset to check (required)
# 1 - Name of existing workspace (required)
# 2 - Boolean value to control the model
# 3 - Value of feature dataset name, if it exists
#
# ---------------------------------------------------------------------------

# Import system modules
import arcpy, sys, string, os

# Get the input in the model
InputFDS = arcpy.GetParameterAsText(0)
arcpy.env.workspace = arcpy.GetParameterAsText(1)

# Statement to check the existence of the feature dataset
if arcpy.Exists(InputFDS):
    arcpy.SetParameterAsText(2,"False")
    arcpy.SetParameterAsText(3,InputFDS)
    arcpy.AddMessage("Feature Dataset " + InputFDS + " Already Exists!")
else:
    arcpy.SetParameterAsText(2,"True")
    arcpy.SetParameterAsText(3,"")
    arcpy.AddMessage("Feature Dataset Does Not Exist!")