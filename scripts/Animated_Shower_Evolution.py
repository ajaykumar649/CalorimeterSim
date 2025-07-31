import uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Load ROOT file
file = uproot.open("../build/output.root")
layers = []
i = 0
while f"hLayer{i}" in file:
    layers.append(file[f"hLayer{i}"].to_numpy())
    i += 1

if not layers:
    raise ValueError("No hLayer histograms found.")

# Create animation folder
os.makedirs("plots", exist_ok=True)

# Extract binning
bin_edges = layers[0][1]
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
n_frames = len(layers)

fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot([], [], lw=2, color='blue')
ax.set_xlim(bin_centers[0], bin_centers[-1])
ax.set_ylim(1, max([max(c) for c, _ in layers]) * 1.2)
ax.set_xlabel("Energy Deposition (MeV)")
ax.set_ylabel("Counts")
ax.set_title("Shower Development in Layers")
ax.set_yscale("log")

def update(frame):
    counts, _ = layers[frame]
    line.set_data(bin_centers, counts)
    ax.set_title(f"Shower Energy Deposition - Layer {frame}")
    return line,

ani = animation.FuncAnimation(fig, update, frames=n_frames, blit=True)
ani.save("plots/shower_evolution.gif", writer='pillow', fps=5)

print("✅ Animated shower evolution saved to plots/shower_evolution.gif")

