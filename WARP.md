# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**georouting** is a Python package that provides a unified API for multiple routing services (Google Maps, Bing Maps, OSRM, ESRI, OSMnx). It enables users to calculate routes, travel distance matrices, and visualize routing results using different routing backends with a consistent interface.

**Status**: Pre-alpha (v0.0.8) - under active development

## Development Commands

### Installation

```bash
# Install from source for development
pip install -e .

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_georouting.py

# Run tests with unittest (alternative)
python -m unittest discover tests/

# Run single test function
python -m pytest tests/test_georouting.py::test_osrm_router
```

### Linting

```bash
# Check code style with flake8
flake8 georouting tests
```

### Documentation

```bash
# Build and serve documentation locally (requires mkdocs)
mkdocs serve

# Build documentation
mkdocs build
```

### Version Management

```bash
# Bump version (uses bump2version)
bump2version patch  # 0.0.8 -> 0.0.9
bump2version minor  # 0.0.8 -> 0.1.0
bump2version major  # 0.0.8 -> 1.0.0
```

## Architecture

### Core Design Pattern

The package uses a **Router Pattern** with service-specific implementations inheriting from base classes:

- **Base classes** (`georouting/routers/base.py`):
  - `WebRouter`: Base class for all web-based routing services
  - `Route`: Wrapper for route objects containing origin, destination, and service-specific route data
  - Service-specific route classes (`GoogleRoute`, `BingRoute`, `OSRMRoute`, etc.): Parse and transform API responses

- **Router implementations** (`georouting/routers/`):
  - `GoogleRouter`: Google Maps API
  - `BingRouter`: Bing Maps API  
  - `OSRMRouter`: Open Source Routing Machine (no API key required)
  - `EsriRouter`: ESRI routing service
  - `OSMNXRouter`: Local routing using OSMnx and OpenStreetMap data
  - `PGRouter`: PostgreSQL/pgRouting (database-based)

- **Unified interface** (`georouting/routers/__init__.py`):
  - `Router` class: Duck-typed wrapper that instantiates the appropriate router based on service name
  - `SERVICE_TO_GEOROUTOR`: Registry mapping service names to router classes
  - `get_georoutor_for_service()`: Factory function for obtaining router instances

### Key Methods

All routers implement three core methods:

1. **`get_route(origin, destination)`**: Returns a `Route` object for a single origin-destination pair
   - `Route.get_distance()`: Distance in meters
   - `Route.get_duration()`: Duration in seconds
   - `Route.get_route_geopandas()`: GeoPandas DataFrame with step-by-step route geometry
   - `Route.plot_route()`: Visualize route on a map

2. **`get_distance_matrix(origins, destinations, append_od=False)`**: Returns a DataFrame with distances/durations for all combinations of origins and destinations

3. **`get_distances_batch(origins, destinations, append_od=False)`**: Returns distances/durations for paired origins and destinations (same length lists)

### Coordinate Format

All coordinates should be provided as iterables with format: `[latitude, longitude]` or `(latitude, longitude)`

### Utilities

- `georouting/utils.py`:
  - `convert_to_list()`: Converts numpy arrays to lists for API compatibility
  - `get_batch_od_pairs()`: Intelligently batches origin-destination pairs to respect API rate limits (e.g., Google's 25x25 limit)

## Adding New Routers

When implementing a new routing service:

1. Create a new file in `georouting/routers/` (e.g., `newservice.py`)
2. Subclass `WebRouter` from `base.py`
3. Implement a service-specific Route class (e.g., `NewServiceRoute`) to parse API responses
4. Implement the three core methods: `get_route()`, `get_distance_matrix()`, `get_distances_batch()`
5. Add the new router to `SERVICE_TO_GEOROUTOR` dictionary in `georouting/routers/__init__.py`
6. Add import statement in `georouting/routers/__init__.py`

## Testing Notes

- Tests require API keys stored in environment variables via `.env` file:
  - `google_key`: Google Maps API key
  - `bing_key`: Bing Maps API key  
  - `esri_key`: ESRI API key
- Most API-dependent tests are commented out to avoid requiring keys in CI/CD
- `test_osrm_router()` runs without API keys (uses public OSRM server)
- Test data is fetched from: `https://raw.githubusercontent.com/wybert/georouting/main/docs/data/sample_3.csv`

## Code Style

- Uses `black` code formatter (see badge in README)
- Flake8 for linting (excludes `docs/` directory)
- Python 3.7+ required (supports 3.7, 3.8, 3.9, 3.10)

## CI/CD

- GitHub Actions workflow: `.github/workflows/build.yml`
- Tests run on: Ubuntu, macOS, Windows
- Python versions tested: 3.7, 3.8, 3.9, 3.10
- Uses `unittest` for CI: `python -m unittest discover tests/`

## Important Constraints

- **API Rate Limits**: Be aware of service-specific limits:
  - Google Maps: Max 25 origins OR 25 destinations, max 100 elements per request
  - Implementation includes automatic batching via `get_batch_od_pairs()` utility

- **Distance/Duration Units**: All methods return:
  - Distance in **meters**
  - Duration in **seconds**

- **CRS**: Geographic outputs use WGS84 (EPSG:4326)
