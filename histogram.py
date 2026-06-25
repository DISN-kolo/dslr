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

def draw_histograms_except(df, unquantifiable, houses):
    if (df is None):
        raise DfNoneError
    all_houses = df["Hogwarts House"]
    # FIXME magic number
    fig, plots = plt.subplots(4, 4)
    g_ctr = 0
    for col in df.columns:
        if (col in unquantifiable):
            continue
        col_data = df[col].copy().to_numpy()
        nanned_stuff, col_data = anti_nan(col_data)
        local_houses = all_houses.copy().drop(index=nanned_stuff)
        final_grouping = {}
        for entry in houses:
            final_grouping[entry] = []
        ctr = 0
        for entry in local_houses:
            if (entry in houses):
                final_grouping[entry].append(col_data[ctr])
            ctr += 1
        ctr = 0
        houses_hatching = "-/\\|"
        for entry in houses:
            plots[g_ctr // 4, g_ctr % 4].hist(
                final_grouping[entry],
                alpha=0.5,
                color=(
                    0.1+ctr*0.1,
                    0.5,
                    0.8-ctr*0.1
                ),
                hatch=houses_hatching[ctr],
                label=entry
            )
            ctr += 1
        plots[g_ctr // 4, g_ctr % 4].set_title(col)
        g_ctr += 1
    # FIXME magic number
    while (g_ctr < 16):
        fig.delaxes(plots[g_ctr // 4, g_ctr % 4])
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
