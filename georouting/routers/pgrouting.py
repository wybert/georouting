import requests
import pandas as pd
import georouting.utils as gtl
from georouting.routers.base import WebRouter, Route, PgroutingRoute
import json
import psycopg2
import warnings

class PgroutingRouter(object):

    def __init__(self, conn, mode="driving"):
        self.conn = conn
        self.mode = mode
        self.SQL_TEMPLATE = """
            CREATE OR REPLACE
            FUNCTION public.boston_nearest_id(geom geometry)
            RETURNS bigint
            AS $$
                SELECT node.id
                FROM ways_vertices_pgr node
                JOIN ways edg
                ON(node.id = edg.source OR    -- Only return node that is
                    node.id = edg.target)      --   an edge source or target.
                WHERE edg.source!=edg.target     -- Drop circular edges.
                ORDER BY node.the_geom <->  $1    -- Find nearest node.
                LIMIT 1;
            $$ LANGUAGE 'sql'
            STABLE
            STRICT
            PARALLEL SAFE;

            CREATE SCHEMA IF NOT EXISTS postgisftw;

            CREATE OR REPLACE
            FUNCTION postgisftw.boston_find_route(
                from_lon FLOAT8 DEFAULT -86.250772,
                from_lat FLOAT8 DEFAULT 33.167195,
                to_lon FLOAT8 DEFAULT -92.11463779,
                to_lat FLOAT8 DEFAULT 32.49945204)
            RETURNS
            TABLE(path_seq integer,
                    edge bigint,
                    cost double precision,
                    agg_cost double precision,
                    geom geometry)
            AS $$
                BEGIN
                RETURN QUERY
                -- Convert the clicks into points
                WITH clicks AS (
                SELECT
                    ST_SetSRID(ST_Point(from_lon, from_lat), 4326) AS start,
                    ST_SetSRID(ST_Point(to_lon, to_lat), 4326) AS stop
                )
                SELECT dijk.path_seq, dijk.edge,
                    dijk.cost, dijk.agg_cost, ways.the_geom AS geom
                FROM ways
                CROSS JOIN clicks
                JOIN pgr_dijkstra(
                    'SELECT gid as id, source, target, cost_s as cost, reverse_cost_s as reverse_cost FROM ways',
                    -- source
                    boston_nearest_id(clicks.start),
                    -- target
                    boston_nearest_id(clicks.stop)
                    ) AS dijk
                    ON ways.gid = dijk.edge;
                END;
            $$ LANGUAGE 'plpgsql'
            STABLE
            STRICT
            PARALLEL SAFE;

            DELETE FROM ways
            WHERE cost_s IS NULL;

            select * from  postgisftw.boston_find_route(%f, %f, %f, %f);
        """
    
    def get_route(self, origin, destination):
        """
        Get a route from origin to destination.
        Parameters
        ----------
        - `origin` : tuple
            The origin point as a tuple of (latitude, longitude).
        - `destination` : tuple
            The destination point as a tuple of (latitude, longitude).
        Returns
        -------
        - `Route` :
            A Route object.
        """

        # switch lat,lon to lon,lat
        origin = (origin[1], origin[0])
        destination = (destination[1], destination[0])

        with warnings.catch_warnings():
            import geopandas as gpd
            warnings.simplefilter("ignore")
            sql = self.SQL_TEMPLATE % (origin[0], origin[1], 
                                       destination[0], destination[1])
            route = gpd.read_postgis(sql, self.conn, geom_col='geom')
            route = Route(PgroutingRoute(route), origin, destination)
        return route 

