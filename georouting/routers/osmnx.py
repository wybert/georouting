import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
import igraph as ig
import os
import warnings
from georouting.routers.base import BaseRouter, Route, OSMNXRoute


class OSMNXRouter(object):
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

    def get_route_time_distance(self, origins, destinations):
        # switch longitude and latitude
        origin = (origins[1], origins[0])
        destination = (destinations[1], destinations[0])

        # Find the nearest node to origin and destination
        origin_nodes = ox.distance.nearest_nodes(self.G, *origin)
        destination_nodes = ox.distance.nearest_nodes(self.G, *destination)

        if self.engine == "networkx":
            # Find the shortest path use networkx
            routes = ox.shortest_path(
                self.G, origin_nodes, destination_nodes, weight="travel_time", cpus=None
            )
            # Get the travel time
            travel_times = [
                self.G[u][v][0]["travel_time"] for u, v in zip(routes[:-1], routes[1:])
            ]

        elif self.engine == "igraph":
            # find the shortest path use igraph
            pass
            # travel_time = self._get_short_ig(self.node_dict[origin_nodes],self.node_dict[destination_nodes],"travel_time")
        else:
            raise ValueError("engine should be networkx or igraph")
        return travel_time


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

        

        
        return Route(OSMNXRoute([route,self.G]),origin,destination)


#     def get_route(self, origin, destination):
# #    这里的route是什么呢？🤔，他应该有几个属性
# #    一个是有durations，一个是有sitances。然后还能进行路径的绘图，可以进行路径的可视化
# #   这个其实可以从已有的代码进行抽取，然后进行修改
# # 这里的测试的代码在实验室的电脑上
#         # switch longitude and latitude
#         origin = (origins[1], origins[0])
#         destination = (destinations[1], destinations[0])

#         # Find the nearest node to origin and destination
#         origin_nodes = ox.distance.nearest_nodes(self.G, *origin)
#         destination_nodes = ox.distance.nearest_nodes(self.G, *destination)

#         if self.engine == "networkx":
#             # Find the shortest path use networkx
#             routes = ox.shortest_path(
#                 self.G, origin_nodes, destination_nodes, weight="travel_time", cpus=None
#             )
#             # Get the travel time
#             travel_times = [
#                 self.G[u][v][0]["travel_time"] for u, v in zip(routes[:-1], routes[1:])
#             ]

#         elif self.engine == "igraph":
#             # find the shortest path use igraph
#             pass
#             # travel_time = self._get_short_ig(self.node_dict[origin_nodes],self.node_dict[destination_nodes],"travel_time")
#         else:
#             raise ValueError("engine should be networkx or igraph")
#         return routes
    

    # def get_distance_matrix(self, origins, destinations,append_od=False):
    #     # switch longitude and latitude
    #     origin = (origins[1], origins[0])
    #     destination = (destinations[1], destinations[0])

    #     # Find the nearest node to origin and destination
    #     origin_nodes = ox.distance.nearest_nodes(self.G, *origin)
    #     destination_nodes = ox.distance.nearest_nodes(self.G, *destination)

    #     if self.engine == "networkx":
    #         # Find the shortest path use networkx
    #         routes = ox.shortest_path(
    #             self.G, origin_nodes, destination_nodes, weight="travel_time", cpus=None
    #         )
    #         # Get the travel time
    #         travel_times = [
    #             self.G[u][v][0]["travel_time"] for u, v in zip(routes[:-1], routes[1:])
    #         ]

    #     elif self.engine == "igraph":
    #         # find the shortest path use igraph
    #         pass
    #         # travel_time = self._get_short_ig(self.node_dict[origin_nodes],self.node_dict[destination_nodes],"travel_time")
    #     else:
    #         raise ValueError("engine should be networkx or igraph")
    #     return travel_time

    # def get_distances_batch(self,origins,destinations,append_od=False):

    #     return None

