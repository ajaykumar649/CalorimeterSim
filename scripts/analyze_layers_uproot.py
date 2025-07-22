import uproot
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# Open ROOT file
file = uproot.open("output.root")

# Get all layer histograms
layer_histos = {k: file[k] for k in file.keys() if re.match(r"hLayer\d+", k)}

# Sort by layer index
layer_histos = dict(sorted(layer_histos.items(), key=lambda kv: int(re.findall(r"\d+", kv[0])[0])))

# Arrays to store results
layer_indices = []
means = []
stddevs = []

# Output directory
os.makedirs("plots", exist_ok=True)

# Process each histogram
for name, hist in layer_histos.items():
    bin_edges = hist.axis().edges()
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    counts = hist.values()

    # Normalize to avoid NaNs
    total = np.sum(counts)
    if total == 0:
        mean = 0
        std = 0
    else:
        mean = np.sum(bin_centers * counts) / total
        variance = np.sum(((bin_centers - mean) ** 2) * counts) / total
        std = np.sqrt(variance)

    idx = int(re.findall(r"\d+", name)[0])
    layer_indices.append(idx)
    means.append(mean)
    stddevs.append(std)

    # Plot each histogram
    plt.figure()
    plt.bar(bin_centers, counts, width=np.diff(bin_edges), color="skyblue", edgecolor="k")
    plt.title(f"Layer {idx}: Mean = {mean:.2f} MeV, StdDev = {std:.2f} MeV")
    plt.xlabel("Energy Deposition (MeV)")
    plt.ylabel("Counts")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"plots/{name}.png")
    plt.close()

# Summary plot: Mean and StdDev vs. Layer
plt.figure(figsize=(10, 6))
plt.errorbar(layer_indices, means, yerr=stddevs, fmt='o-', color='darkblue', ecolor='orange', capsize=3)
plt.title("Mean Energy Deposition per Layer with StdDev")
plt.xlabel("Layer Number")
plt.ylabel("Energy Deposition (MeV)")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/layer_mean_stddev.png")
plt.close()

# Save CSV
import csv
with open("plots/layer_stats.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Layer", "Mean (MeV)", "StdDev (MeV)"])
    for i, m, s in zip(layer_indices, means, stddevs):
        writer.writerow([i, f"{m:.4f}", f"{s:.4f}"])

print(f"✅ Plots saved to ./plots and stats saved to layer_stats.csv")

