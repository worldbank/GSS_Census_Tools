# Imagery Tiling
In order to support the use of the satellite basemap provided to GSS by the World Bank, the imagery needs to be chopped up into districts and converted to mbtiles or tpk. As of right now, this is proving difficult and does not seem like the file size will be compatible with the required analysis.

## How to perform tiling
I have tested the [rio tiler](https://github.com/mapbox/rio-mbtiles) package, which has proven successful in generating mbtiles using the following command

'''
rio mbtiles -o C:\folder\outTile.mbtiles --overwrite -f PNG --zoom-levels 15..16 C:\folder\031113120110.tif
'''

However, this has not proven useful concerning file size when testing against a single imagery tile (the country has 2700 tiles, and the test district I am using is covered using 50 tiles):

- original file size: 69 mb
- mbtiles at zoom level 1: 12 kb (this is useless resolution, but included for comparison)
- mbtiles at zoom level 16: 41 mb
- mbtiles at zoom level 17: 148 mb
- mbtiles at zoom level 18: 490 mb

Based on this, the investigation needs to slightly shift to the following questions:

1. Can we compress the mbtile files? The repository [mbutil](https://github.com/mapbox/mbutil) could be useful, but I have not found it to be so.

2. Can we limit the area for which we generate mbtiles? EA types? Maps of built area, etc.
