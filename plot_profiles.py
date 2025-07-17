import uproot
import numpy as np
import matplotlib.pyplot as plt
import os

filename = "build/output.root"  # Adjust path if needed

with uproot.open(filename) as file:
    # 1D Histograms
    hRadial = file["hRadial"]
    hLong   = file["hLong"]
    hTotal  = file["hTotal"]

    # 2D Histogram
    hXY = file["hXY"]

    # Layered 2D Histograms
    layer_histos = {key: file[key] for key in file.keys() if key.startswith("hXY_layer")}

# --- Plot hRadial ---
edges = hRadial.axis().edges()
values = hRadial.values()
centers = 0.5 * (edges[1:] + edges[:-1])

plt.figure()
plt.plot(centers, values, drawstyle="steps-mid")
plt.title("Radial Energy Deposition")
plt.xlabel("Radius [mm]")
plt.ylabel("Energy [MeV]")
plt.grid()
plt.savefig("plot_radial.png")

# --- Plot hLong ---
edges = hLong.axis().edges()
values = hLong.values()
centers = 0.5 * (edges[1:] + edges[:-1])

plt.figure()
plt.plot(centers, values, drawstyle="steps-mid", color="green")
plt.title("Longitudinal Energy Deposition")
plt.xlabel("Z [mm]")
plt.ylabel("Energy [MeV]")
plt.grid()
plt.savefig("plot_longitudinal.png")

# --- Plot hTotal ---
plt.figure()
plt.bar(["Total"], hTotal.values(), color="orange")
plt.title("Total Energy Deposition")
plt.ylabel("Energy [MeV]")
plt.savefig("plot_total.png")

# --- Plot hXY heatmap ---
x_edges = hXY.axis(0).edges()
y_edges = hXY.axis(1).edges()
z_vals = hXY.values()

plt.figure()
plt.pcolormesh(x_edges, y_edges, z_vals.T, shading='auto')
plt.xlabel("X [mm]")
plt.ylabel("Y [mm]")
plt.title("XY Energy Deposition")
plt.colorbar(label="Energy [MeV]")
plt.axis('equal')
plt.savefig("plot_xy.png")

# --- Plot layered XYs (up to 6 layers) ---
for i, (key, hist) in enumerate(sorted(layer_histos.items())[:6]):
    x_edges = hist.axis(0).edges()
    y_edges = hist.axis(1).edges()
    z_vals = hist.values()

    plt.figure()
    plt.pcolormesh(x_edges, y_edges, z_vals.T, shading='auto')
    plt.xlabel("X [mm]")
    plt.ylabel("Y [mm]")
    plt.title(f"{key} Energy Deposition")
    plt.colorbar(label="Energy [MeV]")
    plt.axis('equal')
    plt.savefig(f"{key}.png")

print("✅ Plots saved as PNG.")

