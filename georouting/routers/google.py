import googlemaps
import pandas as pd

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
    
    def _get_directions_request(self, origin, destination):
        return self.client.directions(origin, destination, self.mode)

    def _get_directions_matrix_request(self, origins, destinations):
        return self.client.distance_matrix(origins, destinations, self.mode)

# google direction api returns the route, which also contains the distance and time
# same as bing api
    def get_route(self, origin, destination):
        
        route = self._get_directions_request(origin, destination)
        route = Route(GoogleRoute(route))
        
        return route

# google distance matirx api returns the distance and time matrix not the route
# so the route matrix can be returned as a pandas dataframe
# which contains the distance and time matrix
# same as bing api as well as the ESRI api
# you can put all the results into a  dataframe
    def _parse_json_data(self,json_data):
        
        results = []
        for element in json_data['rows']:
            # print(element)
            # print(element['elements'])
            for i in element['elements']:
                temp = {}
                temp['distance (m)'] = i['distance']['value']
                temp['duration (s)'] = i['duration']['value']
                results.append(temp)
        df = pd.DataFrame(results)

        return df

    def _get_OD_matrix(self, origins, destinations):

        items = []
        for i in origins:
            for j in destinations:
                item = i + j
                items.append(item)
        od_matrix = pd.DataFrame(items, columns=["orgin_lat",
        "orgin_lon","destination_lat","destination_lon"])

        return od_matrix

    def get_route_matrix(self, origins, destinations, append_od=False):

        res = self._get_directions_matrix_request(origins, destinations)
        df = self._parse_json_data(res)
        if append_od:
            od_matrix = self._get_OD_matrix(origins, destinations)
            df = pd.concat([od_matrix, df], axis=1)
        return df
    

