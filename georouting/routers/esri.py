import requests
import json
from georouting.routers.base import WebRouter, Route, EsriRoute
import georouting.utils as gtl
import pandas as pd


class EsriRouter(WebRouter):
    """Esri router.
    The EsriRouter class is a subclass of the WebRouter class and is used for routing using the Esri ArcGIS API.
    This class is designed to provide a convenient and easy-to-use interface for interacting with the Esri ArcGIS API.
    It will return a router object that can be used to get routes and distance matrices.

    Parameters
    ----------

    - `api_key` : str
        The API key for the Esri ArcGIS API.

    - `mode` : str
        The routing mode. Can be either "driving" or "walking".

    - `timeout` : int
        The timeout in seconds for API requests.

    - `language` : str
        The language to be used in API requests.

    Returns
    -------
    - `EsriRouter`:
        A router object that can be used to get routes and distance matrices.

    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        """
        This is the constructor method for the EsriRouter class.
        It initializes the class by calling the super() method and setting up
        the Client object of the Esri ArcGIS API using the provided api_key.
        The mode parameter sets the routing mode, which can be either "driving" or "walking".
        The timeout parameter sets the timeout in seconds for API requests, and the language
        parameter sets the language to be used in API requests.
        """
        super().__init__(api_key, mode=mode, timeout=timeout, language=language)
        self.base_url = "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve"

    def _get_directions_url(self, origin, destination):
        """
        This method is a helper method for sending a directions request to the Esri ArcGIS API.
        It takes two parameters, origin and destination, which represent the starting and ending
        points for the route.
        """

        # specify the distance and time unit it return
        url = (
            "%s?f=json&token=%s&stops=%f,%f;%f,%f&travel_mode=%s&directionsLanguage=%s&returnRoutes=true"
            % (
                self.base_url,
                self.api_key,
                origin[1],
                origin[0],
                destination[1],
                destination[0],
                self.mode,
                self.language,
            )
        )

        return url

    def _get_matrix_distance_url(self, origins, destinations):
        """
        This method is a helper method for sending a distance matrix request to the Esri ArcGIS API.
        """
        base_url = "https://route-api.arcgis.com/arcgis/rest/services/World/OriginDestinationCostMatrix/NAServer/OriginDestinationCostMatrix_World/solveODCostMatrix"
        origins = ";".join(["%f,%f" % (o[1], o[0]) for o in origins])
        destinations = ";".join(["%f,%f" % (d[1], d[0]) for d in destinations])
        url = (
            "%s?f=json&token=%s&origins=%s&destinations=%s&travel_mode=%s&directionsLanguage=%s"
            % (
                base_url,
                self.api_key,
                origins,
                destinations,
                self.mode,
                self.language,
            )
        )

        return url

    def _parse_distance_matrix(self, json_data):
        """
        This method is a helper method for parsing the response from the Esri ArcGIS API.
        It takes one parameter, json_data, which is the response from the API.
        """

        return None

    def get_route(self, origin, destination):
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
        route = Route(EsriRoute(route), origin=origin, destination=destination)

        return route

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        This method returns a distance matrix between the origins and destinations.
        The origins and destinations parameters are lists of tuples/lists/arrays representing the starting and ending points for the route.
        The orgins and destinations parameters should be in the form of iterable objects with two elements, such as
        (latitude, longitude) or [latitude, longitude].

        Parameters
        ----------
        - `origins` : list of iterable objects
            The origin points. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

        - `destinations` : list of iterable objects
            The destination points. Iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude]

        - `append_od` : bool
            If True, the origins and destinations will be appended to the distance matrix as the first two columns.

        Returns
        -------
        - `distance_matrix` : list of lists
            The distance matrix between the origins and destinations.

        """

        # check if the origins and destinations is numpy array
        # if so, convert it to list
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        return res

        distance_matrix = self._parse_distance_matrix(res)

        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix
