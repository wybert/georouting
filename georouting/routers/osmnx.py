import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
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
    
    def get_route_time_distance(self, origin, destination):

        # Find the nearest node to origin and destination
        origin_node = ox.distance.nearest_nodes(self.G, *origin)
        destination_node = ox.distance.nearest_nodes(self.G, *destination)

        # Find the shortest path
        route = nx.shortest_path(self.G, origin_node, destination_node, weight='travel_time')

        # Get the travel time
        travel_time = nx.shortest_path_length(self.G, origin_node, destination_node, weight='travel_time')

        return travel_time