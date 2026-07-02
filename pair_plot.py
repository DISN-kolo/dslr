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
from histogram import draw_hist
from mock_scatter_plot import draw_scatter_plot

def draw_pairplots_of(df, fields_to_draw, houses):
    if (df is None):
        raise DfNoneError
    all_houses = df["Hogwarts House"]
    fig, plots = plt.subplots(len(fields_to_draw), len(fields_to_draw))
    # All nans as in an array of arrays of nanned indicies per column.
    # Used for caching, basically.
    all_nans = {}
    # a triangle of nan intersections, cached. diagonal just remains empty.
    # index thru as [index_y][index_x - index_y]
    fields_amt = len(fields_to_draw)
    nanned_stuff_xy = [
        [
            set() for j in range(i, fields_amt)
        ] for i in range(fields_amt)
    ]

    index_y = 0
    for field_y in fields_to_draw:
        print(f"   entered y: {index_y:3d}: {field_y:20}")
        col_data_y = df[field_y]
        if (field_y not in all_nans):
            all_nans[field_y] = set(just_get_nans(col_data_y))

        nanned_stuff_y = all_nans[field_y]

        index_x = 0
        for field_x in fields_to_draw:
            print(f" entered x: {index_x:3d}: {field_x:20}")
            col_data_x = df[field_x]
            if (index_x < index_y):
                print("reverse on", index_x, index_y)
                current_pair = df[[field_x, field_y]]
                current_pair = current_pair.drop(
                    index=nanned_stuff_xy[index_x][index_y - index_x]
                )

                local_houses = all_houses.copy().drop(
                    index=nanned_stuff_xy[index_x][index_y - index_x]
                )

                final_grouping = current_pair.groupby(local_houses)
                print("reverse scatter draw called")
                draw_scatter_plot(
                    plots[index_y, index_x],
                    houses,
                    final_grouping
                )
                index_x += 1
                continue

            if (field_x == field_y):
                local_houses = all_houses.copy().drop(index=nanned_stuff_y)

                col_data = col_data_y.drop(index=nanned_stuff_y)
                final_grouping = col_data.groupby(local_houses)

                print("histogram draw called")
                draw_hist(
                    plots[index_y, index_x],
                    houses,
                    final_grouping
                )
                index_x += 1
                continue

            if (field_x not in all_nans):
                all_nans[field_x] = set(just_get_nans(col_data_x))

            nanned_stuff_x = all_nans[field_x]
            nanned_stuff_xy[
                    index_y][
                    index_x - index_y] = nanned_stuff_x.union(
                nanned_stuff_y
            )
            current_pair = df[[field_x, field_y]]
            current_pair = current_pair.drop(
                index=nanned_stuff_xy[index_y][index_x - index_y]
            )

            local_houses = all_houses.copy().drop(
                index=nanned_stuff_xy[index_y][index_x - index_y]
            )

            final_grouping = current_pair.groupby(local_houses)
            print("scatter draw called")
            draw_scatter_plot(
                plots[index_y, index_x],
                houses,
                final_grouping
            )
            index_x += 1
        index_y += 1

    for index, field in enumerate(fields_to_draw):
        plots[0, index].set_title(field)
        plots[index, 0].set_ylabel(field)

    for single_plot in plots.flat:
        single_plot.set_box_aspect(1)

    handles, labels = plots[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower right')
    fig.subplots_adjust(top=0.98, bottom=0.02)
    plt.show()


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
