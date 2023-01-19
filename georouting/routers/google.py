import googlemaps

class GoogleRouter(object):
    def __init__(self, key, mode="driving"):
        self.key = key
        self.mode = mode
        self.client = googlemaps.Client(key=key)

    def get_route_time_distance(self, origin, destination):
        res = self.client.distance_matrix(origin, destination, self.mode)
        if res["rows"][0]["elements"][0]["status"] == "OK":
            return res['rows'][0]["elements"][0]['duration']['value']
        else:
            return None

