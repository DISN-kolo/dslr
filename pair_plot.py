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

def draw_pairplots_of(df, fields_to_draw, houses):
    if (df is None):
        raise DfNoneError
    all_houses = df["Hogwarts House"]
    fig, plots = plt.subplots(len(fields_to_draw), len(fields_to_draw))
    # All nans as in an array of arrays of nanned indicies per column.
    # Used for caching, basically.
    all_nans = {}
    # nan intersections, cached. Note that the diagonal is not cached,
    #as diagonals are just histograms of a single column and do not
    #require any intersections.
    # to go thru, use [index_y - 1][index_x - 1], since the diagonal is empty.
    fields_amt = len(fields_to_draw)
    nanned_stuff_xy = [
        [
            set() for j in range(i, fields_amt - 1)
        ] for i in range(fields_amt - 1)
    ]

    index_x = 0
    for field_x in fields_to_draw:
        if (field_x not in all_nans):
            all_nans[field_x] = just_get_nans(col_x_data)
        nanned_stuff_x = set(all_nans[field_x])

        index_y = 0
        for field_y in fields_to_draw:
            if (field_x == field_y):
                draw_histogram()
                continue
            if (field_y not in all_nans):
                all_nans[field_y] = just_get_nans(col_y_data)
            nanned_stuff_y = set(all_nans[field_y])
            nanned_stuff_xy[


if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        draw_pairplots_of(df, [
            "Astronomy",
            "Divination",
            "History of Magic",
            "Muggle Studies",
            "Charms",
            "Anctient Runes",
        ],
        [
            "Ravenclaw",
            "Slytherin",
            "Gryffindor",
            "Hufflepuff",
        ])
    except Exception as exc:
        exit_by_exception(exc, sys.argv[1])
