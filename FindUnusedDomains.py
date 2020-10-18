#-------------------------------------------------------------------------------
# Name:             Find Unused Domains
# Author:           Marie Cline Delgado
# Last Updated:     29 SEPT 2018
#-------------------------------------------------------------------------------

import arcpy, os, sys, logging

def main():
    try:
        # Connection path to geodatabse (as administrator if SDE)
        myGDB = r"C:\Users\1528874122E\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\Connection to HQV_72.sde"

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
        #del domainsExisting
        #del domainsUnused_names

    finally:
        # Cleanup
        arcpy.ClearWorkspaceCache_management()

if __name__ == '__main__':
    main()