# Table of Contents

* [georouting.routers.google](#georouting.routers.google)
  * [GoogleRouter](#georouting.routers.google.GoogleRouter)
    * [\_\_init\_\_](#georouting.routers.google.GoogleRouter.__init__)
    * [get\_route](#georouting.routers.google.GoogleRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.google.GoogleRouter.get_distance_matrix)
    * [get\_distances\_batch](#georouting.routers.google.GoogleRouter.get_distances_batch)

<a id="georouting.routers.google"></a>

# georouting.routers.google

<a id="georouting.routers.google.GoogleRouter"></a>

## GoogleRouter Objects

```python
class GoogleRouter(WebRouter)
```

Google Map router.
The GoogleRouter class is a subclass of the WebRouter class and is used for routing using the Google Maps API.
This class is designed to provide a convenient and easy-to-use interface for interacting with the Google Maps API.

It will return a router object that can be used to get routes and distance matrices.

Parameters
----------

- `api_key` : str
    The API key for the Google Maps API.

- `mode` : str
    The routing mode. Can be either "driving" or "walking".

- `timeout` : int
    The timeout in seconds for API requests.

- `language` : str
    The language to be used in API requests.

Returns
-------
- `GoogleRouter`:
    A router object that can be used to get routes and distance matrices.

<a id="georouting.routers.google.GoogleRouter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(api_key, mode="driving", timeout=10, language="en")
```

This is the constructor method for the GoogleRouter class.
It initializes the class by calling the super() method and setting up
the Client object of the Google Maps API using the provided api_key.
The mode parameter sets the routing mode, which can be either "driving" or "walking".
The timeout parameter sets the timeout in seconds for API requests, and the language
parameter sets the language to be used in API requests.

<a id="georouting.routers.google.GoogleRouter.get_route"></a>

#### get\_route

```python
def get_route(origin, destination)
```

This method returns a Route object representing the route between the origin and destination points.
The origin and destination parameters are tuples/list/arrays representing the starting and ending points for the route.
The orgin and destination parameters should be in the form of iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude].

Parameters
----------
- `origin` : iterable objects
    The origin point. Iterable objects with two elements, such as
(latitude, longitude) or [latitude, longitude]

- `destination` : iterable objects
    The destination point. Iterable objects with two elements, such as
(latitude, longitude) or [latitude, longitude]

Returns
-------
`route` : Route object
    The route between the origin and destination.

The returned Route object has the following functions:

- `get_distance()` returns the distance of the route in meters.
- `get_duration()` returns the duration of the route in seconds.
- `get_route()` returns the raw route data returned as a dictionary.
- `get_route_geodataframe()` returns the route as a GeoDataFrame.

<a id="georouting.routers.google.GoogleRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

This method returns a Pandas dataframe representing a distance matrix between the `origins` and `destinations` points. It returns the duration and distance for
all possible combinations between each origin and each destination. If you want just
return the duration and distance for specific origin-destination pairs, use the `get_distances_batch` method.

The origins and destinations parameters are lists of origins and destinations.

If the `append_od` parameter is set to True, the method also returns a matrix of origin-destination pairs.

Google Maps API has following limitations for distance matrix requests:
the following usage limits are in place for the Distance Matrix API, for more information,
see in [google maps api documentation](https://developers.google.com/maps/documentation/distance-matrix/usage-limits):

- Maximum of 25 origins or 25 destinations per request.
- Maximum 100 elements per server-side request.
- Maximum 100 elements per client-side request.
- 1000 elements per second (EPS), calculated as the sum of client-side and server-side queries.

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

Here is an example of how to use this method:
__TODO: add example__


<a id="georouting.routers.google.GoogleRouter.get_distances_batch"></a>

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

