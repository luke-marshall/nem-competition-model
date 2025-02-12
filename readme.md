# National Electricity Market Competition Model
This repository contains a suite of tools developed to provide insights into competitionin Australia's National Electricity Market. Specifically, it contains implementations of a number of data mining tools that cross-reference market events (such as peak prices) with participant behaviour and network operation. A number of key insights have been extracted from this tool. 

## Data Mining - Random Forests Analysis
A random forests algorithm was used to examine correlation between peak pricing events, competition indicators, and transmission network events (which reduce available participants). It was found that the herfindahl-hirschmann competition index was the single most important factor in determining peak pricing events in the electricity market. 

![Random Forests Explanation](https://user-images.githubusercontent.com/7201209/51463523-b8941580-1da6-11e9-936f-1213262e6d41.png)

![Random Forests Results](https://user-images.githubusercontent.com/7201209/51463549-ca75b880-1da6-11e9-853f-342c89eea365.png)

## Herfindahl-Hirschmann Index Analysis
The Herfindahl-Hirschmann Index, a commonly used measure of market competition, is applied here to energy market datasets. Using this technique, it has been found that competition in the National Electricity Market has been either 'Moderately' or 'Highly' concentrated at all times in 2016-17. 

![HHI Visualisation](https://user-images.githubusercontent.com/7201209/51463488-a619dc00-1da6-11e9-88ff-19b6a0195a11.png)


## Network Graph Analysis
network-analysis.py provides a utility to convert transmission line maps and generator locations into graph data structures, with generators and substations as nodes and transmission lines as edges. It uses datasets taken from the AREMI [NationalMap](https://nationalmap.gov.au/renewables/) project. Network flow algorithms can then be applied to these data structures to measure the efficacy and reslisience of the network under various conditions.

![Network Graph Visualisation](https://user-images.githubusercontent.com/7201209/51463432-8aaed100-1da6-11e9-995a-e19c28562fb8.png)

### Network Mapping Technical Notes
Name formats in the GEOjson file were 'X to Y' ie. "Liddell Power Station to Newcastle"
I was originally stripping the X and Y and using them as node keys.
Unfortunately, the order in which the label was written often did not correspond to the order of the points in the GEOJSON file ie. the first and last point in the multi-line-string representing the transmission line may have been in reverse order to the title. Thus there was no way to tell which coordinates corresponded to which node.

I then tried using the pure lat,long coordinates of the start and end of the transmission line as node keys - but the subtle differences in colocated transmission endpoints mean that no two origins and destinations were ever the same - ie no graphs with more than 2 nodes were ever found.

To fix this, I started by rounding the lats and longs to 3 decimal places, which by google maps appeared to be a reasonable approximate length/width range for colocated nodes. There were however a few glaring exceptions, with a number of features in the Hunter Valley and the Snowy Hyrdoelectric scheme not appearing geolocated and thus being disconnected, when they should have been connected. Some drawbacks of wholesale lat-long rounding is that the range of distance deviation changes geographically, and is more pronounced in longitude than latitude. 

The final strategy was to use an estimate of the distance of a node from any other already-registered node, and assume that the nodes are colocated if the distance was under a threshold. For this I used the Vincenty distance measure from the geopy library. A threshold of 150 meters appears adequate for linking all colocated nodes and seems a reasonable distance for a facility to be considered cohesive. This strategy works well but slows graph creation time significantly as it increases algorithmic complexity to O(n^2). 

Another option would be to use a pre-pass clustering method but this does not seem necessary given that a colocation distance of 150 meters is sufficient to link all cohesive nodes in the transmission network structure. 

### Generator Mapping Technical Notes
A list of generators was found on the NationalMap service. File format was GML. I used instructions here https://gis.stackexchange.com/questions/28613/convert-gml-to-geojson to convert to geojson.