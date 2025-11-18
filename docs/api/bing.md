# Table of Contents

* [georouting.routers.bing](#georouting.routers.bing)
  * [BingRouter](#georouting.routers.bing.BingRouter)
    * [get\_route](#georouting.routers.bing.BingRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.bing.BingRouter.get_distance_matrix)
    * [get\_distances\_batch](#georouting.routers.bing.BingRouter.get_distances_batch)

<a id="georouting.routers.bing"></a>

# georouting.routers.bing

<a id="georouting.routers.bing.BingRouter"></a>

## BingRouter Objects

```python
class BingRouter(WebRouter)
```

Bing Maps router.
The BingRouter class is a subclass of the WebRouter class and is used for routing using the Bing Maps API.
This class is designed to provide a convenient and easy-to-use interface for interacting with the Bing Maps API.

It will return a router object that can be used to get routes and distance matrices.

Parameters
----------

- `api_key` : str
    The API key for the Bing Maps API.

- `mode` : str
    The routing mode. Can be either "driving" or "walking".

- `timeout` : int
    The timeout in seconds for API requests.

- `language` : str
    The language to be used in API requests.


Returns
-------
- `BingRouter` :
    A router object that can be used to get routes and distance matrices.

<a id="georouting.routers.bing.BingRouter.get_route"></a>

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

<a id="georouting.routers.bing.BingRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

This method returns a Pandas dataframe representing a distance matrix between the `origins` and `destinations` points. It returns the duration and distance for
all possible combinations between each origin and each destination. If you want just
return the duration and distance for specific origin-destination pairs, use the `get_distances_batch` method.

The origins and destinations parameters are lists of origins and destinations.

If the `append_od` parameter is set to True, the method also returns a matrix of origin-destination pairs.

The Bing Maps API has the following limitations for distance matrix requests,
for more information see [here](https://learn.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-distance-matrix#api-limits):

- For travel mode driving a distance matrix that has up to 2,500 origins-destinations pairs can be requested for Basic Bing Maps accounts,
- while for Enterprise Bing Maps accounts the origin-destination pairs limit is 10,000.
- For travel mode transit and walking, a distance matrix that has up to 650 origins-destinations pairs can be request for all Bing Maps account types.

Pairs are calculated by multiplying the number of origins, by the number of destinations.
For example 10,000 origin-destination pairs can be reached if you have: 1 origin, and 10,000 destinations,
or 100 origins and 100 destinations defined in your request.


Parameters
----------
- `origins` : iterable objects
    An iterable object containing the origin points. It can be a list of tuples, a list of lists, a list of arrays, etc.
    It should be in the form of iterable objects with two elements, such as
    (latitude, longitude) or [latitude, longitude].
- `destinations` : iterable objects
    An iterable object containing the destination points. It can be a list of tuples, a list of lists, a list of arrays, etc.
    It should be in the form of iterable objects with two elements, such as
    (latitude, longitude) or [latitude, longitude].
- `append_od` : bool
    If True, the method also returns a matrix of origin-destination pairs.

Returns
-------
- `distance_matrix` : pandas.DataFrame
    A pandas DataFrame containing the distance matrix.

<a id="georouting.routers.bing.BingRouter.get_distances_batch"></a>

#### get\_distances\_batch

```python
def get_distances_batch(origins, destinations, append_od=False)
```

This method returns a Pandas dataframe contains duration and disatnce for all the `origins` and `destinations` pairs. Use this function if you don't want to get duration and distance for all possible combinations between each origin and each destination.

The origins and destinations parameters are lists of origin-destination pairs. They should be the same length.

If the `append_od` parameter is set to True, the method also returns the input origin-destination pairs.

Parameters
----------
- `origins` : iterable objects
    An iterable object containing the origin points. It can be a list of tuples, a list of lists, a list of arrays, etc.
    It should be in the form of iterable objects with two elements, such as
    (latitude, longitude) or [latitude, longitude].

- `destinations` : iterable objects
    An iterable object containing the destination points. It can be a list of tuples, a list of lists, a list of arrays, etc.
    It should be in the form of iterable objects with two elements, such as
    (latitude, longitude) or [latitude, longitude].

- `append_od` : bool
    If True, the method also returns the input origin-destination pairs.

Returns
-------
- `distance_matrix` : pandas.DataFrame
    A pandas DataFrame containing the distance matrix.

