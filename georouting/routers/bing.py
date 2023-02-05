import requests
import pandas as pd
from georouting.routers.base import WebRouter, Route, BingRoute
import json

# from georouting.routers.base import BaseRouter

# smilarly to google.py, we need to improve the documentation
class BingRouter(WebRouter):
    """
    Bing Maps router.
    The BingRouter class is a subclass of the WebRouter class and is used for routing using the Bing Maps API.
    This class is designed to provide a convenient and easy-to-use interface for interacting with the Bing Maps API.

    It will return a router object that can be used to get routes and distance matrices.

    Parameters
    ----------

    `api_key` : str
        The API key for the Bing Maps API.

    `mode` : str
        The routing mode. Can be either "driving" or "walking".

    `timeout` : int
        The timeout in seconds for API requests.

    `language` : str
        The language to be used in API requests.


    Returns
    -------
    `BingRouter` :
        A router object that can be used to get routes and distance matrices.

    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://dev.virtualearth.net/REST/v1/Routes/"

    def _get_directions_url(self, origin, destination):
        """
        Helper function for getting the URL for a directions request.
        """

        return "%s%s?wp.0=%f,%f&wp.1=%f,%f&routeAttributes=routePath&key=%s" % (
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
        """

        origins = [str(item[0]) + "," + str(item[1]) for item in origins]
        destinations = [str(item[0]) + "," + str(item[1]) for item in destinations]
        origins = ";".join(origins)
        destinations = ";".join(destinations)
        return (
            "%sDistanceMatrix?origins=%s&destinations=%s&travelMode=%s&timeUnit=second&key=%s"
            % (self.base_url, origins, destinations, self.mode, self.api_key)
        )

    def _parse_distance_matrix(self, json_data):
        """
        Helper function for parsing the response from a distance matrix request.
        """

        df = pd.DataFrame(json_data["resourceSets"][0]["resources"][0]["results"])
        df = df[["travelDistance", "travelDuration"]]
        df.columns = ["distance (m)", "duration (s)"]
        return df

    def get_route(self, origin, destination):
        """
        This method returns a Route object representing the route between the origin and destination points. 
        The origin and destination parameters are tuples/list/arrays representing the starting and ending points for the route.
        The orgin and destination parameters should be in the form of iterable objects with two elements, such as  
        (latitude, longitude) or [latitude, longitude].

        Parameters
        ----------
        `origin` : iterable objects
            The origin point. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

        `destination` : iterable objects
            The destination point. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

        Returns
        -------
        `route` : Route object
            The route between the origin and destination.

        The returned Route object has the following functions:

        - `get_distance()` returns the distance of the route in meters.
        - `get_duration()` returns the duration of the route in seconds.
        - `get_route()` returns the raw route data returned as a dictionary.
        - `get_route_geodataframe()` returns the route as a GeoDataFrame.
        
        """

        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        route = Route(BingRoute(route))
        return route

    def get_distance_matrix(self, origins, destinations, append_od=False):

        """
        This method returns a Pandas dataframe representing a distance matrix between the `origins` and `destinations` points. It returns the duration and distance for
        all possible combinations between each origin and each destination. If you want just
        return the duration and distance for specific origin-destination pairs, use the `get_distances_batch` method.
        
        The origins and destinations parameters are lists of origins and destinations.

        If the `append_od` parameter is set to True, the method also returns a matrix of origin-destination pairs.

        Parameters
        ----------
        `origins` : iterable objects
            An iterable object containing the origin points. It can be a list of tuples, a list of lists, a list of arrays, etc.
            It should be in the form of iterable objects with two elements, such as
            (latitude, longitude) or [latitude, longitude].
        `destinations` : iterable objects
            An iterable object containing the destination points. It can be a list of tuples, a list of lists, a list of arrays, etc.
            It should be in the form of iterable objects with two elements, such as
            (latitude, longitude) or [latitude, longitude].
        `append_od` : bool
            If True, the method also returns a matrix of origin-destination pairs.

        Returns
        -------
        `distance_matrix` : pandas.DataFrame
            A pandas DataFrame containing the distance matrix.
        """

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)
        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix

    def get_distances_batch(self, origins, destinations, append_od=False):
        
        """
        This method returns a Pandas dataframe contains duration and disatnce for all the `origins` and `destinations` pairs. Use this function if you don't want to get duration and distance for all possible combinations between each origin and each destination. 
        
        The origins and destinations parameters are lists of origin-destination pairs. They should be the same length.

        If the `append_od` parameter is set to True, the method also returns the input origin-destination pairs.
        """

        # raise the not implemnt error
        raise NotImplementedError