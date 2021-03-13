import matplotlib.pyplot as plt

__colors = ["red", "yellow"]
__shapes = ["o", "s"]


def show_grid(grid, colors=None, shapes=None):
    if colors is None and shapes is None:
        colors = __colors
        shapes = __shapes
    n = grid.shape[0]
    for x in range(n + 1):
        plt.plot([-0.5, n + 0.5], [x - 0.5, x - 0.5], "-", color='lightgray')
        plt.plot([x - 0.5, x - 0.5], [-0.5, n + 0.5], '-', color='lightgray')
    plt.xlim([-0.5, n + 0.5])
    plt.ylim([-0.5, n + 0.5])
    for cid in range(n):
        for rid in range(n):
            if grid[rid][cid][0]:
                plt.plot([rid], [cid], "*", markersize=24)
            if grid[rid][cid][1]:
                if grid[rid][cid][2] == 0:
                    edge = "k"
                else:
                    edge = None
                color = "k"
                for i in range(len(colors)):
                    if grid[rid][cid][3 + i]:
                        color = colors[i]
                shape = "."
                for i in range(len(shapes)):
                    if grid[rid][cid][3 + len(colors) + i]:
                        shape = shapes[i]
                alpha = 1.0
                if grid[rid][cid][0]:
                    alpha = 0.5
                plt.plot([rid], [cid], marker=shape, color=color, markersize=12,
                         markeredgecolor=edge, alpha=alpha)
    plt.show()

