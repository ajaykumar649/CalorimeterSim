```python
import uproot
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Parse command-line arguments for flexibility
parser = argparse.ArgumentParser(description="Plot energy deposition profiles from CalorimeterSim")
parser.add_argument("--energy", type=float, default=10.0, help="Incident particle energy in GeV (e.g., 5, 10, 20)")
parser.add_argument("--layers", type=int, default=10, help="Number of calorimeter layers (e.g., 5, 10, 15)")
parser.add_argument("--particle", type=str, default="electron", help="Particle type (electron, gamma, pi+)")
parser.add_argument("--material", type=str, default="lead", help="Absorber material (lead, tungsten, copper)")
args = parser.parse_args()

# Load ROOT file
file = uproot.open("output.root")

# Total energy histogram
hTotal = file["hTotal"]
energy_range = args.energy * 1.5  # Scale range to accommodate fluctuations
hTotal_bins = 100
hTotal_range = (0, energy_range * 1000)  # Convert GeV to MeV for hTotal
plt.figure()
hTotal.plot.hist(bins=hTotal_bins, range=hTotal_range, histtype="step")
plt.title(f"Total Energy Deposition ({args.particle}, {args.energy} GeV, {args.material})")
plt.xlabel("Energy [MeV]")
plt.ylabel("Events")
plt.savefig("figures/plot_total.png")
plt.close()

# Longitudinal profile
hLong = file["hLong"]
hLong_bins = args.layers  # Match binning to number of layers
plt.figure()
hLong.plot.hist(bins=hLong_bins, range=(0, args.layers), histtype="step")
plt.title(f"Longitudinal Profile ({args.particle}, {args.energy} GeV, {args.material})")
plt.xlabel("Layer Number")
plt.ylabel("Energy [MeV]")
plt.savefig("figures/plot_longitudinal.png")
plt.close()

# Radial profile
hRadial = file["hRadial"]
hRadial_bins = 50
hRadial_range = (0, 5.0) if args.material == "tungsten" else (0, 10.0)  # Narrower for tungsten
plt.figure()
hRadial.plot.hist(bins=hRadial_bins, range=hRadial_range, histtype="step")
plt.title(f"Radial Profile ({args.particle}, {args.energy} GeV, {args.material})")
plt.xlabel("Radius [cm]")
plt.ylabel("Energy [MeV]")
plt.savefig("figures/plot_radial.png")
plt.close()

# XY map
hXY = file["hXY"]
plt.figure()
hXY.plot.hist(cmap="viridis")
plt.title(f"XY Energy Map ({args.particle}, {args.energy} GeV, {args.material})")
plt.xlabel("X [cm]")
plt.ylabel("Y [cm]")
plt.colorbar(label="Energy [MeV]")
plt.savefig("figures/plot_xy.png")
plt.close()
```