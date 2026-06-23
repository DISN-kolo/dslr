#!venv/bin/python

import pandas as pd
import numpy as np
import sys

from utils.csv_reading import read_or_raise
import utils.additional_exceptions
from utils.additional_utils import exit_with_print, exit_by_exception
from utils.stat_helpers import *

def describe_necessary_cols(df):
    if (df is None):
        raise DfNoneError
    for col in df.columns:
        print(col)

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        print(df)
        describe_necessary_cols(df)
    except Exception as exc:
        exit_by_exception(exc, sys.argv[1])
