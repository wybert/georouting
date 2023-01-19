import requests
import json
# from georouting.routers.base import BaseRouter

class BingRouter(object):
    """Bing Maps API router"""

    def __init__(self, api_key,mode="driving"):
        self.api_key = api_key
        self.mode = mode

    def _get_url(self, origin, destination):
        return "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=%f,%f&destinations=%f,%f&travelMode=%s&key=%s" % (
            origin[0], origin[1], destination[0], destination[1], self.mode, self.api_key)

    def get_route_time_distance(self, origin, destination):
        url = self._get_url(origin, destination)
        resp = requests.get(url)
        res = json.loads(resp.content)
        if res['statusDescription'] == "OK":

            return res['resourceSets'][0]['resources'][0]['results'][0]['travelDuration']
        else:
            print(res)
            return None
