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


def normalizer_when_normalization_is_known(cols, norms_df):
    for col in cols:
        cols[col] -= norms_df.loc[col, 'norm_b']
        cols[col] /= norms_df.loc[col, 'norm_a']
    return cols

def predict_one(theta, df, m):
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

def predict_with(
        df,
        thetas_df,
        norms_df,
        fields_to_use,
        houses,
        output_path='houses.csv'):
    thetas_df = thetas_df.set_index('House')
    norms_df = norms_df.set_index('field')

    cols = df[fields_to_use]
    nans, cols_denanned = anti_nan_multiple(cols)
    cols_normalized = normalizer_when_normalization_is_known(
        cols_denanned,
        norms_df
    )
    cols_normalized.insert(0, 'x0', 1)
    m = ft_count(cols_normalized['x0'])
    resulting_predictions = {}
    for house in houses:
        theta = thetas_df.loc[house].to_numpy()
        local_array = predict_one(theta, cols_normalized, m)
        resulting_predictions[house] = local_array
    df_rp = pd.DataFrame(resulting_predictions)
    final_verdict = get_verdict(df_rp, houses, m)
    print(final_verdict)

    final_verdict[['Hogwarts House']].to_csv(output_path, index_label='Index')

if __name__=="__main__":
    if (len(sys.argv) != 4 and len(sys.argv) != 5):
        exit_with_print(
            1,
            f"Usage: {sys.argv[0]} <path/to/csv> <path/to/thetas.csv> "\
            "<path/to/norms.csv> [<path/to/houses_out.csv>]"
        )
    if (len(sys.argv) == 5):
        output_path = sys.argv[4]
    else:
        output_path = 'houses.csv'
    try:
        df = read_or_raise(sys.argv[1])
        thetas_df = read_or_raise(sys.argv[2])
        norms_df = read_or_raise(sys.argv[3])
        # TODO this should accept the subjects from a file.
        # that is to say, logreg_train should write the used subjects
        #down into a used_subjects.csv or something.
        # same with houses I think?
        predict_with(
            df,
            thetas_df,
            norms_df,
            [
                "Astronomy",
                "Divination",
                "History of Magic",
#                "Muggle Studies",
                "Charms",
                "Ancient Runes",
            ],
            [
                "Ravenclaw",
                "Slytherin",
                "Gryffindor",
                "Hufflepuff",
            ],
            output_path
        )
    except Exception as exc:
        raise exc
        exit_by_exception(exc, sys.argv[1])
