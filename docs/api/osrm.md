# Table of Contents

* [georouting.routers.osrm](#georouting.routers.osrm)
  * [OSRMRouter](#georouting.routers.osrm.OSRMRouter)
    * [get\_route](#georouting.routers.osrm.OSRMRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.osrm.OSRMRouter.get_distance_matrix)
    * [get\_distances\_batch](#georouting.routers.osrm.OSRMRouter.get_distances_batch)

<a id="georouting.routers.osrm"></a>

# georouting.routers.osrm

<a id="georouting.routers.osrm.OSRMRouter"></a>

## OSRMRouter Objects

```python
class OSRMRouter(WebRouter)
```

OSRM router.
The OSRMRouter class is a subclass of the WebRouter class and is used for routing using the OSRM API.
This class is designed to provide a convenient and easy-to-use interface for interacting with the OSRM API.

It will return a router object that can be used to get routes and distance matrices.

Parameters
----------
- `mode` : str
    The routing mode. Can be either "driving" or "walking". Default is "driving".

- `timeout` : int
    The timeout in seconds for API requests. Default is 10.

- `language` : str
    The language to be used in API requests. Default is "en".

- `base_url` : str
    The base URL for the OSRM API. Default is "http://router.project-osrm.org".

Returns
-------
- `OSRMRouter`:
    A router object that can be used to get routes and distance matrices.

<a id="georouting.routers.osrm.OSRMRouter.get_route"></a>

#### get\_route

```python
def get_route(origin, destination)
```

This method returns a Route object contains duration and disatnce for the route between the given origin and destination coordinates.
The origin and destination parameters are lists of latitude and longitude coordinates.
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

<a id="georouting.routers.osrm.OSRMRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

This method returns a Pandas dataframe representing a distance matrix between the `origins` and `destinations` points. It returns the duration and distance for
all possible combinations between each origin and each destination. If you want just
return the duration and distance for specific origin-destination pairs, use the `get_distances_batch` method.

The origins and destinations parameters are lists of origins and destinations.

If the `append_od` parameter is set to True, the method also returns a matrix of origin-destination pairs.

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


<a id="georouting.routers.osrm.OSRMRouter.get_distances_batch"></a>

#### get\_distances\_batch

```python
def get_distances_batch(origins,
                        destinations,
                        append_od=False,
                        use_local_server=False)
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

