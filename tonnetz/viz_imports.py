import libmogra as lm

# from libmogra import tonnetz
# tonnetz doesn't exist there yet, so meanwhile
import mock_tonnetz as tonnetz
import bisect

import numpy as np
import plotly.graph_objects as go
from vedo import Plotter, Point, Points, Text3D, Axes, Line, Box, show

# color scheme
DARK_GREY = "#323539"
LIGHT_GREY = "#dcd8cf"
BG_GREY = "#f3f3f3"
POSTER_BG_GREY = "#f0ebe9"
WRONG_RED = "#a83232"
ANNOTATION_GREEN = "#3e7a32"
SPHERE_SIZE = 14
DOT_SIZE = 21
DOT_LABEL_SIZE = 13
ANNOTATION_OFFSET = 0.5

# define the net
gs = tonnetz.EFGenus.from_list([3, 3, 3, 3, 5, 5])
tn = tonnetz.Tonnetz(gs)
et_tones = np.arange(0, 12, 0.5)

raag_gt_ratios = {
    "Bhoop": [1, 10 / 9, 5 / 4, 3 / 2, 5 / 3],
    "Deshkar": [1, 9 / 8, 81 / 64, 3 / 2, 27 / 16],
    "Yaman": [1, 9 / 8, 5 / 4, 45 / 32, 3 / 2, 27 / 16, 15 / 8],
}
raag_gt_nodes = {
    "Bhoop": [(0, 0), (1, 0), (0, 1), (-1, 1), (-2, 1)],
    "Deshkar": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    "Yaman": [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1), (0, 1), (3, 0)],
}
raag_nodecolor = {
    "Bhoop": "#f08b65",
    "Deshkar": "#f4c05b",
    "Yaman": "#b06b83",
}
