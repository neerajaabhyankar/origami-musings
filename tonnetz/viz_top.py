from viz_imports import *

""" independent figures """

for raag, gt_nodes in raag_gt_nodes.items():
    fig = go.Figure(
        data=[
            go.Scatter(
                x=tn.coords3d[0],
                y=tn.coords3d[1],
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

    # axes
    fig.update_layout(
        title=f"Raag {raag}",
        xaxis_title="powers of 3",
        yaxis_title="powers of 5",
        plot_bgcolor=BG_GREY,
        width=820,
        height=500,
    )
    fig.update_xaxes(tickvals=np.arange(-4, 5))
    fig.update_yaxes(tickvals=np.arange(-2, 3))

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
            x=np.array(tn.coords3d[0])[gt_node_indices],
            y=np.array(tn.coords3d[1])[gt_node_indices],
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
        )
    )

# achal nodes
hpt = 0.18
curvept = 1.2 * hpt
for achal_node in achal_nodes:
    fig.add_shape(
        type="path",
        path=f"M {0+achal_node[0]},{-hpt+achal_node[1]} C {curvept+achal_node[0]},{-hpt+achal_node[1]} {curvept+achal_node[0]},{hpt+achal_node[1]} {0+achal_node[0]},{hpt+achal_node[1]} Z",
        xref="x",
        yref="y",
        fillcolor=raag_nodecolor["Deshkar"],
        line=dict(width=0),
        layer="between",
    )
    fig.add_shape(
        type="path",
        path=f"M {0+achal_node[0]},{-hpt+achal_node[1]} C {-curvept+achal_node[0]},{-hpt+achal_node[1]} {-curvept+achal_node[0]},{hpt+achal_node[1]} {0+achal_node[0]},{hpt+achal_node[1]} Z",
        xref="x",
        yref="y",
        fillcolor=raag_nodecolor["Bhoop"],
        line=dict(width=0),
        layer="between",
    )


# rest of the points and text
fig.add_trace(
    go.Scatter(
        x=tn.coords3d[0],
        y=tn.coords3d[1],
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

# axes
fig.update_layout(
    # title=f"Raags Bhoop and Deshkar",
    xaxis_title="powers of 3",
    yaxis_title="powers of 5",
    plot_bgcolor=BG_GREY,
    paper_bgcolor=POSTER_BG_GREY,
    width=820,
    height=500,
    showlegend=False,
)
fig.update_xaxes(tickvals=np.arange(-4, 5))
fig.update_yaxes(tickvals=np.arange(-2, 3))

# custom legend
fig.add_trace(
    go.Scatter(
        x=[-3.8],
        y=[2.8],
        mode="markers+text",
        marker=dict(size=DOT_SIZE, color=raag_nodecolor["Bhoop"]),
        text="Bhoop",
        textposition="middle right",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=[-2.8],
        y=[2.8],
        mode="markers+text",
        marker=dict(size=DOT_SIZE, color=raag_nodecolor["Deshkar"]),
        text="Deshkar",
        textposition="middle right",
        showlegend=False,
    )
)

fig.show(scale=1.5)
