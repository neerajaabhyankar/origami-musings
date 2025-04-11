from viz_imports import *


ratio_to_swarval = lambda ff: np.log2(ff) * 12
swarvals = [
    ratio_to_swarval(tn.node_frequencies[ii]) for ii in range(len(tn.node_names))
]

achal_nodes = [(0, 0), (1, 0)]

# for an arbitrary raag
raag_nodecolor = {
    "custom": "#f08b65",
}
raag_gt_nodes = {
    "custom": [],
}
nnotes = input("Enter the number of notes in your Raag:\n")
for ii in range(int(nnotes)):
    print(f"Enter the prime factorization of note {ii+1} in the format `q3, q5`:")
    powers = input().split(", ")
    raag_gt_nodes["custom"].append(tuple(map(int, powers)))


""" interactive plot """

fig = go.Figure()

# all nodes and text
fig.add_trace(go.Scatter3d(
    x=tn.coords3d[0],
    y=tn.coords3d[1],
    z=swarvals,
    mode="text+markers",
    marker=dict(size=SPHERE_SIZE, symbol="circle"),
    marker_color=DARK_GREY,
    text=tn.node_names,
    textposition="middle center",
    textfont=dict(family="Overpass", size=10, color="white"),
    showlegend=False,
))

# raag-specific nodes
for raag, gt_nodes in raag_gt_nodes.items():
    # for the Bhoop-Deshkar viz
    # if raag == "Yaman":
    #     continue
    # gt_node_indices = [tn.node_coordinates.index(coord) for coord in gt_nodes if coord not in achal_nodes]
    
    # for an arbitrary raag
    gt_node_indices = [tn.node_coordinates.index(coord) for coord in gt_nodes]

    fig.add_trace(go.Scatter3d(
        x=np.array(tn.coords3d[0])[gt_node_indices],
        y=np.array(tn.coords3d[1])[gt_node_indices],
        z=np.array(swarvals)[gt_node_indices],
        mode="text+markers",
        marker=dict(
            size=SPHERE_SIZE,
            symbol="circle",
            color=raag_nodecolor[raag],
        ),
        text=np.array(tn.node_names)[gt_node_indices],
        textposition="middle center",
        textfont=dict(family="Overpass", size=DOT_LABEL_SIZE, color="white"),
        showlegend=False,
    ))

# # syntonic comma
# idx_D1 = 18
# idx_D2 = 37
# ratios = ["5/3", "27/16"]
# fig.add_trace(go.Scatter3d(
#     x=[tn.coords3d[0][idx_D1], tn.coords3d[0][idx_D2]],
#     y=[tn.coords3d[1][idx_D1], tn.coords3d[1][idx_D2]],
#     z=[swarvals[idx_D1] + ANNOTATION_OFFSET, swarvals[idx_D2] + ANNOTATION_OFFSET],
#     mode="text",
#     text=ratios,
#     textposition="middle center",
#     textfont=dict(family="Overpass", size=1.5*DOT_LABEL_SIZE, color=ANNOTATION_GREEN),
#     showlegend=False,
# ))

# fig.add_trace(go.Scatter3d(
#     x=[tn.coords3d[0][idx_D1], tn.coords3d[0][idx_D2]],
#     y=[tn.coords3d[1][idx_D1], tn.coords3d[1][idx_D2]],
#     z=[swarvals[idx_D1], swarvals[idx_D2]],
#     mode="lines",
#     line=dict(color=ANNOTATION_GREEN, width=5),
#     showlegend=False,
# ))
# fig.add_trace(go.Scatter3d(
#     x=[(tn.coords3d[0][idx_D1] + tn.coords3d[0][idx_D2]) / 2],
#     y=[(tn.coords3d[1][idx_D1] + tn.coords3d[1][idx_D2]) / 2],
#     z=[(swarvals[idx_D1] + swarvals[idx_D2])/2 + ANNOTATION_OFFSET/2],
#     mode="text",
#     text=["syntonic comma"],
#     textposition="middle center",
#     textfont=dict(family="Overpass", size=1.5*DOT_LABEL_SIZE, color=ANNOTATION_GREEN),
#     showlegend=False,
# ))

# # send the last two traces to the back
# fig.data = (*fig.data[-2:], *fig.data[:-2])

# custom legend

# axes
fig.update_layout(
    scene=dict(
        xaxis_title="powers of " + str(tn.primes[0]),
        yaxis_title="powers of " + str(tn.primes[1]),
        zaxis_title="octave-normalized frequency ratio (relative pitch)",
    ),
    # make axis labels integers only
    scene_xaxis_tickvals=list(range(-tn.powers[0], tn.powers[0] + 1)),
    scene_yaxis_tickvals=list(range(-tn.powers[1], tn.powers[1] + 1)),
    scene_zaxis_tickvals=list(range(-1, 13)),
)

fig.show(scale=2)
