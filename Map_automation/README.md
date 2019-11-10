# Map Automation 

The mapping process is the final step in EA delineation, and therefore has the greatest opportunity for efficiency improvement (it has the most work remaining). Individual EA maps are generated, depending on the type, and then individual SA maps are generated. The cartographic rules for generating these maps have been clearly defined, but there are three processes for improving efficiency:

1. Layer files and definition queries: while the layer cartography has been clearly defined, the mappers are not regularly using layer style files to speed up visualization. When generating a map for a single EA, the shape is exported to a new shapefile in order to eliminate neighbouring EAs from the map - a definition query will improve that in one step.
2. Automatic MXD generation - as the map stylying is clearly defined, it SHOULD be possible to automatically generate MXD files that use defined layers with defined styles. This has not been tested yet, however.
3. Automatic MAP generation - As individual EAs have consistent style, it should be possible to generate all the individual EA files by looping through each individual country. See script *map-generation.py* for more information
