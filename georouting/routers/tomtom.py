import requests
import pandas as pd

import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, TomTomRoute


class TomTomRouter(WebRouter):
    """
    TomTom router.

    Provides access to TomTom Routing and Matrix APIs to retrieve routes and distance
    matrices with a unified interface.
    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://api.tomtom.com/routing/1"

    def _map_mode(self):
        """Map internal mode to TomTom travelMode values."""
        mapping = {"driving": "car", "walking": "pedestrian", "bicycling": "bicycle"}
        return mapping.get(self.mode, self.mode)

    def _get_directions_url(self, origin, destination):
        """
        Helper to build the URL for a directions request.
        """
        return (
            f"{self.base_url}/calculateRoute/"
            f"{origin[0]},{origin[1]}:{destination[0]},{destination[1]}/json"
            f"?key={self.api_key}&travelMode={self._map_mode()}"
        )

    def _get_matrix_distance_url(self):
        """
        Helper to build the URL for a matrix distance request.
        """
        return f"{self.base_url}/matrix/sync/json?key={self.api_key}"

    def _build_matrix_payload(self, origins, destinations):
        """Construct the payload for the matrix API."""
        return {
            "origins": [
                {"point": {"latitude": o[0], "longitude": o[1]}} for o in origins
            ],
            "destinations": [
                {"point": {"latitude": d[0], "longitude": d[1]}} for d in destinations
            ],
            "options": {"travelMode": self._map_mode(), "traffic": False},
        }

    def _post_request(self, url, payload):
        """Send a POST request to TomTom."""
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _parse_distance_matrix(self, json_data, num_origins, num_destinations):
        """
        Parse TomTom matrix response into a tidy dataframe ordered by
        origin->destination.
        """
        routes = json_data.get("routes", [])
        lookup = {
            (route.get("originIndex"), route.get("destinationIndex")): route.get(
                "summary", {}
            )
            for route in routes
        }

        distances = []
        durations = []
        for i in range(num_origins):
            for j in range(num_destinations):
                summary = lookup.get((i, j), {})
                distances.append(summary.get("lengthInMeters"))
                durations.append(summary.get("travelTimeInSeconds"))

        return pd.DataFrame({"distance (m)": distances, "duration (s)": durations})

    def get_route(self, origin, destination):
        """
        Return a Route object representing the path between origin and destination.
        """
        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        route = Route(TomTomRoute(route), origin=origin, destination=destination)
        return route

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        Return a Pandas dataframe of durations and distances for all origin/destination pairs.
        """
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        url = self._get_matrix_distance_url()
        payload = self._build_matrix_payload(origins, destinations)
        res = self._post_request(url, payload)
        distance_matrix = self._parse_distance_matrix(
            res, len(origins), len(destinations)
        )

        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix
