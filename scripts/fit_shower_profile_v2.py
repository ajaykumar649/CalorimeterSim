import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma

# --- Gamma distribution function ---
def gamma_shower(z, a, b, scale):
    z = np.maximum(z, 1e-3)  # avoid z=0
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        return scale * b * (b * z) ** (a - 1) * np.exp(-b * z) / gamma(a)

# --- Load energy data from ROOT ---
with uproot.open("../build/output.root") as file:
    layer_keys = [k for k in file.keys() if k.startswith("hLayer")]
    layer_keys.sort(key=lambda x: int(x.split("Layer")[-1].split(";")[0]))  # Sort by index

    z_vals = []
    y_vals = []

    print(f"📊 Loaded {len(layer_keys)} layers.")
    for idx, key in enumerate(layer_keys):
        hist = file[key]
        counts = hist.values()
        total_edep = np.sum(counts)
        z = idx * 5.5  # depth (1.5 mm Pb + 4 mm Scint)
        z_vals.append(z)
        y_vals.append(total_edep)
        print(f"Layer {idx:2d} → z = {z:5.1f} mm, Total Edep = {total_edep:.2f} MeV")

z_vals = np.array(z_vals)
y_vals = np.array(y_vals)

# --- Check for flat profile ---
if np.allclose(y_vals, y_vals[0]):
    print("\n⚠️ Uniform energy profile detected. Fit is not meaningful.")

    # Plot raw data only
    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Flat Energy Deposition')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Shower Profile (Flat – No Fit)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("shower_fit_flat.png", dpi=300)
    plt.show()
    exit()

# --- Fit Gamma distribution ---
z_fit = z_vals[1:-1]
y_fit = y_vals[1:-1]
a0, b0, scale0 = 4.0, 0.1, np.max(y_fit)

print(f"\n🔧 Initial fit guess: a = {a0}, b = {b0}, scale = {scale0:.2f}")

try:
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        popt, _ = curve_fit(gamma_shower, z_fit, y_fit, p0=[a0, b0, scale0], maxfev=10000)
    a_fit, b_fit, scale_fit = popt

    z_max = (a_fit - 1) / b_fit
    shower_width = np.sqrt(a_fit) / b_fit

    print("\n✅ Fit success:")
    print(f"Gamma Fit Parameters: a = {a_fit:.2f}, b = {b_fit:.4f}, scale = {scale_fit:.2f}")
    print(f"Shower Max (z_max) = {z_max:.2f} mm")
    print(f"Shower Width (σ)   = {shower_width:.2f} mm")

    # --- Plot ---
    y_model = gamma_shower(z_vals, *popt)
    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Simulated Data')
    plt.plot(z_vals, y_model, 'r--', label=f'Gamma Fit')
    plt.axvline(z_max, color='gray', linestyle='--', label=f'z_max ≈ {z_max:.1f} mm')
    plt.fill_betweenx([0, 1.1 * np.max(y_vals)],
                      z_max - shower_width, z_max + shower_width,
                      color='gray', alpha=0.2, label=f'±σ ≈ {shower_width:.1f} mm')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Longitudinal Shower Profile with Gamma Fit")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("shower_fit.png", dpi=300)
    plt.show()

except RuntimeError as e:
    print("❌ Fit failed:", e)
    plt.figure(figsize=(8, 5))
    plt.plot(z_vals, y_vals, 'bo-', label='Simulated Data')
    plt.xlabel("Depth z (mm)")
    plt.ylabel("Total Energy Deposition (MeV)")
    plt.title("Shower Profile (Fit Failed)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("shower_fit_failed.png", dpi=300)
    plt.show()

