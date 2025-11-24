import requests
import json
import pandas as pd
import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, OSRMRoute
import numpy as np


# add document for this class
class OSRMRouter(WebRouter):
    """
    OSRM router.
    The OSRMRouter class is a subclass of the WebRouter class and is used for routing using the OSRM API.
    This class is designed to provide a convenient and easy-to-use interface for interacting with the OSRM API.

    It will return a router object that can be used to get routes and distance matrices.

    Parameters
    ----------
    - `mode` : str
        The routing mode. Can be either "driving" or "walking". Default is "driving".

    - `timeout` : int
        The timeout in seconds for API requests. Default is 10.

    - `language` : str
        The language to be used in API requests. Default is "en".

    - `base_url` : str
        The base URL for the OSRM API. Default is "http://router.project-osrm.org".

    Returns
    -------
    - `OSRMRouter`:
        A router object that can be used to get routes and distance matrices.

    """

    def __init__(
        self,
        mode="driving",
        timeout=10,
        language="en",
        base_url="http://router.project-osrm.org",
        auto_start_backend=False,
        backend_runtime="docker",  # or "singularity"
        backend_region="north-america/us/massachusetts",
        backend_port=5000,
        backend_tag="osrm-backend",
        backend_dockerfile=None,
        backend_context=None,
        backend_profile=None,
        backend_base_image=gtl.DEFAULT_OSRM_BASE_IMAGE,
        backend_sif_path=None,
        backend_recipe_path=None,
        backend_instance_name="osrm",
        backend_extra_run_args=None,
    ):
        super().__init__(
            api_key=None, mode=mode, timeout=timeout, language=language, base_url=None
        )

        def _mode_to_profile(m):
            m = m.lower()
            if m in ["driving", "drive", "car", "auto"]:
                return "car"
            if m in ["walking", "walk", "foot"]:
                return "foot"
            if m in ["bicycling", "cycling", "bike", "bicycle"]:
                return "bicycle"
            return "car"

        if auto_start_backend:
            profile = backend_profile or _mode_to_profile(mode)
            try:
                print(
                    f"[osrm] Auto-starting local OSRM backend ({backend_runtime}) for region '{backend_region}' on port {backend_port} (profile: {profile})"
                )
                print(
                    "[osrm] Requires Docker/Singularity and sufficient disk/RAM for the region extract."
                )
                if backend_runtime.lower() == "docker":
                    gtl.build_and_run_osrm(
                        region=backend_region,
                        port=backend_port,
                        tag=backend_tag,
                        dockerfile_path=backend_dockerfile,
                        context=backend_context,
                        auto_fetch=True,
                        prefer_html=True,
                        profile=profile,
                        base_image=backend_base_image,
                        extra_run_args=backend_extra_run_args,
                    )
                    self.base_url = f"http://localhost:{backend_port}"
                    print(f"[osrm] Local Docker backend started at {self.base_url}")
                elif backend_runtime.lower() in ["singularity", "apptainer"]:
                    gtl.build_and_run_osrm_singularity(
                        region=backend_region,
                        port=backend_port,
                        sif_path=backend_sif_path,
                        recipe_path=backend_recipe_path,
                        auto_fetch=True,
                        base_image=backend_base_image,
                        profile=profile,
                        instance_name=backend_instance_name,
                        extra_run_args=backend_extra_run_args,
                    )
                    self.base_url = f"http://localhost:{backend_port}"
                    print(f"[osrm] Local Singularity backend started at {self.base_url}")
                else:
                    print(f"[osrm] Unsupported backend_runtime: {backend_runtime}")
                    self.base_url = base_url
            except Exception as exc:
                print(
                    f"[osrm] Failed to auto-start local backend: {exc}. Falling back to provided base_url."
                )
                self.base_url = base_url
        else:
            self.base_url = base_url

    def _get_directions_url(self, origin, destination):
        """
        Helper function for getting the URL for a directions request (To request a route
        between the given origin and destination coordinates).
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
        Helper function for getting the URL for a distance matrix request.
        Generates the URL to request a distance matrix between the given lists of
        origins and destinations coordinates.
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
        Helper function for parsing the distance matrix response.
        Parses the response from the distance matrix API and returns a dataframe of
        durations and distances.
        """
        durations = json_data["durations"]
        distances = json_data["distances"]

        # flatten the list
        durations = [item for sublist in durations for item in sublist]
        distances = [item for sublist in distances for item in sublist]

        # combine the dutation and destinations list to a dataframe
        # print(len(durations), len(distances))
        df = pd.DataFrame({"distance (m)": distances, "duration (s)": durations})

        return df

    def get_route(self, origin, destination):
        """
        This method returns a Route object contains duration and disatnce for the route between the given origin and destination coordinates.
        The origin and destination parameters are lists of latitude and longitude coordinates.
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
        route = Route(OSRMRoute(route), origin, destination)
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
        # check if the origins and destinations are numpy arrays
        # if so, convert them to lists

        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        url = self._get_matrix_distance_url(origins, destinations)
        res = super()._get_request(url)
        distance_matrix = self._parse_distance_matrix(res)
        if append_od:
            od_matrix = super()._get_OD_matrix(origins, destinations)
            distance_matrix = pd.concat([od_matrix, distance_matrix], axis=1)

        return distance_matrix

    def get_distances_batch(
        self, origins, destinations, append_od=False, use_local_server=False
    ):
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
        if use_local_server:
            df = super().get_distances_batch(
                origins, destinations, max_batch_size=np.infty, append_od=append_od
            )
        else:
            df = super().get_distances_batch(
                origins, destinations, max_batch_size=100, append_od=append_od
            )
        return df
