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
