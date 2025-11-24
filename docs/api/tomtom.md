# Table of Contents

* [georouting.routers.tomtom](#georouting.routers.tomtom)
  * [TomTomRouter](#georouting.routers.tomtom.TomTomRouter)
    * [get\_route](#georouting.routers.tomtom.TomTomRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.tomtom.TomTomRouter.get_distance_matrix)

<a id="georouting.routers.tomtom"></a>

# georouting.routers.tomtom

<a id="georouting.routers.tomtom.TomTomRouter"></a>

## TomTomRouter Objects

```python
class TomTomRouter(WebRouter)
```

TomTom router.

Provides access to TomTom Routing and Matrix APIs to retrieve routes and distance
matrices with a unified interface.

<a id="georouting.routers.tomtom.TomTomRouter.get_route"></a>

#### get\_route

```python
def get_route(origin, destination)
```

Return a Route object representing the path between origin and destination.

<a id="georouting.routers.tomtom.TomTomRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

Return a Pandas dataframe of durations and distances for all origin/destination pairs.

