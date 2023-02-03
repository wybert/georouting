from georouting.routers.google import GoogleRouter
from georouting.routers.osmnx import OSMNXRouter
from georouting.routers.bing import BingRouter
# from georouting.routers.esri import EsriRouter
from georouting.routers.osrm import OSRMRouter

# when adding a new router, add it to the list of routers below
# and add the import statement above
# the key is the name of the service
# the value is the class of the router


SERVICE_TO_GEOROUTOR = {
    "google": GoogleRouter,
    "osmnx": OSMNXRouter,
    "bing": BingRouter,
    # "esri": EsriRouter,
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
