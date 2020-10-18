# version for 3.1.1 Shell

import arcpy, os

timestamp = time.strftime("%Y%d%m %H%M%S", time.localtime())
print "Started @ " + timestamp

gdb_path = r"C:\Users\1528874122E\Desktop\ScriptProjects\Python_scripts\CIP\cipFINAL\311_AF_GeoBase_Shell_DRAFT_20180723_CIP_FINALwMeta.gdb".replace("\\","/")
arcpy.env.workspace = gdb_path

CIP_Datasets = ('Auditory', 'Cadastre', 'environmentalCulturalResources', 'environmentalNaturalResources', 'environmentalRestoration', 'MilitaryRangeTraining', 'Pavements',
                'Planning', 'RealProperty', 'Recreation', 'Security', 'Transportation', 'WaterWays')

CIP_Layers = ('NoiseZone_A', 'Installation_A', 'LandParcel_A', 'Outgrant_A', 'Site_A', 'Site_P', 'HistoricDistrict_A', 'Wetland_A', 'EnvironmentalRemediationSite_A', 'ImpactArea_A',
              'MilitaryRange_A', 'MilitaryTrainingLocation_A', 'MilQuantityDistCombinedArc_A', 'PavementBranch_A', 'PavementSection_A', 'AirAccidentZone_A', 'LandUse_A', 'Building_A',
              'Tower_P', 'GolfCourse_A', 'RecreationArea_A', 'AccessControl_L', 'AccessControl_P', 'Fence_L', 'Bridge_A', 'Bridge_L', 'RailSegment_L', 'RailTrack_L', 'RoadCenterline_L',
              'RoadPath_L', 'RoadSeg_L', 'VehicleParking_A', 'DocksAndWharfs_A')

# Remove non-CIP feature datasets
for fd in arcpy.ListDatasets():
    fdName = os.path.basename(fd)

    if fdName not in CIP_Datasets:
        arcpy.Delete_management(in_data=fd)

    else:
        for fc in arcpy.ListFeatureClasses("*", "All", fdName):
            fcName = os.path.basename(fc)

            if fcName not in CIP_Layers:
                arcpy.Delete_management(in_data=fc)

timestamp_end = time.strftime("%Y%d%m %H%M%S", time.localtime())
print "Finished @ " + timestamp_end
