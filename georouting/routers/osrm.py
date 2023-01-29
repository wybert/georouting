import requests
import json
import pandas as pd
from georouting.routers.base import WebRouter, Route, OSRMRoute


class OSRMRouter(WebRouter):
    """OSRM router"""

    def __init__(self,mode="driving", timeout=10, language="en",base_url="http://router.project-osrm.org"):
        super().__init__(api_key=None, mode=mode, timeout=timeout, language=language,base_url=None)
        # nned let user reset the base_url
        self.base_url = base_url



    def _get_directions_url(self, origin, destination):
        return "%s/route/v1/%s/%f,%f;%f,%f?steps=true&annotations=true&geometries=geojson" % (
            self.base_url, self.mode, origin[1], origin[0], destination[1], destination[0])
    
    def _get_matrix_distance_url(self, origins, destinations):
        origins = [str(item[1]) + "," + str(item[0])  for item in origins]
        destinations = [str(item[1]) + "," + str(item[0])  for item in destinations]
        origins = ";".join(origins)
        destinations = ";".join(destinations)
        return "%s/table/v1/%s/%s;%s?overview=false" % (self.base_url,self.mode,origins,destinations)

    def _parse_distance_matrix(self, json_data):
        df = pd.DataFrame(json_data['durations'])
        df.columns = json_data['destinations']
        df.index = json_data['sources']
        return df

    def get_route(self, origin, destination):
        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        route = Route(OSRMRoute(route))
        return route

    def get_distance_matrix(self, origins, destinations,append_od=False):

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)
        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix

    # def _get_url(self, origin, destination):
    #     return "http://router.project-osrm.org/route/v1/%s/%f,%f;%f,%f?overview=false" % (
    #         self.mode, origin[1], origin[0], destination[1], destination[0])

    # def get_route_time_distance(self, origin, destination):
    #     url = self._get_url(origin, destination)
    #     resp = requests.get(url)
    #     res = json.loads(resp.content)
    #     self.raw = res

    #     if res['code'] == "Ok":

    #         return res["routes"][0]['duration']
    #     else:
    #         print(res)
    #         return None

