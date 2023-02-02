
![georouting](https://raw.githubusercontent.com/wybert/georouting/main/docs/images/georouting%20icon2.png)

[![image](https://img.shields.io/pypi/v/georouting.svg)](https://pypi.python.org/pypi/georouting)
[![image](https://img.shields.io/conda/vn/conda-forge/georouting.svg)](https://anaconda.org/conda-forge/georouting)


**Geo routing for Python users**

Warning!!! This project is under active developing, the API may change in the future. Wait for the release of version 1.0.0. This package is inspired by [geopy](https://geopy.readthedocs.io/en/stable/). Please help to improve this package by submitting issues and pull requests.


-   Free software: MIT license
-   Documentation: https://wybert.github.io/georouting
    
## Installation

```bash
pip install git+https://github.com/wybert/georouting.git
``` 

## Usage

```python

# how to get routing distance matrix from OSRMRouter
from georouting.routers.osrm import OSRMRouter
orings = 
destinations =
router = OSRMRouter()
distance_matrix = router.get_distance_matrix(orings, dstrings,append_od=True)
distance_matrix.head()
```


## Features

- [x] Google Maps
- [x] Bing Maps
- [x] OSRM Routing
- [ ] add more documentation
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
