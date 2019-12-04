import time, arcpy, os, sys, shutil, logging

def DetermineOrientation(inFile, orientationField="ORIENT"):
    '''
    inFile = r'C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\2020 GUSHIEGU\TYPE 2\gushiegu final1.shp'
    '''
    with arcpy.da.UpdateCursor(inFile, ['OID@','SHAPE@',orientationField]) as cur:
        for feat in cur:
            orientation = "LANDSCAPE"
            if feat[1].extent.width < feat[1].extent.height:
                orientation = "PORTRAIT"
            feat[2] = orientation
            cur.updateRow(feat)

class mappingDistrict(object):
    ''' DEBUGGING
    districtFolder = r'C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\EDITED_DISTRICTS\2020 GUSHIEGU\TYPE 2'
    t2Map = r'C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\t2Map.mxd'
    t3Map = r'C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\t3Map.mxd'
    saMap = r'C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\saMap.mxd'
    '''
    def __init__ (self, districtFolder, t2Map, t3Map, saMap):
        ''' Generate properly formatted mapping 
        
        INPUTS
        districtFolder [string] - path to folder of district level data
        t2Map, t3Map, saMap [ string ] - path to three map templates
        [ optional ] outputMapFolder [ string ] - where to create output maps
        '''
        self.districtFolder = districtFolder
        #copy maps               
        self.t2Map = os.path.join(districtFolder, os.path.basename(t2Map))
        self.t3Map = os.path.join(districtFolder, os.path.basename(t3Map))
        self.saMap = os.path.join(districtFolder, os.path.basename(saMap))
        if not os.path.exists(self.t2Map):
            shutil.copy(t2Map, self.t2Map)
        if not os.path.exists(self.t3Map):
            shutil.copy(t3Map, self.t3Map)
        if not os.path.exists(self.saMap):
            shutil.copy(saMap, self.saMap)
        
    def setMapInputs(self, mapDocument):
        '''
        '''            
        mxd = arcpy.mapping.MapDocument(mapDocument)
        layers = arcpy.mapping.ListLayers(mxd)
        for l in layers:
            # find the data source and search for the same file in the input folder
            try:
                l.findAndReplaceWorkspacePath('', self.districtFolder, True)
            except:
                logging.warning("Could not fix path for %s" % l.name)
        mxd.save()
        
def createMapFromMXD_loop(mxd, outputImage, zoomLayer, layerName, labels=[], totalEA=2, saveMap=False):
    ''' Generate map for each feature in a layer
    
    INPUTS
    outputImage [string] - path to create output images
    '''
    #Get reference to output type
    outputType = outputImage[-3:]    
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    #Get a reference to the specific layer of interest
    layers = arcpy.mapping.ListLayers(mxd)
    for l in layers:        
        if l.name == zoomLayer:
            loopLyr = l
            l.visible = True
    # Get list of fields to extract from loop layer
    featCnt = 0
    searchFields = ["OID@", layerName]
    for x in labels:
        searchFields.append(x)
    # get reference to text boxes
    allLabels = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
    otherTitle = allLabels[0]
    districtCode = allLabels[1]
    districtName = allLabels[2]
    # loop through the features in loop layer
    with arcpy.da.SearchCursor(loopLyr, searchFields) as cur:
        for feat in cur:
            featCnt += 1
            if featCnt > totalEA:
                sys.exit()
            # Select the feature of interest
            arcpy.SelectLayerByAttribute_management(loopLyr, "NEW_SELECTION", '"FID" = %s' % feat[0])
            df.extent = loopLyr.getSelectedExtent()
            df.scale = df.scale * 1.05
            arcpy.SelectLayerByAttribute_management(loopLyr, "CLEAR_SELECTION", '"FID" = %s' % feat[0])
            #Set EA definition so featured EA is not visible
            loopLyr.definitionQuery = '"FID" = %s' % feat[0]    
            #Update labels
            otherTitle.text = feat[2]
            districtCode.text = feat[3]
            districtName.text = feat[4]                        
            #Export map
            time.sleep(1)
            outputMap = outputImage.replace(".%s" % outputType, "_%s.%s" % (feat[1], outputType))                  
            if outputType == 'png':
                arcpy.mapping.ExportToPNG(mxd, outputMap)
            elif outputType == 'pdf':
                arcpy.mapping.ExportToPDF(mxd, outputMap)            
            if saveMap:
                mxd.saveACopy(outputMap.replace(".%" % outputType, ".mxd"))
            loopLyr.definitionQuery = ""

mxd = arcpy.mapping.MapDocument("CURRENT")
focal_layer = "diss"     # Layer with individual features for which to create atlas
feature_name = "LOC_NAME"         # column containing unique name for each feature - drives the filenames
labelFields = ["FIRST_DIST",feature_name,"FIRST_TYP"] # columns to populate text on map
outputImage = "C:/temp/GSS_Maps/SA_Maps.pdf"           #Output filename, make sure folder exists

createMapFromMXD_loop(mxd, 
                      outputImage, 
                      focal_layer, 
                      feature_name, 
                      labelFields, 
                      totalEA=3,        #Set this number to be very high (3000) in order to process everything
                      saveMap=False)    #Set this to True in order to save a mxd of each EA
