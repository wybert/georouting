import requests
import json
from georouting.routers.base import BaseRouter

class EsriRouter(BaseRouter):
    """Esri router"""

    def __init__(self,key,mode="driving"):
        self.key = key
        self.mode = mode

    def _get_url(self, origin, destination, mode):
        return "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?travel_mode=%s&f=json&token=%s&stops=%f,%f;%f,%f" % (
            self.mode, self.key, origin[1], origin[0], destination[1], destination[0])
    def get_route_time_distance(self, origin, destination, mode):
        url = self._get_url(origin, destination, self.mode)
        resp = requests.get(url)
        res = json.loads(resp.content)
        try:
            return res['directions'][0]['summary']['totalDriveTime']
        except:
            return None

