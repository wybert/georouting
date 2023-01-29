import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
import igraph as ig
import os
# from georouting.routers.base import BaseRouter

class OSMNXRouter(object):

    def __init__(self, mode='drive', area = 'Boston, USA',network_type='drive', engine="networkx", use_cache=True, log_console=False):
        self.mode = mode
        self.area = area
        self.network_type = network_type
        self.engine  = engine
        self.use_cache = use_cache
        self.log_console = log_console
        self.G = self._download_road_network()
        if self.engine == "igraph":
            self.node_dict = self._get_node_dict()
            self.G_ig = self._nx_to_ig(weight="travel_time")

    def _download_road_network(self):
        # Download road network
        # it seems this dosen't work
        ox.settings.log_console=self.log_console
        ox.settings.use_cache=self.use_cache
        ox.settings.cache_folder = os.path.join(os.path.dirname(__file__), 'cache')
        # ox.config(use_cache=self.use_cache, log_console=self.log_console)
        G = ox.graph_from_place(self.area, network_type=self.network_type)
        G = ox.speed.add_edge_speeds(G)
        G = ox.speed.add_edge_travel_times(G)
        return G
    
    def _get_node_dict(self):
        node_dict = dict().fromkeys(list(self.G.nodes))
        [node_dict.update({k:i}) for i,k in enumerate(node_dict)]
        return node_dict

    def _nx_to_ig(self,weight='length'):
    # print(node_dict)
        nodes = [self.node_dict[item] for item in self.G.nodes]
        edges = [(self.node_dict[u],self.node_dict[v]) for u,v in self.G.edges()]
        w = [attr[weight] for u,v,attr in self.G.edges(data=True)]
        G_ig = ig.Graph(directed=True)
        G_ig.add_vertices(nodes)
        G_ig.add_edges(edges)
        G_ig.vs["osmid"] = nodes
        G_ig.es[weight] = w
        return G_ig

    def _get_short_ig(self,source,target,weight):
        sr =self.G_ig.shortest_paths(source=source, 
                                target=target, weights=weight)[0][0]
        return sr



    def get_route_time_distance(self, origins, destinations):
        # switch longitude and latitude
        origin = (origins[1],origins[0])
        destination = (destinations[1],destinations[0])

        # Find the nearest node to origin and destination
        origin_nodes = ox.distance.nearest_nodes(self.G, *origin)
        destination_nodes = ox.distance.nearest_nodes(self.G, *destination)

        if self.engine == "networkx":
        # Find the shortest path use networkx
            routes = ox.shortest_path(self.G, origin_nodes, destination_nodes, weight='travel_time',cpus=None)
        # Get the travel time
            travel_times = [self.G[u][v][0]['travel_time'] for u, v in zip(routes[:-1], routes[1:])]

        elif self.engine == "igraph":
            # find the shortest path use igraph
            pass
            # travel_time = self._get_short_ig(self.node_dict[origin_nodes],self.node_dict[destination_nodes],"travel_time")
        else:
            raise ValueError("engine should be networkx or igraph")
        return travel_time