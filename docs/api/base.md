# Table of Contents

* [georouting.routers.base](#georouting.routers.base)
  * [GoogleRoute](#georouting.routers.base.GoogleRoute)
    * [get\_duration](#georouting.routers.base.GoogleRoute.get_duration)
    * [get\_distance](#georouting.routers.base.GoogleRoute.get_distance)
    * [get\_route](#georouting.routers.base.GoogleRoute.get_route)
    * [get\_route\_geopandas](#georouting.routers.base.GoogleRoute.get_route_geopandas)
  * [BingRoute](#georouting.routers.base.BingRoute)
    * [get\_duration](#georouting.routers.base.BingRoute.get_duration)
    * [get\_distance](#georouting.routers.base.BingRoute.get_distance)
    * [get\_route](#georouting.routers.base.BingRoute.get_route)
    * [get\_route\_geopandas](#georouting.routers.base.BingRoute.get_route_geopandas)
  * [OSRMRoute](#georouting.routers.base.OSRMRoute)
    * [get\_duration](#georouting.routers.base.OSRMRoute.get_duration)
    * [get\_distance](#georouting.routers.base.OSRMRoute.get_distance)
    * [get\_route](#georouting.routers.base.OSRMRoute.get_route)
    * [get\_route\_geopandas](#georouting.routers.base.OSRMRoute.get_route_geopandas)
  * [EsriRoute](#georouting.routers.base.EsriRoute)
  * [Route](#georouting.routers.base.Route)
    * [\_\_init\_\_](#georouting.routers.base.Route.__init__)
    * [get\_duration](#georouting.routers.base.Route.get_duration)
    * [get\_distance](#georouting.routers.base.Route.get_distance)
    * [get\_route](#georouting.routers.base.Route.get_route)
    * [get\_route\_geopandas](#georouting.routers.base.Route.get_route_geopandas)
    * [plot\_route](#georouting.routers.base.Route.plot_route)
  * [BaseRouter](#georouting.routers.base.BaseRouter)
    * [get\_distances\_batch](#georouting.routers.base.BaseRouter.get_distances_batch)
  * [WebRouter](#georouting.routers.base.WebRouter)

<a id="georouting.routers.base"></a>

# georouting.routers.base

<a id="georouting.routers.base.GoogleRoute"></a>

## GoogleRoute Objects

```python
class GoogleRoute()
```

The class "GoogleRoute" which allows to retrieve information from a route provided as an argument.

The class has the following methods:

- `get_duration()`: Returns the duration of the route in seconds.

- `get_distance()`: Returns the distance of the route in meters.

- `get_route()`: Returns the complete route information.

- `get_route_geopandas()`: Returns a GeoDataFrame with information such as distance, duration, and speed of each step in the route.

It is assumed that the polyline module is used for decoding the polyline into a LineString geometry. The GeoDataFrame is created with a specified coordinate reference system (CRS) of "4326".

<a id="georouting.routers.base.GoogleRoute.get_duration"></a>

#### get\_duration

```python
def get_duration()
```

Returns the duration of the route in seconds.

<a id="georouting.routers.base.GoogleRoute.get_distance"></a>

#### get\_distance

```python
def get_distance()
```

Returns the distance of the route in meters.

<a id="georouting.routers.base.GoogleRoute.get_route"></a>

#### get\_route

```python
def get_route()
```

Returns the complete route information.

<a id="georouting.routers.base.GoogleRoute.get_route_geopandas"></a>

#### get\_route\_geopandas

```python
def get_route_geopandas()
```

Returns a GeoDataFrame with information such as distance, duration, and speed of each step in the route. It is assumed that the polyline module is used for decoding the polyline into a LineString geometry. The GeoDataFrame is created with a specified coordinate reference system (CRS) of "4326".

<a id="georouting.routers.base.BingRoute"></a>

## BingRoute Objects

```python
class BingRoute()
```

BingRoute class that allows you to extract various information from a route stored in a dictionary. It has the following functions:

- `get_duration()`: Returns the travel duration in seconds.
- `get_distance()`: Returns the travel distance in meters.
- `get_route()`: Returns the entire route in a dictionary.
- `get_route_geopandas()`: Returns the route information in a GeoPandas dataframe.

This function extracts the duration and distance information for each leg of the route, creates a list of shapely LineStrings representing the route, and then creates a GeoDataFrame with columns for the duration, distance, and geometry. Additionally, it calculates the speed in meters per second for each leg.

The class is designed to work with data returned by the Bing Maps REST Services API, as the data is stored in a dictionary with a specific structure.

<a id="georouting.routers.base.BingRoute.get_duration"></a>

#### get\_duration

```python
def get_duration()
```

get the travel duration in seconds

<a id="georouting.routers.base.BingRoute.get_distance"></a>

#### get\_distance

```python
def get_distance()
```

get the travel distance in meters

<a id="georouting.routers.base.BingRoute.get_route"></a>

#### get\_route

```python
def get_route()
```

get the entire route in a dictionary

<a id="georouting.routers.base.BingRoute.get_route_geopandas"></a>

#### get\_route\_geopandas

```python
def get_route_geopandas()
```

This function extracts the duration and distance information for each leg of the route, creates a list of shapely LineStrings representing the route, and then creates a GeoDataFrame with columns for the duration, distance, and geometry. Additionally, it calculates the speed in meters per second for each leg.

Returns the route information in a GeoPandas dataframe.

<a id="georouting.routers.base.OSRMRoute"></a>

## OSRMRoute Objects

```python
class OSRMRoute()
```

This class represents a route returned by the OpenStreetMap Routing Machine API.

**Methods**:

  - `get_duration()` -> float: Returns the duration of the route in seconds.
  - `get_distance()` -> float: Returns the distance of the route in meters.
  - `get_route()` -> dict: Returns the full route as a dictionary.
  - `get_route_geopandas()` -> geopandas.GeoDataFrame: Returns the route as a GeoDataFrame. The GeoDataFrame contains columns for 'duration (s)', 'distance (m)', 'geometry', and 'speed (m/s)'.

<a id="georouting.routers.base.OSRMRoute.get_duration"></a>

#### get\_duration

```python
def get_duration()
```

Get the duration of the route in seconds.

<a id="georouting.routers.base.OSRMRoute.get_distance"></a>

#### get\_distance

```python
def get_distance()
```

Get the distance of the route in meters.

<a id="georouting.routers.base.OSRMRoute.get_route"></a>

#### get\_route

```python
def get_route()
```

Get the full route information as a dictionary.

<a id="georouting.routers.base.OSRMRoute.get_route_geopandas"></a>

#### get\_route\_geopandas

```python
def get_route_geopandas()
```

Get the route as a GeoDataFrame. The GeoDataFrame contains columns for 'duration (s)', 'distance (m)', 'geometry', and 'speed (m/s)'.

<a id="georouting.routers.base.EsriRoute"></a>

## EsriRoute Objects

```python
class EsriRoute()
```

The EsriRoute class is a class for handling a route obtained from the Esri ArcGIS routing service.

The class has the following methods:

- `get_duration`: returns the total travel time of the route.

- `get_distance`: returns the total distance of the route in meters.

- `get_route`: returns the entire route as a dictionary.

- `get_route_geopandas`: raises a NotImplementedError. This method is not yet implemented and will be added in the future.

<a id="georouting.routers.base.Route"></a>

## Route Objects

```python
class Route(object)
```

A wrapper class that wraps different routing engines' route objects.

It will return a Route object that can be used to get the duration, distance, and route information.

The class has the following methods:

- `get_duration()`: Returns the duration of the route in seconds.

- `get_distance()`: Returns the distance of the route in meters.

- `get_route()`: Returns the complete route information.

- `get_route_geopandas()`: Returns a GeoDataFrame with information such as distance, duration, and speed of each step in the route.

<a id="georouting.routers.base.Route.__init__"></a>

#### \_\_init\_\_

```python
def __init__(route, origin, destination)
```

Initialize a Route object by passing the routing engine's route object.

**Arguments**:

- `route`: An instance of a routing engine's route object

<a id="georouting.routers.base.Route.get_duration"></a>

#### get\_duration

```python
def get_duration()
```

Get the duration of the route.

<a id="georouting.routers.base.Route.get_distance"></a>

#### get\_distance

```python
def get_distance()
```

Get the distance of the route.

<a id="georouting.routers.base.Route.get_route"></a>

#### get\_route

```python
def get_route()
```

Get the raw route information.

<a id="georouting.routers.base.Route.get_route_geopandas"></a>

#### get\_route\_geopandas

```python
def get_route_geopandas()
```

Get the route information as a GeoDataFrame.

<a id="georouting.routers.base.Route.plot_route"></a>

#### plot\_route

```python
def plot_route()
```

Plot the route on a map.

<a id="georouting.routers.base.BaseRouter"></a>

## BaseRouter Objects

```python
class BaseRouter(object)
```

The class BaseRouter serves as a base class for routers, which are used to compute the optimal route between two points. The class has an instance variable mode, which is a string that defines the mode of transportation (e.g. "driving").

The BaseRouter class has a single method _get_OD_matrix, which takes two arguments origins and destinations and returns an origin-destination matrix. The method creates an empty list items and loops through each origin and destination pair, appending the concatenated origin and destination to the list. The origin-destination matrix is then created from the list items and returned.

<a id="georouting.routers.base.BaseRouter.get_distances_batch"></a>

#### get\_distances\_batch

```python
def get_distances_batch(origins,
                        destinations,
                        max_batch_size=25,
                        append_od=False)
```

This method returns a Pandas dataframe contains duration and disatnce for all the `origins` and `destinations` pairs. Use this function if you don't want to get duration and distance for all possible combinations between each origin and each destination.

The origins and destinations parameters are lists of origin-destination pairs. They should be the same length.

If the `append_od` parameter is set to True, the method also returns the input origin-destination pairs.

<a id="georouting.routers.base.WebRouter"></a>

## WebRouter Objects

```python
class WebRouter(BaseRouter)
```

The WebRouter class is a class for handling a route obtained from a web-based routing service.

