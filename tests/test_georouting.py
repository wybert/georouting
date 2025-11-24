#!/usr/bin/env python

"""Tests for `georouting` package."""

import os

import pytest
from click.testing import CliRunner
from dotenv import find_dotenv, load_dotenv

from georouting import cli, georouting

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)
google_key = os.environ.get("google_key")
bing_key = os.environ.get("bing_key")
esri_key = os.environ.get("esri_key")
baidu_key = os.environ.get("baidu_key")
tomtom_key = os.environ.get("tomtom_key")
mapbox_key = os.environ.get("mapbox_key")
here_key = os.environ.get("here_key")
ors_key = os.environ.get("ors_key")
run_remote = os.environ.get("RUN_REMOTE_ROUTER_TESTS", "").lower() in ("1", "true", "yes")


import pandas as pd

data = pd.read_csv(
    "https://raw.githubusercontent.com/wybert/georouting/main/docs/data/sample_3.csv",
    index_col=0,
)
one_od_pair = data.iloc[2]

origin = [one_od_pair["ZIP_lat"], one_od_pair["ZIP_lon"]]
destination = [one_od_pair["AHA_ID_lat"], one_od_pair["AHA_ID_lon"]]

origins = data[["ZIP_lat", "ZIP_lon"]].values.tolist()
destinations = data[["AHA_ID_lat", "AHA_ID_lon"]].values.tolist()

# Baidu test coordinates (China: Beijing -> Tianjin)
baidu_origin = [39.9042, 116.4074]  # Beijing
baidu_destination = [39.3434, 117.3616]  # Tianjin
baidu_origins = [[39.9042, 116.4074], [31.2304, 121.4737]]  # Beijing, Shanghai
baidu_destinations = [[39.3434, 117.3616], [30.2741, 120.1551]]  # Tianjin, Hangzhou


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "georouting.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


@pytest.mark.skipif(not google_key, reason="Google API key not set")
def test_google_router():
    """Test google router"""
    from georouting.routers import GoogleRouter

    router = GoogleRouter(google_key, mode="driving")
    # test get_route
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_route_geopandas()
    route.plot_route()

    # test get_distance_matrix
    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)


# def test_bing_router():
#     """Test bing router"""
#     from georouting.routers import BingRouter

#     router = BingRouter(bing_key, mode="driving")
#     # test get_route
#     route = router.get_route(origin, destination)
#     route.get_distance()
#     route.get_route_geopandas()
#     route.plot_route()

#     # test get_distance_matrix
#     router.get_distance_matrix(origins, destinations)
#     router.get_distances_batch(origins, destinations)


def test_osrm_router():
    """Test osrm router"""
    from georouting.routers import OSRMRouter

    router = OSRMRouter(mode="driving")
    # test get_route
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_route_geopandas()
    route.plot_route()

    # test get_distance_matrix
    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)


@pytest.mark.skipif(not esri_key, reason="ESRI API key not set")
def test_esri_router():
    """Test esri router"""
    from georouting.routers import EsriRouter

    router = EsriRouter(esri_key, mode="driving")
    # test get_route
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_route_geopandas()
    route.plot_route()

    # test get_distance_matrix
    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)


@pytest.mark.skipif(not baidu_key, reason="Baidu API key not set")
def test_baidu_router():
    """Test baidu router"""
    from georouting.routers import BaiduRouter

    router = BaiduRouter(baidu_key, mode="driving")
    # test get_route
    route = router.get_route(baidu_origin, baidu_destination)
    route.get_distance()
    route.get_duration()
    route.get_route_geopandas()
    route.plot_route()

    # test get_distance_matrix
    router.get_distance_matrix(baidu_origins, baidu_destinations)
    router.get_distances_batch(baidu_origins, baidu_destinations)


@pytest.mark.skipif(not tomtom_key or not run_remote, reason="TomTom API key not set or remote tests disabled")
def test_tomtom_router():
    """Test tomtom router"""
    from georouting.routers import TomTomRouter

    router = TomTomRouter(tomtom_key, mode="driving")
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_duration()
    route.get_route_geopandas()
    route.plot_route()

    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)


@pytest.mark.skipif(not mapbox_key or not run_remote, reason="Mapbox API key not set or remote tests disabled")
def test_mapbox_router():
    """Test mapbox router"""
    from georouting.routers import MapboxRouter

    router = MapboxRouter(mapbox_key, mode="driving")
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_duration()
    route.get_route_geopandas()
    route.plot_route()

    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)


@pytest.mark.skipif(not here_key or not run_remote, reason="HERE API key not set or remote tests disabled")
def test_here_router():
    """Test HERE router"""
    from georouting.routers import HereRouter

    router = HereRouter(here_key, mode="driving")
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_duration()
    route.get_route_geopandas()
    route.plot_route()

    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)


@pytest.mark.skipif(not ors_key or not run_remote, reason="OpenRouteService API key not set or remote tests disabled")
def test_openrouteservice_router():
    """Test OpenRouteService router"""
    from georouting.routers import ORSRouter

    router = ORSRouter(ors_key, mode="driving")
    route = router.get_route(origin, destination)
    route.get_distance()
    route.get_duration()
    route.get_route_geopandas()
    route.plot_route()

    router.get_distance_matrix(origins, destinations)
    router.get_distances_batch(origins, destinations)
