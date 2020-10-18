import arcpy, logging, os, sys

def main():

    # Set up logging
    LOG_FILENAME =  r"C:\Users\1528874122E\Desktop\test\UnusedDomain.log"

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= LOG_FILENAME,
                    filemode='w')
    try:

        # Connection path to geodatabse
        myGDB = r"C:\Users\1528874122E\Desktop\test\311_Croughton_CIP.gdb"

        # Get domains that are assigned to a field
        domainsUsed_names = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(myGDB, datatype=["FeatureClass", "Table"]):
            for filename in filenames:
                print("Checking {}".format(os.path.join(dirpath, filename)))

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

        print "{} unused domains in {}".format(len(domainsUnused_names), myGDB)
        logging.info( "{} unused domains in {}".format(len(domainsUnused_names), myGDB))
##        for dom in domainsUnused:
##            logging.info( "{}".format(dom.name))

        print "{} active domains in {}".format(len(set(domainsUsed_names)), myGDB)
        logging.info( "{} active domains in {}".format(len(set(domainsUsed_names)), myGDB))
        for dom in domainsUsed_names:
            logging.info( "{}".format(dom))

    except:
        logging.info('Failed...')
        sys.exit(2)

    finally:
        # Cleanup
        arcpy.ClearWorkspaceCache_management()

if __name__ == '__main__':
   main()