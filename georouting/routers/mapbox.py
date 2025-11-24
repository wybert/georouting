import json
import pandas as pd
import requests

import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, MapboxRoute


class MapboxRouter(WebRouter):
    """
    Mapbox router.

    Uses Mapbox Directions and Matrix APIs to fetch routes and distance matrices.
    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://api.mapbox.com"

    def _map_mode(self):
        mapping = {
            "driving": "driving",
            "walking": "walking",
            "bicycling": "cycling",
            "cycling": "cycling",
        }
        return mapping.get(self.mode, self.mode)

    def _format_coords(self, coords):
        # Mapbox expects lon,lat
        return ";".join([f"{c[1]},{c[0]}" for c in coords])

    def _get_directions_url(self, origin, destination):
        coords = self._format_coords([origin, destination])
        return (
            f"{self.base_url}/directions/v5/mapbox/{self._map_mode()}/{coords}"
            f"?geometries=geojson&steps=true&access_token={self.api_key}"
        )

    def _get_matrix_distance_url(self, coords):
        return (
            f"{self.base_url}/directions-matrix/v1/mapbox/{self._map_mode()}/{coords}"
            f"?annotations=distance,duration&access_token={self.api_key}"
        )

    def _parse_distance_matrix(self, json_data):
        durations = json_data.get("durations", [])
        distances = json_data.get("distances", [])

        durations = [item for sublist in durations for item in sublist]
        distances = [item for sublist in distances for item in sublist]

        return pd.DataFrame({"distance (m)": distances, "duration (s)": durations})

    def get_route(self, origin, destination):
        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        return Route(MapboxRoute(route), origin, destination)

    def get_distance_matrix(self, origins, destinations, append_od=False):
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        coords = self._format_coords(origins + destinations)
        url = self._get_matrix_distance_url(coords)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)

        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix
