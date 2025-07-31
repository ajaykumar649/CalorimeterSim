import uproot
import numpy as np
import matplotlib.pyplot as plt
import re
import os
from scipy.special import gamma

# Settings
E0 = 10.0  # Incident energy in MeV (match /gun/energy)
X0 = 5.6  # Pb radiation length in mm (approximate)
Ec = 8.9   # Critical energy in MeV for Pb
b = 0.5    # Shape parameter (constant)

# Compute a parameter
a = 1.0 + 0.5 * np.log(E0 / Ec)

# Output
os.makedirs("plots_bethe", exist_ok=True)
file = uproot.open("output.root")

# Read and sort hLayer histograms
layer_histos = {k: file[k] for k in file.keys() if re.match(r"hLayer\d+", k)}
layer_histos = dict(sorted(layer_histos.items(), key=lambda kv: int(re.findall(r"\d+", kv[0])[0])))

# Sum energy per layer
total_energy_per_layer = []
layer_z = []

for i, (name, hist) in enumerate(layer_histos.items()):
    counts = hist.values()
    bins = hist.axis().edges()
    energy = np.sum(counts * np.diff(bins))  # Approximate total energy in this layer
    total_energy_per_layer.append(energy)
    z = i * (1.5 + 4.0)  # mm: assuming absorber=1.5mm Pb + 4mm scint
    layer_z.append(z)

# Normalize
total_energy_per_layer = np.array(total_energy_per_layer)
layer_z = np.array(layer_z)
norm_energy = total_energy_per_layer / np.sum(total_energy_per_layer)

# Compute Bethe-Heitler shape
t_vals = layer_z / X0
expected_shape = (b * (b * t_vals) ** (a - 1) * np.exp(-b * t_vals)) / gamma(a)
expected_shape /= np.sum(expected_shape)  # Normalize to unit area

# Plot overlay
plt.figure(figsize=(10, 6))
plt.plot(layer_z, norm_energy, "o-", label="Simulated Shower (Geant4)", color="tab:blue")
plt.plot(layer_z, expected_shape, "--", label=f"Bethe-Heitler Fit (E₀={E0} MeV)", color="crimson")

plt.xlabel("Depth z (mm)")
plt.ylabel("Normalized Energy Deposition")
plt.title("Longitudinal Shower Profile vs. Bethe–Heitler Expectation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/longitudinal_overlay.png")
plt.show()

