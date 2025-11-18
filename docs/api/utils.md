# Table of Contents

* [georouting.utils](#georouting.utils)
  * [convert\_to\_list](#georouting.utils.convert_to_list)
  * [get\_batch\_od\_pairs](#georouting.utils.get_batch_od_pairs)

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

