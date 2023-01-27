
# -*- coding: utf-8 -*-


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
        raise NotImplementedError

    def get_route_matrix(self, origins, destinations):
        raise NotImplementedError

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