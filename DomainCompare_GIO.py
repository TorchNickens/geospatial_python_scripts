import arcpy, logging, os, sys, collections

def main():

    # Set up logging
    LOG_FILENAME =  r"C:\Users\1528874122E\Desktop\test\DomainCompare.log"

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= LOG_FILENAME,
                    filemode='w')
    try:

        # Percent to consider a strong match
        percent = 75

        # Connection path to geodatabse
        myGDB = r"C:\Users\1528874122E\Desktop\ScriptProjects\AFAdaptation311\311_AF_GeoBase_Shell_2018.gdb"

        # List of all existing domains (as domain objects)
        domainDesc = dict((str(domain.name), sorted(list(value.lower() for value in domain.codedValues.values()))) for domain in arcpy.da.ListDomains(myGDB) if domain.domainType == 'CodedValue')

        # Finds domains with duplicate values in the exact same order
        rev_domainDesc = {}
        for key, value in domainDesc.items():
            rev_domainDesc.setdefault(str(value), set()).add(key)
        dup_domainDesc = dict((key, values) for key, values in rev_domainDesc.items() if len(values) > 1)

        print "{} sets of identical matching domain descriptions found in {}".format(len(dup_domainDesc), myGDB)
        logging.info("{} sets of identical matching domain descriptions found in {}".format(len(dup_domainDesc), myGDB))

        for values in dup_domainDesc.values():
            logging.info(", ".join(val for val in values))

        strongMatch=[]
        # Finds domains with a % match of coded value descriptions
        for aKey, aValList in domainDesc.iteritems():
            for bKey, bValList in domainDesc.iteritems():
                if aKey != bKey:
                    matches = [x for x in aValList if x in bValList]
                    if len(matches)>0:
                        percentMatchAB = (float(len(matches))/float(len(aValList)))*100
                        percentMatchBA = (float(len(matches))/float(len(bValList)))*100
                        if percentMatchAB>=percent and percentMatchBA>=percent:
                            strongMatch.append(list((aKey, bKey)))

        print "{} sets of strong matching domain descriptions found in {}".format(len(strongMatch), myGDB)
        logging.info("{} sets of strong matching domain descriptions found in {}".format(len(strongMatch), myGDB))

        for values in strongMatch:
            logging.info(", ".join(val for val in values))

    except:
        logging.info('Failed...')
        sys.exit(2)

    finally:
        # Cleanup
        arcpy.ClearWorkspaceCache_management()

if __name__ == '__main__':
   main()