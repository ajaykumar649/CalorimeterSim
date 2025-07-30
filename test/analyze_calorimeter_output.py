# analyze_calorimeter_output.py

import uproot
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

data_dir = Path("/Users/ajay/Work/geantexercise/CalorimeterSim/Output")
root_files = sorted(data_dir.glob("*.root"))

def parse_filename(filename):
    pattern = r"(?P<particle>\w+-?)_(?P<energy>\d+)GeV_(?P<events>\d+)evt_(?P<abs_thick>\d+)mm_(?P<abs_mat>G4_\w+)_(?P<scin_thick>\d+)mm"
    match = re.search(pattern, filename)
    return match.groupdict() if match else {}

def analyze_file(file_path):
    info = parse_filename(file_path.name)
    print(f"📂 Analyzing {file_path.name}")
    with uproot.open(file_path) as f:
        tree = f["CalorimeterSim"]
        branches = tree.keys()
        layer_keys = [k for k in branches if k.startswith("Layer")]
        layers = sorted(layer_keys, key=lambda x: int(x.replace("Layer", "")))

        energy_per_layer = np.stack([tree[layer].array(library="np") for layer in layers], axis=1)
        total_energy = energy_per_layer.sum(axis=1)

        avg_profile = energy_per_layer.mean(axis=0)
        std_profile = energy_per_layer.std(axis=0)

        # Plot: Shower Profile
        plt.figure(figsize=(8, 5))
        plt.title(f"Shower Profile: {info.get('particle')} {info.get('energy')} GeV")
        plt.xlabel("Layer Number")
        plt.ylabel("Mean Energy Deposition (MeV)")
        plt.errorbar(range(len(layers)), avg_profile, yerr=std_profile, fmt="o-", capsize=3)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(file_path.with_suffix(".profile.png"))
        plt.close()

        # Plot: Total Energy Distribution
        plt.figure(figsize=(6, 4))
        plt.hist(total_energy, bins=50, color='steelblue', edgecolor='black')
        plt.title(f"Total Energy Deposition\n{file_path.name}")
        plt.xlabel("Total Energy (MeV)")
        plt.ylabel("Events")
        plt.tight_layout()
        plt.savefig(file_path.with_suffix(".total_energy.png"))
        plt.close()

        print(f"✅ Plots saved: {file_path.with_suffix('.profile.png').name}, {file_path.with_suffix('.total_energy.png').name}\n")

# Batch analyze all files
for root_file in root_files:
    analyze_file(root_file)

