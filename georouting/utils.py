import numpy as np

def convert_to_list(data):
    """
    This method converts the data to a list.
    """
    if isinstance(data, np.ndarray):
        data = data.tolist()
    return data
