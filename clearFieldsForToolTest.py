import arcpy, os

def govPath(filePath):
    """Replace backslashes with forwardslashes for use on government computer.
    :param a file path
    """
    return filePath.replace("\\", "/")

def getWorkspaceFromToolParams(gdbParamAsText, subsetFCParamAsText):
    """Prepare input features from GetParameterAsText when geodatabase is required
    and a subset of feature classes is optional.
    :params gdbParamAsText: geeodatabase
    subsetFCParamAsText: text string of a subset of feature classes to geoprocess separated by
    a semicolon and must reside within the gdb
    """
    arcpy.env.workspace = gdbParamAsText
    extension = os.path.splitext(gdbParamAsText)[1]
    fdfcList=[]
    # feature classes in the input geodatabase if no subset is specified
    if len(subsetFCParamAsText) == 0:
        for fd in arcpy.ListDatasets():
            for fc in arcpy.ListFeatureClasses("*","",fd):   #for fld in arcpy.ListFields(fc):
                fdfcList.append((os.path.join(arcpy.env.workspace, fd, fc)).replace("\\", "/"))
        for fc in arcpy.ListFeatureClasses():
            fdfcList.append((os.path.join(arcpy.env.workspace, fc)).replace("\\", "/"))

    elif len(subsetFCParamAsText) > 0:
        fdfcList = [fcPath.rstrip("'").lstrip("'").replace("\\","/") for fcPath in subsetFCParamAsText.split(';')]
        # confirm all feature classes of the subset reside within the geodatabase
        subsetGDBs = [os.path.splitext(item) for item in fdfcList if extension in item]
        arcpy.AddMessage(subsetGDBs)
        for db in subsetGDBs:
            if db == os.path.splitext(gdbParamAsText)[0]:
                arcpy.AddError("All optional feature classes must reside within the input geodatabase, {}. Remove the feature classes that are not within the input geodatabase from the tool input parameters and then try running the tool again.".format(gdbParamAsText))
                sys.exit(0)

    # returns a list of full paths to each feature class that will be geoprocessed unless feature layer dragged from mxd
    return fdfcList

gdb = r"C:\Users\1528874122E\Desktop\AFMC_SDSFIE311_Dec14_2018.gdb"
gdb = govPath(gdb)

fcList = getWorkspaceFromToolParams(gdb, "")
autoPFields = ['geoloc', "installationid", "installationname", "country", "majorcommand", "realpropertysiteuniqueid"]
clrNumFields = ['latitude', 'longitude', 'latitudefrom', 'latitudeto', 'longitudefrom',  'longitudeto', 'lengthsize', "areasize", "perimetersize"]
clrTxtFields = ['sdsid', 'MGRS', 'MGRScentroid', 'owner', 'datacollection', 'lengthsizeuom', "areasizeuom", "perimetersizeuom"]

for fc in fcList:
    print fc
    fldNames = [field.name for field in arcpy.ListFields(fc)]
    for fld in fldNames:
        if fld.lower() in clrNumFields:
            arcpy.CalculateField_management(fc, fld, 0, "PYTHON")
        elif fld.lower() in clrTxtFields:
            arcpy.CalculateField_management(fc, fld, "'"+"'", "PYTHON")
        elif fld.lower().endswith("idpk"):
            arcpy.CalculateField_management(fc, fld, "'"+"'", "PYTHON")

print("Complete")

delField = 'MGRScentroid'
for fc in fcList:
    print fc
    fldNames = [field.name for field in arcpy.ListFields(fc)]
    if delField in fldNames:
        arcpy.CalculateField_management(fc, delField, "'"+"'", "PYTHON")
        #arcpy.CalculateField_management(fc, delField, 0, "PYTHON")
print ("Complete")

delField = ''
for fc in fcList:
    print fc
    fldNames = [field.name for field in arcpy.ListFields(fc)]
    for fld in fldNames:
        if fld.endswith("IDPK"):
            arcpy.CalculateField_management(fc, fld, "'"+"'", "PYTHON")
print ("Complete")

