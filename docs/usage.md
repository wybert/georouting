# Usage


Here is a simple example of how to use georouting:

```python
# Load the some data
import pandas as pd
data = pd.read_csv("https://raw.githubusercontent.com/wybert/georouting/main/docs/data/sample_3.csv",index_col=0)
data.head()

# Get a route between two points is easy, 
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

# You can also return the routing results in a GeoDataFrame, 
# It will return the distance, duration, speed and the route geometry,

df= route.get_route_geopandas()
df.head()

# Now can visualize the route in a map,

df.explore(column="speed (m/s)",style_kwds={"weight":11,"opacity":0.8})

```

For more examples, please refer to the [Documentation](https://wybert.github.io/georouting/)

