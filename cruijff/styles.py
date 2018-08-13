import matplotlib as mpl

gc = "a0a0a0"

style = {
    "figure.figsize": (10, 5),
    "axes.grid": True,
    "lines.linewidth": 3,
    "axes.spines.bottom": False,
    "axes.spines.left": False,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "grid.alpha": 1.0,
    "grid.color": gc,
    "grid.linestyle": ":",
    "grid.linewidth": 1,
    "lines.dotted_pattern": [0.5, 2],
    "xtick.major.size": 0,
    "xtick.minor.width": 1,
    "ytick.major.size": 0,
    "ytick.color": gc,
    "text.color": gc,
    "xtick.color": gc,
    "ytick.labelsize": "medium",

    "xtick.labelsize": "medium",
    "font.sans-serif": ["Founders Grotesk", "SF UI Text", "Arial",
                        "sans-serif"],
    "font.weight": 500,
    "font.size": 16,
    "axes.labelsize": 14,
}

mpl.style.use(style)
