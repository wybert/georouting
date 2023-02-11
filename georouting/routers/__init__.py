from georouting.routers.google import GoogleRouter
from georouting.routers.osmnx import OSMNXRouter
from georouting.routers.bing import BingRouter

from georouting.routers.esri import EsriRouter
from georouting.routers.osrm import OSRMRouter

# when adding a new router, add it to the list of routers below
# and add the import statement above
# the key is the name of the service
# the value is the class of the router


SERVICE_TO_GEOROUTOR = {
    "google": GoogleRouter,
    "osmnx": OSMNXRouter,
    "bing": BingRouter,
    "esri": EsriRouter,
    "osrm": OSRMRouter,
}


def get_georoutor_for_service(service):
    """Returns a georoutor for the given service.

    Args:
        service (str): The service to use for georouting.

    Returns:
        A georoutor for the given service.

    """
    try:
        return SERVICE_TO_GEOROUTOR[service]
    except KeyError as exc:
        raise ValueError(f"Unknown service: {service}") from exc


# define the Router class use duck typing

class Router:
    """
    Router class.

    """
    def __init__(self, router, api_key=None, area = "Cambridge, Massachusetts, USA", mode="driving", timeout=10, language="en"):

        self.router = router
        self.api_key = api_key
        self.area = area
        self.mode = mode
        self.timeout = timeout
        self.language = language

        if self.router == "osrm":
            self.router = OSRMRouter(mode = self.mode, timeout = self.timeout,language= self.language)
        elif self.router == "google":
            self.router = GoogleRouter(api_key = self.api_key,mode= self.mode, timeout = self.timeout, language = self.language)
        elif self.router == "bing":
            self.router = BingRouter(api_key = self.api_key,mode= self.mode, timeout = self.timeout, language = self.language)
        elif self.router == "esri":
            self.router = EsriRouter(api_key = self.api_key,mode= self.mode, timeout = self.timeout, language = self.language)
        elif self.router == "osmnx":
            self.router = OSMNXRouter(area = self.area, mode = self.mode, timeout = self.timeout,  language =self.language)
        else:
            raise ValueError("Router not supported.")

    def available_routers(self):
        """
        Returns a list of available routers.
        """
        return SERVICE_TO_GEOROUTOR.keys()

    def get_route(self, origin, destination):
        """
        Returns a route object.
        """
        return self.router.get_route(origin, destination)

    def get_distance_matrix(self, origins, destinations, append_od=False, **kwargs):
        """
        Returns a distance matrix.
        """
        return self.router.get_distance_matrix(origins, destinations, append_od, **kwargs)

    def get_distances_batch(self, origins, destinations,append_od=False):
        """
        Returns a list of distances.
        """
        return self.router.get_distances_batch(origins, destinations,append_od=False)

    