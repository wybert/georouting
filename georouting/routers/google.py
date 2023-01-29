import googlemaps

from georouting.routers.base import WebRouter, RouteMatrix, Route, GoogleRoute

class GoogleRouter(WebRouter):
    """Google router"""
    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode)
        self.base_url = "https://maps.googleapis.com/maps/api/directions/json"
        self.client = googlemaps.Client(key=self.api_key)

    # def _get_url(self, origin, destination):
    #     url = self.base_url + "?origin=%f,%f&destination=%f,%f&mode=%s&key=%s" % (
    #         origin[0], origin[1], destination[0], destination[1], self.mode, self.api_key)
    #     return url
    
    def _get_request(self, origin, destination):
        return self.client.directions(origin, destination, self.mode)

# What's the difference between directions and distance_matrix?
    def get_route(self, origin, destination):
        
        route = self._get_request(origin, destination)
        route = Route(GoogleRoute(route))
        
        return route

# distance_matrix is a matrix of distance and time between origins and destinations
# it not contains the route, right?
    def get_route_matrix(self, origins, destinations):
        res = self.client.distance_matrix(origins, destinations, self.mode)
        return res
    
    # This is maybe not needed
    # add some error handling
    # def get_route_time_distance(self, origin, destination,timeout=10,language="en"):
    #     res = self.client.distance_matrix(origin, destination, self.mode)
    #     if res["rows"][0]["elements"][0]["status"] == "OK":
    #         return res['rows'][0]["elements"][0]['duration']['value']
    #     else:
    #         return None

