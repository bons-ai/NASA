# -*- coding: utf-8 -*-
import pandas as pd
import h5py
import numpy as np
import os
import time

ti = time.time()
# h5_file = "ATL03_20190502235300_05300309_001_01.h5"
# f = h5py.File(h5_file, mode="r")
# rays = [ray for ray in f.keys() if ray[0:2] == "gt"]
# print(rays)
# print(list(f["gt1l"].values()))
#
# temp = np.array(f["gt1l"]["heights"]["h_ph"])
# print(list(f["gt1l"]["heights"]))
# for i in list(f.keys()):
#     print(i)


def extract_from_filename(h5_file):
    """
        # ATL03_20190502235300_
        # 0530 : Track
        # 03   : cycle seulement la premiere fois (01)
        # 09   : nombre du split de la track
        # _001_01
    """
    track_var = h5_file.split("_")[2]
    track_nb = track_var[0:4]
    track_cy = track_var[4:6]
    track_seg = track_var[6:8]

    return track_nb, track_cy, track_seg


def concat(ds, rays):
    # lon, lat, lz = np.ndarray([]), np.ndarray([]), np.ndarray([])

    lon = np.concatenate(tuple([ds[ray]["heights"]["lon_ph"] for ray in rays]))
    lat = np.concatenate(tuple([ds[ray]["heights"]["lat_ph"] for ray in rays]))
    lz = np.concatenate(tuple([ds[ray]["heights"]["h_ph"] for ray in rays]))
    print(len(lon))
    print(lon)

    # for ray in rays:
    #     print(list(ds[ray]["heights"]["lon_ph"])[:10])
    #     lon = np.concatenate(lon,ds[ray]["heights"]["lon_ph"][:10])
    #     lat = ds[ray]["heights"]["lat_ph"][:10]
    #     lz = ds[ray]["heights"]["h_ph"][:10]

    return lon, lat, lz


def read_data(h5_file="ATL03_20190502235300_05300309_001_01.h5"):
    """
    :param h5_file:
    :return: lon, lat, lz
             lon: longitude
             lat: latitude
             lz : laser height
    """
    lon, lat, lz = [], [], []

    track_nb, track_cy, track_seg = extract_from_filename(h5_file)
    new_filename = f"data_{track_nb}_{track_cy}_{track_seg}.npy"


    f = h5py.File(h5_file, mode="r")

    rays = [ray for ray in f.keys() if ray[0:2] == "gt"] #e.g. "gt1l"
    # print(type(f["gt1l"]["heights"]["lon_ph"][0:10]))
    # print(list(f["gt1l"]["heights"]["lon_ph"])[:10])
    lon, lat, lz = concat(f, rays)

    return lon, lat, lz, new_filename

def search_h5file():

    for file_ in os.listdir("data"):
        if os.path.splitext(file_)[1] == ".h5":
            lon, lat, lz, new_filename = read_data("data" + "/" + file_)
            print(lon, lat, lz)

            np.save(new_filename, {"lon": lon, "lat": lat, "lz": lz})

search_h5file()



print(str(time.time() - ti))
print(100000*(time.time() - ti))
