import numpy as np
import pandas as pd

def convert_to_list(data):
    """
    This function converts the data to a list.
    """
    if isinstance(data, np.ndarray):
        data = data.tolist()
    return data

def get_batch_od_pairs(orgins,destinations,max_batch_size=25):

    """
    This function returns a list of dataframes containing the origin-destination pairs to 
    avoid the repeated requests to the travel distance API.
    """
    
    orgins = pd.DataFrame(orgins,columns=["lat","lon"])
    destinations = pd.DataFrame(destinations,columns=["lat","lon"])
    df = pd.merge(orgins,destinations,left_index=True,right_index=True,suffixes=("_origin","_destination"))
    df["origin"] = df["lat_origin"].astype(str) + "," + df["lon_origin"].astype(str)
    df["destination"] = df["lat_destination"].astype(str) + "," + df["lon_destination"].astype(str)

    if df["destination"].nunique() >= df["origin"].nunique():
        according = "origin"
    else:
        according = "destination"
    # print(according)
    grouped = df.groupby(according)
    orgins_destinations_list = []
    for i,group in grouped:
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
            for i in range(ngroups-1):
                sub_group = group.iloc[i*max_batch_size:(i+1)*max_batch_size]

                orgins = sub_group[["lat_origin","lon_origin"]].value_counts().index.to_list()
                destinations = sub_group[["lat_destination","lon_destination"]].value_counts().index.to_list()
                orgins_destinations_list.append((orgins,destinations))
            
            sub_group = group.iloc[(ngroups-1)*max_batch_size:]
            orgins = sub_group[["lat_origin","lon_origin"]].value_counts().index.to_list()
            destinations = sub_group[["lat_destination","lon_destination"]].value_counts().index.to_list()
            orgins_destinations_list.append((orgins,destinations))
            
        else:

            orgins = group[["lat_origin","lon_origin"]].value_counts().index.to_list()
            destinations = group[["lat_destination","lon_destination"]].value_counts().index.to_list()
            orgins_destinations_list.append((orgins,destinations))

    return orgins_destinations_list
