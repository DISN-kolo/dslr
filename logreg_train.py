#!venv/bin/python

import pandas as pd
import numpy as np
import sys

from utils.csv_reading import read_or_raise, read_subjects_or_raise
import utils.additional_exceptions
from utils.additional_utils import (
    exit_with_print,
    exit_by_exception,
)
from utils.stat_helpers import *

def J(theta, m, y, x, hs_cached):
    res = 0
    for i in range(m):
        h_cached = h(theta, x.iloc[i])
        hs_cached[i] = h_cached
        res += (
            (
                y.iloc[i] * np.log(h_cached)
                + (1.0 - y.iloc[i])*np.log(1.0 - h_cached)
            ) / m
        )
    return res, hs_cached

def g(z):
    return 1.0 / (1.0 + np.exp(-z))

def h(theta, x):
    return g(np.dot(theta, x))

# per-axis. 
def dJ_dtheta(hs_cached, y, xj, m):
    res = 0
    for i in range(m):
        res += (
            (hs_cached[i] - y.iloc[i]
            )
            * xj.iloc[i] / m
        )
    return res

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
# y_i is the Hogwarts House yes/no 1/0.
# x_i is the vector of subject scores.
def run_singular_logreg(y_and_x, m):
    eta = 0.1
    hs_cached = np.zeros(m)
    y = y_and_x.iloc[:, 0]
    x = y_and_x.iloc[:, 1:]
    theta = np.array([0.0 for column in x])
    dJ = np.array([0.0 for column in x])
    J_now, hs_cached = J(theta, m, y, x, hs_cached)
    J_old = J_now * 10
    i = 0
    while (abs(J_old - J_now) > 1e-6 and i < 200):
        print(
            f"Iteration {i:5d}, "\
            f"J_now: {J_now:16.10g}, diff: {abs(J_old - J_now):16.10g}"
        )
        j = 0
        for col in x:
            dJ[j] = dJ_dtheta(hs_cached, y, x[col], m)
            j += 1
        theta = theta - eta * dJ
#        print("theta now:", theta)
        J_old = J_now
        J_now, hs_cached = J(theta, m, y, x, hs_cached)
        i += 1
    print(
        f"after quiting on {i:5d}, "\
        f"J_now: {J_now:16.10g}, diff: {abs(J_old - J_now):16.10g}"
    )
    print("==========================\n\n")
    return theta

def logreg(tables, m):
    thetas = {}
    for house in tables.keys():
        thetas[house] = run_singular_logreg(tables[house], m)
    return thetas

def train_with(
        df,
        fields_to_use,
        houses,
        thetas_path='thetas.csv',
        norms_path='norms.csv'):
    cols = df[fields_to_use]
    nans, cols_denanned = anti_nan_multiple(cols)
    # field = field_normalized * a + b
    # of course, the x0 = 1 field is not normalized
    cols_normalized, norm_a, norm_b = normalize_all(cols_denanned)
    print(norm_a)
    print(norm_b)
    # x_j for j == 0 is equal to 1 in order to reproduce a
    # y = theta_0 + theta_1 * x_1 + theta_2 * x_2 ...
    cols_normalized.insert(0, 'x0', 1)
    m = ft_count(cols_normalized['x0'])

    all_houses = df["Hogwarts House"]
    all_houses = all_houses.drop(index = nans)

    house_labels = houses_to_binary(all_houses, houses)

    joined_tables = join_houses_and_cols(house_labels, cols_normalized)

    thetas = logreg(joined_tables, m)
    print(thetas)

    thetas_df = pd.DataFrame.from_dict(
        thetas, orient='index', columns=cols_normalized.columns
    )
    thetas_df.index.name = 'House'
    thetas_df.to_csv(thetas_path)

    norms_df = pd.DataFrame(
        {'norm_a': norm_a, 'norm_b': norm_b}, index=fields_to_use
    )
    norms_df.index.name = 'field'
    norms_df.to_csv(norms_path)

if __name__=="__main__":
    if (len(sys.argv) not in (2, 4, 5)):
        exit_with_print(
            1,
            f"Usage: {sys.argv[0]} <path/to/csv> "\
            "[<path/to/thetas_out.csv> <path/to/norms_out.csv> "\
            "[<path/to/subjects.subjects>]]"
        )
    if (len(sys.argv) >= 4):
        thetas_path = sys.argv[2]
        norms_path = sys.argv[3]
    else:
        thetas_path = 'thetas.csv'
        norms_path = 'norms.csv'
    if (len(sys.argv) == 5):
        subjects_path = sys.argv[4]
    else:
        subjects_path = None
    try:
        df = read_or_raise(sys.argv[1])
        if (subjects_path is not None):
            fields_to_use = read_subjects_or_raise(subjects_path)
        else:
            fields_to_use = [
                "Astronomy",
                "Divination",
                "History of Magic",
#                "Muggle Studies",
                "Charms",
                "Ancient Runes",
            ]
        train_with(df, fields_to_use,
        [
            "Ravenclaw",
            "Slytherin",
            "Gryffindor",
            "Hufflepuff",
        ],
        thetas_path,
        norms_path)
    except Exception as exc:
        raise exc
        exit_by_exception(exc, sys.argv[1])
