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

def calc_dimensions(df, unquantifiable):
    subj_ctr = 0
    for col in df.columns:
        if (col in unquantifiable):
            continue
        subj_ctr += 1
    x_dim = math.floor(math.sqrt(subj_ctr))
    y_dim = math.ceil(subj_ctr/x_dim)
    return x_dim, y_dim

def fill_final_grouping(local_houses, houses, col_data):
    final_grouping = {}
    for entry in houses:
        final_grouping[entry] = []

    ctr = 0
    for entry in local_houses:
        if (entry in houses):
            final_grouping[entry].append(col_data[ctr])
        ctr += 1
    return final_grouping

def set_up_plots(
        plots,
        houses,
        g_ctr,
        x_dim,
        y_dim,
        final_grouping,
        col):
    ctr = 0
    houses_hatching = "-/\\|"
    for entry in houses:
        plots[g_ctr % x_dim, g_ctr // x_dim].hist(
            final_grouping[entry],
            alpha=0.5,
            color=(
                0.0+ctr*0.2,
                (0.7+ctr*0.2) % 1.0,
                1.0-ctr*0.2
            ),
            hatch=houses_hatching[ctr],
            label=entry
        )
        ctr += 1
    plots[g_ctr % x_dim, g_ctr // x_dim].set_title(col)
#
# (example + generalization)
# x_dim = 4, y_dim = 3
# linear = x + y * x_dim => x =  linear - y * x_dim  = linear  % x_dim
#                           y = (linear - x) / x_dim = linear // x_dim
#   x--->
#  y
#  |  0, 0 | 1, 0 | 2, 0 | 3, 0
#  v  0, 1 | 1, 1 | 2, 1 | 3, 1
#     0, 2 | 1, 2 | 2, 2 | 3, 2
#
def draw_histograms_except(df, unquantifiable, houses):
    if (df is None):
        raise DfNoneError
    all_houses = df["Hogwarts House"]
    x_dim, y_dim = calc_dimensions(df, unquantifiable)
    fig, plots = plt.subplots(x_dim, y_dim)
    g_ctr = 0
    for col in df.columns:
        if (col in unquantifiable):
            continue
        # initial data structures setup and cleanup.
        # it might be better to keep everything as dfs since they probably
        #are more optimized than python loops for filtering data by
        #value-based criteria
        col_data = df[col].copy().to_numpy()
        nanned_stuff, col_data = anti_nan(col_data)

        local_houses = all_houses.copy().drop(index=nanned_stuff)

        final_grouping = fill_final_grouping(local_houses, houses, col_data)

        set_up_plots(
            plots,
            houses,
            g_ctr,
            x_dim,
            y_dim,
            final_grouping,
            col
        )
        g_ctr += 1
    while (g_ctr < x_dim * y_dim):
        fig.delaxes(plots[g_ctr % x_dim, g_ctr // x_dim])
        g_ctr += 1
    plt.legend()
    plt.show()

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        draw_histograms_except(df, [
            "Index",
            "Hogwarts House",
            "First Name",
            "Last Name",
            "Birthday",
            "Best Hand",
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
