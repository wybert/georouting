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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ZIP_lat</th>
      <th>ZIP_lon</th>
      <th>AHA_ID_lat</th>
      <th>AHA_ID_lon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6010</th>
      <td>42.376239</td>
      <td>-72.605400</td>
      <td>42.819978</td>
      <td>-73.916518</td>
    </tr>
    <tr>
      <th>5333</th>
      <td>42.293923</td>
      <td>-72.967189</td>
      <td>41.753841</td>
      <td>-72.682788</td>
    </tr>
    <tr>
      <th>7678</th>
      <td>42.158520</td>
      <td>-72.585325</td>
      <td>40.709320</td>
      <td>-74.212500</td>
    </tr>
  </tbody>
</table>
</div>




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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>geometry</th>
      <th>duration (s)</th>
      <th>distance (m)</th>
      <th>speed (m/s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>LINESTRING (-72.58532 42.15852, -72.58523 42.1...</td>
      <td>22.6</td>
      <td>279.5</td>
      <td>12.367257</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LINESTRING (-72.58194 42.15850, -72.58194 42.1...</td>
      <td>12.3</td>
      <td>163.2</td>
      <td>13.268293</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LINESTRING (-72.58090 42.15734, -72.58092 42.1...</td>
      <td>128.2</td>
      <td>1929.9</td>
      <td>15.053822</td>
    </tr>
    <tr>
      <th>3</th>
      <td>LINESTRING (-72.58196 42.14028, -72.58205 42.1...</td>
      <td>111.8</td>
      <td>1703.5</td>
      <td>15.237030</td>
    </tr>
    <tr>
      <th>4</th>
      <td>LINESTRING (-72.58437 42.12533, -72.58492 42.1...</td>
      <td>98.1</td>
      <td>1783.3</td>
      <td>18.178389</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>orgin_lat</th>
      <th>orgin_lon</th>
      <th>destination_lat</th>
      <th>destination_lon</th>
      <th>distance (m)</th>
      <th>duration (s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>42.376239</td>
      <td>-72.605400</td>
      <td>42.819978</td>
      <td>-73.916518</td>
      <td>185141.8</td>
      <td>8639.8</td>
    </tr>
    <tr>
      <th>1</th>
      <td>42.376239</td>
      <td>-72.605400</td>
      <td>41.753841</td>
      <td>-72.682788</td>
      <td>82634.6</td>
      <td>4058.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>42.376239</td>
      <td>-72.605400</td>
      <td>40.709320</td>
      <td>-74.212500</td>
      <td>300008.0</td>
      <td>13819.9</td>
    </tr>
    <tr>
      <th>3</th>
      <td>42.293923</td>
      <td>-72.967189</td>
      <td>42.819978</td>
      <td>-73.916518</td>
      <td>126934.5</td>
      <td>6829.4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>42.293923</td>
      <td>-72.967189</td>
      <td>41.753841</td>
      <td>-72.682788</td>
      <td>90821.8</td>
      <td>5550.6</td>
    </tr>
  </tbody>
</table>
</div>



## Get distances according OD pairs

Sometimes you may want to get the durations and distances for some specific origin-destination pairs not for all possible combinations between them. you can use the `get_distances_batch` function. 


```python
distances = router.get_distances_batch(origins, destinations, append_od=True)
distances
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>origin_lat</th>
      <th>origin_lon</th>
      <th>destination_lat</th>
      <th>destination_lon</th>
      <th>distance (m)</th>
      <th>duration (s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>42.376239</td>
      <td>-72.605400</td>
      <td>42.819978</td>
      <td>-73.916518</td>
      <td>185141.8</td>
      <td>8639.8</td>
    </tr>
    <tr>
      <th>0</th>
      <td>42.293923</td>
      <td>-72.967189</td>
      <td>41.753841</td>
      <td>-72.682788</td>
      <td>90821.8</td>
      <td>5550.6</td>
    </tr>
    <tr>
      <th>0</th>
      <td>42.158520</td>
      <td>-72.585325</td>
      <td>40.709320</td>
      <td>-74.212500</td>
      <td>268234.5</td>
      <td>12313.4</td>
    </tr>
  </tbody>
</table>
</div>



It will automatically split the OD pairs into batches and get the distance matrix for each batch to avoid the API limit.

## What's more

`georouting` provides a unified API for routing services, you can use the similar code to get the routing results from different routing services like Google Maps, Bing Maps, OSRM, etc.
