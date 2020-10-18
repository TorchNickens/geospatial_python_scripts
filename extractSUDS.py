import arcpy, logging, os, traceback

def main():

    # Set up logging
    LOG_FILENAME =  r"C:\Users\1528874122E\Desktop\afSuds\sudsResults.log"

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= LOG_FILENAME,
                    filemode='w')
    try:

        # Connection path to geodatabse
        folder = r"C:\Users\1528874122E\Desktop\inSuds"
        subsFolder = r"C:\Users\1528874122E\Desktop\afSuds"

        arcpy.env.workspace = folder

        for db in arcpy.ListWorkspaces():
            arcpy.env.workspace = db
            print (os.path.basename(db))
            logging.info (os.path.basename(db))
            if db.endswith(('.gdb', '.mdb')):
                dbName = os.path.splitext(os.path.basename(db))[0]
                if 'SpaceUtilization' in arcpy.ListDatasets():
                    arcpy.CreateFileGDB_management(subsFolder, dbName)
                    arcpy.CreateFeatureDataset_management(os.path.join(subsFolder, dbName+'.gdb'), 'SpaceUtilization')
                    sudsFCs = arcpy.ListFeatureClasses("*", "", "SpaceUtilization")
                    for fc in sudsFCs:
                        arcpy.FeatureClassToFeatureClass_conversion(fc, os.path.join(subsFolder, dbName+'.gdb', 'SpaceUtilization'), fc)
                    arcpy.Compact_management(os.path.join(subsFolder, dbName+'.gdb'))
                    print ("  > {} SpaceUtilization feature classes present".format(len(sudsFCs)))
                    print ("   "+", ".join(fc for fc in sudsFCs))
                    logging.info ("  > {} SpaceUtilization feature classes present".format(len(sudsFCs)))
                    logging.info ("   "+", ".join(fc for fc in sudsFCs))
                else:  # Check for suds data in loose feature classes
                    print ("  > SpaceUtilization datasest not provided")
                    logging.info ("  > SpaceUtilization datasest not provided")
                    looseFCs = [fc for fc in arcpy.ListFeatureClasses("*", "", "") if fc in ['FloorArea_P', 'BuildingFloor_A', 'BuildingRoomArea_A', 'BuildingSpaceObstruction_A', 'BuildingSpace_A', 'CadFloorPlan_L']]
                    if len(looseFCs) > 0:
                        arcpy.CreateFileGDB_management(subsFolder, dbName)
                        arcpy.CreateFeatureDataset_management(os.path.join(subsFolder, dbName+'.gdb'), 'SpaceUtilization')
                        for fc in looseFCs:
                            arcpy.FeatureClassToFeatureClass_conversion(fc, os.path.join(subsFolder, dbName+'.gdb', 'SpaceUtilization'), fc)
                        arcpy.Compact_management(os.path.join(subsFolder, dbName+'.gdb'))
                        print ("  > {} loose SpaceUtilization feature classes present".format(len(looseFCs)))
                        print ("   "+", ".join(fc for fc in looseFCs))
                        logging.info ("  > {} loose SpaceUtilization feature classes present".format(len(looseFCs)))
                        logging.info ("   "+", ".join(fc for fc in looseFCs))
                    else:
                        print ("  > SpaceUtilization feature classes not provided")
                        logging.info ("  > SpaceUtilization feature classes not provided")


    except:
        logging.info('Failed...')

        # Return any Python specific errors
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        print ("PYTHON ERRORS:\nTraceback Info:\n{}\n  Error Info:\n    {}: {}\n".format(tbinfo, sys.exc_type, sys.exc_value))
        logging.info ("PYTHON ERRORS:\nTraceback Info:\n{}\n  Error Info:\n    {}: {}\n".format(tbinfo, sys.exc_type, sys.exc_value))

    finally:
        # Cleanup
        arcpy.ClearWorkspaceCache_management()

if __name__ == '__main__':
   main()