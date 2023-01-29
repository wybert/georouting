
# -*- coding: utf-8 -*-


# make a class for the route object and the route matrix object
# the route object can have several methods to get the information, like time, distance, route, etc.
# what's the difference between the route object and the route matrix object?
# the route object is the route between two points, and the route matrix object is the route between a list of points
# the route object can be used to get the time, distance, route, etc. of the route between two points
# the route matrix object can be used to get the time, distance, route, etc. of the route between a list of points
# This may need duck typing

class GoogleRoute:
    def __init__(self, route):
        self.route = route

    def get_time(self):
        return self.route[0]['legs'][0]['duration']['value']

    def get_distance(self):
        return self.route[0]['legs'][0]['distance']['value']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        
        import geopandas as gpd
        import polyline
        from shapely.geometry import LineString

        steps_google = self.route[0]['legs'][0]['steps']

        google_route1 = []
        for step in steps_google:
            step_g = {}
            step_g["distance"] = step["distance"]["value"]
            step_g["duration"] = step["duration"]["value"]
            step_g["geometry"] = polyline.decode(step['polyline']["points"], 5,
                        geojson=True
                        )
            step_g["geometry"] = LineString(step_g["geometry"])
            google_route1.append(step_g)
        google_route1 = gpd.GeoDataFrame(google_route1,geometry="geometry",crs = "4326")
        google_route1["speed(m/s)"] = google_route1["distance"] /  google_route1["duration"]  
        return google_route1


class GoogleRouteMatrix:
    def __init__(self, route_matrix):
        self.route_matrix = route_matrix

    def get_time(self):
        return self.route_matrix["rows"][0]["elements"][0]['duration']['value']

    def get_distance(self):
        return self.route_matrix["rows"][0]["elements"][0]['distance']['value']

    def get_route(self):
        return self.route_matrix

    def get_route_geopandas(self):
        raise NotImplementedError

class BingRoute:
    def __init__(self, route):
        self.route = route

    def get_time(self):
        return self.route['resourceSets'][0]['resources'][0]['results'][0]['travelDuration']

    def get_distance(self):
        return self.route['resourceSets'][0]['resources'][0]['results'][0]['travelDistance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError

class BingRouteMatrix:

    def __init__(self, route_matrix):
        self.route_matrix = route_matrix

    def get_time(self):
        return self.route_matrix['resourceSets'][0]['resources'][0]['results'][0]['travelDuration']

    def get_distance(self):
        return self.route_matrix['resourceSets'][0]['resources'][0]['results'][0]['travelDistance']

    def get_route(self):
        return self.route_matrix

    def get_route_geopandas(self):
        raise NotImplementedError

class MapboxRoute:

    def __init__(self, route):
        self.route = route

    def get_time(self):
        return self.route['routes'][0]['duration']

    def get_distance(self):
        return self.route['routes'][0]['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError

class MapboxRouteMatrix:

    def __init__(self, route_matrix):
        self.route_matrix = route_matrix

    def get_time(self):
        return self.route_matrix['durations'][0][1]

    def get_distance(self):
        return self.route_matrix['distances'][0][1]

    def get_route(self):
        return self.route_matrix

    def get_route_geopandas(self):
        raise NotImplementedError

class HereRoute:

    def __init__(self, route):
        self.route = route

    def get_time(self):
        return self.route['response']['route'][0]['summary']['travelTime']

    def get_distance(self):
        return self.route['response']['route'][0]['summary']['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError

class HereRouteMatrix:

    def __init__(self, route_matrix):
        self.route_matrix = route_matrix

    def get_time(self):
        return self.route_matrix['response']['matrixEntry'][0]['summary']['travelTime']

    def get_distance(self):
        return self.route_matrix['response']['matrixEntry'][0]['summary']['distance']

    def get_route(self):
        return self.route_matrix

    def get_route_geopandas(self):
        raise NotImplementedError

class MapQuestRoute:

    def __init__(self, route):
        self.route = route

    def get_time(self):
        return self.route['route']['time']

    def get_distance(self):
        return self.route['route']['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError

class MapQuestRouteMatrix:

    def __init__(self, route_matrix):
        self.route_matrix = route_matrix

    def get_time(self):
        return self.route_matrix['distance'][0][1]

    def get_distance(self):
        return self.route_matrix['time'][0][1]

    def get_route(self):
        return self.route_matrix

    def get_route_geopandas(self):
        raise NotImplementedError


class Route(object):
    def __init__(self, route):
        self.route = route

    def get_time(self):
        return self.route.get_time()

    def get_distance(self):
        return self.route.get_distance()

    def get_route(self):
        return self.route.get_route()

    def get_route_geopandas(self):
        return self.route.get_route_geopandas()

class RouteMatrix(object):
    def __init__(self, route_matrix):
        self.route_matrix = route_matrix

    def get_time(self):
        raise NotImplementedError

    def get_distance(self):
        raise NotImplementedError

    def get_route(self):
        raise NotImplementedError

    def get_route_geopandas(self):
        raise NotImplementedError

# base class for routers
class BaseRouter(object):
    def __init__(self, mode="driving"):
        self.mode = mode
    
    def _get_url(self, origin, destination):
        pass

    def _get_request(self):
        raise NotImplementedError
        

#   FIXME: if it can return the object which enable to do the further analysis, and this object 
#   can have several methods to get the information, like time, distance, route, etc.
    def get_route(self, origin, destination):
        
        return Route(self._get_request(origin, destination))

    def get_route_matrix(self, origins, destinations):
        
        return RouteMatrix(self._get_request(origins, destinations))

    def get_route_time_distance(self, origin, destination):
        raise NotImplementedError

    def get_route_time_distance_matrix(self, origins, destinations):
        raise NotImplementedError

    def get_route_geopandas(self, origin, destination):
        raise NotImplementedError

    def get_route_geopandas_matrix(self, origins, destinations):
        raise NotImplementedError

class WebRouter(BaseRouter):
    def __init__(self, api_key, mode="driving", timeout=10, language="en",base_url=None):
        self.api_key = api_key
        self.timeout = timeout
        self.language = language
        self.base_url = base_url
        super().__init__(mode=mode)


    def get_route_time_distance(self, origin, destination):
        raise NotImplementedError

    def get_route_time_distance_matrix(self, origins, destinations):
        raise NotImplementedError

    def get_route_geopandas(self, origin, destination):
        raise NotImplementedError

    def get_route_geopandas_matrix(self, origins, destinations):
        raise NotImplementedError

# make a class for local router 
class LocalRouter(BaseRouter):
    def __init__(self, mode="driving"):
        self.mode = mode

    def get_route_time_distance(self, origin, destination):
        raise NotImplementedError

    def get_route_time_distance_matrix(self, origins, destinations):
        raise NotImplementedError

    def get_route_geopandas(self, origin, destination):
        raise NotImplementedError

    def get_route_geopandas_matrix(self, origins, destinations):
        raise NotImplementedError