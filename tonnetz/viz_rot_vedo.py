import libmogra as lm

# from libmogra import tonnetz
# tonnetz doesn't exist there yet, so meanwhile
import mock_tonnetz as tonnetz

import numpy as np
from vedo import Plotter, Point, Points, Text3D, Axes, Line, Box

# color scheme
DARK_GREY = "#323539"
LIGHT_GREY = "#dcd8cf"
WRONG_RED = "#a83232"

# define the net
gs = tonnetz.EFGenus.from_list([3, 3, 3, 3, 5, 5])
tn = tonnetz.Tonnetz(gs)
et_tones = np.arange(0, 12, 0.5)

SPHERE_SIZE = 30

# Plotter
plotter = Plotter(axes=1)

# Points
# points = Points(
#     [list([tn.coords3d[aa][ii] for aa in range(len(tn.coords3d))]) for ii in range(len(tn.node_names))],
#     r=SPHERE_SIZE, c="navy"
# )
points = [
    Point(
        list([tn.coords3d[aa][ii] for aa in range(len(tn.coords3d))]),
        r=SPHERE_SIZE,
        c=DARK_GREY,
    )
    for ii in range(len(tn.node_names))
]
ratio_to_swarval = lambda ff: np.log2(ff) * 12
points_elevations = [
    ratio_to_swarval(tn.node_frequencies[ii]) for ii in range(len(tn.node_names))
]
plotter += points

# Text
texts = [
    Text3D(
        name,
        pos=(tn.coords3d[0][i], tn.coords3d[1][i], tn.coords3d[2][i] + 0.5),
        s=0.2,
        c=LIGHT_GREY,
        justify="center",
    )
    for i, name in enumerate(tn.node_names)
]
plotter += texts

# Axes
RANGE = {
    "X": [-6, 6],
    "Y": [-4, 4],
    "Z": [-1, 13],
}
ax = Axes(
    xrange=RANGE["X"],
    yrange=RANGE["Y"],
    zrange=RANGE["Z"],
    xtitle="3",
    ytitle="5",
    ylabel_rotation=90,
    ztitle="Octave Normalized Frequency",
    axes_linewidth=3,
    grid_linewidth=0.5,
)
ax.SetOrigin(0, 0, 0)
plotter += ax

# Gridlines
for y in range(RANGE["Y"][0], RANGE["Y"][1]):
    for z in range(RANGE["Z"][0], RANGE["Z"][1]):
        line = Line(
            (RANGE["X"][0], y, z), (RANGE["X"][1], y, z), c="lightgray", alpha=0.2
        )
        plotter += line
for x in range(RANGE["X"][0], RANGE["X"][1]):
    for z in range(RANGE["Z"][0], RANGE["Z"][1]):
        line = Line(
            (x, RANGE["Y"][0], z), (x, RANGE["Y"][1], z), c="lightgray", alpha=0.2
        )
        plotter += line
for x in range(RANGE["X"][0], RANGE["X"][1]):
    for y in range(RANGE["Y"][0], RANGE["Y"][1]):
        line = Line(
            (x, y, RANGE["Z"][0]), (x, y, RANGE["Z"][1]), c="lightgray", alpha=0.2
        )
        plotter += line


# Camera
cdict = {
    "position": [0, 0, 50],
    "focalPoint": [0, 0, 6],
    "viewup": [0, 1, 0],
}
# plotter.camera.SetParallelProjection(True)
plotter.show(camera=cdict, interactive=False, axes=1)


# Motion
for angle in range(90):  # TODO: 300 instead of 90
    plotter.camera.Elevation(-0.0001)  # hacky way to pause
    plotter.render()
for angle in range(90):  # 90 steps to rotate by 90 degrees
    plotter.camera.Elevation(-1)  # around the X axis
    # plotter.camera.Azimuth(0.5)  # around the Z axis
    for pp, point in enumerate(points):
        pos = point.pos()
        point.pos([pos[0], pos[1], pos[2] + points_elevations[pp] / 90])
        texts[pp].pos(
            [
                pos[0] + 0.5 * np.sin(np.radians(angle)),
                pos[1],
                pos[2] + points_elevations[pp] / 90 + 0.5 * np.cos(np.radians(angle)),
            ]
        )
        # TODO: fix this rotation
        # texts[pp].rotate_x(-1, around=np.array(pos))  # pos -(0, 0, 0.5)
    plotter.render()

plotter.camera.SetParallelProjection(True)
plotter.show(interactive=True)

"""
TODO:

In the 2D view:
    - gridlines ✅
    - correct zoom ✅
    - pause for a few seconds ✅
    - fix axis location

In the 3D view:
    - rotate text along with the camera ✅ kinda
    - as the camera is moving, elevate the text to normalized fs ✅
    - pause for a few seconds ✅

In the 2D view again:
    - get a paerfect flattened view

Next:
    - Highlight equal temperament frequencies
    - Highlight Bhoop and Deshkar notes in different colors (green, dark yellow, light yellow)
    - Transition to 3D view and back to top view
    - Keep the notes highlighted
"""
