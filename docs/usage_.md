# Usage

<!-- [![image](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://demo.leafmap.org/lab/index.html?path=notebooks/29_pydeck.ipynb) -->

[![image](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wybert/georouting/blob/main/docs/usage.ipynb)



```python
pip install georouting
```

## Prepare some data


```python
import pandas as pd
data = pd.read_csv(
    "https://raw.githubusercontent.com/wybert/georouting/main/docs/data/sample_3.csv",
    index_col=0)
data = data[['ZIP_lat', 'ZIP_lon', 'AHA_ID_lat', 'AHA_ID_lon']]
data.head()
```




|  | ZIP_lat | ZIP_lon | AHA_ID_lat | AHA_ID_lon |
| --- | --- | --- | --- | --- |
| 6010 | 42.376239 | -72.605400 | 42.819978 | -73.916518 |
| 5333 | 42.293923 | -72.967189 | 41.753841 | -72.682788 |
| 7678 | 42.158520 | -72.585325 | 40.709320 | -74.212500 |




```python
origin = [data.iloc[2]["ZIP_lat"],data.iloc[2]["ZIP_lon"]]
destination = [data.iloc[2]["AHA_ID_lat"],data.iloc[2]["AHA_ID_lon"]]

origins = data[['ZIP_lat', 'ZIP_lon']].values.tolist()
destinations = data[['AHA_ID_lat', 'AHA_ID_lon']].values.tolist()
```

## Get a route use OSRM 

Get a route between two points is easy, 


```python
from georouting.routers import OSRMRouter
# create a router object 
router = OSRMRouter(mode="driving")
# get the route between the origin and destination, this will return a Route object
# this will call the OSRM API
route = router.get_route(origin, destination)
# Now you can get the distance and duration of the route in meters and seconds
print("Distance: {} meters".format(route.get_distance()))
print("Duration: {} seconds".format(route.get_duration()))
```

    Distance: 268234.5 meters
    Duration: 12313.4 seconds


You can easily get the distance, duration.

You can also return the routing results in a GeoDataFrame, It will return the distance, duration, speed and the route geometry,


```python
df= route.get_route_geopandas()
df.head()
```




|  | geometry | duration (s) | distance (m) | speed (m/s) |
| --- | --- | --- | --- | --- |
| 0 | LINESTRING (-72.58532 42.15852, -72.58523 42.1... | 22.6 | 279.5 | 12.367257 |
| 1 | LINESTRING (-72.58194 42.15850, -72.58194 42.1... | 12.3 | 163.2 | 13.268293 |
| 2 | LINESTRING (-72.58090 42.15734, -72.58092 42.1... | 128.2 | 1929.9 | 15.053822 |
| 3 | LINESTRING (-72.58196 42.14028, -72.58205 42.1... | 111.8 | 1703.5 | 15.237030 |
| 4 | LINESTRING (-72.58437 42.12533, -72.58492 42.1... | 98.1 | 1783.3 | 18.178389 |



You can visualize the route in a map,


```python
route.plot_route()
```




*[Interactive map - view in Jupyter notebook]*



## Get a distance matrix


```python
distance_matrix = router.get_distance_matrix(origins, destinations, append_od=True)
distance_matrix.head()
```




|  | orgin_lat | orgin_lon | destination_lat | destination_lon | distance (m) | duration (s) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 42.376239 | -72.605400 | 42.819978 | -73.916518 | 185141.8 | 8639.8 |
| 1 | 42.376239 | -72.605400 | 41.753841 | -72.682788 | 82634.6 | 4058.1 |
| 2 | 42.376239 | -72.605400 | 40.709320 | -74.212500 | 300008.0 | 13819.9 |
| 3 | 42.293923 | -72.967189 | 42.819978 | -73.916518 | 126934.5 | 6829.4 |
| 4 | 42.293923 | -72.967189 | 41.753841 | -72.682788 | 90821.8 | 5550.6 |



## Get distances according OD pairs

Sometimes you may want to get the durations and distances for some specific origin-destination pairs not for all possible combinations between them. you can use the `get_distances_batch` function. 


```python
distances = router.get_distances_batch(origins, destinations, append_od=True)
distances
```




|  | origin_lat | origin_lon | destination_lat | destination_lon | distance (m) | duration (s) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 42.376239 | -72.605400 | 42.819978 | -73.916518 | 185141.8 | 8639.8 |
| 0 | 42.293923 | -72.967189 | 41.753841 | -72.682788 | 90821.8 | 5550.6 |
| 0 | 42.158520 | -72.585325 | 40.709320 | -74.212500 | 268234.5 | 12313.4 |



It will automatically split the OD pairs into batches and get the distance matrix for each batch to avoid the API limit.

## What's more

`georouting` provides a unified API for routing services, you can use the similar code to get the routing results from different routing services like Google Maps, Bing Maps, OSRM, etc.
