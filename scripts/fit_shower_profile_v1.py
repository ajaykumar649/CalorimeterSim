import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma

# Gamma fit function
def gamma_shower(z, a, b, scale):
    z = np.maximum(z, 1e-3)  # avoid z=0 for power law
    return scale * b * (b * z) ** (a - 1) * np.exp(-b * z) / gamma(a)

# --- Load data from ROOT file ---
with uproot.open("../build/output.root") as file:
    layer_keys = sorted([k for k in file.keys() if k.startswith("hLayer")],
                        key=lambda x: int(x.split("Layer")[-1].split(";")[0]))
    
    z_vals, y_vals = [], []
    for idx, key in enumerate(layer_keys):
        hist = file[key]
        counts = hist.values()
        total_edep = np.sum(counts)
        z_vals.append(idx * 5.5)  # mm
        y_vals.append(total_edep)

    z_vals = np.array(z_vals)
    y_vals = np.array(y_vals)

print("📊 Loaded {} layers.".format(len(z_vals)))

# Optional: Print debug info
for i, (z, y) in enumerate(zip(z_vals, y_vals)):
    print(f"Layer {i:2d} → z = {z:5.1f} mm, Total Edep = {y:.2f} MeV")

# --- Fit only central region: remove 1st & last 2 bins ---
z_fit = z_vals[2:-2]
y_fit = y_vals[2:-2]

# Initial parameter guesses
a0, b0, scale0 = 4.0, 0.1, np.max(y_fit)
print(f"\n🔧 Initial fit guess: a = {a0}, b = {b0}, scale = {scale0:.2f}")

# --- Fit Gamma distribution ---
try:
    popt, pcov = curve_fit(gamma_shower, z_fit, y_fit, p0=[a0, b0, scale0], maxfev=10000)
    a_fit, b_fit, scale_fit = popt
    print(f"\n✅ Fit success:")
    print(f"Gamma Fit Parameters: a = {a_fit:.2f}, b = {b_fit:.4f}, scale = {scale_fit:.2f}")

    z_max = (a_fit - 1) / b_fit
    width = np.sqrt(a_fit) / b_fit
    print(f"Shower Max (z_max) = {z_max:.2f} mm")
    print(f"Shower Width (σ)   = {width:.2f} mm")

    # Plot result
    z_plot = np.linspace(0, max(z_vals) + 10, 300)
    y_model = gamma_shower(z_plot, a_fit, b_fit, scale_fit)

    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Simulated Data')
    plt.plot(z_plot, y_model, 'r-', label='Gamma Fit')
    plt.axvline(z_max, color='gray', linestyle='--', label=f'z_max ≈ {z_max:.1f} mm')
    plt.fill_betweenx([0, max(y_vals)], z_max - width, z_max + width,
                      color='gray', alpha=0.2, label=f'±σ ≈ {width:.1f} mm')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Longitudinal Shower Profile (Gamma Fit)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("shower_fit.png", dpi=300)
    plt.show()

except RuntimeError as e:
    print(f"\n❌ Fit failed: {e}")
    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Simulated Data')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Shower Profile (Fit Failed)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("shower_fit_failed.png", dpi=300)
    plt.show()

