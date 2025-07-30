# compare_calorimeter_showers.py

import uproot
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 🔍 Files to compare
FILES = {
    "e- 5 GeV (Pb)": "e-_5GeV_10000evt_8mm_G4_Pb_4mm.root",
    "γ 10 GeV (Pb)": "gamma_10GeV_10000evt_8mm_G4_Pb_4mm.root",
    "π⁻ 10 GeV (Fe)": "pi-_10GeV_10000evt_10mm_G4_Fe_5mm.root",
    "μ⁻ 2 GeV (Fe)": "mu-_2GeV_10000evt_5mm_G4_Fe_2mm.root"
}

data_dir = Path("/Users/ajay/Work/geantexercise/CalorimeterSim/Output")

def load_energy_per_layer(file_path):
    with uproot.open(file_path) as f:
        tree = f["CalorimeterSim"]
        layer_keys = [k for k in tree.keys() if k.startswith("Layer")]
        layers = sorted(layer_keys, key=lambda x: int(x.replace("Layer", "")))
        return np.stack([tree[layer].array(library="np") for layer in layers], axis=1)

energy_profiles = {}

for label, fname in FILES.items():
    full_path = data_dir / fname
    energy = load_energy_per_layer(full_path)
    energy_profiles[label] = {
        "mean": energy.mean(axis=0),
        "std": energy.std(axis=0),
        "total": energy.sum(axis=1)
    }

# 🔷 Plot 1: Average Shower Profiles
plt.figure(figsize=(10, 6))
for label, data in energy_profiles.items():
    plt.plot(data["mean"], label=label)
plt.title("🔬 Average Energy Deposition per Layer")
plt.xlabel("Layer Number")
plt.ylabel("Mean Energy (MeV)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("compare_shower_profiles.png")
plt.close()

# 🔷 Plot 2: Total Energy Distribution
plt.figure(figsize=(10, 6))
for label, data in energy_profiles.items():
    plt.hist(data["total"], bins=60, alpha=0.6, label=label, histtype='step', linewidth=1.5)
plt.title("📈 Total Energy Deposition Distribution")
plt.xlabel("Total Energy per Event (MeV)")
plt.ylabel("Events")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("compare_total_energy.png")
plt.close()

# 🔷 Plot 3: Shower RMS (spread per layer)
plt.figure(figsize=(10, 6))
for label, data in energy_profiles.items():
    plt.plot(data["std"], label=label)
plt.title("📉 Shower Width (RMS) per Layer")
plt.xlabel("Layer Number")
plt.ylabel("Energy Std Dev (MeV)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("compare_shower_rms.png")
plt.close()

print("✅ Comparison plots saved: ")
print(" - compare_shower_profiles.png")
print(" - compare_total_energy.png")
print(" - compare_shower_rms.png")

