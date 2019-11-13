###############################################################################
# Extract Image Tiles
# Benjamin P Stewart, November 2019
# Purpose: Allow user to extract image tiles from GHANA basemap based on
#   intersection between shapefile and image extents
###############################################################################

import os, sys, shutil, arcpy

fpLyr = "fp"
extLyr = "ext"
filePath_column = "File"

def SelectFootprints(footprintLayer, extentLyr):
    ''' Select the features in the footprints layer that intersect the layer object
    
    INPUT
    fpLyr [string] - name of layer with image footprints
    extentLyr [string] - name of layer describing extent
    
    RETURNS
    [array of string paths] - list of image paths covering extent (extracted from 
        column in fpLyr
    '''
    arcpy.SelectLayerByLocation_management(footprintLayer, "INTERSECT", extentLyr)
    with arcpy.da.SearchCursor(footprintLayer, [filePath_column]) as inCur:
        results = [x[0] for x in inCur]
    return(results)
    
    
def getLayers(fpLyr_path, extentLyr_path):
    ''' Get layer objects based on strings
    
    INPUT
    fpLyrName [string] - path to input string layer describing footprint extents
    extentLyr [string] - path to input extents layer
    
    REUTRNS
    [None] - creates two layer files in memory
    '''
    arcpy.MakeFeatureLayer_management(fpLyr_path, fpLyr)
    arcpy.MakeFeatureLayer_management(extentLyr_path, extLyr)
    return(True)
    
def copyFiles(file_list, outfolder, fpLayer, verbose=True):
    ''' Copy list of raster images to output folder
    
    INPUT
    file_list [ list of strings ] - list of images to copy (full path)
    outfolder [ string path ] - output location for images
    
    RETURNS
    [NONE]
    '''
    for imgFile in file_list:
        if not os.path.exists(imgFile):
            oFile = imgFile
            imgFile = os.path.join(fpLayer.replace("_extents.shp",""), os.path.basename(imgFile))
            if not os.path.exists(imgFile):
                raise(ValueError("Could not find image file at either %s or %s") % (oFile, imgFile))
        shutil.copy(imgFile, os.path.join(outfolder, os.path.basename(imgFile)))
        if verbose:
            print(imgFile)
fp_layer = r"E:\GHANA_Data\basemap\raster_tiles_extents.shp"
#extent_layer = r"C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\UNEDITED_DSITRICTS\TANO NORTH.gdb\EAs\unedited_eas"
#extent_layer = r"C:\Users\WB411133\OneDrive - WBG\AAA_BPS\GOST\Projects\Ghana_Census_Support\Data\GSS_Data\UNEDITED_DSITRICTS\KARLE_KLOTE_fieldTest.shp"
extent_layer = r"C:/Users/WB411133/OneDrive - WBG/AAA_BPS/GOST/Projects/Ghana_Census_Support/Data/GSS_Data/UNEDITED_DSITRICTS/Tano North.shp"
output_folder = r"E:\GHANA_Data\basemap\selected"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

getLayers(fp_layer, extent_layer)
selectedFiles = SelectFootprints(fpLyr, extLyr)
copyFiles(selectedFiles, output_folder, fp_layer)

# arcpy.DefineProjection_management(in_dataset="C:/Users/WB411133/OneDrive - WBG/AAA_BPS/GOST/Projects/Ghana_Census_Support/Data/GSS_Data/UNEDITED_DSITRICTS/Tano North.shp", coor_system="PROJCS['Custom',GEOGCS['GCS_Leigon',DATUM['D_Leigon',SPHEROID['Clarke_1880_RGS',6378249.145,293.465]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',899998.392388452],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-1.0],PARAMETER['Scale_Factor',0.99975],PARAMETER['Latitude_Of_Origin',4.666666666666667],UNIT['Foot',0.3048]]")