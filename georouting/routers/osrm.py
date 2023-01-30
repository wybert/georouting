import requests
import json
import pandas as pd
from georouting.routers.base import WebRouter, Route, OSRMRoute


# add document for this class
class OSRMRouter(WebRouter):
    """
    OSRM router.
    The base_url is the url of the osrm server,
    the default is the public server of osrm,
    you can also use your own server.

    mode: The mode of transportation to use for routing, default is "driving".
    timeout: The number of seconds to wait for a response from the API, default is 10.
    language: The language to use for the API response, default is "en".
    base_url: The base URL for the OSRM API, default is "http://router.project-osrm.org".
    """

    def __init__(
        self,
        mode="driving",
        timeout=10,
        language="en",
        base_url="http://router.project-osrm.org",
    ):
        super().__init__(
            api_key=None, mode=mode, timeout=timeout, language=language, base_url=None
        )
        # nned let user reset the base_url
        self.base_url = base_url

    def _get_directions_url(self, origin, destination):
        """
        Helper function for getting the URL for a directions request (To request a route between the given origin and destination coordinates).
        """
        return (
            "%s/route/v1/%s/%f,%f;%f,%f?steps=true&annotations=true&geometries=geojson"
            % (
                self.base_url,
                self.mode,
                origin[1],
                origin[0],
                destination[1],
                destination[0],
            )
        )

    def _get_matrix_distance_url(self, origins, destinations):
        """
        Helper function for getting the URL for a distance matrix request. Generates the URL to request a distance matrix between the given lists of origins and destinations coordinates.
        """

        # get the need cal location
        s = (
            str(list(range(len(origins))))
            .replace(",", ";")
            .replace("[", "")
            .replace("]", "")
            .replace(" ", "")
        )
        d = (
            str(list(range(len(origins), len(origins) + len(destinations))))
            .replace(",", ";")
            .replace("[", "")
            .replace("]", "")
            .replace(" ", "")
        )

        origins = [str(item[1]) + "," + str(item[0]) for item in origins]
        destinations = [str(item[1]) + "," + str(item[0]) for item in destinations]
        origins = ";".join(origins)
        destinations = ";".join(destinations)

        url = (
            "%s/table/v1/%s/%s;%s?sources=%s&destinations=%s&annotations=duration,distance"
            % (self.base_url, self.mode, origins, destinations, s, d)
        )
        return url

    def _parse_distance_matrix(self, json_data):
        """
        Helper function for parsing the distance matrix response. Parses the response from the distance matrix API and returns a dataframe of durations and distances.
        """
        durations = json_data["durations"]
        distances = json_data["distances"]

        # flatten the list
        durations = [item for sublist in durations for item in sublist]
        distances = [item for sublist in distances for item in sublist]

        # combine the dutation and destinations list to a dataframe
        print(len(durations), len(distances))
        df = pd.DataFrame({"distance (m)": durations, "duration (s)": distances})

        return df

    def get_route(self, origin, destination):
        """
        Get the route between the given origin and destination coordinates.  Requests a route from the API using the _get_directions_url method and returns the result as a Route object.
        """
        url = self._get_directions_url(origin, destination)
        route = super()._get_request(url)
        route = Route(OSRMRoute(route))
        return route

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        Get the distance matrix between the given lists of origins and destinations coordinates. Requests a distance matrix from the API using the _get_matrix_distance_url method and returns the result as a dataframe. If append_od is set to True, the origins and destinations are also included in the dataframe.
        """

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)
        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix
