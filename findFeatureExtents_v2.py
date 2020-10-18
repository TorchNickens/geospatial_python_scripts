#-------------------------------------------------------------------------------
# Name:             Read Feature Extents and P
# Author:           Marie Cline Delgado
# Last Updated:     13 SEPT 2018
#-------------------------------------------------------------------------------

import arcpy, os

wkspace = r"C:\Users\1528874122E\Desktop\test\Croughton311_CIP_orig.gdb".replace("\\", "/")
#wkspace = r"G:/someFolders/yourSpatialDatabase.sde"
arcpy.env.workspace = wkspace

def getExtent(featureClass):
    '''Pass in a feature class and function returns the feature class extent in
    a tuple formatted as xMin, xMax, yMin, yMax'''
    desc = arcpy.Describe(featureClass)
    xmin = desc.extent.XMin
    xmax = desc.extent.XMax
    ymin = desc.extent.YMin
    ymax = desc.extent.YMax
    return (xmin, xmax, ymin, ymax)

def getSpatialIdx(featureClass):
    '''Pass in a feature class and function uses a data access search cursor to
    search all features and store the smallest xmin and ymin found and the
    largest xmax and ymax formatted as a tuple xMin, xMax, yMin, yMax'''
    xmin = xmax = ymin = ymax = None
    with arcpy.da.SearchCursor(fc, ["SHAPE@"]) as cur:
        for row in cur:
            shpObj = row[0]
            xmin = shpObj.extent.XMin if xmin is None or shpObj.extent.XMin < xmin else xmin
            xmax = shpObj.extent.XMax if xmax is None or shpObj.extent.XMax > xmax else xmax
            ymin = shpObj.extent.YMin if ymin is None or shpObj.extent.YMin < xmin else ymin
            ymax = shpObj.extent.YMax if ymax is None or shpObj.extent.YMax > ymax else ymax
    return (xmin, xmax, ymin, ymax)

# Loop through data within feature datasets to read extents
for fd in arcpy.ListDatasets():
    for fc in arcpy.ListFeatureClasses("*","",fd):
        fcExtent = getExtent(fc)
        fcSI = getSpatialIdx(fc)
        # Apply whatever further logic here
        print "---------------------------------"
        print fcExtent
        print fcSI
        if fcExtent != fcSI:
            print "FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for {} \n   Feature Extent: {} \n   Pseudo Spatial Index: {}".format(fc, fcExtent, fcSI)

# Then loop through feature classes not in datasets if you have any
for fc in arcpy.ListFeatureClasses():
    fcExtent = getExtent(fc)
    fcSI = getSpatialIdx(fc)
    # And apply same logic here if you have feature classes outside of datasets
    print "---------------------------------"
    print fcExtent
    print fcSI
    if fcExtent != fcSI:
        print "FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for {} \n   Feature Extent:       {} \n   Pseudo Spatial Index: {}".format(fc, fcExtent, fcSI)



"""
###################################
RESULT EXAMPLE
   I dont have any datasets with mismatching Feature Extent and Spatial Index bounds.  It still found
   some mismatches because of rounding.  If you can confirm this method works with your data, then it
   would probably be good to incorporate some rounding to reduce the false-positive result.

---------------------------------
(-1.3791597139810703, -1.1395737399999462, 51.916981916000054, 52.01738019715006)
(-1.379159713999968, -1.139573739999948, 51.98350185700008, 52.01738019700005)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for NoiseZone_A
   Feature Extent: (-1.3791597139810703, -1.1395737399999462, 51.916981916000054, 52.01738019715006)
   Pseudo Spatial Index: (-1.379159713999968, -1.139573739999948, 51.98350185700008, 52.01738019700005)
---------------------------------
(-1.3715496679999433, -0.15247743999992736, 51.114338255000064, 52.00997128500006)
(-1.3715496679999433, -0.15247743999993174, 51.99736238700007, 52.00997128500007)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Installation_A
   Feature Extent: (-1.3715496679999433, -0.15247743999992736, 51.114338255000064, 52.00997128500006)
   Pseudo Spatial Index: (-1.3715496679999433, -0.15247743999993174, 51.99736238700007, 52.00997128500007)
---------------------------------
(-1.194464413999924, -1.1632470529999637, 51.98015637800006, 51.99705116000007)
(-1.194464413999924, -1.1632470529999643, 51.98015637800006, 51.99705116000006)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Outgrant_A
   Feature Extent: (-1.194464413999924, -1.1632470529999637, 51.98015637800006, 51.99705116000007)
   Pseudo Spatial Index: (-1.194464413999924, -1.1632470529999643, 51.98015637800006, 51.99705116000006)
---------------------------------
(-1.3715496679999433, -0.15247743999993174, 51.114338255000064, 52.00997128500007)
(-1.3715496679999433, -0.15247743999993174, 51.99736238700007, 52.00997128500007)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Site_A
   Feature Extent: (-1.3715496679999433, -0.15247743999993174, 51.114338255000064, 52.00997128500007)
   Pseudo Spatial Index: (-1.3715496679999433, -0.15247743999993174, 51.99736238700007, 52.00997128500007)
---------------------------------
(-1.3570466829999646, -0.15265639699993017, 51.115322038000045, 52.00395278000008)
(-1.3570466829999646, -0.15265639699993017, 52.00395278000008, 52.00395278000008)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Site_P
   Feature Extent: (-1.3570466829999646, -0.15265639699993017, 51.115322038000045, 52.00395278000008)
   Pseudo Spatial Index: (-1.3570466829999646, -0.15265639699993017, 52.00395278000008, 52.00395278000008)
---------------------------------
(-1.1980709629999637, -1.1634163929999772, 51.979927383000074, 51.99705116000007)
(-1.1980709629999637, -1.1634163929999557, 51.99230455800006, 51.99705116000007)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for LandUse_A
   Feature Extent: (-1.1980709629999637, -1.1634163929999772, 51.979927383000074, 51.99705116000007)
   Pseudo Spatial Index: (-1.1980709629999637, -1.1634163929999557, 51.99230455800006, 51.99705116000007)
---------------------------------
(-1.370403863999968, -0.15248631999997997, 51.11489188000007, 52.006124484000054)
(-1.370403863999968, -0.15248631999996787, 51.99166291200004, 52.00612448400005)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Building_A
   Feature Extent: (-1.370403863999968, -0.15248631999997997, 51.11489188000007, 52.006124484000054)
   Pseudo Spatial Index: (-1.370403863999968, -0.15248631999996787, 51.99166291200004, 52.00612448400005)
---------------------------------
(-1.368027816999927, -1.1696649269999284, 51.98341553100005, 52.007716808000055)
(-1.368027816999927, -1.1696649269999284, 51.99122637500005, 52.007716808000055)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Tower_P
   Feature Extent: (-1.368027816999927, -1.1696649269999284, 51.98341553100005, 52.007716808000055)
   Pseudo Spatial Index: (-1.368027816999927, -1.1696649269999284, 51.99122637500005, 52.007716808000055)
---------------------------------
(-1.370610777999957, -0.43251969699997517, 51.11476811400007, 52.00616712400006)
(-1.370610777999957, -0.4325196969999745, 51.11828264600007, 52.00616712400006)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for AccessControl_L
   Feature Extent: (-1.370610777999957, -0.43251969699997517, 51.11476811400007, 52.00616712400006)
   Pseudo Spatial Index: (-1.370610777999957, -0.4325196969999745, 51.11828264600007, 52.00616712400006)
---------------------------------
(-1.352205013999935, -1.352205013999935, 52.00498351600004, 52.00498351600004)
(-1.352205013999935, -1.352205013999935, 52.00498351600004, 52.00498351600004)
---------------------------------
(-1.3681689031247326, -0.4322454919999359, 51.114338255000064, 52.007869303000064)
(-1.3681689029999689, -0.4322454919999714, 51.92056631200006, 52.00786930300004)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Fence_L
   Feature Extent: (-1.3681689031247326, -0.4322454919999359, 51.114338255000064, 52.007869303000064)
   Pseudo Spatial Index: (-1.3681689029999689, -0.4322454919999714, 51.92056631200006, 52.00786930300004)
---------------------------------
(-1.1938033599999471, -1.1779065309999623, 51.995095899000034, 51.99660380800003)
(-1.1938033599999471, -1.177906530999974, 51.99525364600004, 51.99660380800003)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for Bridge_A
   Feature Extent: (-1.1938033599999471, -1.1779065309999623, 51.995095899000034, 51.99660380800003)
   Pseudo Spatial Index: (-1.1938033599999471, -1.177906530999974, 51.99525364600004, 51.99660380800003)
---------------------------------
(-1.3705942089999326, -1.1395290599999726, 51.916376022000065, 52.005267709000066)
(-1.3705942089999326, -1.139529059999925, 51.99241785700008, 52.00526770900006)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for RoadCenterline_L
   Feature Extent: (-1.3705942089999326, -1.1395290599999726, 51.916376022000065, 52.005267709000066)
   Pseudo Spatial Index: (-1.3705942089999326, -1.139529059999925, 51.99241785700008, 52.00526770900006)
---------------------------------
(-1.360018623999963, -0.4323139739999533, 51.114471380000055, 52.004637503000026)
(-1.360018623999963, -0.4323139739999704, 51.98897436000004, 52.004637503000055)
FOUND ONE! Feature Extent and Pseudo Spatial Index do not match for VehicleParking_A
   Feature Extent: (-1.360018623999963, -0.4323139739999533, 51.114471380000055, 52.004637503000026)
   Pseudo Spatial Index: (-1.360018623999963, -0.4323139739999704, 51.98897436000004, 52.004637503000055)