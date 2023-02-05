
![georouting](https://raw.githubusercontent.com/wybert/georouting/main/docs/img/georouting.png)

[![image](https://img.shields.io/pypi/v/georouting.svg)](https://pypi.python.org/pypi/georouting)
[![image](https://img.shields.io/conda/vn/conda-forge/georouting.svg)](https://anaconda.org/conda-forge/georouting)


**Geo routing for Python users**

Warning!!! This project is under active development, the API may change in the future. Wait for the release of version 1.0.0. This package is inspired by [geopy](https://geopy.readthedocs.io/en/stable/). Please help to improve this package by submitting issues and pull requests.


-   Free software: MIT license
-   Documentation: https://wybert.github.io/georouting
    
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


## Features

- Support most of the routing services, including Google Maps, Bing Maps, OSRM, etc.
- Provide a unified API for routing services
- Support calculating the travel distance matrix between multiple origins and destinations
- Return the travel distance matrix in a Pandas `Dataframe` you like
- Return the routing results in a Geopandas `GeoDataFrame`
- Easy to extend to support more routing services


## TODO
- [x] Google Maps
- [x] Bing Maps
- [x] OSRM Routing
- [x] add more documentation for google router
- [x] add more documentation for bing router
- [x] add more documentation for osrm router
- [x] built and host documentation
- [x] Fix the update in Pypi
- [ ] add get_route_distance_batch API
- [ ] add visualization for the route, better with o and d markers
- [ ] Add more routing services
- [x] Add test 
- [ ] Add more examples
- [ ] Add how to contribute
- [ ] Add how to cite



## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
