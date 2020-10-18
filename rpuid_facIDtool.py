#-------------------------------------------------------------------------------
# Name:        Appending Feature Classes by Shape Type for RPUID and facilityID evaluation
# Author:      Marie Cline Delgado
# Created:     10 JAN 2019
#-------------------------------------------------------------------------------

import arcpy, os, Tkinter, tkFileDialog, itertools

timestamp = time.strftime("%Y%d%m %H%M%S", time.localtime())
print "Started @ " + timestamp

#====================================================================================================
# Setting up Tkinter directory dialog window
root = Tkinter.Tk()
root.withdraw()
root.attributes('-topmost', True)
getGDBLoc = tkFileDialog.askdirectory(parent=root, initialdir="C:", title='Select the GDB for realPropertyUniqueIdentifier and facilityID evaluation')
root.attributes('-topmost', False)
inWork = os.path.abspath(getGDBLoc).replace("\\","/")
if len(inWork) > 0:
    print("GDB selected: %s" % inWork)
    root.destroy()

# Seting up Tkinter radio button selection to selection of CIP data consideration or Full GDB
dataUse = ''
def buttonAction():
    global dataUse
    dataUse = choice.get()
    master.destroy()

master = Tkinter.Tk()
master.attributes('-topmost', True)
master.title("Data usage selection")
master.geometry("250x130")

choice = Tkinter.StringVar()
choice.set("CIP")

chooseOption = Tkinter.Label(master, text="Select datasets to use in geoprocessing")
rButtonCIP = Tkinter.Radiobutton(master, text="CIP data only", variable=choice, value="CIP")
rButtonFULL = Tkinter.Radiobutton(master, text="Full geodatabase", variable=choice, value="FULL")
confirmButton = Tkinter.Button(master, text="OK", command=buttonAction)

chooseOption.grid(column="1", row="0")
rButtonCIP.grid(column="1", row="1")
rButtonFULL.grid(column="1", row="2")
confirmButton.grid(column="1", row="3")

master.mainloop()
if dataUse == "CIP":
    gdbTag = "_cip"
    print (" > Geoprocessing CIP data only")
elif dataUse == "FULL":
    gdbTag = "_full"
    print (" > Geoprocessing full geodatabase")
#====================================================================================================

arcpy.env.workspace = inWork
arcpy.env.overwriteOutput = True

# Create output workspace and variables
outWork = os.path.dirname(inWork)
outName = os.path.splitext(os.path.basename(inWork))[0]+"_rpuidFacilityIDtool"+gdbTag
arcpy.CreateFileGDB_management(outWork, outName, "CURRENT")
outName = outName+".gdb"
CIP_Datasets = ['Auditory', 'Cadastre', 'environmentalCulturalResources', 'environmentalNaturalResources',
                'environmentalRestoration', 'MilitaryRangeTraining', 'Pavements','Planning', 'RealProperty',
                'Recreation', 'Security', 'Transportation', 'WaterWays']
CIP_Layers = ['NoiseZone_A', 'Installation_A', 'LandParcel_A', 'Outgrant_A', 'Site_A', 'Site_P',
                'HistoricDistrict_A', 'Wetland_A', 'EnvironmentalRemediationSite_A', 'ImpactArea_A',
                'MilitaryRange_A', 'MilitaryTrainingLocation_A', 'MilQuantityDistCombinedArc_A',
                'PavementBranch_A', 'PavementSection_A', 'AirAccidentZone_A', 'LandUse_A', 'Building_A',
                'Tower_P', 'GolfCourse_A', 'RecreationArea_A', 'AccessControl_L', 'AccessControl_P', 'Fence_L',
                'Bridge_A', 'Bridge_L', 'RailSegment_L', 'RailTrack_L', 'RoadCenterline_L','RoadPath_L',
                'RoadSeg_L', 'VehicleParking_A', 'DocksAndWharfs_A']

# Sorting through data to determine which datasets are kept and which final output they will append to
polygonFC, pointFC, lineFC, SUpolygonFC, SUlineFC = [], [], [], [], []
datasets = CIP_Datasets if dataUse == "CIP" else arcpy.ListDatasets()
for dataset in datasets:
    fcs = list(set(arcpy.ListFeatureClasses('*','',dataset)).intersection(CIP_Layers)) if dataUse == "CIP" else arcpy.ListFeatureClasses('*','',dataset)
    for fc in fcs:
        fields = [fld.name.lower() for fld in arcpy.ListFields(fc)]
        shpType = arcpy.Describe(fc).shapeType
        if "realpropertyuniqueidentifier" in fields and "facilityid" in fields:
            print("  >> {} : {}".format(fc, shpType))
            if dataset != 'SpaceUtilization' and shpType == 'Polygon':
                polygonFC.append(fc)
            elif dataset != 'SpaceUtilization' and shpType == 'Point':
                pointFC.append(fc)
            elif dataset != 'SpaceUtilization' and shpType == 'Polyline':
                lineFC.append(fc)
            elif dataset == 'SpaceUtilization' and shpType == 'Polygon':
                SUpolygonFC.append(fc)
            elif dataset == 'SpaceUtilization' and shpType == 'Polyline':
                SUlineFC.append(fc)
        elif "realpropertyuniqueidentifier" in fields and "buildingnumber" in fields:
            print("  >> {} : {}".format(fc, shpType))
            if fc == "Building_A":
                # For auto field mapping in append
                arcpy.CopyFeatures_management(fc, "in_memory//Building_A")
                arcpy.AddField_management("in_memory//Building_A", "facilityID", "Text", 5)
                arcpy.CalculateField_management("in_memory//Building_A", "facilityID", "!buildingNumber!", "PYTHON_9.3")
                polygonFC.append("in_memory//Building_A")

# Creating feature classes and fields in geodatabase for append
fc_LL = [[polygonFC,"PolygonFeatures","POLYGON"], [pointFC,"PointFeatures","POINT"],
        [lineFC,"LineFeatures","POLYLINE"], [SUpolygonFC,"SpaceUse_PolygonFeatures","POLYGON"],
        [SUlineFC,"SpaceUse_LineFeatures","POLYLINE"]]
for grp in fc_LL:
    var = grp[0]
    fc = grp[1]
    shp = grp[2]
    arcpy.CreateFeatureclass_management(out_path=os.path.join(outWork, outName), out_name=fc, geometry_type=shp, spatial_reference=arcpy.SpatialReference(4326))   # spatial ref object of 'GCS_WGS_1984'
    arcpy.AddField_management(os.path.join(outWork, outName, fc), "sdsFeatureName", "Text", 80)
    arcpy.AddField_management(os.path.join(outWork, outName, fc), "realPropertyUniqueIdentifier", "Text", 20)
    arcpy.AddField_management(os.path.join(outWork, outName, fc), "facilityID", "Text", 5)
    arcpy.AddField_management(os.path.join(outWork, outName, fc), "realPropertySiteUniqueID", "Text", 20)
    if len(var) > 0:
        print("Appending {}".format(fc))
        arcpy.Append_management(var, os.path.join(outWork, outName,fc).replace("\\", "/"), "NO_TEST")
        # Changing name of facilityID field to facilityNumber because James asked me to.  Eases workflow for analysts.
        # Changing name after append so auto field mapping functions successfully.
        arcpy.AlterField_management(in_table=os.path.join(outWork, outName,fc), field="facilityID", new_field_name="facilityNumber", new_field_alias="facilityNumber")
    else:
        print("No {} data to append".format(fc))

timestamp = time.strftime("%Y%d%m %H%M%S", time.localtime())
print "Complete @ " + timestamp
raw_input("Press enter to close")