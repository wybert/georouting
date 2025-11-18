# Table of Contents

* [georouting.routers.esri](#georouting.routers.esri)
  * [EsriRouter](#georouting.routers.esri.EsriRouter)
    * [\_\_init\_\_](#georouting.routers.esri.EsriRouter.__init__)
    * [get\_route](#georouting.routers.esri.EsriRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.esri.EsriRouter.get_distance_matrix)

<a id="georouting.routers.esri"></a>

# georouting.routers.esri

<a id="georouting.routers.esri.EsriRouter"></a>

## EsriRouter Objects

```python
class EsriRouter(WebRouter)
```

Esri router.
The EsriRouter class is a subclass of the WebRouter class and is used for routing using the Esri ArcGIS API.
This class is designed to provide a convenient and easy-to-use interface for interacting with the Esri ArcGIS API.
It will return a router object that can be used to get routes and distance matrices.

Parameters
----------

- `api_key` : str
    The API key for the Esri ArcGIS API.

- `mode` : str
    The routing mode. Can be either "driving" or "walking".

- `timeout` : int
    The timeout in seconds for API requests.

- `language` : str
    The language to be used in API requests.

Returns
-------
- `EsriRouter`:
    A router object that can be used to get routes and distance matrices.

<a id="georouting.routers.esri.EsriRouter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(api_key, mode="driving", timeout=10, language="en")
```

This is the constructor method for the EsriRouter class.
It initializes the class by calling the super() method and setting up
the Client object of the Esri ArcGIS API using the provided api_key.
The mode parameter sets the routing mode, which can be either "driving" or "walking".
The timeout parameter sets the timeout in seconds for API requests, and the language
parameter sets the language to be used in API requests.

<a id="georouting.routers.esri.EsriRouter.get_route"></a>

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

<a id="georouting.routers.esri.EsriRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

This method returns a distance matrix between the origins and destinations.
The origins and destinations parameters are lists of tuples/lists/arrays representing the starting and ending points for the route.
The orgins and destinations parameters should be in the form of iterable objects with two elements, such as
(latitude, longitude) or [latitude, longitude].

Parameters
----------
- `origins` : list of iterable objects
    The origin points. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

- `destinations` : list of iterable objects
    The destination points. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

- `append_od` : bool
    If True, the origins and destinations will be appended to the distance matrix as the first two columns.

Returns
-------
- `distance_matrix` : list of lists
    The distance matrix between the origins and destinations.

