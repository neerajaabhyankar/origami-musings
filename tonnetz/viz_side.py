from viz_imports import *


ratio_to_swarval = lambda ff: np.log2(ff) * 12
swarvals = [
    ratio_to_swarval(tn.node_frequencies[ii]) for ii in range(len(tn.node_names))
]

# shortcut: hardcoding
integer_swarvals = [2, 4, 7, 9]
parallax_x = 0.7
parallax_y = 0.2

""" independent figures """

for raag, gt_nodes in raag_gt_nodes.items():
    fig = go.Figure(
        data=[
            go.Scatter(
                x=np.array(tn.coords3d[0]) * parallax_x
                + np.array(tn.coords3d[1]) * parallax_y,
                y=swarvals,
                mode="text+markers",
                marker=dict(
                    size=DOT_SIZE,
                    symbol="circle",
                    color=[
                        raag_nodecolor[raag] if coord in gt_nodes else DARK_GREY
                        for coord in tn.node_coordinates
                    ],
                ),
                text=tn.node_names,
                textposition="middle center",
                textfont=dict(family="Overpass", size=DOT_LABEL_SIZE, color="white"),
            )
        ]
    )

    # horizontal lines for integer swarvals
    [
        fig.add_shape(
            type="line",
            x0=-4,
            y0=isw,
            x1=4,
            y1=isw,
            line=dict(color=WRONG_RED, width=2),
            opacity=1,
        )
        for isw in integer_swarvals
    ]

    # axes
    fig.update_layout(
        title=f"Raag {raag}",
        xaxis_title="view along tonnetz diagram",
        yaxis_title="normalized frequency ratio",
        plot_bgcolor=BG_GREY,
        width=800,
        height=550,
    )
    fig.update_xaxes(tickvals=np.arange(-4, 5), showticklabels=False)
    fig.update_yaxes(tickvals=np.arange(-1, 13))

    fig.show(scale=1.5)


""" combined figure """

achal_nodes = [(0, 0), (1, 0)]

fig = go.Figure()

# bhoop and deshkar nodes
for raag, gt_nodes in raag_gt_nodes.items():
    if raag == "Yaman":
        continue
    gt_node_indices = [tn.node_coordinates.index(coord) for coord in gt_nodes]

    fig.add_trace(
        go.Scatter(
            x=np.array(tn.coords3d[0])[gt_node_indices] * parallax_x
            + np.array(tn.coords3d[1])[gt_node_indices] * parallax_y,
            y=np.array(swarvals)[gt_node_indices],
            mode="markers",
            marker=dict(
                size=DOT_SIZE,
                symbol="circle",
                color=raag_nodecolor[raag],
                opacity=np.array(
                    [
                        1 if coord not in achal_nodes else 0
                        for coord in tn.node_coordinates
                    ]
                )[gt_node_indices],
            ),
            text=tn.node_names,
            textposition="middle center",
            textfont=dict(family="Overpass", size=DOT_LABEL_SIZE, color="white"),
        )
    )


# achal nodes
hpt = 0.36
curvept = 0.45 * hpt
for achal_node in achal_nodes:
    achal_node_pos = (
        achal_node[0] * parallax_x + achal_node[1] * parallax_y,
        ratio_to_swarval(tn.node_frequencies[tn.node_coordinates.index(achal_node)]),
    )
    fig.add_shape(
        type="path",
        path=f"M {0+achal_node_pos[0]},{-hpt+achal_node_pos[1]} C {curvept+achal_node_pos[0]},{-hpt+achal_node_pos[1]} {curvept+achal_node_pos[0]},{hpt+achal_node_pos[1]} {0+achal_node_pos[0]},{hpt+achal_node_pos[1]} Z",
        xref="x",
        yref="y",
        fillcolor=raag_nodecolor["Deshkar"],
        line=dict(width=0),
        layer="between",
    )
    fig.add_shape(
        type="path",
        path=f"M {0+achal_node_pos[0]},{-hpt+achal_node_pos[1]} C {-curvept+achal_node_pos[0]},{-hpt+achal_node_pos[1]} {-curvept+achal_node_pos[0]},{hpt+achal_node_pos[1]} {0+achal_node_pos[0]},{hpt+achal_node_pos[1]} Z",
        xref="x",
        yref="y",
        fillcolor=raag_nodecolor["Bhoop"],
        line=dict(width=0),
        layer="between",
    )


# rest of the points and text
fig.add_trace(
    go.Scatter(
        x=np.array(tn.coords3d[0]) * parallax_x + np.array(tn.coords3d[1]) * parallax_y,
        y=swarvals,
        mode="text+markers",
        marker=dict(
            size=DOT_SIZE,
            symbol="circle",
            color=DARK_GREY,
            opacity=[
                (
                    1
                    if coord not in (raag_gt_nodes["Bhoop"] + raag_gt_nodes["Deshkar"])
                    else 0
                )
                for coord in tn.node_coordinates
            ],
        ),
        text=tn.node_names,
        textposition="middle center",
        textfont=dict(family="Overpass", size=DOT_LABEL_SIZE, color="white"),
        zorder=3,
    )
)

# horizontal lines for integer swarvals
[
    fig.add_shape(
        type="line",
        x0=-4,
        y0=isw,
        x1=4,
        y1=isw,
        line=dict(color=WRONG_RED, width=2),
        opacity=1,
    )
    for isw in integer_swarvals
]

# axes
fig.update_layout(
    # title=f"Raags Bhoop and Deshkar",
    xaxis_title="view along tonnetz diagram",
    yaxis_title="normalized frequency ratio",
    plot_bgcolor=BG_GREY,
    paper_bgcolor=POSTER_BG_GREY,
    width=800,
    height=550,
    showlegend=False,
)
fig.update_xaxes(tickvals=np.arange(-4, 5), showticklabels=False)
fig.update_yaxes(tickvals=np.arange(-1, 13))

# custom legend
fig.add_trace(
    go.Scatter(
        x=[-3.9],
        y=[10.2],
        mode="markers+text",
        marker=dict(size=DOT_SIZE, color=raag_nodecolor["Bhoop"]),
        text="Bhoop",
        textposition="middle right",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=[-2.9],
        y=[10.2],
        mode="markers+text",
        marker=dict(size=DOT_SIZE, color=raag_nodecolor["Deshkar"]),
        text="Deshkar",
        textposition="middle right",
        showlegend=False,
    )
)

fig.show(scale=1.5)
