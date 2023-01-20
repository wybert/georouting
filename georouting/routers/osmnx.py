import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
import igraph as ig
# from georouting.routers.base import BaseRouter

class OSMNXRouter(object):

    def __init__(self, mode='drive', area = 'Boston, USA',network_type='drive', engine="networkx"):
        self.mode = mode
        self.area = area
        self.network_type = network_type
        self.engine  = engine
        self.G = self._download_road_network()

    def _download_road_network(self):
        # Download road network
        G = ox.graph_from_place(self.area, network_type=self.network_type)
        G = ox.speed.add_edge_speeds(G)
        G = ox.speed.add_edge_travel_times(G)
        return G
    
    def _get_node_dict(self):
        node_dict = dict().fromkeys(list(self.G.nodes))
        [node_dict.update({k:i}) for i,k in enumerate(node_dict)]
        return node_dict

    def _nx_to_ig(self,node_dict,weight='length'):
    # print(node_dict)
        nodes = [node_dict[item] for item in self.G.nodes]
        edges = [(node_dict[u],node_dict[v]) for u,v in self.G.edges()]
        w = [attr[weight] for u,v,attr in self.G.edges(data=True)]
        G_ig = ig.Graph(directed=True)
        G_ig.add_vertices(nodes)
        G_ig.add_edges(edges)
        G_ig.vs["osmid"] = nodes
        G_ig.es[weight] = w
        return G_ig

    def _get_short_ig(self,G_ig,source,target,weight):
        sr =G_ig.shortest_paths(source=source, 
                                target=target, weights=weight)[0][0]
        return sr



    def get_route_time_distance(self, origin, destination):

        # Find the nearest node to origin and destination
        origin_node = ox.distance.nearest_nodes(self.G, *origin)
        destination_node = ox.distance.nearest_nodes(self.G, *destination)

        if self.engine == "networkx":
        # Find the shortest path use networkx
        # route = nx.shortest_path(self.G, origin_node, destination_node, weight='travel_time')
        # Get the travel time
            travel_time = nx.shortest_path_length(self.G, origin_node, destination_node, weight='travel_time')

        elif self.engine == "igraph":
            # find the shortest path use igraph
            
            node_dict = self._get_node_dict()
            G_ig = self._nx_to_ig(node_dict,weight="travel_time")

            travel_time = self._get_short_ig(G_ig, node_dict[origin_node],node_dict[destination_node],"travel_time")
        else:
            raise ValueError("engine should be networkx or igraph")
        return travel_time