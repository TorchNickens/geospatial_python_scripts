import arcpy, os, sys, traceback
from arcpy import env
env.overwriteOutput = True


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Post Migration Tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Add_Release_Policy_domain_and_add_to_feature_classes, Calc_releasePolicy, Calc_installationID]


#----------Add_Release_Policy_domain_and_add_to_feature_classes----------
#

class Add_Release_Policy_domain_and_add_to_feature_classes(object):
    def __init__(self):
        self.label = "1 Add Release Policy domain and associate with the releasePolicy field"
        self.description = "Adds the ReleasePolicy domain and it's coded values to a database. \
                            Then adds a releasePolicy field to each feature class in that database \
                            and associates the domain to that feature class"
        self.canRunInBackground = False

    def getParameterInfo(self):

        # First parameter
        workspace = arcpy.Parameter(
        displayName="Input DB",
        name="Input DB",
        datatype="Workspace",
        parameterType="Required",
        direction="Input")

        params = [workspace]

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return


    # Code block in here!
    def execute(self, parameters, messages):

        # Sub to see if a given domain exists
        def DomainExist(workspace, domainName):
            existingDomains = arcpy.da.ListDomains(workspace)
            # check if myNewDomain already exists
            for domain in existingDomains:
                if domain.name == domainName:
                    # print "Domain " + domName + " exists!"
                    return True
                    break

        # Set the input workspace
        workspace = parameters[0].valueAsText


        # Create output file
        logfile = os.path.splitext(workspace)[0] + "_" + "Add_Domain_logfile.csv"
        arcpy.AddMessage(logfile)
        output = open(logfile, "w")

        # Make a list of feature classes
        feature_classes = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype='FeatureClass'):
            for filename in filenames:
                feature_classes.append(os.path.join(dirpath, filename))


        # Set local parameters
        domName = "ReleasePolicy"
        inField = "releasePolicy"

        if not DomainExist(workspace, domName):
            # Create the coded value domain
            arcpy.CreateDomain_management(workspace, domName, "Release Policy", "TEXT", "CODED", "DEFAULT", "DEFAULT")

            # Store all the domain values in a dictionary with the domain code as the "key" and the
            # domain description as the "value" (domDict[code])
            domDict = {"UCNI":"Unclassified Nuclear Information", "FOUO":"For official use only"}

            # use a for loop to cycle through all the domain codes in the dictionary
            for code in domDict:
                arcpy.AddCodedValueToDomain_management(workspace, domName, code, domDict[code])

            for feature_class in feature_classes:
                arcpy.AddField_management(feature_class, inField, "TEXT", field_length = 4)
                print >> output, "added " + inField + " to " + feature_class
                arcpy.AddMessage("added " + inField + " to " + feature_class)
                arcpy.AssignDomainToField_management(feature_class, inField, domName)
            else:
                print "That domain already exists."
	output.close()

#----------end Add_Release_Policy_domain_and_add_to_feature_classes----------
#

#----------Calc_releasePolicy----------
#

class Calc_releasePolicy(object):
    def __init__(self):
        self.label = "2 Calc REL_POLICY to releasePolicy"
        self.description = "Calcs the data in REL_POLICY to the releasePolicy field"
        self.canRunInBackground = False

    def getParameterInfo(self):

        # First parameter
        workspace = arcpy.Parameter(
        displayName="Input DB",
        name="Input DB",
        datatype="Workspace",
        parameterType="Required",
        direction="Input")

        params = [workspace]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return


    # Code block in here!
    def execute(self, parameters, messages):

        def FieldExist(featureclass, fieldname):
            fieldList = arcpy.ListFields(featureclass, fieldname)
            fieldCount = len(fieldList)
            if (fieldCount == 1):
                return True
            else:
                return False

        # Set the input workspace
        workspace = parameters[0].valueAsText


        # Create output file
        #logfile = os.path.splitext(workspace)[0] + "_"calc_releasePolicy_log.csv"calc_releasePolicy_log.csv"
        logfile = os.path.join(os.environ['USERPROFILE'], "Desktop", os.path.splitext(workspace)[0].split(" ")[-1]+"_calc_releasePolicy_log.csv")   #####   HERE IS THE LINE I CHANGED  #####
        arcpy.AddMessage(logfile)
        output = open(logfile, "w")
        #print >> output, "Feature Dataset, Feature Class, Attribute, Total Features, Percent Complete"

        # Make a list of feature classes
        feature_classes = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype='FeatureClass'):
            for filename in filenames:
                feature_classes.append(os.path.join(dirpath, filename))


        # Set local parameters
        #domName = "ReleasePolicy"
        #inField = "releasePolicy"


        for feature_class in feature_classes:
            if FieldExist(feature_class, "REL_POLICY"):
                rows = arcpy.UpdateCursor(feature_class)

                for row in rows:
                    row.releasePolicy = row.REL_POLICY
                    rows.updateRow(row)

                try: del row
                except: pass
                del rows



		arcpy.DeleteField_management(feature_class, "REL_POLICY")
		arcpy.AddMessage("{} updated".format(feature_class))
		print >> output, "{} updated".format(feature_class)

        output.close()
#----------end Calc_releasePolicy----------
#


#---------------------------------------------------------------------------------------

class Calc_installationID(object):
    def __init__(self):
        self.label = "3 Calc installationID"
        self.description = "Deletes INSTL_ID if it exists and calc installationID fields"
        self.canRunInBackground = False

    def getParameterInfo(self):

        # First parameter
        workspace = arcpy.Parameter(
        displayName="Input DB",
        name="Input DB",
        datatype="Workspace",
        parameterType="Required",
        direction="Input")

        # Second parameter
        Installation = arcpy.Parameter(
        displayName="Installation",
        name="Installation",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        )

        Installation.filter.type = 'ValueList'
        Installation.filter.list = ['AWUB', 'GHLN', 'NZAS', 'QJVF', 'YWHG']


        params = [workspace, Installation]

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):

        workspace = parameters[0].valueAsText
        Installation = parameters[1].valueAsText

        env.overwriteOutput = True

        targetField1 = "InstallationID"
        targetField2 = "INSTLN_ID"

        targetValueRoot1 = Installation
        targetValue1 = "\"" + targetValueRoot1 + "\""
        targetValueRoot2 = "USAF"
        targetValue2 = "\"" + targetValueRoot2 + "\""


        # Set up log file
        #logfile = os.path.splitext(workspace)[0] + "_logfile.txt"
        logfile = os.path.join(os.environ['USERPROFILE'], "Desktop", os.path.splitext(workspace)[0].split(" ")[-1]+"_logfile.txt")   #####   HERE IS THE OTHER LINE I CHANGED  #####
        output = open(logfile, "a")
        startTime = datetime.datetime.now()
        print >> output, "Starting script Calc Static Fields at {}".format(startTime.strftime("%H:%M"))

        # Sub to see if a given field exists
        def FieldExist(featureclass, fieldname):
            fieldList = arcpy.ListFields(featureclass, fieldname)

            fieldCount = len(fieldList)
            if (fieldCount == 1):
                return True
            else:
                return False

        fcs = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype='FeatureClass'):
            for filename in filenames:
                fcs.append(os.path.join(dirpath, filename))


        for fc in fcs:
           arcpy.AddMessage("Calcing fc {}".format(fc))
           if (FieldExist(fc, targetField1)):
               arcpy.AddMessage("Calcing {0}".format(targetField1))
               arcpy.CalculateField_management(fc, targetField1, targetValue1, "VB", "")
           if (FieldExist(fc, targetField2)):
               arcpy.DeleteField_management(fc, targetField2)

        # Add finish time to log file and close
        finishTime = datetime.datetime.now()
        print >> output, "Ending script Calc Static Fields at {}".format(finishTime.strftime("%H:%M"))
        output.close()

#-----------------------------------------------------------------------------------------------

#
