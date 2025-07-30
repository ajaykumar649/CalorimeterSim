import uproot
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
os.makedirs("plots", exist_ok=True)

# Open ROOT file
file = uproot.open("../build/output.root")

# --- Total Energy ---
hTotal = file["hTotal"]
x_total = hTotal.axis().edges()
y_total = hTotal.values()

# Set desired range for plotting (in MeV)
min_range = 0
max_range = 1300

# Compute bin centers
bin_centers = 0.5 * (x_total[:-1] + x_total[1:])

# Apply mask to filter data in range
mask = (bin_centers >= min_range) & (bin_centers <= max_range)
x_filtered = bin_centers[mask]
y_filtered = y_total[mask]

plt.figure()
plt.step(x_filtered, y_filtered, where="mid", color="blue")
plt.title("Total Energy Deposition (Zoomed)")
plt.xlabel("E_dep (MeV)")
plt.ylabel("Counts")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/hTotal.png")

# --- Radial and Longitudinal Profiles ---
for key, color, fname, title, xlabel in [
    ("hRadial", "green", "hRadial.png", "Radial Profile", "Radius (mm)"),
    ("hLong", "red", "hLong.png", "Longitudinal Profile", "z (mm)"),
]:
    hist = file[key]
    x = hist.axis().edges()
    y = hist.values()
    plt.figure()
    plt.step(x[:-1], y, where="mid", color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Counts")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"plots/{fname}")

# --- XY Shower Profile (2D Histogram) ---
hXY = file["hXY"]
x_edges = hXY.axis(0).edges()
y_edges = hXY.axis(1).edges()
z_vals = hXY.values()

plt.figure(figsize=(6, 5))
plt.pcolormesh(x_edges, y_edges, z_vals.T, shading='auto', cmap="viridis")
plt.colorbar(label="Counts")
plt.title("XY Shower Profile")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.tight_layout()
plt.savefig("plots/hXY.png")

# --- Layer-wise Energy Analysis ---
layer_means = []
layer_stddevs = []
layer_numbers = []
colors = plt.cm.tab10.colors

for i in range(100):  # Try up to 100 layers
    name = f"hLayer{i}"
    if name not in file:
        break
    hist = file[name]
    x_edges = hist.axis().edges()
    y_vals = hist.values()

    if np.sum(y_vals) == 0:
        mean, std = 0, 0
    else:
        bin_centers = 0.5 * (x_edges[1:] + x_edges[:-1])
        mean = np.average(bin_centers, weights=y_vals)
        std = np.sqrt(np.average((bin_centers - mean) ** 2, weights=y_vals))

    layer_means.append(mean)
    layer_stddevs.append(std)
    layer_numbers.append(i)

# Overlay all layer histograms
plt.figure(figsize=(10, 7))
for i in range(len(layer_numbers)):
    name = f"hLayer{i}"
    hist = file[name]
    x = hist.axis().edges()
    y = hist.values()
    plt.step(x[:-1], y, where="mid", label=f"Layer {i}", color=colors[i % len(colors)])
plt.yscale("log")
plt.xlabel("E_dep (MeV)")
plt.ylabel("Counts")
plt.title("Energy Deposition per Layer")
plt.legend(ncol=2, fontsize="small", loc="upper right")
plt.tight_layout()
plt.savefig("plots/hLayers_overlay.png")

# --- Summary Stats ---
shower_max_layer = int(np.argmax(layer_means))
tail_leakage = float(sum(layer_means[shower_max_layer + 1:]))

print("\n📊 Calorimeter Layer Summary:")
print(f" - Total Layers: {len(layer_means)}")
print(f" - Shower Max: Layer {shower_max_layer} with Mean = {layer_means[shower_max_layer]:.3f} MeV")
print(f" - Tail Leakage (sum beyond max): {tail_leakage:.3f} MeV")

# Table-style output
print("\n Layer |   Mean (MeV)  |  StdDev (MeV)")
print("---------------------------------------")
for i, (mean, std) in enumerate(zip(layer_means, layer_stddevs)):
    print(f"  {i:3d}  |   {mean:10.3f}  |   {std:10.3f}")

# --- Ntuple (Optional) ---
if "hits" in file:
    hits_tree = file["hits"]
    edep = hits_tree["edep"].array(library="np")

    plt.figure()
    plt.hist(edep, bins=100, range=(0, 20), color='gray', histtype='stepfilled', alpha=0.8)
    plt.xlabel("E_dep (MeV)")
    plt.ylabel("Counts")
    plt.title("Energy Deposition from Ntuple")
    plt.tight_layout()
    plt.savefig("plots/edep_from_tree.png")

print("\n✅ All plots and stats saved to ./plots/")

