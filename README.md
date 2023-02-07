
![georouting](https://raw.githubusercontent.com/wybert/georouting/main/docs/img/georouting.png)




[![image](https://img.shields.io/pypi/v/georouting.svg)](https://pypi.python.org/pypi/georouting)
[![image](https://img.shields.io/conda/vn/conda-forge/georouting.svg)](https://anaconda.org/conda-forge/georouting)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wybert/georouting/blob/main/docs/usage.ipynb)
<!-- [![Open in Binder](https://mybinder.org/badge_logo.svg)](https://gishub.org/geemap-binder) -->
<!-- [![Open In Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/giswqs/geemap/blob/master/examples/notebooks/00_geemap_key_features.ipynb) -->
<!-- [![image](https://img.shields.io/conda/vn/conda-forge/geemap.svg)](https://anaconda.org/conda-forge/geemap) -->
<!-- [![image](https://pepy.tech/badge/geemap)](https://pepy.tech/project/geemap) -->
[![image](https://github.com/wybert/georouting/workflows/docs/badge.svg)](https://wybert.github.io/georouting/)
[![image](https://github.com/wybert/georouting/workflows/build/badge.svg)](https://github.com/wybert/georouting/actions?query=workflow%3Abuild)
[![image](https://img.shields.io/badge/YouTube-Channel-red)](https://youtube.com/@xiaokangfu3118)
[![image](https://img.shields.io/twitter/follow/fxk123?style=social)](https://twitter.com/fxk123)
[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- [![image](https://joss.theoj.org/papers/10.21105/joss.02305/status.svg)](https://joss.theoj.org/papers/10.21105/joss.02305) -->


**Geo routing for Python users**


Warning!!! This project is under active development, wait for the release of version 1.0.0 if you want to use it in production. This package is inspired by [geopy](https://geopy.readthedocs.io/en/stable/). Please help to improve this package by submitting issues and pull requests.


-   Free software: MIT license
-   Documentation: [https://wybert.github.io/georouting](https://wybert.github.io/georouting)
    

## Features

- Support most of the routing services, including Google Maps, Bing Maps, OSRM, etc.
- Provide a unified API for routing services
- Support calculating the travel distance matrix between multiple origins and destinations
- Support calculating the travel distance according to OD pairs.
- Easy to visualize the routing results
- Return the travel distance matrix in a Pandas `Dataframe` you like
- Return the routing results in a Geopandas `GeoDataFrame`
- Easy to extend to support more routing services


## Installation

### Using pip


To install georouting, run this command in your terminal:

```bash
pip install georouting
```

or install from GitHub source

```
pip install git+https://github.com/wybert/georouting.git
```


If you don't have [pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

### Using conda

This is not yet available on conda-forge,

```
conda install -c conda-forge georouting
```

or use mamba

```
mamba install -c conda-forge georouting
```


## Install from sources

The sources for georouting can be downloaded from the Github repo.

You can clone the public repository:

```
git clone git://github.com/wybert/georouting
```

Then install it with:

```
python setup.py install
```



## Usage

```python

# how to get routing distance matrix from OSRMRouter
import pandas as pd
data = pd.read_csv("https://raw.githubusercontent.com/wybert/georouting/main/docs/data/sample_3.csv",index_col=0)
one_od_pair = data.iloc[2]
data.head()

from georouting.routers import GoogleRouter
# create a router object with the google_key
router = GoogleRouter(google_key,mode="driving")
# get the route between the origin and destination, this will return a Route object
# this will call the Google Maps API
route = router.get_route([one_od_pair["ZIP_lat"],one_od_pair["ZIP_lon"]],
                           [one_od_pair["AHA_ID_lat"],one_od_pair["AHA_ID_lon"]])
# Now you can get the distance and duration of the route in meters and seconds
print("Distance: {} meters".format(route.get_distance()))
print("Duration: {} seconds".format(route.get_duration()))

df= route.get_route_geopandas()
df.head()

df.explore(column="speed (m/s)",style_kwds={"weight":11,"opacity":0.8})

```


## TODO
- [x] Google Maps
- [x] Bing Maps
- [x] OSRM Routing
- [x] add more documentation for google router
- [x] add more documentation for bing router
- [x] add more documentation for osrm router
- [x] built and host documentation
- [x] Fix the update in Pypi
- [x] add get_route_distance_batch API
- [x] add visualization for the route, better with o and d markers
- [x] Limit the number of origins and destinations in the distance matrix
- [x] avoid repeat documentation
- [ ] Add more routing services
- [x] Add test 
- [x] Add more examples
- [x] Add how to contribute
- [ ] Add how to cite
- [x] change the show case use OSRM


## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
