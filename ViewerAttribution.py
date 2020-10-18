#-------------------------------------------------------------------------------
# Name:        GIS Viewer Attribution Evaluation
# Version:     V_1.3
# Purpose:     Produce report for installtion geodatabase detailing data attribution
#
# Author:      Marie Cline Delgado
#
# Created:     26 JAN 2018
# Last Update: 09 AUG 2018
# Description: Evaluate installation geodatabases for minimum attribution required
#              by AFCEC GIS viewer for best display of data.
#-------------------------------------------------------------------------------

# Import modules
import arcpy, time, os, sys, Tkinter, tkFileDialog, collections, xlwt
from datetime import datetime
from operator import itemgetter

# Start time
startT = datetime.now()
print(startT)

# Main folder directory variable
mainDir = os.path.dirname(sys.argv[0])
if not os.path.exists(os.path.join(mainDir, "_Output")):
    os.mkdir(os.path.join(mainDir, "_Output"))
outputLoc = os.path.join(mainDir, "_Output")

vwrMinGDB = os.path.join(mainDir, "Viewer_minimum.gdb")
compGDB = vwrMinGDB
gdbTag = "_viewerMinimum"

# Setting up Tkinter file dialog ask directory to get file path for installation geodatabase being compared
root = Tkinter.Tk()
root.withdraw()
root.attributes('-topmost', True)
currentDir = mainDir
gdbDir = tkFileDialog.askdirectory(parent=root, initialdir=currentDir, title='Select the installation geodatabase for evaluation')
installationName = os.path.splitext((os.path.split(gdbDir)[1]))[0]
if len(gdbDir) > 0:
    print("Geodatabase selected: %s" % os.path.abspath(gdbDir))
root.destroy()


#Block for later upgrade
#===================================================================================================================================
### Seting up Tkinter radio button selection for Viewer Minimum Attribution comparison or Other Geodatabase Attribution comparison
##compGDB = ''
##def buttonAction():
##    global compGDB
##    compGDB = choice.get()
##    print compGDB
##    master.destroy()
##
###vwrMinGDB3101 = os.path.join(mainDir, "Viewer_minimum3101.gdb")
###vwrMinGDB311 = os.path.join(mainDir, "Viewer_minimum311.gdb")
##
##master = Tkinter.Tk()
##master.attributes('-topmost', True)
##master.title("Schema comparison")
##master.geometry("250x130")
##
##choice = Tkinter.StringVar()
##choice.set(vwrMinGDB3101)
##
##chooseOption = Tkinter.Label(master, text="Slect geodatabase for schema comparison")
##rButton1 = Tkinter.Radiobutton(master, text="Viewer Minimum Attribution for 3.101", variable=choice, value=vwrMinGDB3101)
##rButton2 = Tkinter.Radiobutton(master, text="Viewer Minimum Attribution for 3.11", variable=choice, value=vwrMinGDB311)
##confirmButton = Tkinter.Button(master, text="OK", command=buttonAction)
##
##chooseOption.grid(column="1", row="0")
##rButton1.grid(column="1", row="1")
##rButton2.grid(column="1", row="2")
##confirmButton.grid(column="1", row="3")
##
##master.mainloop()
##if compGDB == vwrMinGDB3101:
##    gdbTag = "_viewerMinimum3101"
##elif compGDB == vwrMinGDB311:
##    gdbTag = "_viewerMinimum311"
#===================================================================================================================================

try:
    # Set workspace to viewer minimum attribution geodatabase or full database attribution database
    workpath = compGDB
    arcpy.env.workspace = workpath

    # Storing variables for minimum attribution
    print("Reading geodatabase attribution requirements...")
    print("Patience, grasshopper...\n")
    print("              //_____ __        ")
    print("             @ )====// .\___    ")
    print("             \#\_\__(_/_\\_/    ")
    print("               / /       \\     \n")

    def listFcsInGDB():
        ''' set your arcpy.env.workspace to viewer minimum attribution gdb before calling '''
        for fds in arcpy.ListDatasets('','feature') + ['']:
            for fc in arcpy.ListFeatureClasses('','',fds):
                minFields = (fld.name for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
                reqDomains = (fld.domain for fld in arcpy.ListFields(fc) if str(fld.name) not in ['Shape', 'OBJECTID', 'Shape_Length', 'Shape_Area'])
                for f, d in zip(minFields, reqDomains):
                    yield os.path.join(fds, fc, f, d) # add arcpy.env.workspace at beginning of join if want to keep the viewer workspace in the file path
    vwrDataList = list(listFcsInGDB())
    print("Minimum attribution stored")

    # Create XLSX workbook
    wb = xlwt.Workbook(encoding = "utf-8")

    # Add worksheets to workbook
    missingFCSheet = wb.add_sheet('MissingFC', cell_overwrite_ok=True)
    missingFieldSheet = wb.add_sheet('MissingFields', cell_overwrite_ok=True)
    emptyFCSheet = wb.add_sheet('EmptyFC', cell_overwrite_ok=True)
    nullSheet = wb.add_sheet('NullFC', cell_overwrite_ok=True)
    populatedValuesSheet = wb.add_sheet('PopulatedValues', cell_overwrite_ok=True)

    # Set up formatting
    style0 = xlwt.easyxf('pattern: pattern solid, fore_color blue; font: name Calibri, height 240, color white, bold True; align: horiz left;'
                'borders: top thin, bottom thin, left thin, right thin;')
    style1 = xlwt.easyxf('pattern: pattern solid, fore_color white; font: name Calibri, height 240, color black, bold True; align: horiz left;'
                'borders: top thick, bottom thin, left thin, right thin, top_color gray50, bottom_color gray25, left_color gray25, right_color gray25;'
                'align: vert bottom;')
    style2 = xlwt.easyxf('pattern: pattern solid, fore_color white; font: name Calibri, height 240, color black, bold False; align: horiz left;'
                'borders: top thin, bottom thin, left thin, right thin, top_color gray25, bottom_color gray25, left_color gray25, right_color gray25;'
                'align: vert bottom;')
    style3 = xlwt.easyxf('pattern: pattern solid, fore_color white; font: name Calibri, height 240, color red, bold False; align: horiz left;'
                'borders: top thin, bottom thin, left thin, right thin, top_color gray25, bottom_color gray25, left_color gray25, right_color gray25;'
                'align: vert bottom;')
    missingFCSheet.col(0).width = 500 * 30
    missingFieldSheet.col(0).width = 400 * 30
    missingFieldSheet.col(1).width = 300 * 30
    emptyFCSheet.col(0).width = 500 * 30
    emptyFCSheet.col(1).width = 300 * 30
    nullSheet.col(0).width = 800 * 30
    nullSheet.col(1).width = 400 * 15
    populatedValuesSheet.col(0).width = 800 * 30
    populatedValuesSheet.col(1).width = 400 * 15

    # Add header row
    missingFCSheet.write(0,0,"FEATURE CLASS", style0)
    missingFieldSheet.write(0,0,"FEATURE CLASS", style0)
    missingFieldSheet.write(0,1, "SYMBOLOGY-DEPENDENT FIELD", style0)
    emptyFCSheet.write(0,0,"FEATURE CLASS", style0)
    emptyFCSheet.write(0,1,"SYMBOLOGY-DEPENDENT FIELD", style0)
    nullSheet.write(0,0,"FEATURE CLASS | FIELD | DOMAIN", style0)
    nullSheet.write(0,1,"NULL VALUE COUNT", style0)
    populatedValuesSheet.write(0,0,"FEATURE CLASS | FIELD | DOMAIN", style0)
    populatedValuesSheet.write(0,1,"VALUE COUNT", style0)

    # Change workspace to installation geodatabase for evaluation
    workpath = gdbDir
    arcpy.env.workspace = workpath

    # Search installation database for minimum attribution and write findings to Excel spreadsheet
    print("Evaluating installation geodatabase and writing results to Excel for... " + installationName + "\n")
    mFCRow = 1
    mFldRow = 1
    eFCRow = 1
    nullRow = 1
    popRow = 1
    for data in vwrDataList:
        theFDFC = data.rsplit("\\", 2)[0]
        theFLD = data.rsplit("\\", 2)[1]
        theDMN = data.rsplit("\\", 2)[2]
        # CHECK FOR EXISTANCE OF FEATURE CLASS
        if arcpy.Exists(theFDFC):
            print ("Evaluating: " + data)
            instFCFields = [(str(afld.name).upper(), afld) for afld in arcpy.ListFields(theFDFC)]
            domains = arcpy.da.ListDomains()
            # CHECK FOR EXISTANCE OF FIELD IN FEATURE CLASS
            if theFLD.upper() in map(itemgetter(0), instFCFields):
                idx = map(itemgetter(0), instFCFields).index(theFLD.upper())
                # BUILD LIST OF VALUES AND COUNTS OF SYMBOLOGY-DEPENDENT FIELD
                with arcpy.da.SearchCursor(theFDFC, theFLD) as cur:
                    nullValues = [None, "None", "none", "NONE", "", " ", "NA", "N/A", "n/a", "Other", "other", "OTHER", "TBD", "<Null>"]
                    NoneType = type(None)
                    countValues = collections.Counter(row[0] for row in cur)
                    sumValues = sum(collections.Counter(countValues).values())
                    countNulls = list((n[0], n[1]) for n in countValues.items() if n[0] in nullValues)
                    sumNulls = sum(n[1] for n in countNulls)
                    domainName = map(itemgetter(1), instFCFields)[idx].domain
                    domainVals = []
                    domainRng = []
                    for domain in domains:
                        if domain.name == domainName:
                            if domain.domainType == 'CodedValue':
                                domainVals = [val for val, desc in domain.codedValues.items()]
                            elif domain.domainType == 'Range':
                                domainRng = range(int(domain.range[0]), int((domain.range[1]+1)))
                # FEATURE CLASS IS EMPTY
                if len(countValues) == 0:
                    print('FEATURE CLASS IS EMPTY\n\n')
                    emptyFCSheet.write(eFCRow, 0, theFDFC, style2)
                    emptyFCSheet.write(eFCRow, 1, theFLD, style2)
                    eFCRow+=1
                # GREATER THAN 90% NULLS IN SYMBOLOGY-DEPENDENT FIELD
                elif sumNulls >= sumValues*.9:
                    nullSheet.write(nullRow, 0, theFDFC + " | FIELD:  " + theFLD + " | DOMAIN:  " + theDMN, style1)
                    nullSheet.write(nullRow, 1, "", style1)
                    nullRow+=1
                    for v in countNulls:
                        print (theFLD + " FIELD CONTAINS 90% NULL VALUES")
                        nullSheet.write(nullRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                        nullSheet.write(nullRow, 1, v[1], style2)
                        nullRow+=1
                    print("\n")
                # POPULATED WITH VARIATION OF VALUES
                else:
                    # CREATE NEW SHEET WHEN MAX EXCEL ROWS APPROACHED
                    if popRow == 65500:
                        populatedValuesSheetCont = wb.add_sheet('PopulatedValues_cont', cell_overwrite_ok=True)
                        populatedValuesSheetCont.col(0).width = 800 * 30
                        populatedValuesSheetCont.col(1).width = 400 * 15
                        populatedValuesSheetCont.write(0,0,"FEATURE CLASS | FIELD | DOMAIN", style0)
                        populatedValuesSheetCont.write(0,1,"VALUE COUNT", style0)
                        newPopRow = 1
                        popRow+=1
                    # CREATE ANOTHER NEW SHEET WHEN MAX EXCEL ROWS APPROACHED AGAIN
                    elif popRow == 131000:
                        populatedValuesSheetCont2 = wb.add_sheet('PopulatedValues_cont2', cell_overwrite_ok=True)
                        populatedValuesSheetCont2.col(0).width = 800 * 30
                        populatedValuesSheetCont2.col(1).width = 400 * 15
                        populatedValuesSheetCont2.write(0,0,"FEATURE CLASS | FIELD | DOMAIN", style0)
                        populatedValuesSheetCont2.write(0,1,"VALUE COUNT", style0)
                        newPopRow = 1
                        popRow+=1
                    # ADD DATASET HEADER TO MAIN OR CONTINUATION SHEET
                    if popRow < 65500:
                        populatedValuesSheet.write(popRow, 0, theFDFC + " | FIELD:  " + theFLD + " | DOMAIN:  " + theDMN, style1)
                        populatedValuesSheet.write(popRow, 1, "", style1)
                        popRow+=1
                    elif popRow > 65500 and popRow < 131000:
                        populatedValuesSheetCont.write(newPopRow, 0, theFDFC + " | FIELD:  " + theFLD + " | DOMAIN:  " + theDMN, style1)
                        populatedValuesSheetCont.write(newPopRow, 1, "", style1)
                        newPopRow+=1
                        popRow+=1
                    elif popRow > 131000:
                        populatedValuesSheetCont2.write(newPopRow, 0, theFDFC + " | FIELD:  " + theFLD + " | DOMAIN:  " + theDMN, style1)
                        populatedValuesSheetCont2.write(newPopRow, 1, "", style1)
                        newPopRow+=1
                        popRow+=1
                    for v in sorted(countValues.items(), key=lambda x:x[1]):
                        # CREATING CONTINUATION PAGES IF 65000 OR 131000 OCCURS DEEPER IN THE LOOPS
                        # CONTINUATION PAGE
                        if popRow == 65500:
                            populatedValuesSheetCont = wb.add_sheet('PopulatedValues_cont', cell_overwrite_ok=True)
                            populatedValuesSheetCont.col(0).width = 800 * 30
                            populatedValuesSheetCont.col(1).width = 400 * 15
                            populatedValuesSheetCont.write(0,0,"FEATURE CLASS | FIELD | DOMAIN", style0)
                            populatedValuesSheetCont.write(0,1,"VALUE COUNT", style0)
                            newPopRow = 1
                            populatedValuesSheetCont.write(newPopRow, 0, theFDFC + " | FIELD:  " + theFLD + " | DOMAIN:  " + theDMN, style1)
                            populatedValuesSheetCont.write(newPopRow, 1, "", style1)
                            newPopRow+=1
                        # SECOND CONTINUATION PAGE
                        elif popRow == 131000:
                            populatedValuesSheetCont2 = wb.add_sheet('PopulatedValues_cont2', cell_overwrite_ok=True)
                            populatedValuesSheetCont2.col(0).width = 800 * 30
                            populatedValuesSheetCont2.col(1).width = 400 * 15
                            populatedValuesSheetCont2.write(0,0,"FEATURE CLASS | FIELD | DOMAIN", style0)
                            populatedValuesSheetCont2.write(0,1,"VALUE COUNT", style0)
                            newPopRow = 1
                            populatedValuesSheetCont2.write(newPopRow, 0, theFDFC + " | FIELD:  " + theFLD + " | DOMAIN:  " + theDMN, style1)
                            populatedValuesSheetCont2.write(newPopRow, 1, "", style1)
                            newPopRow+=1
                        # OPEN TEXT FIELDS; NO DOMAIN CONSTRAINT
                        # FIRST PAGE
                        if domainVals == [] and domainRng == [] and popRow < 65500:
                            try:
                                populatedValuesSheet.write(popRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                                populatedValuesSheet.write(popRow, 1, v[1], style2)
                                popRow+=1
                            except:
                                populatedValuesSheet.write(popRow, 0, "ERROR: CHECK SOURCE DATA", style2)
                                populatedValuesSheet.write(popRow, 1, v[1], style2)
                                popRow+=1
                        # CONTINUATION PAGE
                        elif domainVals == [] and domainRng == [] and popRow >= 65500 and popRow < 131000:
                            try:
                                populatedValuesSheetCont.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                                populatedValuesSheetCont.write(newPopRow, 1, v[1], style2)
                                newPopRow+=1
                                popRow+=1
                            except:
                                populatedValuesSheetCont.write(newPopRow, 0, "ERROR: CHECK SOURCE DATA", style2)
                                populatedValuesSheetCont.write(newPopRow, 1, v[1], style2)
                                newPopRow+=1
                                popRow+=1
                        # SECOND CONTINUATION PAGE
                        elif domainVals == [] and domainRng == [] and popRow >= 131000:
                            try:
                                populatedValuesSheetCont2.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                                populatedValuesSheetCont2.write(newPopRow, 1, v[1], style2)
                                newPopRow+=1
                                popRow+=1
                            except:
                                populatedValuesSheetCont2.write(newPopRow, 0, "ERROR: CHECK SOURCE DATA", style2)
                                populatedValuesSheetCont2.write(newPopRow, 1, v[1], style2)
                                newPopRow+=1
                                popRow+=1
                        # CORRECTLY POPULATED CODED VALUES WITHIN A DOMAIN CONSTRAINED FIELD
                        # FIRST PAGE
                        elif domainVals != [] and str(v[0]) in domainVals and popRow < 65500:
                            populatedValuesSheet.write(popRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                            populatedValuesSheet.write(popRow, 1, v[1], style2)
                            popRow+=1
                        # CONTINUATION PAGE
                        elif domainVals != [] and str(v[0]) in domainVals and popRow >= 65500 and popRow < 131000:
                            populatedValuesSheetCont.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                            populatedValuesSheetCont.write(newPopRow, 1, v[1], style2)
                            newPopRow+=1
                            popRow+=1
                        # SECOND CONTINUATION PAGE
                        elif domainVals != [] and str(v[0]) in domainVals and popRow >= 131000:
                            populatedValuesSheetCont2.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                            populatedValuesSheetCont2.write(newPopRow, 1, v[1], style2)
                            newPopRow+=1
                            popRow+=1
                        # CORRECTLY POPULATED RANGE VALUES WITHIN A DOMAIN CONSTRAINED FIELD
                        # FIRST PAGE
                        elif domainRng != [] and v[0] in domainRng and popRow < 65500:
                            populatedValuesSheet.write(popRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                            populatedValuesSheet.write(popRow, 1, v[1], style2)
                            popRow+=1
                        # CONTINUATION PAGE
                        elif domainRng != [] and v[0] in domainRng and popRow >= 65500 and popRow < 131000:
                            populatedValuesSheetCont.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                            populatedValuesSheetCont.write(newPopRow, 1, v[1], style2)
                            newPopRow+=1
                            popRow+=1
                        # SECOND CONTINUATION PAGE
                        elif domainRng != [] and v[0] in domainRng and popRow >= 131000:
                            populatedValuesSheetCont2.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style2)
                            populatedValuesSheetCont2.write(newPopRow, 1, v[1], style2)
                            newPopRow+=1
                            popRow+=1
                        else:
                            # INCORRECTLY POPULATED VALUES WITHIN DOMAIN CONSTRAINED FIELDS
                            # FIRST PAGE
                            if popRow < 65500:
                                populatedValuesSheet.write(popRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style3)
                                populatedValuesSheet.write(popRow, 1, v[1], style3)
                                popRow+=1
                            # CONTINUATION PAGE
                            elif popRow >= 65500 and popRow < 131000:
                                populatedValuesSheetCont.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style3)
                                populatedValuesSheetCont.write(newPopRow, 1, v[1], style3)
                                newPopRow+=1
                                popRow+=1
                            # SECOND CONTINUATION PAGE
                            elif popRow >= 131000:
                                populatedValuesSheetCont2.write(newPopRow, 0, v[0] if not isinstance(v[0], NoneType) else 'Null', style3)
                                populatedValuesSheetCont2.write(newPopRow, 1, v[1], style3)
                                newPopRow+=1
                                popRow+=1
                    print ("\n")
            # SYMBOLOGY-DEPENDENT FIELD DOES NOT EXIST
            else:
                print(theFLD + ' FIELD DOES NOT EXIST\n')
                missingFieldSheet.write(mFldRow, 0, theFDFC, style2)
                missingFieldSheet.write(mFldRow, 1, theFLD, style2)
                mFldRow+=1
        # FEATURE CLASS DOES NOT EXIST
        else:
            print (theFDFC + ' FEATURE CLASS DOES NOT EXIST\n')
            missingFCSheet.write(mFCRow, 0, theFDFC, style2)
            mFCRow+=1

    # Save Excel workbook
    wb.save(os.path.join(outputLoc, installationName + gdbTag + ".xls"))


except Exception as e:
    # Error time
    errorT = datetime.now()
    errorRunT = str(errorT - startT)
    print(errorT)
    # Save up to error time
    wb.save(os.path.join(outputLoc, installationName + gdbTag + ".xls"))
    print ("***EXCEPTION OCCURED***")
    print e.args[0]
    print("Installation processing: %s" % installationName)
    print("Total runtime until error: %s" % errorRunT)
    raw_input("Press enter to exit")

else:
    # End time
    endT = datetime.now()
    runT = str(endT - startT)
    print(endT)
    print("***EVALUATION COMPLETE***")
    print("Installation processed: %s" % installationName)
    print("Total runtime: %s" % runT)
    raw_input("Press enter to exit")

raw_input("Press Enter to Close Message Window")
