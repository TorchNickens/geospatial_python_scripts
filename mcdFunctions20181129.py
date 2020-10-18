#----------------------------------------------------------------------------------------------------------
# Name:            Functions
# Purpose:         Repository of functions worth saving for later use
#
# Author:          Marie Cline Delgado
#
# Last Updated:    23 JULY 2018
#----------------------------------------------------------------------------------------------------------

idea
itertools.repeat(object[, times])
Make an iterator that returns object over and over again. Runs indefinitely unless the times argument is specified. Used as argument to imap() for invariant function parameters. Also used with izip() to create constant fields in a tuple record. Roughly equivalent to:

def repeat(object, times=None):
    # repeat(10, 3) --> 10 10 10
    if times is None:
        while True:
            yield object
    else:
        for i in xrange(times):
            yield object
A common use for repeat is to supply a stream of constant values to imap or zip:

>>> list(imap(pow, xrange(10), repeat(2)))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# =========================================================================================================

desc = arcpy.Describe(featureClass)
if hasattr(desc, 'path'):
    descPth = arcpy.Describe(desc.path)
    if hasattr(descPth, 'dataType'):
        if descPth.dataType == 'FeatureDataset':
            featureClass = os.path.join(descPth.name, featureClass)

# =========================================================================================================

Build dictionary inline with conditions. Ex: Domain name as dictionary keys with list of coded values as dictionary values

domainValues_dic = dict((domain.name, domain.codedValues.keys())
                        for domain in domains
                        if domain.domainType == 'CodedValue')
Access example
if C not in [val for cKeys, cVals in domainValues_dic.iteritems() for val in cVals if cKeys == DTN]:
    do your thing

# =========================================================================================================

def govPath(filePath):
    """Replace backslashes with forwardslashes for use on government computer.
    :param a file path
    """
    return filePath.replace("\\", "/")

# =========================================================================================================

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
                if int(arcpy.GetCount_management(fc)[0]) > 0:
                    fdfcList.append((os.path.join(arcpy.env.workspace, fd, fc)).replace("\\", "/"))
        for fc in arcpy.ListFeatureClasses():
            if int(arcpy.GetCount_management(fc)[0]) > 0:
                fdfcList.append((os.path.join(arcpy.env.workspace, fc)).replace("\\", "/"))

    elif len(subsetFCParamAsText) > 0:
        fdfcList = [fcPath.rstrip("'").lstrip("'").replace("\\","/") for fcPath in subsetFCParamAsText.split(';')]
        # confirm all feature classes of the subset reside within the geodatabase
        subsetGDBs = [fc.split(extension)[0] for fc in fdfcList]
        featLyr = list(set([True if extension not in fc else False for fc in fdfcList]))
        # Test if the subset are all feature classes and none feature layers
        if len(featLyr) == 1 and featLyr[0] == 'False': # Utilizing all feature classes
            # Test if the subset of feature classes all reside within the workspace geodatabase
            if not (len(set(subsetGDBs)) == 1 and subsetGDBs[0] == os.path.splitext(gdbParamAsText)[0]): # One or more does not
                arcpy.AddError("All optional feature classes must reside within the input geodatabase, {}. Remove the feature classes that are not within the input geodatabase from the tool input parameters and then try running the tool again.".format(gdbParamAsText))
                sys.exit()
        elif len(featLyr) == 1 and featLyr[0] == 'True': # Utilizing all feature layers
            pass
        elif len(featLyr) == 2: # Utilizing a mix of feature classes and feature layers
            arcpy.AddError("All optional feature class data must be of the same layer type. Try referencing all feature classes as: 1) layers; by dragging from a map's table of contents into the tool input parameter or 2) feature classes; by selecting the feature class from its geodatabase location using the tool's file explorer window.")
            sys.exit()

    # returns a list of full paths to each feature class that will be geoprocessed unless feature layer dragged from mxd
    return fdfcList

# =========================================================================================================

def triggerSubTool(gdbParamAsText):
    """Return True if tool is triggered to run.
    :params not sure yet.
    """
    if len(gdbParamAsText) > 0:
        return True

# =========================================================================================================

def get_geodatabase_path(input_table):
  """Return the Geodatabase path from the input table or feature class.
  :param input_table: path to the input table or feature class
  """
  workspace = os.path.dirname(input_table)
  if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
    return workspace
  else:
    return os.path.dirname(workspace)

# =========================================================================================================

def error_ckIfGeodatabase(path):
    """
    Error checking. Confirms path is a geodatabase workspace.
    """
    if arcpy.Describe(path).dataElementType != "DEWorkspace":
        arcpy.AddError("Your input workspace is type {} and requires a file geodatabase of type DEWorkspace".format(arcpy.Describe(path).dataElementType))
        return False
    else:
        return True


# =========================================================================================================
def error_ckIfNested(path):
    """
    Error checking. Tests if a path is nested in a folder named with a file extension ending.
    """
    if len(os.path.dirname(path).split(".")) > 1:
        nestedExt = os.path.splitext(os.path.dirname(path))[1]
        arcpy.AddError("Your file resides in a folder with the {} extension. Try renaming the folder by removing the {} extension.".format(nestedExt, nestedExt))
        return True
    else:
        return False


# =========================================================================================================
def error_validateFileExtension(path, extension):
    """
    Error checking. Tests if a file has a given extension.
    """
    if path.endswith(extension):
        return True
    elif not path.endswith(extension):
        actual = os.path.splitext(path)[1]
        arcpy.AddError("The extension of this file is {} and NOT {}.".format(actual, extension))
        return False


# =========================================================================================================
def error_replaceFileExtension(path, extension):
    """
    Error checking. Replaces the file path's extension with the given extension.
    """
    if not extension.startswith("."):
        extension = "."+extension
    if not path.endswith(extension):
        path = os.path.splitext(path)[0]+extension
        arcpy.AddMessage("The file extension was replaced with {}.".format(extension))
        return True


# =========================================================================================================
def getTimeNow():
    timeNow = datetime.datetime.now()
    return timeNow


# =========================================================================================================
def getRunTime(startTime, endTime):
    runTime = endTime - startTime
    return runTime


# =========================================================================================================
def unique_values(table , field):
    """
    Returns a unique list of values for a specified field of a given table.
    """
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


# =========================================================================================================
def get_fc_count(gdb):
    """
    Returns a count of all feature classes within a geodatabase.
    """
    arcpy.env.workspace = gdb
    fccount = 0
    for dataset in arcpy.ListDatasets():
        fcs = arcpy.ListFeatureClasses('*','',dataset)
        fccount += len(fcs) if fcs is not None else 0
    # Get any stand alone FCs
    saFC = arcpy.ListFeatureClasses("","")
    fccount += len(saFC) if saFC is not None else 0
    return fccount


# =========================================================================================================
def find_overlaps(input_features):
    """Find and print OID value pairs for overlapping features."""
    for row in arcpy.da.SearchCursor(input_features, ('OID@', 'SHAPE@')):
        for row2 in arcpy.da.SearchCursor(input_features, ('OID@', 'SHAPE@')):
            if row2[1].overlaps(row[1]):
                print '{0} overlaps {1}'.format(str(row2[0]), str(row[0]))

# This one should be faster.  Need to test.
def find_overlaps(input_features):
    """Find and print OID value pairs for overlapping features."""
    with arcpy.da.SearchCursor(input_features, ['OID@', 'SHAPE@']) as cur:
        for e1,e2 in itertools.combinations(cur, 2):
            if e1[1].overlaps(e2[1]):
                print "{} overlaps {}".format(e1[0],e2[0])


# =========================================================================================================
def compactGDBs(aFolder):
    """
    Compacts geodatabases within a given folder directory.
    """
    for dirpath, dirnames, filenames in arcpy.da.Walk(aFolder, datatype="Container"):
        for dirname in dirnames:
            if dirname.endswith('.gdb') and arcpy.Describe(os.path.join(dirpath, dirname)).dataElementType == "DEWorkspace":
                try:
                    arcpy.Compact_management(os.path.join(dirpath, dirname))
                    print ("Successfully compacted " + dirname)
                except:
                    print ("ERROR: " + str(os.path.join(dirpath, dirname)))


# =========================================================================================================
myVars = ['ex1', 'ex2', 'ex3']
def deleteMyVars(myVars_StringList):
    """
    Deletes user defined local variables.
    """
    for v in myVars_StringList:
        if v in locals():
            del v


# =========================================================================================================
def gdbSelection(boxTitle):
    """
    Tkinter window for Geodatabase or folder selection.
    Param: Window message for user instruction in string data type
    Result: Absolute path to the geodatabase or folder selected
    """
    root = Tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    slctGDB = os.path.abspath(tkFileDialog.askdirectory(parent=root, initialdir="C:", title=boxTitle))
    root.attributes('-topmost', False)
    if len(slctGDB) > 0:
        root.destroy()
        return slctGDB


# =========================================================================================================
def selectFile(boxTitle):
    """
    Tkinter window for file selection.
    Param: Window message for user instruction in string data type
    Result: Absolute path to the file selected
    """
    root = Tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    fileLoc = os.path.abspath(tkFileDialog.askopenfilename(parent=root, initialdir="C:", title=boxTitle))
    root.attributes('-topmost', False)
    if len(fileLoc) > 0:
        root.destroy()
        return fileLoc


# =========================================================================================================
def fromCSV_PandaImitation(csvLoc):
    """
    Imitates the functionality of a Pandas dataframe when reading a csv file.  Beneficial when searching
    for a column by column name and evaluating the columns contents.
    """
    # Open the csv file in universal line ending mode
    with open(csvLoc, 'rU') as infile:
        # Read the file as dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header.upper()].append(value.upper())
                except KeyError:
                    data[header.upper()] = [value.upper()]
    return data

# Extract the columns you want by header name
column = data['column_name']


# =========================================================================================================
def fieldMapDictionary(newFieldList, oldFieldList):
    """
    Uses fnmatch to search through a new field list and and old field list and match fields to build a
    dictionary for use in the Field Mapping process.
    Param: List of new fields and list of old fields
    Result: A dictionary
    """
    for x in newFieldList:

# TESTING======================================================================DOWN
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

bldgFloorFldsNew = get_field_names(os.path.join(targetGDB,suBldgFloor[0]))
bldgFloorFldsOld = get_field_names(os.path.join(inGDB,suBldgFloor[1]))
list(set(bldgFloorFldsNew).intersection(bldgFloorFldsOld))

BldgRmFldsNew = get_field_names(os.path.join(targetGDB,suBldgRm[0]))
bldgRmFldsOld = get_field_names(os.path.join(inGDB,suBldgRm[1]))

bldgSpcFldsNew = get_field_names(os.path.join(targetGDB,suBldgSpc[0]))
bldgSpcFldsNew = get_field_names(os.path.join(inGDB,suBldgSpc[1]))

bldgSpcObFldsNew = get_field_names(os.path.join(targetGDB,suBldgSpcObst[0]))
bldgSpcObFldsOld = get_field_names(os.path.join(inGDB,suBldgSpcObst[1]))

CadFlrFldsNew = get_field_names(os.path.join(targetGDB,suCadFlrPlan[0]))
CadFlrFldsOld = get_field_names(os.path.join(inGDB,suCadFlrPlan[1]))

print ("Pause")




# TESTING========================================================================UP




# =========================================================================================================
def fromGIS_PandaImitation(inFC, searchFieldsList):
    """
    Imitates the functionality of a Pandas dataframe when reading a GIS table.  Arranges the desired data
    in a dictionary.
    Parameters:  Input feature class and a list of field names with desired.
    Result:  A dictionary of the input data and fields.
    """
    with arcpy.da.SearchCursor(inFC, searchFieldsList, where_clause=sWhere) as cursor:
        data = {}
        for row in cursor:
            joinFID = row[0]
            dod = row[1]
            altNum = row[2]
            rpuid = row[3]
            blNum = row[4]
            data[joinFID] = [blNum, rpuid, dod, altNum]


# =========================================================================================================
def createSiteP():
    # Site_P is empty
    if int(arcpy.GetCount_management(os.path.join(cadDS,sitePtFC))[0]) == 0:
        arcpy.MakeFeatureLayer_management(os.path.join(cadDS,siteAreaFC), 'Site_Alyr')
        tempSiteP = arcpy.FeatureToPoint_management('Site_Alyr', "in_memory\\tmp", "INSIDE")
        arcpy.Append_management(tempSiteP, sitePtFC, "NO_TEST")
        arcpy.AddMessage("{} Site points created for empty Site_P".format(arcpy.GetCount_management(tempSiteP)[0]))
    # Site_P contains data
    elif int(arcpy.GetCount_management(os.path.join(cadDS,sitePtFC))[0]) > 0:
        arcpy.MakeFeatureLayer_management(os.path.join(cadDS,siteAreaFC), 'Site_Alyr')
        # Select polygons that do not contain a point
        siteAselection = arcpy.SelectLayerByLocation_management('Site_Alyr', "COMPLETELY_CONTAINS", os.path.join(cadDS,sitePtFC), selection_type="NEW_SELECTION", invert_spatial_relationship="INVERT")
        if int(arcpy.GetCount_management(siteAselection)[0]) > 0:
            tempSiteP = arcpy.FeatureToPoint_management(siteAselection, "in_memory\\tmp", "INSIDE")
            arcpy.Append_management(tempSiteP, sitePtFC, "NO_TEST")
            arcpy.AddMessage("{} Additional site points created and appended to Site_P".format(arcpy.GetCount_management(tempSiteP)[0]))


# =========================================================================================================
def listFcsInGDB(inGDB):
    """
    Returns a list of FeatureDataset//FeatureClass//Field//Domain for the given geodatabase.
    """
    arcpy.env.workspace = inGDB
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            minFields = (fld.name for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
            reqDomains = (fld.domain for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
            for f, d in zip(minFields, reqDomains):
                yield os.path.join(fds, fc, f, d) # add arcpy.env.workspace at beginning of join if want to keep the viewer workspace in the file path


# =========================================================================================================
def get_fdfc(inGDB):
    """
    NEEDS MORE WORK
    Accesses GDB, cycles through all feature datasets and feature classes, and returns their names.
    """
    arcpy.env.workspace = inGDB
    for dataset in arcpy.ListDatasets():
        print dataset
        fcs = arcpy.ListFeatureClasses('*','',dataset)
        for fc in fcs:
            print fc
    # Get any stand alone FCs
    saFC = arcpy.ListFeatureClasses("","")
    for sa in saFC:
        print sa


# =========================================================================================================
def GetFieldMappings(fc_in, dico):
    """
    Create Field Mapping object from a single input feature classes.
    """
    field_mappings = arcpy.FieldMappings()
    field_mappings.addTable(fc_in)
    for input, output in dico.iteritems():
        field_map = arcpy.FieldMap()
        field_map.addInputField(fc_in, input)
        field = field_map.outputField
        field.name = output
        field_map.outputField = field
        field_mappings.addFieldMap(field_map)
        del field, field_map
    return field_mappings
# Call as follows:
fc_in = r'C:/input.shp'
dico = {'OBJECTID':               'O_OID',
        'BLOCKSTAGE':          'BLOCKSTAGE',
        'AREAGIS':                 'AREAGIS',
        'OPERATIONSTYPE':   'OPTYPE',
        'BLOCKTYPE':             'BLOCKTYPE',
        'HARVESTSEASON':    'HARVSEASON',
        'ROADPERCENTAGE':  'ROADPERCNT'}
Mapper = GetFieldMappings(fc_in, dico)


# =========================================================================================================
def GetFieldMappings(fc_in, dico, fc_inB, dicoB):
    """
    Create Field Mapping object from 2 input feature classes.
    """
    field_mappings = arcpy.FieldMappings()
    for input, output in dico.iteritems():
        field_map = arcpy.FieldMap()
        field_map.addInputField(fc_in, input)
        field = field_map.outputField
        field.name = output
        field_map.outputField = field
        field_mappings.addFieldMap(field_map)
        del field, field_map
    for input, output in dicoB.iteritems():
        field_map = arcpy.FieldMap()
        field_map.addInputField(fc_inB, input)
        field = field_map.outputField
        field.name = output
        field_map.outputField = field
        field_mappings.addFieldMap(field_map)
        del field, field_map
    return field_mappings


# =========================================================================================================
def GetFieldMap(fc_in, dico):
    """
    Create Field Map Object to add to a Field Mapping object.
    """
    for inName, outName in dico.iteritems():
        fieldMap = arcpy.FieldMap()
        fieldMap.addInputField(fc_in, inName)
        field = fieldMap.outputField
        field.name = outName
        fieldMap.outputField = field
        del field
    return fieldMap


# =========================================================================================================
def GetFullTableName(table):
    """
    Get full table name from workspace parameters and table.
    """
    return os.path.join(workspaceParam, table)


# =========================================================================================================
def get_geodatabase_path(input_table):
    """
    Return the Geodatabase path from the input table or feature class.
    Parameter: input_table - path to the input table or feature class.
    """
    workspace = os.path.dirname(input_table)
    if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
        return workspace
    else:
        return os.path.dirname(workspace)


# =========================================================================================================
def checkEnds(line, ends):
    """
    Test a given line to evaluate if it ends with any one of an end values contained in a given input list.
    """
    for end in ends:
        if line.endswith(end):
            return True


# =========================================================================================================
def clearWSLocks(inputWS):
    """
    Attempts to clear locks on a workspace, returns stupid message.
    """
    if all([arcpy.Exists(inputWS), arcpy.Compact_management(inputWS), arcpy.Exists(inputWS)]):
        return ('Workspace {} clear to continue...').format(inputWS)
    else:
        return ('!!!!!!!! ERROR WITH WORKSPACE {} !!!!!!!!').format(inputWS)


# =========================================================================================================
def listFields(fc):
    """
    Returns a string list of the fields within the given feature class.
    """
    fieldnames = [str(field.name) for field in arcpy.ListFields(fc)]
    return fieldnames


# =========================================================================================================
def findField(fc, fi):
    """
    Checks for the extenence of a field in a feature class.
    """
    fieldnames = [field.name.upper() for field in arcpy.ListFields(fc)]
    if fi.upper() in fieldnames:
        return True
    else:
        return False


# =========================================================================================================
def get_field_names(table):
    """
    Get a list of field names not inclusive of the geometry and object id fields.
    Parameters:  table - Table readable by ArcGIS
    Returns:  List of field names.
    """
    # list to store values
    field_list = []

    # iterate the fields
    for field in arcpy.ListFields(table):

        # if the field is not geometry nor object id, add it as is
        if field.type != 'Geometry' and field.type != 'OID':
            field_list.append(field.name)

        # if geomtery is present, add both shape x and y for the centroid
        elif field.type == 'Geometry':
            field_list.append('SHAPE@XY')

    # return the field list
    return field_list


# =========================================================================================================
def list_layers(gdb):
    """
    Creates a list of feature classes in current workspace with full paths (including path
    to parent geodatabase). Returns list of layers.
    """
    print('\nGenerating layer list...')
    lyrs = []
    for ds in arcpy.ListDatasets():
        for fc in arcpy.ListFeatureClasses(feature_dataset = ds):
            fullpath = os.path.join(gdb, ds, fc)
            lyrs.append(fullpath)
        return lyrs


# =========================================================================================================
def csv_from_excel():
    """
    Convert from Excel spreadsheet to csv file and format for import to GIS table
    """
    os.chdir(os.path.abspath(xlPath))
    wb = xlrd.open_workbook(xlFile)
    sh = wb.sheet_by_index(0)
    csvFile = open(str(xlFile.split(".")[0]) + ".csv", 'wb')
    wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
    findHeader = ["InstallationCode", "Installation Code"]
    # Find header row and building column
    # Format field names to remove invalid characters
    for column in range(sh.ncols):
        for row in range(sh.nrows):
            if sh.cell(row,column).value in findHeader:
                headerRow = row
                print "Header Row Line Number " + str(headerRow)
                head = sh.row_values(headerRow)
                headAsString = [x.encode('UTF8') for x in head[0:20]]
                invalChars = [" ", "(", ")", "-"]
                for y in invalChars:
                    headAsString = [s.replace(y, "") for s in headAsString]
                wr.writerow(headAsString)
            if sh.cell(row,column).value == "Bldg Num" or sh.cell(row,column).value == "BldgNum":
                global bldgCol
                bldgCol = column
                print "Building Field Number " + str(bldgCol)
                break
        # Once header row found  exit loop
        if 'headerRow' in locals() and 'bldgCol' in locals():
            break
        else:
            continue
    # Format data types
    print "Preparing remaining " + str(sh.nrows-headerRow) + " rows of data..."
    for rownum in xrange(sh.nrows):
        if rownum > headerRow:
            dataLine = sh.row_values(rownum)
            NoneType = type(None)
            formatDataLine = ["{0:.0f}".format(d) if isinstance(d, float) else d if isinstance(d, NoneType) else str(d).encode('UTF8') for d in dataLine[0:20]]
            wr.writerow(formatDataLine)
    csvFile.close


# =========================================================================================================
def xls_from_csv():
    f=open(xlPath + "\\" + str(xlFile.split(".")[0]) + '.csv', 'rb')
    g = csv.reader ((f), delimiter=",")
    wbk= xlwt.Workbook()
    sheet = wbk.add_sheet("Sheet")

    for rowi, row in enumerate(g):
        for coli, value in enumerate(row):
            if coli == bldgCol and value == '':
                sheet.write(rowi,coli, str(-999))
            else:
                sheet.write(rowi,coli, str(value))

    wbk.save(xlPath + "\\Formatted_" + str(xlFile.split(".")[0]) + '.xls')


# =========================================================================================================
def validate_filename(s):
    """
    Validate file name function.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename


# =========================================================================================================
def cleanupdir(path):
    """
    Removes any log files in the given directory that are older than 32 days.
    """
    now = time.time()
    for logs in os.listdir(path):
        fullpath = os.path.join(path, logs)
        if os.stat(fullpath).st_ctime < (now - 2765000): # seconds in 32 days
            if os.path.isfile(fullpath):
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                cleanupdir(fullpath)


# =========================================================================================================
def getFeaturesdf(GDB):
    """
    Get a dataframe of unique FDS, FC, and FIELDS of a geodatabase.
    Parameters:  GDB = path to GDB
    Returns:  Pandas dataframe of with two columns: Feature Dataset, Feature Class for each fc in gdb.
    """

    d = pandas.DataFrame([])
    arcpy.env.workspace = GDB
    for theFDS in arcpy.ListDatasets():
        for theFC in arcpy.ListFeatureClasses(feature_dataset=theFDS):
            minFields = (fld.name.upper() for fld in arcpy.ListFields(os.path.join(GDB,theFDS,theFC)) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
            minFields = list(minFields)
            for FLD in minFields:
                d = d.append(pandas.DataFrame({'FDS': str(theFDS), 'FC': str(theFC), 'FLD': str(FLD.name)}, index=[0]), ignore_index=True)
    return(d)


# =========================================================================================================
def table_to_pandas_dataframe(table, field_names=None):
    """
    Converts an ArcGIS table to pandas dataframe.
    Parameters:
        table = Table readable by ArcGIS.
        field_names: List of fields.
    Returns: Pandas DataFrame object.
    """
    # If field names are not specified
    if not field_names:

        # get a list of field names
        field_names = get_field_names(table)

    # create a pandas data frame
    dataframe = DataFrame(columns=field_names)

    # use a search cursor to iterate rows
    with arcpy.da.SearchCursor(table, field_names) as search_cursor:

        # iterate the rows
        for row in search_cursor:

            # combine the field names and row items together, and append them
            dataframe = dataframe.append(
                dict(zip(field_names, row)),
                ignore_index=True
            )

    # return the pandas data frame
    return dataframe


# =========================================================================================================
# To
def pandas_to_table(pddf,tablename):
    """
    Converts a pandas dataframe into an ArcGIS table.
    Parameters:
        pddf = pandas dataframe
        tablename = output table name to 'installGDB'
    Returns:  A geodatabase table from pandas dataframe inside 'installGDB' geodatabase object (string to .gdb path)
    """
    x = numpy.array(numpy.rec.fromrecords(pddf))
    names = pddf.dtypes.index.tolist()
    x.dtype.names = tuple(names)
    gdbTbl = os.path.join(installGDB,tablename)
    if arcpy.Exists(gdbTbl):
        arcpy.Delete_management(gdbTbl)
    arcpy.da.NumPyArrayToTable(x, gdbTbl)


# =========================================================================================================
