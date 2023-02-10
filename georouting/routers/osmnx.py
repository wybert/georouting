import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
import igraph as ig
import os
import warnings
from georouting.routers.base import BaseRouter, Route, OSMNXRoute
import georouting.utils as gtl


class OSMNXRouter(object):
    # FIXME: mode drive should be the same as mode driving
    # FIXME: add igraph support
    # FIXME: can we use networkit
    # FIXME: can we use GPU based network package
    # routing is basically a shortest path problem, it should be any package can solve it
    # How about A* algorithm in datashader
    def __init__(
        self,
        area="Piedmont, California, USA",
        mode="drive",
        engine="networkx",
        use_cache=True,
        log_console=False,
    ):
        self.mode = mode
        self.area = area
        self.engine = engine
        self.use_cache = use_cache
        self.log_console = log_console

        self.G = self._download_road_network()
        if self.engine == "igraph":
            self.node_dict = self._get_node_dict()
            self.G_ig = self._nx_to_ig(weight="travel_time")

    def _download_road_network(self):
        # Download road network
        # it seems this dosen't work
        ox.settings.log_console = self.log_console
        ox.settings.use_cache = self.use_cache
        # ox.settings.cache_folder = os.path.join(os.path.dirname(__file__), "cache")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            G = ox.graph_from_place(self.area, network_type=self.mode)
        G = ox.speed.add_edge_speeds(G)
        G = ox.speed.add_edge_travel_times(G)
        return G

    def _get_node_dict(self):
        # this is a dict to map the node id to the index of the node
        node_dict = dict().fromkeys(list(self.G.nodes))
        [node_dict.update({k: i}) for i, k in enumerate(node_dict)]
        return node_dict

    def _nx_to_ig(self, weight="length"):
        # print(node_dict)
        nodes = [self.node_dict[item] for item in self.G.nodes]
        edges = [(self.node_dict[u], self.node_dict[v]) for u, v in self.G.edges()]
        w = [attr[weight] for u, v, attr in self.G.edges(data=True)]
        G_ig = ig.Graph(directed=True)
        G_ig.add_vertices(nodes)
        G_ig.add_edges(edges)
        G_ig.vs["osmid"] = nodes
        G_ig.es[weight] = w
        return G_ig

    def _get_short_ig(self, source, target, weight):
        sr = self.G_ig.shortest_paths(source=source, target=target, weights=weight)[0][
            0
        ]
        return sr

    def _get_OD_pairs(self, origins, destinations):
        # switch longitude and latitude
        origin_df = pd.DataFrame(origins, columns=["origin_lat", "origin_lon"])
        destination_df = pd.DataFrame(
            destinations, columns=["destination_lat", "destination_lon"]
        )

        origin_df["origin_node"] = ox.distance.nearest_nodes(
            self.G, origin_df["origin_lon"], origin_df["origin_lat"]
        )
        destination_df["destination_node"] = ox.distance.nearest_nodes(
            self.G, destination_df["destination_lon"], destination_df["destination_lat"]
        )

        joint_data = origin_df.merge(destination_df, how="cross")

        return joint_data

    def _parse_distance_matrix(self, routes):
        # Get the distance matrix

        distance_matrix = []
        for r in routes:
            if r is not None:
                route = OSMNXRoute([r, self.G])
                duration = route.get_duration()
                distance = route.get_distance()
            else:
                duration = None
                distance = None
            distance_matrix.append([duration, distance])

        distance_matrix = pd.DataFrame(
            distance_matrix, columns=["duration (s)", "distance (m)"]
        )

        return distance_matrix

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

        #  download the
        # G = self._download_road_network()

        # switch longitude and latitude
        origin = (origin[1], origin[0])
        destination = (destination[1], destination[0])

        # get the nearest network nodes to two lat/lng points with the distance module
        orig = ox.distance.nearest_nodes(self.G, *origin)
        dest = ox.distance.nearest_nodes(self.G, *destination)

        # find the shortest path between nodes, minimizing travel time, then plot it
        route = ox.shortest_path(self.G, orig, dest, weight="travel_time")

        return Route(OSMNXRoute([route, self.G]), origin, destination)

    #         elif self.engine == "igraph":
    #             # find the shortest path use igraph
    #             pass
    #             # travel_time = self._get_short_ig(self.node_dict[origin_nodes],self.node_dict[destination_nodes],"travel_time")
    #         else:
    #             raise ValueError("engine should be networkx or igraph")
    #         return routes

    def get_distance_matrix(self, origins, destinations, append_od=False):
        """
        This method returns a Pandas dataframe representing a distance matrix between the `origins` and `destinations` points. It returns the duration and distance for
        all possible combinations between each origin and each destination. If you want just
        return the duration and distance for specific origin-destination pairs, use the `get_distances_batch` method.

        The origins and destinations parameters are lists of origins and destinations.

        If the `append_od` parameter is set to True, the method also returns a matrix of origin-destination pairs.

        The Bing Maps API has the following limitations for distance matrix requests,
        for more information see [here](https://learn.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-distance-matrix#api-limits):

        - For travel mode driving a distance matrix that has up to 2,500 origins-destinations pairs can be requested for Basic Bing Maps accounts,
        - while for Enterprise Bing Maps accounts the origin-destination pairs limit is 10,000.
        - For travel mode transit and walking, a distance matrix that has up to 650 origins-destinations pairs can be request for all Bing Maps account types.

        Pairs are calculated by multiplying the number of origins, by the number of destinations.
        For example 10,000 origin-destination pairs can be reached if you have: 1 origin, and 10,000 destinations,
        or 100 origins and 100 destinations defined in your request.


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
        """

        # check if the origins and destinations is numpy array
        # if so, convert it to list
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)
        # build OD pairs

        od_pairs_df = self._get_OD_pairs(origins, destinations)

        # print(od_pairs_df)
        origs = od_pairs_df["origin_node"].values.tolist()
        dests = od_pairs_df["destination_node"].values.tolist()
        # print(origs)
        # print(dests)

        routes = ox.shortest_path(self.G, origs, dests, weight="travel_time", cpus=None)

        distance_matrix = self._parse_distance_matrix(routes)

        if append_od:
            distance_matrix = pd.concat([od_pairs_df, distance_matrix], axis=1)
            distance_matrix.drop(
                columns=["origin_node", "destination_node"], inplace=True
            )

        return distance_matrix

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

        # convert the origins and destinations to lists
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)

        # check if the origins and destinations are the same length
        if len(origins) != len(destinations):
            raise ValueError(
                "The origins and destinations should have the same length."
            )

        # build OD pairs

        origins_df = pd.DataFrame(origins, columns=["origin_lat", "origin_lon"])
        destinations_df = pd.DataFrame(destinations, columns=["dest_lat", "dest_lon"])
        # create id column
        origins_df["origin_id"] = origins_df.index
        destinations_df["destination_id"] = destinations_df.index
        od_pairs_df = pd.concat([origins_df, destinations_df], axis=1)
        # print(od_pairs_df)

        # get cross product of origins and destinations
        import numpy as np

        v = np.vstack([origins_df.values, destinations_df.values])
        all_points = pd.DataFrame(v, columns=["lat", "lon", "id"])
        # print(all_points)

        # drop duplicates
        all_points.drop_duplicates(subset=["lat", "lon"], inplace=True)
        # get the nearest nodes for origins and destinations
        # print(all_points)
        all_points["node"] = ox.distance.nearest_nodes(
            self.G, all_points["lon"], all_points["lat"]
        )

        # print(all_points)
        # get the origin nodes
        od_pairs_df["origin_node"] = pd.merge(
            od_pairs_df,
            all_points,
            left_on=["origin_lat", "origin_lon"],
            right_on=["lat", "lon"],
            how="left",
        )["node"]
        # get the destination nodes
        od_pairs_df["destination_node"] = pd.merge(
            od_pairs_df,
            all_points,
            left_on=["dest_lat", "dest_lon"],
            right_on=["lat", "lon"],
            how="left",
        )["node"]

        # print(od_pairs_df)

        # get the shortest path
        routes = ox.shortest_path(
            self.G,
            od_pairs_df["origin_node"].tolist(),
            od_pairs_df["destination_node"].tolist(),
            weight="travel_time",
            cpus=None,
        )

        distance_matrix = self._parse_distance_matrix(routes)

        if append_od:
            distance_matrix = pd.concat([od_pairs_df, distance_matrix], axis=1)
            distance_matrix.drop(
                columns=[
                    "origin_node",
                    "destination_node",
                    "origin_id",
                    "destination_id",
                ],
                inplace=True,
            )

        return distance_matrix
