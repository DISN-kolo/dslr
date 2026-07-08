#!venv/bin/python

import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from utils.csv_reading import read_or_raise
import utils.additional_exceptions
from utils.additional_utils import (
    exit_with_print,
    exit_by_exception,
)
from utils.stat_helpers import *

def J(theta, m, y, x, hs_cached):
    res = 0
    for i in range(m):
        h_cached = h(theta, x[i:i+1])
        hs_cached[i] = h_cached
        res += (
            (
                y[i] * np.log(h_cached)
                + (1 - y[i])*np.log(1 - h_cached)
            ) / m
        )
    return res, hs_cached

def g(z):
    return 1 / (1 + np.exp(-z))

def h(theta, x):
    return g(np.dot(theta, x))

def dJ_dtheta(theta, df):
    return

# returns what is basically
# { "House_name": df(index: does_it_belong_to_House_name), .. }
def houses_to_binary(all_houses, houses):
    house_labels = {}
    for house in houses:
        is_house = (all_houses == house)
        house_labels[house] = is_house.astype(int)
    return house_labels

# same structure as houses to binary, but also with the actual
#scores table appended to each house.
def join_houses_and_cols(house_labels, cols):
    joined_tables = {}
    for house_name in house_labels.keys():
        joined_tables[house_name] = pd.concat(
            [house_labels[house_name], cols],
            axis=1
        )
    return joined_tables

# reminder:
# y is the Hogwarts House yes/no 1/0.
# x is the vector of subject scores.
def run_singular_logreg(y_and_x, m):
    thetas = [0 for theta in y_and_x]
    hs_cached = [0 for i in range(m)]
    y = y_and_x.iloc[:, 0]
    x = y_and_x.iloc[:, 1:]
    J_now, hs_cached = J(thetas, m, y, x)
    J_old = J_now * 10
    i = 0
    while (math.abs(J_old - J_now) > 1e-6 and i < 500):
        print(f"Iteration {i:5d}")
        dJ_dtheta(theta, df) # HERE
        J_old = J_now
        J_now, hs_cached = J(thetas, m, y, x)
    return thetas

def logreg(tables, m):
    thetas = {}
    for house in tables.keys():
        thetas[house] = run_singular_logreg(tables[house], m)
    return thetas

def train_with(df, fields_to_use, houses):
    cols = df[fields_to_use]
    nans, cols_denanned = anti_nan_multiple(cols)
    all_houses = df["Hogwarts House"]
    all_houses = all_houses.drop(index = nans)

    house_labels = houses_to_binary(all_houses, houses)

    joined_tables = join_houses_and_cols(house_labels, cols_denanned)

    m = ft_count(cols_denanned.to_numpy())
    thetas = logreg(joined_tables, m)

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        train_with(df, [
            "Astronomy",
            "Divination",
            "History of Magic",
            "Muggle Studies",
            "Charms",
            "Ancient Runes",
        ],
        [
            "Ravenclaw",
            "Slytherin",
            "Gryffindor",
            "Hufflepuff",
        ])
    except Exception as exc:
        raise exc
        exit_by_exception(exc, sys.argv[1])
