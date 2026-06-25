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
    for col in df.columns:
        if (col in unquantifiable):
            continue
        col_data = df[col].copy().to_numpy()
        nanned_stuff, col_data = anti_nan(col_data)
        plt.hist(col_data, alpha=0.1)
        plt.title(col)
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
