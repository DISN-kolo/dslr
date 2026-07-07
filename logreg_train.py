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

def train_with(df, fields_to_use, houses):
    cols = df[fields_to_use]
    nans, cols_denanned = anti_nan_multiple(cols)
    

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
        exit_by_exception(exc, sys.argv[1])
