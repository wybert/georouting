
![georouting](docs/img/georouting.png)

[![image](https://img.shields.io/pypi/v/georouting.svg)](https://pypi.python.org/pypi/georouting)
[![image](https://img.shields.io/conda/vn/conda-forge/georouting.svg)](https://anaconda.org/conda-forge/georouting)


**Geo routing for Python users**

Warning!!! This project is under active development, the API may change in the future. Wait for the release of version 1.0.0. This package is inspired by [geopy](https://geopy.readthedocs.io/en/stable/). Please help to improve this package by submitting issues and pull requests.


-   Free software: MIT license
-   Documentation: https://wybert.github.io/georouting
    
## Installation

```bash
pip install git+https://github.com/wybert/georouting.git
``` 
It will be on pypi soon.
## Usage

```python

# how to get routing distance matrix from OSRMRouter
from georouting.routers import OSRMRouter
orings = 
destinations =
router = OSRMRouter()
distance_matrix = router.get_distance_matrix(orings, dstrings,append_od=True)
distance_matrix.head()
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
- [ ] built and host documentation
- [ ] Fix the update in Pypi
- [ ] Add more routing services
- [ ] Add more tests
- [ ] Add more examples
- [ ] Add more documentation
- [ ] Add how to contribute
- [ ] Add how to cite



## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
