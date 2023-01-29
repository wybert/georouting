import requests
import pandas as pd
from georouting.routers.base import WebRouter, Route, BingRoute
import json
# from georouting.routers.base import BaseRouter

class BingRouter(WebRouter):
    """Bing Maps API router"""

    def __init__(self, api_key,mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://dev.virtualearth.net/REST/v1/Routes/"

    def _get_url(self, origin, destination):
        return "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=%f,%f&destinations=%f,%f&travelMode=%s&key=%s" % (
            origin[0], origin[1], destination[0], destination[1], self.mode, self.api_key)

    def _get_request(self, origin, destination):
        url = self._get_url(origin, destination)
        return super()._get_request(url)

    def get_route(self, origin, destination):
        route = self._get_request(origin, destination)
        route = Route(BingRoute(route))
        return route

    def get_distance_matrix(self, origins, destinations):
        url = self._get_url(origins, destinations)
        return super()._get_request(url)

