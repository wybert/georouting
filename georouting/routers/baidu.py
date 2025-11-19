import pandas as pd
import numpy as np
import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, BaiduRoute


class BaiduRouter(WebRouter):
    """
    Baidu Maps router.
    The BaiduRouter class is a subclass of the WebRouter class and is used for routing using the Baidu Maps API.
    This class is designed to provide a convenient and easy-to-use interface for interacting with the Baidu Maps API.

    It will return a router object that can be used to get routes and distance matrices.

    Parameters
    ----------

    - `api_key` : str
        The API key for the Baidu Maps API.

    - `mode` : str
        The routing mode. Can be either "driving" or "walking".

    - `timeout` : int
        The timeout in seconds for API requests.

    - `language` : str
        The language to be used in API requests.

    
    Returns
    -------
    - `BaiduRouter` :
        A router object that can be used to get routes and distance matrices.

    """
    
    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://api.map.baidu.com/direction/v2/"
        self.matrix_url = "https://api.map.baidu.com/routematrix/v2/"
    
    def _get_directions_url(self, origin, destination):
        """
        Helper function for getting the URL for a directions request.
        """
        
        return "%s%s?origin=%f,%f&destination=%f,%f&coord_type=wgs84&ak=%s" % (
            self.base_url,
            self.mode,
            origin[0],
            origin[1],
            destination[0],
            destination[1],
            self.api_key,
        )
    
    def _get_matrix_distance_url(self, origins, destinations):
        """
        Helper function for getting the URL for a distance matrix request.
        Baidu routematrix API uses format: lat,lng|lat,lng|...
        """
        # Format origins and destinations for Baidu API (lat,lng|lat,lng|...)
        origins_str = "|".join([f"{o[0]},{o[1]}" for o in origins])
        destinations_str = "|".join([f"{d[0]},{d[1]}" for d in destinations])

        return "%s%s?origins=%s&destinations=%s&coord_type=wgs84&output=json&ak=%s" % (
            self.matrix_url,
            self.mode,
            origins_str,
            destinations_str,
            self.api_key,
        )

    def _parse_distance_matrix(self, json_data):
        """
        Helper function for parsing the distance matrix response from Baidu API.
        Returns a dataframe of durations and distances.
        """
        elements = json_data.get("result", [])

        distances = []
        durations = []

        for element in elements:
            # Baidu returns distance in meters and duration in seconds
            distance = element.get("distance", {}).get("value", 0)
            duration = element.get("duration", {}).get("value", 0)
            distances.append(distance)
            durations.append(duration)

        df = pd.DataFrame({"distance (m)": distances, "duration (s)": durations})
        return df
    
    def get_route(self,origin,destination):
        """
        This method returns a Route object representing the route between the origin and destination points.
        The origin and destination parameters are tuples/list/arrays representing the starting and ending points for the route.
        The orgin and destination parameters should be in the form of iterable objects with two elements, such as
        (latitude, longitude) or [latitude, longitude].

        Parameters
        ----------
        - `origin` : iterable objects
            The origin point. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

        - `destination` : iterable objects
            The destination point. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

        Returns
        -------
        - `route` : Route object
            The route between the origin and destination.

        The returned Route object has the following functions:

        - `get_distance()` returns the distance of the route in meters.
        - `get_duration()` returns the duration of the route in seconds.
        - `get_route()` returns the raw route data returned as a dictionary.
        - `get_route_geodataframe()` returns the route as a GeoDataFrame.

        """

        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        route = Route(BaiduRoute(route), origin=origin, destination=destination)
        return route

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        This method returns a Pandas dataframe representing a distance matrix between the origins and destinations.
        It returns the duration and distance for all possible combinations between each origin and each destination.

        Parameters
        ----------
        - `origins` : iterable objects
            An iterable object containing the origin points (latitude, longitude).

        - `destinations` : iterable objects
            An iterable object containing the destination points (latitude, longitude).

        - `append_od` : bool
            If True, the method also returns a matrix of origin-destination pairs.

        Returns
        -------
        - `distance_matrix` : pandas.DataFrame
            A pandas DataFrame containing the distance matrix.
        """
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)

        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix

    def get_distances_batch(self, origins, destinations, append_od=False):
        """
        This method returns a Pandas dataframe contains duration and distance for all the origins and destinations pairs.
        Use this function if you don't want to get duration and distance for all possible combinations.

        Parameters
        ----------
        - `origins` : iterable objects
            An iterable object containing the origin points (latitude, longitude).

        - `destinations` : iterable objects
            An iterable object containing the destination points (latitude, longitude).

        - `append_od` : bool
            If True, the method also returns the input origin-destination pairs.

        Returns
        -------
        - `distance_matrix` : pandas.DataFrame
            A pandas DataFrame containing the distances for each OD pair.
        """
        # Baidu routematrix API has a limit of 50 origins/destinations
        df = super().get_distances_batch(
            origins, destinations, max_batch_size=50, append_od=append_od
        )
        return df