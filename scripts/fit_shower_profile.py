import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma

# Open the ROOT file
with uproot.open("../build/output.root") as file:
    # Collect layer-wise histograms
    layer_keys = [k for k in file.keys() if k.startswith("hLayer")]
    layer_keys.sort(key=lambda x: int(x.split("Layer")[-1].split(";")[0]))  # Sort by layer number

    z_vals = []
    y_vals = []

    for idx, key in enumerate(layer_keys):
        hist = file[key]
        counts = hist.values()
        y_vals.append(np.sum(counts))  # Total Edep per layer
        z_vals.append(idx * 5.5)       # Depth in mm (assumes 1.5 mm Pb + 4 mm Sc per layer)

    z_vals = np.array(z_vals)
    y_vals = np.array(y_vals)

# Define a safe gamma function for fitting
def gamma_shower(z, a, b, scale):
    z = np.maximum(z, 1e-3)  # Avoid z=0
    return scale * b * (b * z) ** (a - 1) * np.exp(-b * z) / gamma(a)

# Choose region of interest (e.g., remove noisy tails)
z_fit = z_vals[1:-1]
y_fit = y_vals[1:-1]

# Fit initial guesses
a0, b0, scale0 = 2.0, 0.05, np.max(y_fit)

# Fit and handle failure gracefully
try:
    popt, pcov = curve_fit(gamma_shower, z_fit, y_fit, p0=[a0, b0, scale0], maxfev=5000)
    a_fit, b_fit, scale_fit = popt
    y_model = gamma_shower(z_vals, a_fit, b_fit, scale_fit)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Simulated Data')
    plt.plot(z_vals, y_model, 'r--', label=f'Fit: a={a_fit:.2f}, b={b_fit:.2f}')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Longitudinal Shower Profile with Gamma Fit")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("shower_fit.png", dpi=300)
    plt.show()

except RuntimeError as e:
    print("Fit failed:", e)
    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Simulated Data')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Shower Profile (Fit Failed)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("shower_fit_failed.png", dpi=300)
    plt.show()

