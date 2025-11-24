# Table of Contents

* [georouting.routers.here](#georouting.routers.here)
  * [HereRouter](#georouting.routers.here.HereRouter)
    * [get\_route](#georouting.routers.here.HereRouter.get_route)
    * [get\_distance\_matrix](#georouting.routers.here.HereRouter.get_distance_matrix)

<a id="georouting.routers.here"></a>

# georouting.routers.here

<a id="georouting.routers.here.HereRouter"></a>

## HereRouter Objects

```python
class HereRouter(WebRouter)
```

HERE router (Routing API 7.2).
Provides route and matrix queries.

<a id="georouting.routers.here.HereRouter.get_route"></a>

#### get\_route

```python
def get_route(origin, destination)
```

Return a Route object representing the route between origin and destination.

<a id="georouting.routers.here.HereRouter.get_distance_matrix"></a>

#### get\_distance\_matrix

```python
def get_distance_matrix(origins, destinations, append_od=False)
```

Return duration/distance for all origin-destination pairs.

