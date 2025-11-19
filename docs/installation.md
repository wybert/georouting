# Installation


## Stable release

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


```
conda install -c conda-forge georouting
```

or use mamba

```
mamba install -c conda-forge georouting
```


## From sources

The sources for georouting can be downloaded from the Github repo.

You can clone the public repository:

```
git clone git://github.com/wybert/georouting
```

Then install it with:

```
python setup.py install
```

## Dependencies

georouting requires:

-   Python (>=3.9 and ≤3.13)
-   [pandas](https://pandas.pydata.org/)
-   [geopandas](https://geopandas.org/)
-   [requests](https://requests.readthedocs.io/en/master/)
-   [numpy](https://numpy.org/)
-   [shapely](https://shapely.readthedocs.io/en/stable/)
-   [pyproj](https://pyproj4.github.io/pyproj/stable/)
