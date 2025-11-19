import pandas as pd
import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, BaiduRoute
import json

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
        """
        
        return "%sdriving?origins=%s&destinations=%s&ak=%s" % (
            self.base_url,
            gtl._format_coords(origins),
            gtl._format_coords(destinations),
            self.api_key,
        )
    
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
        route = Route(BaiduRoute(route),origin=origin,destination=destination)
        return route