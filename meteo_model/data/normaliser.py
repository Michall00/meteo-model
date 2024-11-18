"""Module for normalising weather attributes"""
import json
import numpy as np
from pathlib import Path
from config import PATH_TO_STATS, PATHS_TO_DATA_FILES_STR
from get_stats import create_stat_file
import pandas as pd


if not Path(PATH_TO_STATS).exists():
    create_stat_file()

with open(PATH_TO_STATS) as f:
    stats = json.load(f)


def _normalise_norm_like(array, attr_name: str):
    mean = stats[attr_name]["mean"]
    std = stats[attr_name]["std"]
    return (array - mean)/std



def _normalise_tavg(array):
    return _normalise_norm_like(array, "tavg")

def _normalise_tmin(array):
    return _normalise_norm_like(array, "tmin")

def _normalise_tmax(array):
    return _normalise_norm_like(array, "tmax")

def _normalise_prcp(array):
    return np.log1p(array)

def _normalise_snow(array):
    mean_snow = stats["snow"]["mean"]
    mean_snow_log = np.log1p(mean_snow)
    return np.log1p(array) / mean_snow_log

def _normalise_wdir(array):
    rad_array = np.deg2rad(array)
    return np.sin(rad_array), np.cos(rad_array)

def _normalise_wspd(array):
    return _normalise_norm_like(array, "wspd")

def _normalise_pres(array):
    return _normalise_norm_like(array, "pres")

def _inverse_normalize_norm_like(array, attr_name):
    mean = stats[attr_name]["mean"]
    std = stats[attr_name]["std"]
    return array * std + mean

def _inverse_pres(array):
    return _inverse_normalize_norm_like(array, 'pres')

def _inverse_tavg(array):
    return _inverse_normalize_norm_like(array, 'tavg')

def _inverse_tmin(array):
    return _inverse_normalize_norm_like(array, 'tmin')

def _inverse_tmax(array):
    return _inverse_normalize_norm_like(array, 'tmax')

def _inverse_wspd(array):
    return _inverse_normalize_norm_like(array, 'wspd')

def _inverse_prcp(array):
    return np.expm1(array)

def _inverse_snow(array):
    mean_snow = stats["snow"]["mean"]
    mean_snow_log = np.log1p(mean_snow)
    return np.expm1(array* mean_snow_log)

def _inverse_wdir(array_sin, array_cos):
    angle_rad = np.arctan2(array_sin, array_cos)
    angle_deg = np.rad2deg(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return angle_deg




def normalize_data(df):
    columns = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'sin_wdir', 'cos_wdir', 'wspd', 'pres']
    normalised_df = pd.DataFrame(columns=columns)
    normalised_df["tavg"] = _normalise_tavg(df["tavg"])
    normalised_df["tmin"] = _normalise_tmin(df["tmin"])
    normalised_df["tmax"] = _normalise_tmax(df["tmax"])
    normalised_df["prcp"] = _normalise_prcp(df["prcp"])
    normalised_df["snow"] = _normalise_snow(df["snow"])
    sin_wdir, cos_wdir = _normalise_wdir(df["wdir"])
    normalised_df["sin_wdir"] = sin_wdir
    normalised_df["cos_wdir"] = cos_wdir
    normalised_df["wspd"] = _normalise_wspd(df["wspd"])
    normalised_df["pres"] = _normalise_pres(df["pres"])
    return normalised_df


def inverse_normalize_data(df):
    columns = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'pres']
    inv_df = pd.DataFrame(columns=columns)
    inv_df['tavg'] = _inverse_tavg(df['tavg'])
    inv_df['tmin'] = _inverse_tmin(df['tmin'])
    inv_df['tmax'] = _inverse_tmax(df['tmax'])
    inv_df['prcp'] = _inverse_prcp(df['prcp'])
    inv_df['snow'] = _inverse_snow(df['snow'])
    inv_df['wdir'] = _inverse_wdir(df['sin_wdir'], df['cos_wdir'])
    inv_df['pres'] = _inverse_pres(df['pres'])
    return inv_df




if __name__== "__main__":
    from get_stats import get_dataframe
    import matplotlib.pyplot as plt
    from glob import glob

    variables = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'sin_wdir', 'cos_wdir', 'wspd', 'pres']
    plt.figure(figsize=(12, 10))
    huge_df = get_dataframe(glob(PATHS_TO_DATA_FILES_STR))
    normalised = normalize_data(huge_df)

    for i, var in enumerate(variables, 1):
        plt.subplot(5, 2, i)  # 5 rows, 2 columns grid
        plt.hist(normalised.dropna(subset=[var])[var], bins=100, color='blue')
        plt.title(var)
        plt.xlabel('Value')
        plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig("reports/figures/data/data_featues_histograms_normalised.png")
    plt.show()
