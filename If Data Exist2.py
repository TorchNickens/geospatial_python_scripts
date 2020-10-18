import arcpy

InputDataset = arcpy.GetParameterAsText(0)

arcpy.env.workspace = InputDataset

def checkSchema()

	ML = "wLineMain_L"
	SL = "wLineService_L"
	Fh = "wFireHydrant_P"
	Hy = "wHydrant_P
	MrgLn = "in_memory\mergedlines"
	MrgLn_query = "in_memory\activeLines"
	FH_lyr = "in_memory\FH_active"
	Buffer = "in_memory\defBuf"


Buffer_Distance = arcpy.GetParameterAsText(1)
if arcpy.Exists(Fh):
	arcpy.Merge_management([SL, ML], MrgLn)
	arcpy.MakeFeatureLayer_management(Fh, FH_lyr, "\"OPERATIONALSTATUS\" <> 'abandoned' AND \"OPERATIONALSTATUS\" <> 'removed'")
	arcpy.MakeFeatureLayer_management(MrgLn, MrgLn_query, "\"OPERATIONALSTATUS\" <> 'abandoned' AND \"OPERATIONALSTATUS\" <> 'removed'")
	arcpy.SelectLayerByLocation_management(FH_lyr, "HAVE_THEIR_CENTER_IN", MrgLn)

	### Testing and are not working#
	#arcpy.GraphicBuffer_analysis(MrgLn_query, Prox_Buffer, Buffer_Distance, "ROUND", "ROUND", "10", "0 Meters")
	#arcpy.Buffer_analysis(MrgLn_query, "C:\Users\Morteo\Woolpert, Inc\Nickens, Zac - JIRA PROJECTS\DATA_VALIDATION_FOLDER\MODELS\Testing Tools In-Progress\New File Geodatabase.gdb\Test\Buffer", Buffer_Distance)
	##

	#Creates a in memory buffer
	arcpy.Buffer_analysis(MrgLn_query, Buffer, Buffer_Distance)

	# Copies output that meets above criteria
	arcpy.CopyFeatures_management(MrgLn_query, "C:\Users\Morteo\Woolpert, Inc\Nickens, Zac - JIRA PROJECTS\DATA_VALIDATION_FOLDER\MODELS\Testing Tools In-Progress\New File Geodatabase.gdb\Test\MrgLn_queryLyr")
	arcpy.CopyFeatures_management(Buffer, "C:\Users\Morteo\Woolpert, Inc\Nickens, Zac - JIRA PROJECTS\DATA_VALIDATION_FOLDER\MODELS\Testing Tools In-Progress\New File Geodatabase.gdb\Test\Buffer_lyr")
	arcpy.CopyFeatures_management(FH_lyr, "C:\Users\Morteo\Woolpert, Inc\Nickens, Zac - JIRA PROJECTS\DATA_VALIDATION_FOLDER\MODELS\Testing Tools In-Progress\New File Geodatabase.gdb\Test\On_lineFH")
else:
	print(arcpy.AddMessage("Does not exists"))