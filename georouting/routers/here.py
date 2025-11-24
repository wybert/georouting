import pandas as pd
import requests

import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, HereRoute


class HereRouter(WebRouter):
    """
    HERE router (Routing API 7.2).
    Provides route and matrix queries.
    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.route_url = "https://route.ls.hereapi.com/routing/7.2/calculateroute.json"
        self.matrix_url = (
            "https://matrix.route.ls.hereapi.com/routing/7.2/calculatematrix.json"
        )

    def _mode_string(self):
        mapping = {"driving": "car", "walking": "pedestrian", "bicycling": "bicycle"}
        transport = mapping.get(self.mode, self.mode)
        return f"fastest;{transport};traffic:disabled"

    def _get_directions_url(self, origin, destination):
        """
        Build URL for directions request.
        """
        return (
            f"{self.route_url}?apiKey={self.api_key}"
            f"&mode={self._mode_string()}"
            f"&waypoint0=geo!{origin[0]},{origin[1]}"
            f"&waypoint1=geo!{destination[0]},{destination[1]}"
            f"&representation=display"
        )

    def _get_matrix_distance_url(self, origins, destinations):
        """
        Build URL for matrix request.
        """
        parts = [f"{self.matrix_url}?apiKey={self.api_key}&mode={self._mode_string()}"]
        for idx, o in enumerate(origins):
            parts.append(f"&start{idx}={o[0]},{o[1]}")
        for idx, d in enumerate(destinations):
            parts.append(f"&destination{idx}={d[0]},{d[1]}")
        return "".join(parts)

    def _parse_distance_matrix(self, json_data, num_origins, num_destinations):
        """
        Parse HERE matrix response to a tidy dataframe.
        """
        entries = json_data.get("response", {}).get("matrixEntry", [])
        lookup = {
            (e.get("startIndex"), e.get("destinationIndex")): e.get("summary", {})
            for e in entries
        }

        distances = []
        durations = []
        for i in range(num_origins):
            for j in range(num_destinations):
                summary = lookup.get((i, j), {})
                distances.append(summary.get("distance"))
                durations.append(summary.get("travelTime"))

        return pd.DataFrame({"distance (m)": distances, "duration (s)": durations})

    def get_route(self, origin, destination):
        """
        Return a Route object representing the route between origin and destination.
        """
        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        return Route(HereRoute(route), origin, destination)

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        Return duration/distance for all origin-destination pairs.
        """
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(
            res, len(origins), len(destinations)
        )

        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix
