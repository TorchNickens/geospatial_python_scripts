import arcpy, os

timestamp = time.strftime("%Y%d%m %H%M%S", time.localtime())
print "Started @ " + timestamp

gdb_path = r"C:\Users\1528874122E\Desktop\ScriptProjects\Python_scripts\CIP\cipFINAL\AF_GeoBase_CIP_FINALwMeta20181217.gdb".replace("\\","/")
dest_path = r"C:\Users\1528874122E\Desktop\ScriptProjects\gdb_processing\311_AF_GeoBase_20180723_CIP_BatSurvey.gdb".replace("\\","/")

print("Source Data: {}".format(gdb_path))
print("CIP Shell: {}".format(dest_path))
arcpy.env.workspace = gdb_path

CIP_realPropertyUniqueIdentifier = ('ImpactArea_A', 'MilitaryTrainingLocation_A', 'RecreationArea_A', 'AccessControl_L', 'AccessControl_P', 'Bridge_A', 'Bridge_L')

batSurveySites = ('1377', '5002', '2479', '2480', '3276', '3219', '1555', '3143', '2310', '2525', '2521') #('Andrews AFB', 'Fort Eustis', 'Langley AFB', 'Langley FH Annex', 'Ship Shoal Island', 'Robins AFB', 'Cape Canaveral AFS', 'Patrick AFB', 'Jonathan Dickinson Missile Tracking Annex', 'Malabar Transmitter Annex', 'MacDill AFB')

# Append final CIP data to bat CIP shell
for fd in arcpy.ListDatasets():
    for fc in arcpy.ListFeatureClasses("*", "All", fd):
        print "{}/{}...".format(fd.upper(), fc)
        arcpy.MakeFeatureLayer_management(os.path.join(gdb_path,fd,fc), fc+"_lyr")
        where = "realPropertySiteUniqueID IN {}".format(batSurveySites)
        arcpy.SelectLayerByAttribute_management (in_layer_or_view=fc+"_lyr", selection_type="NEW_SELECTION", where_clause=where)
        count = int(arcpy.GetCount_management(fc + "_lyr").getOutput(0))
        if fc in CIP_realPropertyUniqueIdentifier:
            field_names = [field.name.lower() for field in arcpy.ListFields(os.path.join(dest_path, fd, fc))]
            if "realpropertyuniqueidentifier" in field_names:
                print "***CORRECT RPUID FIELD EXISTS FOR {}***".format(fc)
            else:
                print "***realPropertyUniqueIdentifier FIELD ADDED {}***".format(fc)
                arcpy.AddField_management(in_table=os.path.join(dest_path,fd,fc), field_name="realPropertyUniqueIdentifier", field_type="TEXT", field_length="20", field_alias="realPropertyUniqueIdentifier")
        if count > 0:
            print "   Appending {} features from {}/{} to the geodatabase shell defined".format(count, fd, fc)
            arcpy.Append_management(fc+"_lyr", os.path.join(dest_path,fd,fc), "NO_TEST")
            arcpy.Delete_management(fc+"_lyr")
        else:
            print "   No features for defined sites in source CIP layer {} to append".format(fc)

timestamp_end = time.strftime("%Y%d%m %H%M%S", time.localtime())
print "Finished @ " + timestamp_end
