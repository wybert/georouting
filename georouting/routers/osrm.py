import requests
import json

class OSRMRouter(BaseRouter):
    """OSRM router"""

    def __init__(self,mode="driving"):
        self.mode = mode

    def _get_url(self, origin, destination, mode):
        return "http://router.project-osrm.org/route/v1/%s/%f,%f;%f,%f?overview=false" % (
            self.mode, origin[1], origin[0], destination[1], destination[0])

    def get_route_time_distance(self, origin, destination, mode):
        url = self._get_url(origin, destination, mode)
        resp = requests.get(url)
        res = json.loads(resp.content)

        if res['code'] == "Ok":

            return res["routes"][0]['duration']
        else:
            return None

