#!venv/bin/python

import pandas as pd
import numpy as np
import sys

from utils.csv_reading import read_or_raise
import utils.additional_exceptions
from utils.additional_utils import (
    exit_with_print,
    exit_by_exception,
)
from utils.stat_helpers import *
from logreg_train import h


# FIXME temporary hardcoded copypasted from output of train
norm_a = [991.4762430143062,
    9.3795,
    10.374352872826613,
    17.810389999999998,
    230.7633055712305
]

norm_b = [24.735697373089806,
    0.6524999999999999,
    1.5153598812160975,
    -243.23853000000003,
    514.6329143048929
]

test_results = {
    'Ravenclaw':
        np.array([
            -1.38802496,
            -1.54994402,
            0.39736225,
            0.35403733,
            2.25893113,
            1.58301215
        ]),
    'Slytherin':
        np.array([
            -1.52484785,
            -1.32176275,
            -2.44723171,
            0.22813242,
            -0.87747906,
            -0.82311417
        ]),
    'Gryffindor':
        np.array([
            -1.53354907,
            0.96558933,
            0.0927625 ,
            -2.17480731,
            -1.26207049,
            1.45867707
        ]),
    'Hufflepuff':
        np.array([
            -1.42420807,
            2.11983912,
            0.79517634,
            1.09124969,
            0.20470371,
            -1.9960594
        ])
}

def normalizer_when_normalization_is_known(cols):
    i = 0
    for col in cols:
        cols[col] -= norm_b[i]
        cols[col] /= norm_a[i]
        i += 1
    return cols

def predict_one(house_name, df, m):
    theta = test_results[house_name]
    res = np.zeros(m)
    for i in range(m):
        res[i] = h(theta, df.iloc[i])
    return res

def helper_func(it):
    res_index = 0
    index = 0
    locmax = -10.0
    for item in it:
        if (item > locmax):
            res_index = index
            locmax = item
        index += 1
    return res_index

def get_verdict(rp, houses, m):
    res = rp
    res['Hogwarts House index'] = res.apply(helper_func, axis=1)
    res['Hogwarts House'] = np.array(houses)[
        res['Hogwarts House index'].to_numpy()
    ]
    return res

def predict_with(df, fields_to_use, houses):
    cols = df[fields_to_use]
    nans, cols_denanned = anti_nan_multiple(cols)
    cols_normalized = normalizer_when_normalization_is_known(cols_denanned)
    cols_normalized.insert(0, 'x0', 1)
    m = ft_count(cols_normalized['x0'])
    resulting_predictions = {}
    for house in houses:
        local_array = predict_one(house, cols_normalized, m)
        resulting_predictions[house] = local_array
    df_rp = pd.DataFrame(resulting_predictions)
    final_verdict = get_verdict(df_rp, houses, m)
    print(final_verdict)

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        # TODO this should accept the subjects from a file.
        # that is to say, logreg_train should write the used subjects
        #down into a used_subjects.csv or something.
        # same with houses I think?
        predict_with(df, [
            "Astronomy",
            "Divination",
            "History of Magic",
#            "Muggle Studies",
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
