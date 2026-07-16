#!venv/bin/python

import pandas as pd
import numpy as np
import sys

from utils.csv_reading import read_or_raise
import utils.additional_exceptions
from utils.additional_utils import (
    exit_with_print,
    exit_by_exception,
    ft_pretty_table_print,
)
from utils.stat_helpers import *

def describe_necessary_cols(df, unquantifiable):
    if (df is None):
        raise DfNoneError
    final_table = {
        "Names": [],
        "Count": [],
        "Mean": [],
        "Std": [],
        "Min": [],
        "25%": [],
        "50%": [],
        "75%": [],
        "Max": [],
    }
    for col in df.columns:
        if (col in unquantifiable):
            continue
        final_table["Names"].append(col)
        col_data = df[col].copy()
        nanned_stuff, col_data = anti_nan(col_data)
        col_data = col_data.to_numpy()
        count = ft_count(col_data)
        mean = ft_mean(col_data, count)
        std = ft_std(col_data, count, mean)
#        our_min = ft_min(col_data)
#        our_max = ft_min(col_data)
        sorted_col_data = col_data.copy()
        sorted_col_data = ft_merge_sort(sorted_col_data, 0, count - 1)
        our_min = sorted_col_data[0]
        our_max = sorted_col_data[-1]
        perc25 = ft_percentile(sorted_col_data, count, our_min, our_max, .25)
        perc50 = ft_percentile(sorted_col_data, count, our_min, our_max, .50)
        perc75 = ft_percentile(sorted_col_data, count, our_min, our_max, .75)
        final_table["Count"].append(count)
        final_table["Mean"].append(mean)
        final_table["Std"].append(std)
        final_table["Min"].append(our_min)
        final_table["25%"].append(perc25)
        final_table["50%"].append(perc50)
        final_table["75%"].append(perc75)
        final_table["Max"].append(our_max)
    ft_pretty_table_print(final_table, 15)

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
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
