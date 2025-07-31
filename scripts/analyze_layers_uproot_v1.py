import uproot
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import csv

# --- Open ROOT file ---
file = uproot.open("../build/output.root")
print("Opened ROOT file: ../build/output.root")

# --- Get all hLayer histograms ---
layer_histos = {k: file[k] for k in file.keys() if re.match(r"hLayer\d+", k)}
print(f"Found {len(layer_histos)} layer histograms.")

# --- Sort by layer index ---
layer_histos = dict(sorted(layer_histos.items(), key=lambda kv: int(re.findall(r"\d+", kv[0])[0])))

# --- Prepare results ---
layer_indices = []
means = []
stddevs = []

# --- Ensure output directory exists ---
os.makedirs("plots", exist_ok=True)

# --- Process each layer ---
for name, hist in layer_histos.items():
    bin_edges = hist.axis().edges()
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    counts = hist.values()

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

    # --- Print debug info ---
    print(f"Layer {idx:2d} → Mean = {mean:.2f} MeV, StdDev = {std:.2f} MeV, Total Counts = {int(total)}")

    # --- Save plot with cleaned name ---
    clean_name = name.split(";")[0]  # Remove ROOT histogram version suffix
    plt.figure()
    plt.bar(bin_centers, counts, width=np.diff(bin_edges), color="skyblue", edgecolor="k")
    plt.title(f"Layer {idx}: Mean = {mean:.2f} MeV, StdDev = {std:.2f} MeV")
    plt.xlabel("Energy Deposition (MeV)")
    plt.ylabel("Counts")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"plots/{clean_name}.png")
    plt.close()

# --- Summary plot ---
plt.figure(figsize=(10, 6))
plt.errorbar(layer_indices, means, yerr=stddevs, fmt='o-', color='darkblue', ecolor='orange', capsize=3)
plt.title("Mean Energy Deposition per Layer with StdDev")
plt.xlabel("Layer Number")
plt.ylabel("Energy Deposition (MeV)")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/layer_mean_stddev.png")
plt.close()
print("✅ Summary plot saved: plots/layer_mean_stddev.png")

# --- Save to CSV ---
csv_path = "plots/layer_stats.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Layer", "Mean (MeV)", "StdDev (MeV)"])
    for i, m, s in zip(layer_indices, means, stddevs):
        writer.writerow([i, f"{m:.4f}", f"{s:.4f}"])
print(f"✅ Statistics saved to CSV: {csv_path}")

