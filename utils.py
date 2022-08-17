import os
import urllib
from pathlib import Path

import pandas as pd


def get_file_loc(filename: str):
    """get a path to the words.txt file"""
    path = Path(__file__)
    path = (path.parent).joinpath(filename)
    return path


def read_df(df_name: str):
    """reads the words into a dataframe"""

    file_loc = get_file_loc(df_name)
    words = pd.read_csv(
        file_loc,
        sep="|",
        header=0,
    )

    return words


def save_df(df, name):
    """save some dataframe to disk"""

    path = get_file_loc(name)
    df.to_csv(path, index_label=False, sep="|")


def data_root():
    """returns full path of local data folder"""
    dir_name = os.path.join((Path(__file__).parent), "data")

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    return dir_name


def download_if_needed(url: str, file_name: str):
    """small wrapper function to fetch a file if needed"""

    file_name = os.path.join(data_root(), file_name)

    if os.path.exists(file_name):
        return file_name

    urllib.request.urlretrieve(url, file_name)

    return file_name
