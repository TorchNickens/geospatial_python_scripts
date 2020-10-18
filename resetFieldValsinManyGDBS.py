import arcpy, os

badFCs = ["RealProperty/Building_A", "RealProperty/Tower_P"]

gdbsFolder = r"C:\Users\1528874122E\Desktop\ScriptProjects\Python_scripts\CIP\group11_ANG1\311Package_try\Test".replace("\\", "/")

arcpy.env.workspace = gdbsFolder

for gdb in arcpy.ListWorkspaces(workspace_type="FileGDB"):
    arcpy.env.workspace = gdb
    print gdb
    for fc in badFCs:
        if fc == "RealProperty/Building_A":
            field = "missionDependencyIndex"
        elif fc == "RealProperty/Tower_P":
            field = "pipeOpeningSizeInInches"
        if arcpy.Exists(os.path.join(gdb,fc)):
            with arcpy.da.UpdateCursor(fc, [field]) as cursor:
                for row in cursor:
                    if row[0] == 99999 or row[0] == "TBD":
                        row[0] = 9999
                        print field + " updated"
                    cursor.updateRow(row)


