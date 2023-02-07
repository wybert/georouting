# -*- coding: utf-8 -*-

import geopandas as gpd
import polyline
import pandas as pd
import shapely.geometry as sg
from shapely.geometry import LineString
import numpy as np
import requests
import json
import georouting.utils as gtl
import folium

class GoogleRoute:
    """
    The class "GoogleRoute" which allows to retrieve information from a route provided as an argument.

    The class has the following methods:

    - `get_duration()`: Returns the duration of the route in seconds.

    - `get_distance()`: Returns the distance of the route in meters.

    - `get_route()`: Returns the complete route information.

    - `get_route_geopandas()`: Returns a GeoDataFrame with information such as distance, duration, and speed of each step in the route.

    It is assumed that the polyline module is used for decoding the polyline into a LineString geometry. The GeoDataFrame is created with a specified coordinate reference system (CRS) of "4326".
    """

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        """
        Returns the duration of the route in seconds.

        """
        return self.route[0]["legs"][0]["duration"]["value"]

    def get_distance(self):
        """
        Returns the distance of the route in meters.
        """
        return self.route[0]["legs"][0]["distance"]["value"]

    def get_route(self):
        """
        Returns the complete route information.
        """
        return self.route

    def get_route_geopandas(self):
        """
        Returns a GeoDataFrame with information such as distance, duration, and speed of each step in the route. It is assumed that the polyline module is used for decoding the polyline into a LineString geometry. The GeoDataFrame is created with a specified coordinate reference system (CRS) of "4326".

        """

        steps_google = self.route[0]["legs"][0]["steps"]

        google_route1 = []
        for step in steps_google:
            step_g = {}
            step_g["distance (m)"] = step["distance"]["value"]
            step_g["duration (s)"] = step["duration"]["value"]
            step_g["geometry"] = polyline.decode(
                step["polyline"]["points"], 5, geojson=True
            )
            step_g["geometry"] = LineString(step_g["geometry"])
            google_route1.append(step_g)
        google_route1 = gpd.GeoDataFrame(google_route1, geometry="geometry", crs="4326")
        google_route1["speed (m/s)"] = (
            google_route1["distance (m)"] / google_route1["duration (s)"]
        )
        return google_route1


class BingRoute:
    """
    BingRoute class that allows you to extract various information from a route stored in a dictionary. It has the following functions:

    - `get_duration()`: Returns the travel duration in seconds.
    - `get_distance()`: Returns the travel distance in meters.
    - `get_route()`: Returns the entire route in a dictionary.
    - `get_route_geopandas()`: Returns the route information in a GeoPandas dataframe.

    This function extracts the duration and distance information for each leg of the route, creates a list of shapely LineStrings representing the route, and then creates a GeoDataFrame with columns for the duration, distance, and geometry. Additionally, it calculates the speed in meters per second for each leg.

    The class is designed to work with data returned by the Bing Maps REST Services API, as the data is stored in a dictionary with a specific structure.
    """

    def __init__(self, route):
        self.route = route

    # change the duration to seconds
    def _duration_to_seconds(self, duration):
        """
        change the duration to seconds
        """

        durationUnit = self.route["resourceSets"][0]["resources"][0]["durationUnit"]

        if durationUnit == "Second":
            return duration
        elif durationUnit == "Minute":
            return duration * 60
        elif durationUnit == "Hour":
            return duration * 3600
        else:
            raise ValueError("durationUnit is not recognized")

    # change the distance to meters
    def _distance_to_meters(self, distance):
        """
        change the distance to meters
        """
        distanceUnit = self.route["resourceSets"][0]["resources"][0]["distanceUnit"]
        if distanceUnit in ["mi", "Mile"]:
            distance = distance * 1609.344
        elif distanceUnit in ["km", "Kilometer"]:
            distance = distance * 1000
        return distance

    def get_duration(self):
        "get the travel duration in seconds"
        # durationUnit = self.route["resourceSets"][0]["resources"][0]["durationUnit"]
        travelDuration = self.route["resourceSets"][0]["resources"][0]["travelDuration"]

        return self._duration_to_seconds(travelDuration)

    def get_distance(self):
        "get the travel distance in meters"
        # distanceUnit = self.route["resourceSets"][0]["resources"][0]["distanceUnit"]
        travelDistance = self.route["resourceSets"][0]["resources"][0]["travelDistance"]

        return self._distance_to_meters(travelDistance)

    def get_route(self):
        "get the entire route in a dictionary"
        return self.route

    def get_route_geopandas(self):
        """
        This function extracts the duration and distance information for each leg of the route, creates a list of shapely LineStrings representing the route, and then creates a GeoDataFrame with columns for the duration, distance, and geometry. Additionally, it calculates the speed in meters per second for each leg.

        Returns the route information in a GeoPandas dataframe.

        """
        durations = [
            item["travelDuration"]
            for item in self.route["resourceSets"][0]["resources"][0]["routeLegs"][0][
                "itineraryItems"
            ]
        ]
        # change the duration to seconds
        durations = [self._duration_to_seconds(duration) for duration in durations]

        distances = [
            item["travelDistance"]
            for item in self.route["resourceSets"][0]["resources"][0]["routeLegs"][0][
                "itineraryItems"
            ]
        ]
        # change the distance to meters
        distances = [self._distance_to_meters(distance) for distance in distances]

        startPathIndices = []
        endPathIndices = []
        for item in self.route["resourceSets"][0]["resources"][0]["routeLegs"][0][
            "itineraryItems"
        ]:
            temp = []
            for detail in item["details"]:
                temp.append(detail["startPathIndices"][0])
                temp.append(detail["endPathIndices"][0])
            startPathIndices.append(min(temp))
            endPathIndices.append(max(temp))

        points = self.route["resourceSets"][0]["resources"][0]["routePath"]["line"][
            "coordinates"
        ]

        lines = []
        for start, end in zip(startPathIndices, endPathIndices):
            line_string = points[start : end + 1]
            # change the lon lat to lat lon
            line_string = [(point[1], point[0]) for point in line_string]

            # if the line string is just one point, return linestring with two same points
            if len(line_string) == 1:
                line_string = sg.LineString([line_string[0], line_string[0]])
            else:
                line_string = sg.LineString(line_string)
            lines.append(line_string)
            # # print(line_string)
            # # print(len(line_string))
            # try:
            #     lines.append(sg.LineString(line_string))
            # except:
            #     print(line_string)
            #     print(len(line_string))

        df = pd.DataFrame(
            {"distance (m)": distances, "duration (s)": durations, "geometry": lines}
        )
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
        gdf["speed (m/s)"] = gdf["distance (m)"] / gdf["duration (s)"]

        return gdf


class OSRMRoute:

    """
    This class represents a route returned by the OpenStreetMap Routing Machine API.

    Methods:
    - `get_duration()` -> float: Returns the duration of the route in seconds.
    - `get_distance()` -> float: Returns the distance of the route in meters.
    - `get_route()` -> dict: Returns the full route as a dictionary.
    - `get_route_geopandas()` -> geopandas.GeoDataFrame: Returns the route as a GeoDataFrame. The GeoDataFrame contains columns for 'duration (s)', 'distance (m)', 'geometry', and 'speed (m/s)'.
    """

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        """
        Get the duration of the route in seconds.
        """
        return self.route["routes"][0]["duration"]

    def get_distance(self):
        """
        Get the distance of the route in meters.
        """
        return self.route["routes"][0]["distance"]

    def get_route(self):
        """
        Get the full route information as a dictionary.
        """
        return self.route

    def get_route_geopandas(self):
        """
        Get the route as a GeoDataFrame. The GeoDataFrame contains columns for 'duration (s)', 'distance (m)', 'geometry', and 'speed (m/s)'.
        """

        steps = []
        for step in self.route["routes"][0]["legs"][0]["steps"]:
            temp = {}
            temp["geometry"] = gpd.read_file(json.dumps(step["geometry"]))[
                "geometry"
            ].values[0]
            temp["duration (s)"] = step["duration"]
            temp["distance (m)"] = step["distance"]
            steps.append(temp)
        steps = pd.DataFrame(steps)
        # steps["geometry"] = steps["geometry"].map(gpd.read_file)
        steps = gpd.GeoDataFrame(steps, geometry="geometry", crs="4326")
        steps["speed (m/s)"] = steps["distance (m)"] / steps["duration (s)"]
        return steps


class EsriRoute:
    """
    The EsriRoute class is a class for handling a route obtained from the Esri ArcGIS routing service.

    The class has the following methods:

    get_duration: returns the total travel time of the route.

    get_distance: returns the total distance of the route in meters.

    get_route: returns the entire route as a dictionary.

    get_route_geopandas: raises a NotImplementedError. This method is not yet implemented and will be added in the future.


    """

    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route["routes"]["features"][0]["attributes"]["Total_TravelTime"]

    def get_distance(self):
        return (
            self.route["routes"]["features"][0]["attributes"]["Total_Miles"] * 1609.344
        )

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class MapboxRoute:
    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route["routes"][0]["duration"]

    def get_distance(self):
        return self.route["routes"][0]["distance"]

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class HereRoute:
    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route["response"]["route"][0]["summary"]["travelTime"]

    def get_distance(self):
        return self.route["response"]["route"][0]["summary"]["distance"]

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class MapQuestRoute:
    def __init__(self, route):
        self.route = route

    def get_duration(self):
        return self.route["route"]["time"]

    def get_distance(self):
        return self.route["route"]["distance"]

    def get_route(self):
        return self.route

    def get_route_geopandas(self):
        raise NotImplementedError


class Route(object):
    """
    A wrapper class that wraps different routing engines' route objects.

    It will return a Route object that can be used to get the duration, distance, and route information.

    The class has the following methods:

    - `get_duration()`: Returns the duration of the route in seconds.

    - `get_distance()`: Returns the distance of the route in meters.

    - `get_route()`: Returns the complete route information.

    - `get_route_geopandas()`: Returns a GeoDataFrame with information such as distance, duration, and speed of each step in the route.

    """

    def __init__(self, route,origin, destination):
        """
        Initialize a Route object by passing the routing engine's route object.

        :param route: An instance of a routing engine's route object
        """
        self.route = route
        self.origin = origin
        self.destination = destination

    def get_duration(self):
        """
        Get the duration of the route.
        """
        return self.route.get_duration()

    def get_distance(self):
        """
        Get the distance of the route.
        """
        return self.route.get_distance()

    def get_route(self):
        """
        Get the raw route information.
        """
        return self.route.get_route()

    def get_route_geopandas(self):
        """
        Get the route information as a GeoDataFrame.
        """
        return self.route.get_route_geopandas()
    def plot_route(self):
        """
        Plot the route on a map.
        """
        gdf = self.get_route_geopandas()
        m = gdf.explore(column="speed (m/s)",style_kwds={"weight":11,"opacity":0.8})
        # add a red destination marker, don't show i in the map
        folium.Marker([self.destination[0],self.destination[1]],
        icon=folium.Icon(color="red",icon_color="white",icon="circle", prefix="fa")
            ).add_to(m)

        # folium.Marker([one_od_pair["AHA_ID_lat"],one_od_pair["AHA_ID_lon"]],
        # icon=folium.Icon(color="red",icon_color="white",icon="circle", prefix="fa")).add_to(m)

        return m


# base class for routers
class BaseRouter(object):

    """
    The class BaseRouter serves as a base class for routers, which are used to compute the optimal route between two points. The class has an instance variable mode, which is a string that defines the mode of transportation (e.g. "driving").

    The BaseRouter class has a single method _get_OD_matrix, which takes two arguments origins and destinations and returns an origin-destination matrix. The method creates an empty list items and loops through each origin and destination pair, appending the concatenated origin and destination to the list. The origin-destination matrix is then created from the list items and returned.
    """

    def __init__(self, mode="driving"):
        self.mode = mode

    def _get_OD_matrix(self, origins, destinations):
        items = []
        for i in origins:
            for j in destinations:
                item = i + j
                items.append(item)
        od_matrix = pd.DataFrame(
            items,
            columns=["orgin_lat", "orgin_lon", "destination_lat", "destination_lon"],
        )

        return od_matrix

    def get_route(self, origin, destination):
        return Route(self._get_request(origin, destination))

    def get_distances_batch(self, origins, destinations, max_batch_size=25, append_od=False):
        """
        This method returns a Pandas dataframe contains duration and disatnce for all the `origins` and `destinations` pairs. Use this function if you don't want to get duration and distance for all possible combinations between each origin and each destination. 
        
        The origins and destinations parameters are lists of origin-destination pairs. They should be the same length.

        If the `append_od` parameter is set to True, the method also returns the input origin-destination pairs.
        """

        # convert the origins and destinations to lists
        origins = gtl.convert_to_list(origins)
        destinations = gtl.convert_to_list(destinations)
        
        # check if the origins and destinations are the same length
        if len(origins) != len(destinations):
            raise ValueError("The origins and destinations should have the same length.")
        
        # divide the origins and destinations into batches

        batches = gtl.get_batch_od_pairs(origins, destinations, max_batch_size)

        # get the distance matrix for each batch 
        results = []
        for batch in batches:
            res = self.get_distance_matrix(batch[0], batch[1])
            results.append(res)
        
        # concatenate the results
        df = pd.concat(results, axis=0)
        # revert the order of the rows
        df = df.iloc[::-1]

        if append_od:
            # convert the origins and destinations to numpy arrays
            origins = np.array(origins)
            destinations = np.array(destinations)
            df["origin_lat"] = origins[:,0]
            df["origin_lon"] = origins[:,1]
            df["destination_lat"] = destinations[:,0]
            df["destination_lon"] = destinations[:,1]  

            df = df[["origin_lat", "origin_lon", "destination_lat", "destination_lon", 
            "distance (m)", "duration (s)"]] 
        
        return df


# add documenation for the class
class WebRouter(BaseRouter):
    """
    The WebRouter class is a class for handling a route obtained from a web-based routing service.

    """

    def __init__(
        self, api_key, mode="driving", timeout=10, language="en", base_url=None
    ):
        self.api_key = api_key
        self.timeout = timeout
        self.language = language
        super().__init__(mode=mode)

    def _get_request(self, url):
        """
        Helper function to make a request to the web-based routing service.
        """

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)

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
