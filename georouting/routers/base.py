
# -*- coding: utf-8 -*-

import geopandas as gpd
import polyline
import pandas as pd
import shapely.geometry as sg
import numpy as np
from shapely.geometry import LineString
import requests
import json

class GoogleRoute:
    """ Google route class. 
    """

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route[0]['legs'][0]['duration']['value']

    def get_distance(self):
        return self.route[0]['legs'][0]['distance']['value']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):

        """
        
        """

        steps_google = self.route[0]['legs'][0]['steps']

        google_route1 = []
        for step in steps_google:
            step_g = {}
            step_g["distance (m)"] = step["distance"]["value"]
            step_g["duration (s)"] = step["duration"]["value"]
            step_g["geometry"] = polyline.decode(step['polyline']["points"], 5,
                        geojson=True
                        )
            step_g["geometry"] = LineString(step_g["geometry"])
            google_route1.append(step_g)
        google_route1 = gpd.GeoDataFrame(google_route1,geometry="geometry",crs = "4326")
        google_route1["speed (m/s)"] = google_route1["distance (m)"] /  google_route1["duration (s)"]  
        return google_route1


class BingRoute:
    def __init__(self, route):
        self.route = route

    def get_duration(self):
        " get the duration in seconds"
        durationUnit = self.route['resourceSets'][0]["resources"][0]["durationUnit"]
        travelDuration = self.route['resourceSets'][0]["resources"][0]["travelDuration"]
        
        
        if durationUnit == "Second":
            return travelDuration
        elif durationUnit == "Minute":
            return travelDuration * 60
        elif durationUnit == "Hour":
            return travelDuration * 3600
        else:
            raise ValueError("durationUnit is not recognized")

    def get_distance(self):
        " get the distance in meters"
        distanceUnit = self.route['resourceSets'][0]["resources"][0]["distanceUnit"]
        travelDistance = self.route['resourceSets'][0]["resources"][0]["travelDistance"]
        if distanceUnit in ["mi","Mile"]:
            travelDistance = travelDistance * 1609.344
        elif distanceUnit in ["km","Kilometer"]:
            travelDistance = travelDistance * 1000
        return travelDistance

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        
        durations = [item['travelDuration'] for item in self.route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']]
        distances = [item['travelDistance'] for item in self.route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']]
        endPathIndices = [item['details'][0]['endPathIndices'][0] for item in self.route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']]
        startPathIndices = [item['details'][0]['startPathIndices'][0] for item in self.route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']]
        points = self.route['resourceSets'][0]['resources'][0]['routePath']['line']['coordinates']

        lines = []
        for start,end in zip(startPathIndices,endPathIndices):
            points_ = points[start:end]
            # change the lon lat to lat lon
            points_ = np.array(points_)
            # print(points_.shape)
            if points_.shape[0] > 1:
                points_ = points_[:,::-1]
            else:
                points_ = []
            lines.append(sg.LineString(points_))

        df = pd.DataFrame({'distance (m)':distances,'duration (s)':durations,'geometry':lines})
        gdf = gpd.GeoDataFrame(df,geometry='geometry',crs="EPSG:4326")
        gdf['speed (m/s)'] = gdf['distance (m)'] / gdf['duration (s)']

        return gdf

class OSRMRoute:

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route['routes'][0]['duration']

    def get_distance(self):
        return self.route['routes'][0]['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        
        steps = []
        for step in self.route["routes"][0]["legs"][0]["steps"]:
            temp = {}
            temp["geometry"] = gpd.read_file(json.dumps(step["geometry"]))["geometry"].values[0]
            temp["duration (s)"]= step["duration"]
            temp["distance (m)"] = step["distance"]
            steps.append(temp)
        steps = pd.DataFrame(steps)
        # steps["geometry"] = steps["geometry"].map(gpd.read_file)
        steps = gpd.GeoDataFrame(steps,geometry = "geometry",crs="4326")
        steps["speed (m/s)"] = steps["distance (m)"] / steps["duration (s)"]
        return steps

class EsriRoute:

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route['routes']['features'][0]['attributes']['Total_TravelTime']

    def get_distance(self):
        return self.route['routes']['features'][0]['attributes']['Total_Miles'] * 1609.344

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class MapboxRoute:

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route['routes'][0]['duration']

    def get_distance(self):
        return self.route['routes'][0]['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class HereRoute:

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route['response']['route'][0]['summary']['travelTime']

    def get_distance(self):
        return self.route['response']['route'][0]['summary']['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class MapQuestRoute:

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route['route']['time']

    def get_distance(self):
        return self.route['route']['distance']

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError

class Route(object):
    def __init__(self, route):
        self.route = route
# FIXME: may need rename it as get_duration
    def get_duration(self):
        return self.route.get_duration()

# FIXME: may need rename it as get_distance
    def get_distance(self):
        return self.route.get_distance()

    def get_route(self):
        return self.route.get_route()

    def get_route_geopandas(self):
        return self.route.get_route_geopandas()


# base class for routers
class BaseRouter(object):
    def __init__(self, mode="driving"):
        self.mode = mode
    
    def _get_OD_matrix(self, origins, destinations):

        items = []
        for i in origins:
            for j in destinations:
                item = i + j
                items.append(item)
        od_matrix = pd.DataFrame(items, columns=["orgin_lat",
        "orgin_lon","destination_lat","destination_lon"])

        return od_matrix
        

#   FIXME: if it can return the object which enable to do the further analysis, and this object 
#   can have several methods to get the information, like time, distance, route, etc.
    def get_route(self, origin, destination):
        
        return Route(self._get_request(origin, destination))

    # def get_route_matrix(self, origins, destinations):
        
    #     return RouteMatrix(self._get_request(origins, destinations))

    # def get_route_time_distance(self, origin, destination):
    #     raise NotImplementedError

    # def get_route_time_distance_matrix(self, origins, destinations):
    #     raise NotImplementedError

    # def get_route_geopandas(self, origin, destination):
    #     raise NotImplementedError

    # def get_route_geopandas_matrix(self, origins, destinations):
    #     raise NotImplementedError

class WebRouter(BaseRouter):
    def __init__(self, api_key, mode="driving", timeout=10, language="en",base_url=None):
        self.api_key = api_key
        self.timeout = timeout
        self.language = language
        super().__init__(mode=mode)

    def _get_request(self,url):
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)

        return response.json()

# make a class for local router 
class LocalRouter(BaseRouter):
    def __init__(self, mode="driving"):
        self.mode = mode

    def get_route_time_distance(self, origin, destination):
        raise NotImplementedError

    def get_route_time_distance_matrix(self, origins, destinations):
        raise NotImplementedError

    def get_route_geopandas(self, origin, destination):
        raise NotImplementedError

    def get_route_geopandas_matrix(self, origins, destinations):
        raise NotImplementedError