import uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LogNorm, Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.mplot3d import Axes3D
import os
import re

# ---------- Config ----------
filename = "../build/output.root"
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# ---------- Load ROOT file ----------
with uproot.open(filename) as file:
    def safe_get(name):
        return file[name] if name in file else None

    hRadial = safe_get("hRadial")
    hLong   = safe_get("hLong")
    hTotal  = safe_get("hTotal")
    hXY     = safe_get("hXY")

    layer_histos = {
        int(re.search(r"\d+", key).group()): file[key]
        for key in file.keys()
        if key.startswith("hXY_layer")
    }
    layer_histos = dict(sorted(layer_histos.items()))


# ---------- Plot 1D ----------
def plot_1d(hist, title, xlabel, outname, color="blue"):
    if hist:
        edges = hist.axis().edges()
        values = hist.values()
        centers = 0.5 * (edges[1:] + edges[:-1])
        plt.figure()
        plt.plot(centers, values, drawstyle="steps-mid", color=color)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("Energy [MeV]")
        plt.grid(True)
        plt.savefig(f"{output_dir}/{outname}")
        plt.close()

plot_1d(hRadial, "Radial Energy Deposition", "Radius [mm]", "plot_radial.png")
plot_1d(hLong, "Longitudinal Energy Deposition", "Z [mm]", "plot_longitudinal.png", color="green")

if hTotal:
    plt.figure()
    plt.bar(["Total"], hTotal.values(), color="orange")
    plt.title("Total Energy Deposition")
    plt.ylabel("Energy [MeV]")
    plt.savefig(f"{output_dir}/plot_total.png")
    plt.close()

# ---------- Plot full-layer hXY heatmap ----------
if hXY:
    x_edges = hXY.axis(0).edges()
    y_edges = hXY.axis(1).edges()
    z_vals = hXY.values()

    plt.figure()
    plt.pcolormesh(x_edges, y_edges, z_vals.T, shading='auto', cmap='viridis')
    plt.xlabel("X [mm]")
    plt.ylabel("Y [mm]")
    plt.title("XY Energy Deposition (All Layers)")
    plt.colorbar(label="Energy [MeV]")
    plt.axis("equal")
    plt.savefig(f"{output_dir}/plot_xy.png")
    plt.close()

# ---------- Plot N layered 2D hXY ----------
N = 6
for i, (layer, hist) in enumerate(layer_histos.items()):
    if i >= N:
        break
    x_edges = hist.axis(0).edges()
    y_edges = hist.axis(1).edges()
    z_vals = hist.values()

    plt.figure()
    plt.pcolormesh(x_edges, y_edges, z_vals.T, shading='auto', cmap='viridis')
    plt.xlabel("X [mm]")
    plt.ylabel("Y [mm]")
    plt.title(f"XY Energy Deposition - Layer {layer}")
    plt.colorbar(label="Energy [MeV]")
    plt.axis("equal")
    plt.savefig(f"{output_dir}/hXY_layer{layer:02d}.png")
    plt.close()

print(f"✅ Plots saved to: {output_dir}/")


# ---------- Animation of Layered 2D XY ----------
if layer_histos:
    fig, ax = plt.subplots()
    first_hist = next(iter(layer_histos.values()))
    x_edges = first_hist.axis(0).edges()
    y_edges = first_hist.axis(1).edges()

    all_values = np.array([h.values() for h in layer_histos.values()])
    positive_vals = all_values[all_values > 0]

    if positive_vals.size == 0:
        print("⚠️ All values are non-positive, using linear color scale.")
        norm = Normalize(vmin=0, vmax=np.max(all_values))
    else:
        norm = LogNorm(vmin=np.min(positive_vals), vmax=np.max(positive_vals))

    mesh = ax.pcolormesh(x_edges, y_edges, first_hist.values().T, shading='auto', cmap='viridis', norm=norm)
    cbar = fig.colorbar(ScalarMappable(norm=norm, cmap='viridis'), ax=ax)
    cbar.set_label("Energy [MeV]")
    title = ax.set_title("")

    # Reversed layer playback (out-in shower)
    reversed_layers = list(reversed(list(layer_histos.items())))

    def update(i):
        layer, hist = reversed_layers[i]
        z_vals = hist.values().T
        mesh.set_array(z_vals.ravel())
        title.set_text(f"Layer {layer} (Out → In)")
        return mesh,

    ani = animation.FuncAnimation(
        fig, update, frames=len(reversed_layers), interval=400, blit=False
    )

    gif_path = f"{output_dir}/hXY_layers_animation.gif"
    ani.save(gif_path, writer='pillow', fps=3)
    print(f"🎞️ 2D Animation saved to: {gif_path}")
    plt.close()


# ---------- 3D Surface Animation ----------
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

X, Y = np.meshgrid(x_edges[:-1], y_edges[:-1])
layer_nums = list(layer_histos.keys())
Z_stack = [layer_histos[l].values().T for l in layer_nums]
Z_stack = np.stack(Z_stack, axis=2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

vmin = np.min(positive_vals) if positive_vals.size > 0 else 0.1
vmax = np.max(positive_vals) if positive_vals.size > 0 else 1.0
norm = LogNorm(vmin=vmin, vmax=vmax)

surf = ax.plot_surface(X, Y, Z_stack[:, :, 0], cmap='viridis', norm=norm)
ax.set_xlabel("X [mm]")
ax.set_ylabel("Y [mm]")
ax.set_zlabel("Energy [MeV]")
title = ax.set_title("")

def update_surface(i):
    ax.clear()
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.set_zlabel("Energy [MeV]")
    ax.set_title(f"Layer {layer_nums[i]} (XY as base, Z=Energy)")
    surf = ax.plot_surface(X, Y, Z_stack[:, :, i], cmap='viridis', norm=norm)
    return surf,

ani3d = animation.FuncAnimation(
    fig, update_surface, frames=len(layer_nums), interval=500, blit=False
)

ani3d.save(f"{output_dir}/hXY_3D_layers.gif", writer='pillow', fps=2)
print(f"🎞️ 3D Layer Animation saved to: {output_dir}/hXY_3D_layers.gif")

