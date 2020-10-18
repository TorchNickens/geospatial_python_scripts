##############################################################################
# FC_Check.py
#This script tests for the existence of a Feature class

#Arguements:
#0 -Input Feature Class Name (required)
#1 -Output Boolean Variable for True/False value

#zachary nickens
#February 2018
###############################################################################

#load arcpy
#arcpy makes geoprocessing tools available in script

import sys, os, arcpy, string

#get input from model
InputFC = arcpy.GetParameterAsText(0)
Path ="%Merge FDS%" + "/" + InputFC
arcpy.env.workspace = arcpy.GetParameterAsText(1)
#statement to check existence
if arcpy.Exists(Path):
    arcpy.SetParameterAsText(1, 'False')
    raise Exception("Feature Class Already Exist!")
else:
    arcpy.SetParameterAsText(1,'True')
    arcpy.AddMessage("Feature Class Does Not Exist!")