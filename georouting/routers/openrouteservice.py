import pandas as pd
import requests

import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, ORSRoute


class ORSRouter(WebRouter):
    """
    OpenRouteService router for directions and matrix endpoints.
    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://api.openrouteservice.org"

    def _profile(self):
        mapping = {
            "driving": "driving-car",
            "walking": "foot-walking",
            "bicycling": "cycling-regular",
            "cycling": "cycling-regular",
        }
        return mapping.get(self.mode, self.mode)

    def _directions_endpoint(self):
        return f"{self.base_url}/v2/directions/{self._profile()}"

    def _matrix_endpoint(self):
        return f"{self.base_url}/v2/matrix/{self._profile()}"

    def _post(self, url, payload):
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _parse_distance_matrix(self, json_data, num_origins, num_destinations):
        durations = json_data.get("durations", [])
        distances = json_data.get("distances", [])
        durations = [item for sublist in durations for item in sublist]
        distances = [item for sublist in distances for item in sublist]
        return pd.DataFrame({"distance (m)": distances, "duration (s)": durations})

    def get_route(self, origin, destination):
        coords = [[origin[1], origin[0]], [destination[1], destination[0]]]
        payload = {"coordinates": coords, "instructions": False}
        route = self._post(self._directions_endpoint(), payload)
        return Route(ORSRoute(route), origin, destination)

    def get_distance_matrix(self, origins, destinations, append_od=False):
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        coords = [[c[1], c[0]] for c in origins + destinations]
        sources = list(range(len(origins)))
        destinations_idx = list(range(len(origins), len(origins) + len(destinations)))

        payload = {
            "locations": coords,
            "sources": sources,
            "destinations": destinations_idx,
            "metrics": ["distance", "duration"],
        }

        res = self._post(self._matrix_endpoint(), payload)
        distance_matrix = self._parse_distance_matrix(res, len(origins), len(destinations))

        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix
