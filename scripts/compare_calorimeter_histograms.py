# compare_calorimeter_histograms.py

import uproot
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

FILES = {
    "e⁻ 5 GeV (Pb)": "e-_5GeV_10000evt_8mm_G4_Pb_4mm.root",
    "γ 10 GeV (Pb)": "gamma_10GeV_10000evt_8mm_G4_Pb_4mm.root",
    "π⁻ 10 GeV (Fe)": "pi-_10GeV_10000evt_10mm_G4_Fe_5mm.root",
    "μ⁻ 2 GeV (Fe)": "mu-_2GeV_10000evt_5mm_G4_Fe_2mm.root"
}

data_dir = Path("/Users/ajay/Work/geantexercise/CalorimeterSim/Output")


def extract_layer_means(file_path):
    with uproot.open(file_path) as f:
        # Strip off the ;1 using split
        layer_hists = {
            k.split(";")[0]: f[k] for k in f.keys() if k.startswith("hLayer")
        }
        sorted_keys = sorted(layer_hists.keys(), key=lambda x: int(x.replace("hLayer", "")))
        n_layers = len(sorted_keys)
        means = np.zeros(n_layers)
        stds = np.zeros(n_layers)
        for i, key in enumerate(sorted_keys):
            h = layer_hists[key]
            edges = h.axis(0).edges()
            bin_centers = 0.5 * (edges[:-1] + edges[1:])
            contents = h.values()
            total = contents.sum()
            means[i] = np.sum(bin_centers * contents) / total if total > 0 else 0
            stds[i] = np.sqrt(np.sum(((bin_centers - means[i])**2) * contents) / total) if total > 0 else 0
    return means, stds


# 🔍 Load all datasets
profiles = {}
for label, fname in FILES.items():
    full_path = data_dir / fname
    mean, std = extract_layer_means(full_path)
    profiles[label] = {"mean": mean, "std": std}

# 🔷 Plot 1: Mean Energy Profile
plt.figure(figsize=(10, 6))
for label, data in profiles.items():
    plt.plot(data["mean"], label=label)
plt.title(" Mean Energy Deposition per Layer")
plt.xlabel("Layer Number")
plt.ylabel("Mean Energy (MeV)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("compare_hist_shower_profiles.png")
plt.close()

# 🔷 Plot 2: Shower Width (RMS)
plt.figure(figsize=(10, 6))
for label, data in profiles.items():
    plt.plot(data["std"], label=label)
plt.title(" Shower Width (RMS) per Layer")
plt.xlabel("Layer Number")
plt.ylabel("Energy Std Dev (MeV)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("compare_hist_shower_rms.png")
plt.close()

print("✅ Histogram-based comparison done.")
print(" - compare_hist_shower_profiles.png")
print(" - compare_hist_shower_rms.png")

