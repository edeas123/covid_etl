from functions.covid_etl import extract_data, transform_nyt_dataset
from datetime import datetime
import os
import pandas as pd


TEST_NYT_TINY = os.path.join(os.getcwd(), "tests/nyt_tiny.csv")


def test_extract_data():

    nyt_data = extract_data(TEST_NYT_TINY)
    assert nyt_data.shape == (28, 3)


def test_transform_nyt_dataset_no_start_date():
    nyt_data = extract_data(TEST_NYT_TINY)
    nyt_clean_data = transform_nyt_dataset(nyt_data)

    assert nyt_clean_data.index[0] == pd.to_datetime("2020-03-08")
    assert nyt_clean_data.shape == (28, 2)
    assert nyt_clean_data["cases"][0] == 547
    assert nyt_clean_data["deaths"][0] == 22


def test_transform_nyt_dataset_same_start_date():
    nyt_data = extract_data(TEST_NYT_TINY)
    nyt_clean_data = transform_nyt_dataset(nyt_data, datetime.strptime("2020-03-08", "%Y-%m-%d"))

    assert nyt_clean_data.index[0] == pd.to_datetime("2020-03-08")
    assert nyt_clean_data.shape == (28, 2)
    assert nyt_clean_data["cases"][0] == 547
    assert nyt_clean_data["deaths"][0] == 22


def test_transform_nyt_dataset_after_start_date():
    nyt_data = extract_data(TEST_NYT_TINY)
    nyt_clean_data = transform_nyt_dataset(nyt_data, datetime.strptime("2020-03-09", "%Y-%m-%d"))

    assert nyt_clean_data.index[0] == pd.to_datetime("2020-03-09")
    assert nyt_clean_data.shape == (27, 2)
    assert nyt_clean_data["cases"][0] == 748
    assert nyt_clean_data["deaths"][0] == 26


def test_transform_nyt_dataset_same_last_date():
    nyt_data = extract_data(TEST_NYT_TINY)
    nyt_clean_data = transform_nyt_dataset(nyt_data, datetime.strptime("2020-04-04", "%Y-%m-%d"))

    assert nyt_clean_data.index[0] == pd.to_datetime("2020-04-04")
    assert nyt_clean_data.shape == (1, 2)
    assert nyt_clean_data["cases"][0] == 312525
    assert nyt_clean_data["deaths"][0] == 9488


def test_transform_nyt_dataset_after_last_date():
    nyt_data = extract_data(TEST_NYT_TINY)
    nyt_clean_data = transform_nyt_dataset(nyt_data, datetime.strptime("2020-04-05", "%Y-%m-%d"))

    assert nyt_clean_data.shape == (0, 2)
