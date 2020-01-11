
import pandas as pd
import json
import numpy as np
import random
import csv


# ###  interval function
def retrive_from_interval(df, interval):
    (begin_interval, end_interval) = interval
    new_df = pd.DataFrame(columns=['id', 'timestamp', 'longitude', 'latitude'])
    for _, row in df.iterrows():
        if row['timestamp'] < end_interval and row['timestamp'] >= begin_interval:
            new_df.loc[len(new_df)] = [int(row['id']), int(
                row['timestamp']), row['longitude'], row['latitude']]
        if row['timestamp'] > end_interval and row['timestamp'] > begin_interval:
            break
    return new_df


# ### aggregate!
def aggregate_points(df, NB):
    global longs
    global lats
    step_long = (LONGITUDE_MAX - LONGITUDE_MIN) / NB
    step_lat = (LATITUDE_MAX - LATITUDE_MIN) / NB / 3
    longs = np.arange(LONGITUDE_MIN, LONGITUDE_MAX, step_long)
    lats = np.arange(LATITUDE_MIN, LATITUDE_MAX, step_lat)
    to_nearest_point(df, longs, lats, step_long, step_lat)
    return df


def to_nearest_point(df, longs, lats, step_long, step_lat):
    for _, row in df.iterrows():
        row['longitude'] = row['longitude'] - \
            ((row['longitude'] - longs[0]) % step_long)
        row['latitude'] = row['latitude'] - \
            ((row['latitude'] - lats[0]) % step_lat)
    return df


def make_map(df):
    global longs
    global lats
    global my_map
    dict_long = {round(k, 5): v for v, k in enumerate(longs)}
    dict_lat = {round(k, 5): v for v, k in enumerate(lats)}
    for _, row in df.iterrows():

        my_map[dict_long[round(row['longitude'], 5)]][dict_lat[round(
            row['latitude'], 5)]] = row['height']
    return my_map


def export_map():
    global my_map
    with open("map.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(my_map)
    print("map exported to map.csv")


if __name__ == "__main__":

    LONGITUDE_MIN = 4.8
    LONGITUDE_MAX = 4.93
    LATITUDE_MIN = 45.6
    LATITUDE_MAX = 45.9
    NB = 60
    my_map = [[0 for x in range(NB*3+1)] for y in range(NB)]
    longs = []
    lats = []
    dict_long = {}
    dict_lat = {}

    df1 = pd.read_csv("./data/data1.csv")

    # ### set time interval
    points_interval = retrive_from_interval(df1, [1418550959, 1422480000])
    # ### aggregate the points
    aggregation = aggregate_points(points_interval, NB)
    serie = aggregation.groupby(['longitude', 'latitude']).size()
    final_df = serie.reset_index(name='height')
    # ### make the map without noise:
    make_map(final_df)
    export_map()
