# Table of Contents

* [georouting.routers.baidu](#georouting.routers.baidu)
  * [BaiduRouter](#georouting.routers.baidu.BaiduRouter)
    * [get\_route](#georouting.routers.baidu.BaiduRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.baidu.BaiduRouter.get_distance_matrix)
    * [get\_distances\_batch](#georouting.routers.baidu.BaiduRouter.get_distances_batch)

<a id="georouting.routers.baidu"></a>

# georouting.routers.baidu

<a id="georouting.routers.baidu.BaiduRouter"></a>

## BaiduRouter Objects

```python
class BaiduRouter(WebRouter)
```

Baidu Maps router.
The BaiduRouter class is a subclass of the WebRouter class and is used for routing using the Baidu Maps API.
This class is designed to provide a convenient and easy-to-use interface for interacting with the Baidu Maps API.

It will return a router object that can be used to get routes and distance matrices.

Parameters
----------

- `api_key` : str
    The API key for the Baidu Maps API.

- `mode` : str
    The routing mode. Can be either "driving" or "walking".

- `timeout` : int
    The timeout in seconds for API requests.

- `language` : str
    The language to be used in API requests.


Returns
-------
- `BaiduRouter` :
    A router object that can be used to get routes and distance matrices.

<a id="georouting.routers.baidu.BaiduRouter.get_route"></a>

#### get\_route

```python
def get_route(origin, destination)
```

This method returns a Route object representing the route between the origin and destination points.
The origin and destination parameters are tuples/list/arrays representing the starting and ending points for the route.
The orgin and destination parameters should be in the form of iterable objects with two elements, such as
(latitude, longitude) or [latitude, longitude].

Parameters
----------
- `origin` : iterable objects
    The origin point. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

- `destination` : iterable objects
    The destination point. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

Returns
-------
- `route` : Route object
    The route between the origin and destination.

The returned Route object has the following functions:

- `get_distance()` returns the distance of the route in meters.
- `get_duration()` returns the duration of the route in seconds.
- `get_route()` returns the raw route data returned as a dictionary.
- `get_route_geodataframe()` returns the route as a GeoDataFrame.

<a id="georouting.routers.baidu.BaiduRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

This method returns a Pandas dataframe representing a distance matrix between the origins and destinations.
It returns the duration and distance for all possible combinations between each origin and each destination.

Parameters
----------
- `origins` : iterable objects
    An iterable object containing the origin points (latitude, longitude).

- `destinations` : iterable objects
    An iterable object containing the destination points (latitude, longitude).

- `append_od` : bool
    If True, the method also returns a matrix of origin-destination pairs.

Returns
-------
- `distance_matrix` : pandas.DataFrame
    A pandas DataFrame containing the distance matrix.

<a id="georouting.routers.baidu.BaiduRouter.get_distances_batch"></a>

#### get\_distances\_batch

```python
def get_distances_batch(origins, destinations, append_od=False)
```

This method returns a Pandas dataframe contains duration and distance for all the origins and destinations pairs.
Use this function if you don't want to get duration and distance for all possible combinations.

Parameters
----------
- `origins` : iterable objects
    An iterable object containing the origin points (latitude, longitude).

- `destinations` : iterable objects
    An iterable object containing the destination points (latitude, longitude).

- `append_od` : bool
    If True, the method also returns the input origin-destination pairs.

Returns
-------
- `distance_matrix` : pandas.DataFrame
    A pandas DataFrame containing the distances for each OD pair.

