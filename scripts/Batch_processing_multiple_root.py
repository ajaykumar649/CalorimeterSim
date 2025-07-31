import uproot
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

root_files = glob.glob("*.root")
os.makedirs("batch_plots", exist_ok=True)

for fpath in root_files:
    fname = os.path.basename(fpath).replace(".root", "")
    print(f"📂 Processing {fname}.root ...")
    file = uproot.open(fpath)
    
    means = []
    i = 0
    while f"hLayer{i}" in file:
        hist = file[f"hLayer{i}"].to_numpy()[0]
        bins = file[f"hLayer{i}"].to_numpy()[1]
        centers = 0.5 * (bins[:-1] + bins[1:])
        mean = np.average(centers, weights=hist) if hist.sum() > 0 else 0
        means.append(mean)
        i += 1
    
    plt.figure(figsize=(8,5))
    plt.plot(range(len(means)), means, marker='o')
    plt.title(f"Shower Profile: {fname}")
    plt.xlabel("Layer")
    plt.ylabel("Mean Energy Deposition (MeV)")
    plt.grid(True)
    plt.savefig(f"batch_plots/{fname}_profile.png")
    plt.close()

print("✅ Batch processing complete. Results saved to ./batch_plots/")

