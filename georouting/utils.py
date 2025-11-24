import numpy as np
import pandas as pd
import osmnx as ox
import requests
import json
import html
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


def convert_to_list(data):
    """
    This function converts the data to a list.
    """
    if isinstance(data, np.ndarray):
        data = data.tolist()
    return data


def _format_coords(coords):
    """
    Format a list of coordinates as a pipe-separated string for Baidu API.

    Parameters
    ----------
    coords : list
        List of coordinate pairs, e.g., [[lat1, lon1], [lat2, lon2]]

    Returns
    -------
    str
        Pipe-separated string of coordinates, e.g., "lat1,lon1|lat2,lon2"
    """
    return "|".join([f"{c[0]},{c[1]}" for c in coords])


def get_batch_od_pairs(orgins, destinations, max_batch_size=25):
    """
    This function returns a list of dataframes containing the origin-destination pairs to
    avoid the repeated requests to the travel distance API.
    """

    orgins = pd.DataFrame(orgins, columns=["lat", "lon"])
    destinations = pd.DataFrame(destinations, columns=["lat", "lon"])
    df = pd.merge(
        orgins,
        destinations,
        left_index=True,
        right_index=True,
        suffixes=("_origin", "_destination"),
    )
    df["origin"] = df["lat_origin"].astype(str) + "," + df["lon_origin"].astype(str)
    df["destination"] = (
        df["lat_destination"].astype(str) + "," + df["lon_destination"].astype(str)
    )

    if df["destination"].nunique() >= df["origin"].nunique():
        according = "origin"
    else:
        according = "destination"
    # print(according)
    grouped = df.groupby(according)
    orgins_destinations_list = []
    for i, group in grouped:
        # set batch id
        group["batch_id"] = group.index
        # set batch size
        batch_size = len(group)
        group["batch_size"] = batch_size

        # divide the batch into sub batches according to the max_batch_size
        if batch_size > max_batch_size:
            ngroups = batch_size // max_batch_size
            if batch_size % max_batch_size != 0:
                ngroups += 1
            for i in range(ngroups - 1):
                sub_group = group.iloc[i * max_batch_size : (i + 1) * max_batch_size]

                orgins = (
                    sub_group[["lat_origin", "lon_origin"]]
                    .value_counts()
                    .index.to_list()
                )
                destinations = (
                    sub_group[["lat_destination", "lon_destination"]]
                    .value_counts()
                    .index.to_list()
                )
                orgins_destinations_list.append((orgins, destinations))

            sub_group = group.iloc[(ngroups - 1) * max_batch_size :]
            orgins = (
                sub_group[["lat_origin", "lon_origin"]].value_counts().index.to_list()
            )
            destinations = (
                sub_group[["lat_destination", "lon_destination"]]
                .value_counts()
                .index.to_list()
            )
            orgins_destinations_list.append((orgins, destinations))

        else:
            orgins = group[["lat_origin", "lon_origin"]].value_counts().index.to_list()
            destinations = (
                group[["lat_destination", "lon_destination"]]
                .value_counts()
                .index.to_list()
            )
            orgins_destinations_list.append((orgins, destinations))

    return orgins_destinations_list


# ------------- Geofabrik helpers -------------

DEFAULT_GEOFABRIK_CACHE = (
    Path(__file__).resolve().parent / "cache" / "geofabrik_index.json"
)
DEFAULT_GEOFABRIK_CATALOG = (
    Path(__file__).resolve().parent / "cache" / "geofabrik_catalog.json"
)
GEOFABRIK_INDEX_URL = "https://download.geofabrik.de/index-v1.json"
DEFAULT_OSRM_BASE_IMAGE = "ghcr.io/project-osrm/osrm-backend"
DEFAULT_OSRM_PORT = 5000


def slugify(name):
    return name.lower().replace(" ", "-").replace("_", "-")


def _pbf_to_page_url(pbf_url):
    if not pbf_url.endswith(".osm.pbf"):
        return None
    return pbf_url.replace("-latest.osm.pbf", ".html")


def _parse_human_size(size_str):
    text = html.unescape(size_str).replace("\xa0", " ").strip("() ")
    m = re.match(r"([0-9.]+)\s*([KMG]?)B", text, re.IGNORECASE)
    if not m:
        return None
    value = float(m.group(1))
    unit = m.group(2).upper()
    factor = {"": 1, "K": 1024, "M": 1024**2, "G": 1024**3}.get(unit, 1)
    return int(value * factor)


def _fetch_size_from_html(pbf_url, size_timeout=10, prefer_html=False, fallback_head=True):
    """
    Get size in bytes for a PBF URL.
    - If prefer_html is False: HEAD first, then HTML.
    - If prefer_html is True: HTML first, then HEAD (if fallback_head).
    """

    def try_head():
        try:
            head = requests.head(pbf_url, allow_redirects=True, timeout=size_timeout)
            head.raise_for_status()
            length = head.headers.get("Content-Length")
            if length:
                return int(length)
        except Exception:
            return None
        return None

    def try_html():
        page_url = _pbf_to_page_url(pbf_url)
        if not page_url:
            return None
        try:
            resp = requests.get(page_url, timeout=size_timeout)
            resp.raise_for_status()
            html_text = resp.text
        except Exception:
            return None

        basename = pbf_url.split("/")[-1]
        pattern = re.compile(
            rf'href="[^"]*{re.escape(basename)}"[^<]*</a>\s*</td>\s*<td[^>]*>\(([^<]+)\)',
            re.IGNORECASE | re.DOTALL,
        )
        m = pattern.search(html_text)
        if not m:
            return None
        return _parse_human_size(m.group(1))

    if prefer_html:
        size = try_html()
        if size is None and fallback_head:
            size = try_head()
        return size

    size = try_head()
    if size is None:
        size = try_html()
    return size


def build_geofabrik_region_index(
    cache_path=DEFAULT_GEOFABRIK_CACHE,
    refresh=False,
    include_sizes=False,
    regions=None,
    verbose=False,
    size_timeout=10,
    prefer_html=False,
):
    """
    Build a mapping of region slug -> {url, size_bytes?, size_gb?} using Geofabrik index-v1.json.
    Saves to cache_path (JSON) for reuse unless refresh=True.
    """
    cache_path = Path(cache_path) if cache_path else None

    if not refresh and cache_path and cache_path.exists():
        with cache_path.open() as f:
            return json.load(f)

    resp = requests.get(GEOFABRIK_INDEX_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    feature_list = data.get("features", [])
    if regions:
        wanted = {slugify(r) for r in regions}
        feature_list = [
            f
            for f in feature_list
            if slugify(f.get("properties", {}).get("name", "")) in wanted
            or slugify(f.get("properties", {}).get("id", "")) in wanted
        ]

    regions_map = {}
    total = len(feature_list)
    for idx, feature in enumerate(feature_list):
        props = feature.get("properties", {})
        urls = props.get("urls", {})
        pbf_url = urls.get("pbf")
        if not pbf_url:
            continue
        name = props.get("name")
        fid = props.get("id")
        keys = {k for k in [name, fid] if k}
        keys.add(slugify(name or fid or pbf_url))
        for k in keys:
            regions_map[slugify(k)] = {"url": pbf_url}

    if include_sizes:
        for entry in regions_map.values():
            size_bytes = _fetch_size_from_html(
                entry["url"],
                size_timeout=size_timeout,
                prefer_html=prefer_html,
                fallback_head=not prefer_html,
            )
            entry["size_bytes"] = size_bytes
            entry["size_gb"] = size_bytes / (1024**3) if size_bytes else None
            if verbose:
                print(f"[sizes] {entry.get('url')} -> {entry['size_bytes']}")

    result = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "include_sizes": include_sizes,
        "regions": regions_map,
    }

    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("w") as f:
            json.dump(result, f, indent=2)

    return result


def get_geofabrik_region_info(
    region, cache_path=DEFAULT_GEOFABRIK_CACHE, refresh=False, include_size=True, size_timeout=10
):
    index = build_geofabrik_region_index(
        cache_path=cache_path, refresh=refresh, include_sizes=False
    )
    regions = index.get("regions", {})
    slug = slugify(region)
    entry = regions.get(slug)
    if not entry:
        raise ValueError(f"Region '{region}' not found in Geofabrik index")

    if include_size and "size_bytes" not in entry:
        size_bytes = _fetch_size_from_html(entry["url"], size_timeout=size_timeout)
        entry["size_bytes"] = size_bytes
        entry["size_gb"] = size_bytes / (1024**3) if size_bytes else None

    return entry


def build_geofabrik_catalog(
    cache_path=DEFAULT_GEOFABRIK_CATALOG,
    refresh=False,
    include_sizes=True,
    regions=None,
    size_timeout=10,
    verbose=False,
    prefer_html=True,
):
    """
    Return a list of all Geofabrik PBF datasets with URLs (and sizes if requested).
    Caches the result to JSON for reuse.
    """
    cache_path = Path(cache_path) if cache_path else None
    if not refresh and cache_path and cache_path.exists():
        with cache_path.open() as f:
            return json.load(f)

    resp = requests.get(GEOFABRIK_INDEX_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    feature_list = data.get("features", [])
    if regions:
        wanted = {slugify(r) for r in regions}
        feature_list = [
            f
            for f in feature_list
            if slugify(f.get("properties", {}).get("name", "")) in wanted
            or slugify(f.get("properties", {}).get("id", "")) in wanted
        ]

    entries = []
    total = len(feature_list)
    for idx, feature in enumerate(feature_list):
        props = feature.get("properties", {})
        urls = props.get("urls", {})
        pbf_url = urls.get("pbf")
        if not pbf_url:
            continue
        entry = {
            "id": props.get("id"),
            "name": props.get("name"),
            "parent": props.get("parent"),
            "iso3166_1_alpha2": props.get("iso3166-1:alpha2"),
            "slug": slugify(props.get("name") or props.get("id") or pbf_url),
            "pbf_url": pbf_url,
        }
        if include_sizes:
            size_bytes = _fetch_size_from_html(
                pbf_url,
                size_timeout=size_timeout,
                prefer_html=prefer_html,
                fallback_head=not prefer_html,
            )
            entry["size_bytes"] = size_bytes
            entry["size_gb"] = size_bytes / (1024**3) if size_bytes else None
            if verbose:
                print(f"[{idx+1}/{total}] {entry['slug']}: {size_bytes} bytes")
        entries.append(entry)

    result = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "include_sizes": include_sizes,
        "entries": entries,
    }

    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("w") as f:
            json.dump(result, f, indent=2)

    return result


# ------------- OSRM backend helpers -------------

def resolve_geofabrik_pbf(region, refresh=True, include_size=False):
    """
    Resolve a region string to a Geofabrik PBF URL using the catalog; fallback to slug/path.
    """
    try:
        info = get_geofabrik_region_info(region, refresh=refresh, include_size=include_size)
        return info["url"], info.get("size_bytes"), info.get("size_gb")
    except Exception:
        # Try last segment
        try:
            last = region.split("/")[-1]
            info = get_geofabrik_region_info(last, refresh=False, include_size=include_size)
            return info["url"], info.get("size_bytes"), info.get("size_gb")
        except Exception:
            pass

    # Fallback naive construction
    path = region
    if path.startswith(("http://", "https://")):
        return path, None, None
    if not path.endswith(".osm.pbf"):
        if path.endswith(".osm"):
            path = path + ".pbf"
        elif path.endswith("-latest"):
            path = path + ".osm.pbf"
        else:
            path = path + "-latest.osm.pbf"
    return f"https://download.geofabrik.de/{path}", None, None


def render_osrm_dockerfile(
    region="north-america/us/massachusetts",
    port=DEFAULT_OSRM_PORT,
    base_image=DEFAULT_OSRM_BASE_IMAGE,
    auto_fetch=True,
    prefer_html=True,
    size_timeout=10,
    profile="car",
):
    """
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
    """
    url, _, _ = resolve_geofabrik_pbf(region, refresh=auto_fetch, include_size=False)
    filename = url.split("/")[-1]
    name_no_ext = filename.replace(".osm.pbf", "").replace(".osm", "")
    profile_path = profile if "/" in profile else f"/opt/{profile}.lua"
    return f"""FROM {base_image}
# Ensure wget exists (works for Alpine or Debian bases)
RUN (command -v wget >/dev/null 2>&1) || (apk add --no-cache wget || (apt-get update && apt-get install -y wget))

RUN mkdir /data
WORKDIR /data

# Download extract ({region})
RUN wget {url} -O {filename}
# Preprocess OSM data; ignore failures to allow inspection
RUN osrm-extract -p {profile_path} {filename} || echo "osrm-extract failed"
RUN osrm-partition {name_no_ext}.osrm || echo "osrm-partition failed"
RUN osrm-customize {name_no_ext}.osrm || echo "osrm-customize failed"
RUN rm {filename}

CMD ["osrm-routed", "--ip", "0.0.0.0", "--port", "{port}", "--max-table-size", "1000000000", "--max-viaroute-size", "100000000", "--max-trip-size", "1000000000", "--algorithm", "mld", "/data/{name_no_ext}.osrm"]
EXPOSE {port}
"""


def write_osrm_dockerfile(path="Dockerfile", **kwargs):
    """Write the rendered OSRM Dockerfile to disk and print a preview."""
    content = render_osrm_dockerfile(**kwargs)
    dest = Path(path).resolve()
    dest.write_text(content)
    print(f"[osrm] Dockerfile written to: {dest}")
    print("[osrm] --- Dockerfile preview ---")
    print(content)
    print("[osrm] --------------------------")
    return dest


def build_osrm_image(tag="osrm-backend", dockerfile_path="Dockerfile", context="."):
    """Build the OSRM Docker image using the given Dockerfile and context."""
    dockerfile_path = Path(dockerfile_path)
    context = Path(context)
    print(f"[osrm] Building Docker image '{tag}' using {dockerfile_path} (context={context})")
    cmd = ["docker", "build", "-t", tag, "-f", str(dockerfile_path), str(context)]
    subprocess.run(cmd, check=True)
    print(f"[osrm] Build complete: {tag}")


def run_osrm_container(tag="osrm-backend", port=DEFAULT_OSRM_PORT, detach=True, extra_args=None):
    """Run the OSRM container exposing the selected port."""
    print(f"[osrm] Running container from image '{tag}' on port {port}")
    cmd = ["docker", "run"]
    if detach:
        cmd.append("-d")
    cmd += ["-p", f"{port}:{port}"]
    if extra_args:
        cmd += extra_args
    cmd.append(tag)
    subprocess.run(cmd, check=True)
    print(f"[osrm] Container started. OSRM available at http://localhost:{port}")
    print(f"[osrm] Remember to stop the container when done: docker stop $(docker ps -q --filter ancestor={tag})")
    print("[osrm] More details and issues: https://github.com/Project-OSRM/osrm-backend")


def build_and_run_osrm(
    region="north-america/us/massachusetts",
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
    profile="car",
):
    """
    One-shot: write Dockerfile, build image, run container for the given region.
    """
    # Cross-platform defaults: use system temp dir if not provided
    if dockerfile_path is None:
        slug = slugify(region)
        tmpdir = Path(tempfile.gettempdir())
        dockerfile_path = tmpdir / f"osrm_{slug}.Dockerfile"
    if context is None:
        context = Path(dockerfile_path).parent

    dockerfile = write_osrm_dockerfile(
        path=dockerfile_path,
        region=region,
        port=port,
        base_image=base_image,
        auto_fetch=auto_fetch,
        prefer_html=prefer_html,
        size_timeout=size_timeout,
        profile=profile,
    )
    build_osrm_image(tag=tag, dockerfile_path=dockerfile_path, context=context)
    run_osrm_container(tag=tag, port=port, detach=detach, extra_args=extra_run_args)
