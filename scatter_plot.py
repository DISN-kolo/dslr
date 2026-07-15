#!venv/bin/python

import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from itertools import combinations

from utils.csv_reading import read_or_raise
import utils.additional_exceptions
from utils.additional_utils import (
    exit_with_print,
    exit_by_exception,
)
from utils.stat_helpers import *

def draw_scatter_plot(
        plot,
        houses,
        final_grouping,
        marker='o',
        show_label=True):
    ctr = 0
    for entry in houses:
        if (entry in final_grouping.groups):
            group = final_grouping.get_group(entry)
            x = group.iloc[:, 0]
            y = group.iloc[:, 1]
            plot.scatter(
                x,
                y,
                alpha=0.2,
                marker=marker,
                color=(
                    (0.3+ctr*0.4) % 1.0,
                    (0.7+ctr*0.2) % 1.0,
                    (1.5-ctr*0.4) % 1.0
                ),
                label=entry if show_label else None
            )
        ctr += 1

def calc_dimensions(fields_to_draw):
    pair_ctr = 0
    for pair in combinations(fields_to_draw, 2):
        pair_ctr += 1
    x_dim = math.floor(math.sqrt(pair_ctr))
    y_dim = math.ceil(pair_ctr/x_dim)
    return x_dim, y_dim

def set_up_plots(
        plots,
        houses,
        g_ctr,
        x_dim,
        y_dim,
        final_grouping,
        field_x,
        field_y):
    plot = plots[g_ctr % x_dim, g_ctr // x_dim]
    draw_scatter_plot(plot, houses, final_grouping)
    plot.set_title(f"{field_x} vs {field_y}")

def draw_scatterplots_except(df, unquantifiable, houses):
    if (df is None):
        raise DfNoneError
    all_houses = df["Hogwarts House"]
    fields_to_draw_proto = list(df)
    fields_to_draw = [
        item for item in fields_to_draw_proto if (item not in unquantifiable)
    ]
    x_dim, y_dim = calc_dimensions(fields_to_draw)
    fig, plots = plt.subplots(x_dim, y_dim)
    g_ctr = 0
    for field_x, field_y in combinations(fields_to_draw, 2):
        pair_data = df[[field_x, field_y]].copy()
        nanned_stuff, pair_data = anti_nan_multiple(pair_data)

        local_houses = all_houses.copy().drop(index=nanned_stuff)

        final_grouping = pair_data.groupby(local_houses)

        set_up_plots(
            plots,
            houses,
            g_ctr,
            x_dim,
            y_dim,
            final_grouping,
            field_x,
            field_y
        )
        g_ctr += 1

    while (g_ctr < x_dim * y_dim):
        fig.delaxes(plots[g_ctr % x_dim, g_ctr // x_dim])
        g_ctr += 1

    handles, labels = plots[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower right')
    plt.show()

if __name__=="__main__":
    if (len(sys.argv) != 2):
        exit_with_print(1, f"Usage: {sys.argv[0]} <path/to/csv>")
    try:
        df = read_or_raise(sys.argv[1])
        draw_scatterplots_except(df, [
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
            ]
        )
    except Exception as exc:
        exit_by_exception(exc, sys.argv[1])
