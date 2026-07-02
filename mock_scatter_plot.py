def draw_scatter_plot(plot, houses, final_grouping):
    ctr = 0
    for entry in houses:
        group = final_grouping.get_group(entry)
        x = group.iloc[:, 0]
        y = group.iloc[:, 1]
        plot.scatter(
            x,
            y,
            alpha=0.5,
            color=(
                (0.3+ctr*0.4) % 1.0,
                (0.7+ctr*0.2) % 1.0,
                (1.5-ctr*0.4) % 1.0
            ),
            label=entry
        )
        ctr += 1
