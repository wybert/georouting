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

    def _get_directions_url(self, origin, destination):

        return "%s%s?wp.0=%f,%f&wp.1=%f,%f&key=%s" % (self.base_url,self.mode,
            origin[0], origin[1], destination[0], destination[1], self.api_key)

    def _get_matrix_distance_url(self, origins, destinations):
        origins = [str(item[0]) + "," + str(item[1])  for item in origins]
        destinations = [str(item[0]) + "," + str(item[1])  for item in destinations]
        origins = ";".join(origins)
        destinations = ";".join(destinations)
        return "%sDistanceMatrix?origins=%s&destinations=%s&travelMode=%s&timeUnit=second&key=%s" % (self.base_url,
            origins,destinations, self.mode, self.api_key)

    def _parse_distance_matrix(self, json_data):

        df = pd.DataFrame(json_data['resourceSets'][0]['resources'][0]['results'])
        df = df[['travelDistance','travelDuration']]
        df.columns = ['distance (m)','duration (s)']
        return df

    def get_route(self, origin, destination):

        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        route = Route(BingRoute(route))
        return route
    
    def get_distance_matrix(self, origins, destinations,append_od=False):
        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)
        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix

