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

-   Python (>=3.6 and ≤3.13)
-   [pandas](https://pandas.pydata.org/) (>= 0.25.0)
-   [geopandas](https://geopandas.org/) (>= 0.6.0)
-   [requests](https://requests.readthedocs.io/en/master/) (>= 2.22.0)
-   [numpy](https://numpy.org/) (>= 1.17.0)
-   [shapely](https://shapely.readthedocs.io/en/stable/) (>= 1.6.4.post2)
-   [pyproj](https://pyproj4.github.io/pyproj/stable/) (>= 2.4.2.post1)
