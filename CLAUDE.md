# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

georouting is a Python routing library providing a unified API across multiple routing services (Google Maps, Bing Maps, OSRM, ESRI, OSMnx, pgRouting). Pre-alpha (v0.0.8) - API may change before v1.0.0.

## Development Commands

```bash
# Install for development
pip install -e . && pip install -r requirements_dev.txt

# Run all tests
python -m pytest tests/

# Run single test
python -m pytest tests/test_georouting.py::test_osrm_router -v

# Lint
flake8 georouting tests

# Serve docs locally
mkdocs serve

# Version bump (uses bump2version)
bump2version patch|minor|major

# Build & publish
python setup.py sdist bdist_wheel && twine upload dist/*
```

## Architecture

### Design Pattern: Router Pattern with Service Registry

```
georouting/routers/
├── __init__.py      # Service registry (SERVICE_TO_GEOROUTOR) & unified Router class
├── base.py          # BaseRouter, WebRouter, LocalRouter, Route wrapper
├── google.py        # GoogleRouter
├── bing.py          # BingRouter
├── osrm.py          # OSRMRouter (no API key needed)
├── esri.py          # EsriRouter
├── osmnx.py         # OSMNXRouter (local routing)
├── pgrouting.py     # PGRouter (PostgreSQL)
└── baidu.py         # BaiduRouter
```

### Class Hierarchy

- **BaseRouter** (abstract): Common utilities, batching logic for API limits
  - **WebRouter**: For web-based services (handles API requests)
  - **LocalRouter**: For local routing (OSMnx, pgRouting)
- **Route**: Unified wrapper delegating to service-specific route classes (GoogleRoute, BingRoute, etc.)

### Common Interface (All Routers)

```python
router.get_route(origin, destination)  # Returns Route object
router.get_distance_matrix(origins, destinations)  # Returns DataFrame (all combinations)
router.get_distances_batch(origins, destinations)  # Returns DataFrame (paired lists)
```

### Service Registry

```python
SERVICE_TO_GEOROUTOR = {
    "google": GoogleRouter,
    "osmnx": OSMNXRouter,
    "bing": BingRouter,
    "esri": EsriRouter,
    "osrm": OSRMRouter,
}
```

Use via: `Router(router="osrm", mode="driving")`

## Standards

- **Coordinates**: `[latitude, longitude]` (WGS84/EPSG:4326)
- **Distance**: Meters
- **Duration**: Seconds
- **API limits**: Google Maps max 25x25, automatic batching via `get_batch_od_pairs()`

## Testing

- API keys set in `.env`: `google_key`, `bing_key`, `esri_key`
- OSRM tests work without keys (public API at http://router.project-osrm.org)
- Most API-key tests are commented out in CI

## Adding New Routers

1. Create `georouting/routers/newservice.py`
2. Implement `NewServiceRoute` class with: `get_duration()`, `get_distance()`, `get_route()`, `get_route_geopandas()`
3. Implement `NewServiceRouter(WebRouter)` with: `get_route()`, `get_distance_matrix()`, `get_distances_batch()`
4. Register in `SERVICE_TO_GEOROUTOR` in `georouting/routers/__init__.py`
5. Add tests in `tests/test_georouting.py`
