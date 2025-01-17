"""Module for normalising weather attributes"""

import json
import numpy as np
from pathlib import Path
from meteo_model.data.config import PATH_TO_STATS, PATHS_TO_DATA_FILES_STR, COLUMNS, NORM_COLUMNS
from meteo_model.data.get_stats import create_stat_file
import pandas as pd
from typing import Dict, Any

StatType = Dict[str, Any]


def _normalise_norm_like(array: pd.Series, attr_name: str, stats: StatType):
    attr_stats = stats[attr_name]
    return (array - attr_stats["mean"]) / attr_stats["std"]


def _normalise_prcp(array: pd.Series):
    return np.log1p(array)


def _normalise_snow(array: pd.Series, stats: StatType):
    mean_snow = stats["snow"]["mean"]
    mean_snow_log = np.log1p(mean_snow)
    return np.log1p(array) / mean_snow_log


def _normalise_wdir(array: pd.Series):
    rad_array = np.deg2rad(array)
    return np.sin(rad_array), np.cos(rad_array)


def _inverse_normalize_norm_like(array: pd.Series, attr_name, stats: StatType):
    mean = stats[attr_name]["mean"]
    std = stats[attr_name]["std"]
    return array * std + mean


def _inverse_prcp(array: pd.Series):
    return np.expm1(array)


def _inverse_snow(array: pd.Series, stats: StatType):
    mean_snow = stats["snow"]["mean"]
    mean_snow_log = np.log1p(mean_snow)
    return np.expm1(array * mean_snow_log)


def _inverse_wdir(array_sin: pd.Series, array_cos: pd.Series):
    angle_deg = np.rad2deg(np.arctan2(array_sin, array_cos))
    return angle_deg % 360


def normalize_data(df: pd.DataFrame, stats: StatType):
    columns = NORM_COLUMNS
    norm_like_columns = ["tavg", "tmin", "tmax", "wspd", "pres"]
    normalised_df = pd.DataFrame(columns=columns)
    for col in norm_like_columns:
        normalised_df[col] = _normalise_norm_like(df[col], col, stats)

    normalised_df["prcp"] = _normalise_prcp(df["prcp"])
    normalised_df["snow"] = _normalise_snow(df["snow"], stats)
    normalised_df["sin_wdir"], normalised_df["cos_wdir"] = _normalise_wdir(df["wdir"])
    return normalised_df


def inverse_normalize_data(df: pd.DataFrame, stats: StatType):
    columns = COLUMNS
    inv_df = pd.DataFrame(columns=columns)
    norm_like_columns = ["tavg", "tmin", "tmax", "wspd", "pres"]
    for col in norm_like_columns:
        inv_df[col] = _inverse_normalize_norm_like(df[col], col, stats)
    inv_df["prcp"] = _inverse_prcp(df["prcp"])
    inv_df["snow"] = _inverse_snow(df["snow"], stats)
    inv_df["wdir"] = _inverse_wdir(df["sin_wdir"], df["cos_wdir"])
    return inv_df


if __name__ == "__main__":
    from meteo_model.data.get_stats import get_dataframe
    import matplotlib.pyplot as plt
    from glob import glob

    PATH_TO_NORMALISED_HISTOGRAMS = "reports/figures/data/data_featues_histograms_normalised.png"

    if not Path(PATH_TO_STATS).exists():
        create_stat_file()

    with open(PATH_TO_STATS) as f:
        stats_ = json.load(f)

    plt.figure(figsize=(12, 10))
    huge_df = get_dataframe(glob(PATHS_TO_DATA_FILES_STR))
    normalised = normalize_data(huge_df, stats_)
    variables = normalised.columns

    for i, var in enumerate(variables, 1):
        plt.subplot(5, 2, i)
        plt.hist(normalised.dropna(subset=[var])[var], bins=100, color="blue")
        plt.title(var)
        plt.xlabel("Value")
        plt.ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(PATH_TO_NORMALISED_HISTOGRAMS)
    plt.show()
