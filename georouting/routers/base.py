
# -*- coding: utf-8 -*-


# make a class for the route object and the route matrix object
# the route object can have several methods to get the information, like time, distance, route, etc.
# what's the difference between the route object and the route matrix object?
# the route object is the route between two points, and the route matrix object is the route between a list of points
# the route object can be used to get the time, distance, route, etc. of the route between two points
# the route matrix object can be used to get the time, distance, route, etc. of the route between a list of points

class Route(object):
    def __init__(self, route):
        self.route = route

    def get_time(self):
        raise NotImplementedError

    def get_distance(self):
        raise NotImplementedError

    def get_route(self):
        raise NotImplementedError

    def get_route_geopandas(self):
        raise NotImplementedError

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
        pass
    
    def _get_url(self, origin, destination):
        raise NotImplementedError

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
    def __init__(self, api_key, mode="driving"):
        self.mode = mode

    def get_route_time_distance(self, origin, destination):
        raise NotImplementedError

    def get_route_time_distance_matrix(self, origins, destinations):
        raise NotImplementedError

    def get_route_geopandas(self, origin, destination):
        raise NotImplementedError

    def get_route_geopandas_matrix(self, origins, destinations):
        raise NotImplementedError