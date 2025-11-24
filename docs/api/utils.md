# Table of Contents

* [georouting.utils](#georouting.utils)
  * [convert\_to\_list](#georouting.utils.convert_to_list)
  * [get\_batch\_od\_pairs](#georouting.utils.get_batch_od_pairs)
  * [build\_geofabrik\_region\_index](#georouting.utils.build_geofabrik_region_index)
  * [build\_geofabrik\_catalog](#georouting.utils.build_geofabrik_catalog)
  * [resolve\_geofabrik\_pbf](#georouting.utils.resolve_geofabrik_pbf)
  * [render\_osrm\_dockerfile](#georouting.utils.render_osrm_dockerfile)
  * [write\_osrm\_dockerfile](#georouting.utils.write_osrm_dockerfile)
  * [build\_osrm\_image](#georouting.utils.build_osrm_image)
  * [run\_osrm\_container](#georouting.utils.run_osrm_container)
  * [build\_and\_run\_osrm](#georouting.utils.build_and_run_osrm)

<a id="georouting.utils"></a>

# georouting.utils

<a id="georouting.utils.convert_to_list"></a>

#### convert\_to\_list

```python
def convert_to_list(data)
```

This function converts the data to a list.

<a id="georouting.utils.get_batch_od_pairs"></a>

#### get\_batch\_od\_pairs

```python
def get_batch_od_pairs(orgins, destinations, max_batch_size=25)
```

This function returns a list of dataframes containing the origin-destination pairs to
avoid the repeated requests to the travel distance API.

<a id="georouting.utils.build_geofabrik_region_index"></a>

#### build\_geofabrik\_region\_index

```python
def build_geofabrik_region_index(cache_path=DEFAULT_GEOFABRIK_CACHE,
                                 refresh=False,
                                 include_sizes=False,
                                 regions=None,
                                 verbose=False,
                                 size_timeout=10,
                                 prefer_html=False)
```

Build a mapping of region slug -> {url, size_bytes?, size_gb?} using Geofabrik index-v1.json.
Saves to cache_path (JSON) for reuse unless refresh=True.

<a id="georouting.utils.build_geofabrik_catalog"></a>

#### build\_geofabrik\_catalog

```python
def build_geofabrik_catalog(cache_path=DEFAULT_GEOFABRIK_CATALOG,
                            refresh=False,
                            include_sizes=True,
                            regions=None,
                            size_timeout=10,
                            verbose=False,
                            prefer_html=True)
```

Return a list of all Geofabrik PBF datasets with URLs (and sizes if requested).
Caches the result to JSON for reuse.

<a id="georouting.utils.resolve_geofabrik_pbf"></a>

#### resolve\_geofabrik\_pbf

```python
def resolve_geofabrik_pbf(region, refresh=True, include_size=False)
```

Resolve a region string to a Geofabrik PBF URL using the catalog; fallback to slug/path.

<a id="georouting.utils.render_osrm_dockerfile"></a>

#### render\_osrm\_dockerfile

```python
def render_osrm_dockerfile(region="north-america/us/massachusetts",
                           port=DEFAULT_OSRM_PORT,
                           base_image=DEFAULT_OSRM_BASE_IMAGE,
                           auto_fetch=True,
                           prefer_html=True,
                           size_timeout=10,
                           profile="car")
```

Render a Dockerfile string for an OSRM backend for the given region/profile.

Parameters
----------
region : str
    Geofabrik region slug/path (e.g., "north-america/us/massachusetts").
port : int
    Port to expose in the container.
base_image : str
    OSRM base image to use.
auto_fetch : bool
    If True, refresh Geofabrik index when resolving region.
prefer_html : bool
    Unused here; kept for parity with resolver options.
size_timeout : int
    Timeout (seconds) for size resolution (currently unused in rendering).
profile : str
    OSRM profile name or path (e.g., "car", "foot", "bicycle" or a lua path).

<a id="georouting.utils.write_osrm_dockerfile"></a>

#### write\_osrm\_dockerfile

```python
def write_osrm_dockerfile(path="Dockerfile", **kwargs)
```

Write the rendered OSRM Dockerfile to disk and print a preview.

<a id="georouting.utils.build_osrm_image"></a>

#### build\_osrm\_image

```python
def build_osrm_image(tag="osrm-backend",
                     dockerfile_path="Dockerfile",
                     context=".")
```

Build the OSRM Docker image using the given Dockerfile and context.

<a id="georouting.utils.run_osrm_container"></a>

#### run\_osrm\_container

```python
def run_osrm_container(tag="osrm-backend",
                       port=DEFAULT_OSRM_PORT,
                       detach=True,
                       extra_args=None)
```

Run the OSRM container exposing the selected port.

<a id="georouting.utils.build_and_run_osrm"></a>

#### build\_and\_run\_osrm

```python
def build_and_run_osrm(region="north-america/us/massachusetts",
                       port=DEFAULT_OSRM_PORT,
                       tag="osrm-backend",
                       dockerfile_path=None,
                       context=None,
                       auto_fetch=True,
                       prefer_html=True,
                       size_timeout=10,
                       detach=True,
                       extra_run_args=None,
                       base_image=DEFAULT_OSRM_BASE_IMAGE,
                       profile="car")
```

One-shot: write Dockerfile, build image, run container for the given region.

