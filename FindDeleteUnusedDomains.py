#-------------------------------------------------------------------------------
# Name:             Find/Delete Unused Domains
# Author:           Marie Cline Delgado
# Last Updated:     29 SEPT 2018
#-------------------------------------------------------------------------------

import arcpy
from contextlib import contextmanager
import os
import shutil
import tempfile

def main():
    try:
        # Connection path to geodatabse (as administrator if SDE)
        myGDB = r"C:\GISConnections\SDE@GTEST.sde"

        # Get domains that are assigned to a field
        domainsUsed_names = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(myGDB, datatype=["FeatureClass", "Table"]):
            for filename in filenames:
                print "Checking {}".format(os.path.join(dirpath, filename))

                ## Check for normal field domains
                for field in arcpy.ListFields(os.path.join(dirpath, filename)):
                    if field.domain:
                        domainsUsed_names.append(field.domain)

                ## Check for domains used in a subtype field
                subtypes = arcpy.da.ListSubtypes(os.path.join(dirpath, filename))
                for stcode, stdict in subtypes.iteritems():
                    if stdict["SubtypeField"] != u'':
                        for field, fieldvals in stdict["FieldValues"].iteritems():
                            if not fieldvals[1] is None:
                                domainsUsed_names.append(fieldvals[1].name)
                ## end for subtypes
            ## end for filenames
        ## end for geodatabase Walk

        # List of all existing domains (as domain objects)
        domainsExisting = arcpy.da.ListDomains(myGDB)

        # Find existing domain names that are not in use (using set difference)
        domainsUnused_names = (
            set([dom.name for dom in domainsExisting]) - set(domainsUsed_names)
        )

        # Get domain objects for unused domain names
        domainsUnused = [
            dom for dom in domainsExisting
            if dom.name in domainsUnused_names
        ]
        print "{} unused domains in {}".format(len(domainsUnused), myGDB)

        # Cleanup
        del domainsExisting
        del domainsUnused_names

        # Delete unused domains by owner
        ## For local geodatabses, owner is an empty string ('')
        with makeTempDir() as temp_dir:
            descGDB = arcpy.Describe(myGDB)
            for owner in set([dom.owner for dom in domainsUnused]):
                if descGDB.workspaceType == "RemoteDatabase":
                    ## Use temporary SDE connection as owner
                    myGDB = arcpy.CreateDatabaseConnection_management(
                        temp_dir,  ## out_folder_path
                        owner+".sde",  ## out_name
                        "ORACLE",  ## database_platform
                        "GISTEST.WORLD",  ## instance
                        "DATABASE_AUTH",  ## account_authentication
                        owner,  ## username
                        "myuserpass",  ## password
                    )
                    print arcpy.GetMessages()

                    ## Format result object as string for path to connection file
                    myGDB = str(myGDB)

                # Get unused domains for current owner
                domainsUnused_currentOwner = [
                    dom.name for dom in domainsUnused
                    if dom.owner == owner
                ]
                for domain in domainsUnused_currentOwner:
                    arcpy.DeleteDomain_management(myGDB, domain)
                    print "\t{} deleted".format(domain)
            ## end for domainsExisting_owners
        ## end with temp_dir

    finally:
        # Cleanup
        arcpy.ClearWorkspaceCache_management()

@contextmanager
def makeTempDir():
    """Creates a temporary folder and returns the full path name.
    Use in with statement to delete the folder and all contents on exit.
    Requires contextlib contextmanager, shutil, and tempfile modules.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()