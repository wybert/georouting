import googlemaps
import pandas as pd
from georouting.routers.base import WebRouter, Route, GoogleRoute
import georouting.utils as gtl
import numpy as np

class GoogleRouter(WebRouter):
    """Google Map router. 
    The GoogleRouter class is a subclass of the WebRouter class and is used for routing using the Google Maps API. 
    This class is designed to provide a convenient and easy-to-use interface for interacting with the Google Maps API.
    
    It will return a router object that can be used to get routes and distance matrices.

    Parameters
    ----------

    - `api_key` : str
        The API key for the Google Maps API.
    
    - `mode` : str
        The routing mode. Can be either "driving" or "walking".
    
    - `timeout` : int
        The timeout in seconds for API requests.
    
    - `language` : str
        The language to be used in API requests.

    Returns
    -------
    - `GoogleRouter`:
        A router object that can be used to get routes and distance matrices.
    
    """

    def __init__(self, api_key, mode="driving", timeout=10, language="en"):
        """
        This is the constructor method for the GoogleRouter class. 
        It initializes the class by calling the super() method and setting up 
        the Client object of the Google Maps API using the provided api_key. 
        The mode parameter sets the routing mode, which can be either "driving" or "walking". 
        The timeout parameter sets the timeout in seconds for API requests, and the language 
        parameter sets the language to be used in API requests.
        """
        super().__init__(api_key, mode=mode)
        self.client = googlemaps.Client(key=self.api_key)

    def _get_directions_request(self, origin, destination):
        """
        This method is a helper method for sending a directions request to the Google Maps API. 
        It takes two parameters, origin and destination, which represent the starting and ending 
        points for the route.
        """
        return self.client.directions(origin, destination, self.mode)

    def _get_distance_matrix_request(self, origins, destinations):
        """
        This method is a helper method for sending a distance matrix request to the Google Maps API. 
        It takes two parameters, origins and destinations, which represent the starting and ending 
        points for each pair of routes in the matrix.
        """
        return self.client.distance_matrix(origins, destinations, self.mode)

    def _parse_distance_matrix(self, json_data):
        """
        This method is a helper method for parsing the JSON data returned from the Google Maps API 
        in response to a distance matrix request. It takes one parameter, json_data, which is the 
        raw JSON data. The method returns a Pandas dataframe containing the distances and durations 
        for each pair of routes.
        """

        results = []
        for element in json_data["rows"]:
            # print(element)
            # print(element['elements'])
            for i in element["elements"]:
                temp = {}
                temp["distance (m)"] = i["distance"]["value"]
                temp["duration (s)"] = i["duration"]["value"]
                results.append(temp)
        df = pd.DataFrame(results)

        return df

    def get_route(self, origin, destination):

        """
        This method returns a Route object representing the route between the origin and destination points. 
        The origin and destination parameters are tuples/list/arrays representing the starting and ending points for the route.
        The orgin and destination parameters should be in the form of iterable objects with two elements, such as (latitude, longitude) or [latitude, longitude].

        Parameters
        ----------
        - `origin` : iterable objects
            The origin point. Iterable objects with two elements, such as  
        (latitude, longitude) or [latitude, longitude]

        - `destination` : iterable objects
            The destination point. Iterable objects with two elements, such as  
        (latitude, longitude) or [latitude, longitude]

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

        route = self._get_directions_request(origin, destination)
        route = Route(GoogleRoute(route),origin, destination)

        return route

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        This method returns a Pandas dataframe representing a distance matrix between the `origins` and `destinations` points. It returns the duration and distance for
        all possible combinations between each origin and each destination. If you want just
        return the duration and distance for specific origin-destination pairs, use the `get_distances_batch` method.
        
        The origins and destinations parameters are lists of origins and destinations.

        If the `append_od` parameter is set to True, the method also returns a matrix of origin-destination pairs.

        Google Maps API has following limitations for distance matrix requests:
        the following usage limits are in place for the Distance Matrix API, for more information, 
        see in [google maps api documentation](https://developers.google.com/maps/documentation/distance-matrix/usage-limits):

        - Maximum of 25 origins or 25 destinations per request.
        - Maximum 100 elements per server-side request.
        - Maximum 100 elements per client-side request.
        - 1000 elements per second (EPS), calculated as the sum of client-side and server-side queries.

        Parameters
        ----------
        - `origins` : iterable objects
            An iterable object containing the origin points. It can be a list of tuples, a list of lists, a list of arrays, etc.
            It should be in the form of iterable objects with two elements, such as
            (latitude, longitude) or [latitude, longitude].

        - `destinations` : iterable objects
            An iterable object containing the destination points. It can be a list of tuples, a list of lists, a list of arrays, etc.
            It should be in the form of iterable objects with two elements, such as
            (latitude, longitude) or [latitude, longitude].
            
        - `append_od` : bool
            If True, the method also returns a matrix of origin-destination pairs.

        Returns
        -------
        - `distance_matrix` : pandas.DataFrame
            A pandas DataFrame containing the distance matrix.

        Here is an example of how to use this method:
        # TODO: add example

        """

        # Check if the origins and destinations parameters are lists
        # if ther are numpy arrays, convert them to lists
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        res = self._get_distance_matrix_request(origins, destinations)
        df = self._parse_distance_matrix(res)
        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            df = pd.concat([od_matrix, df], axis=1)
        return df
    
    def get_distances_batch(self, origins, destinations, append_od=False):
        """
        This method returns a Pandas dataframe contains duration and disatnce for all the `origins` and `destinations` pairs. Use this function if you don't want to get duration and distance for all possible combinations between each origin and each destination. 
        
        The origins and destinations parameters are lists of origin-destination pairs. They should be the same length.

        If the `append_od` parameter is set to True, the method also returns the input origin-destination pairs.

        Parameters
        ----------
        - `origins` : iterable objects
            An iterable object containing the origin points. It can be a list of tuples, a list of lists, a list of arrays, etc.
            It should be in the form of iterable objects with two elements, such as
            (latitude, longitude) or [latitude, longitude].

        - `destinations` : iterable objects
            An iterable object containing the destination points. It can be a list of tuples, a list of lists, a list of arrays, etc.
            It should be in the form of iterable objects with two elements, such as
            (latitude, longitude) or [latitude, longitude].

        - `append_od` : bool
            If True, the method also returns the input origin-destination pairs.

        Returns
        -------
        - `distance_matrix` : pandas.DataFrame
            A pandas DataFrame containing the distance matrix.

        """
        return super().get_distances_batch(origins, destinations,max_batch_size=25, append_od=append_od)




