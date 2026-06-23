#!venv/bin/python

import pandas as pd
import numpy as np
import sys

from utils.csv_reading import read_or_raise
import utils.additional_exceptions
from utils.additional_utils import exit_with_print, exit_by_exception
from utils.stat_helpers import *

def describe_necessary_cols(df, unquantifiable):
    if (df is None):
        raise DfNoneError
    for col in df.columns:
        if (col in unquantifiable):
            continue
        col_data = df[col]
        count = ft_count(col_data)
        mean = ft_mean(col_data, count)
        std = ft_std(col_data, count, mean)
#        our_min = ft_min(col_data)
#        our_max = ft_min(col_data)
        sorted_col_data = ft_merge_sort(col_data, 0, count - 1)
        our_min = sorted_col_data[0]
        our_max = sorted_col_data[-1]
        perc25 = ft_percentile(sorted_col_data, count, our_min, our_max, .25)
        perc50 = ft_percentile(sorted_col_data, count, our_min, our_max, .50)
        perc75 = ft_percentile(sorted_col_data, count, our_min, our_max, .75)
        print(col, count, mean, std, our_min, perc25, perc50, perc75, our_max,
                sep="\n")

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        print(df)
        describe_necessary_cols(df, [
            "Index",
            "Hogwarts House",
            "First Name",
            "Last Name",
            "Birthday",
            "Best Hand",
        ])
    except Exception as exc:
        exit_by_exception(exc, sys.argv[1])
