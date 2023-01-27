import googlemaps

from georouting.routers.base import BaseRouter

class GoogleRouter(object):
    """Google router"""
    def __init__(self, key, mode="driving"):
        self.key = key
        self.mode = mode
        self.client = googlemaps.Client(key=key)

# FIXME: return the json object
# FIXME: how to design the interface 
# FIXMR: Maybe can put it into a base class
    def get_route(self, origin, destination):
        res = self.client.directions(origin, destination, self.mode)
        return res
    
    def get_route_matrix(self, origins, destinations):
        res = self.client.distance_matrix(origins, destinations, self.mode)
        return res
    
    def get_route_time_distance(self, origin, destination,timeout=10,language="en"):
        res = self.client.distance_matrix(origin, destination, self.mode)
        if res["rows"][0]["elements"][0]["status"] == "OK":
            return res['rows'][0]["elements"][0]['duration']['value']
        else:
            return None

# FIXME: return the time and distance
# FIXME: return then route geopandas
