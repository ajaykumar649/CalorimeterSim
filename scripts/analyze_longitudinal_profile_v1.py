import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from scipy.optimize import curve_fit
import re

# --- Gamma Fit Function ---
def gamma_profile(z, a, b, scale):
    z = np.clip(z, 1e-3, None)  # ✅ Prevent divide-by-zero or NaN at z=0
    return scale * (b*z)**(a-1) * np.exp(-b*z) * b / gamma(a)

# --- Load ROOT file ---
file = uproot.open("../build/output.root")
layer_histos = {k: v for k, v in file.items() if re.match(r"hLayer\d+", k)}

# --- Sort histograms by layer index ---
sorted_layers = sorted(layer_histos.items(), key=lambda kv: int(re.search(r"\d+", kv[0]).group()))

# --- Extract average energy and errors ---
z_values = []
mean_energy = []
std_energy = []

print("\n--- Layer-by-Layer Energy Deposition ---")  # ✅ Debug info

for i, (name, hist) in enumerate(sorted_layers):
    bin_edges = hist.axis().edges()
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    values = hist.values()
    entries = hist.to_numpy()[0]
    counts = np.sum(entries)

    if np.sum(values) > 0:
        mean = np.sum(bin_centers * values) / np.sum(values)
        std = np.sqrt(np.sum((bin_centers - mean)**2 * values) / np.sum(values))
    else:
        mean = 0
        std = 0

    z_values.append(i * 5.5)  # mm: 1.5 mm (Pb) + 4 mm (Scint)
    mean_energy.append(mean)
    std_energy.append(std)

    print(f"Layer {i:2d}: Mean = {mean:.2f} MeV, StdDev = {std:.2f} MeV")  # ✅ Detailed print

z_values = np.array(z_values)
mean_energy = np.array(mean_energy)
std_energy = np.array(std_energy)

# --- Normalize ---
normalized_energy = mean_energy / np.max(mean_energy)

# --- Fit to Gamma Distribution ---
try:
    popt, _ = curve_fit(gamma_profile, z_values, normalized_energy,
                        p0=[5, 0.1, 1.0], maxfev=10000)
    a_fit, b_fit, scale_fit = popt
    z_max = (a_fit - 1) / b_fit
    shower_width = np.sqrt(a_fit) / b_fit
except RuntimeError as e:
    print("❌ Fit failed:", e)
    a_fit = b_fit = scale_fit = z_max = shower_width = np.nan

# --- Plot ---
plt.figure(figsize=(10,6))
plt.errorbar(z_values, normalized_energy, yerr=std_energy/np.max(mean_energy),
             fmt='o', label='Simulated Data', color='blue')

z_fit = np.linspace(0, max(z_values)+10, 300)
plt.plot(z_fit, gamma_profile(z_fit, *popt), 'r-', label='Gamma Fit')

# Overlay shower max and width
plt.axvline(z_max, color='gray', linestyle='--', label=f'z_max ≈ {z_max:.1f} mm')
plt.fill_betweenx([0, 1.1], z_max - shower_width, z_max + shower_width,
                  color='gray', alpha=0.2, label=f'±σ ≈ {shower_width:.1f} mm')

# --- Finalize ---
plt.xlabel("Depth in Calorimeter (mm)")  # ✅ Clarified label
plt.ylabel("Normalized ⟨E_dep⟩")           # ✅ Clarified label
plt.title("Longitudinal Shower Profile (Gamma Fit)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("longitudinal_profile.png", dpi=300)
plt.show()

# --- Summary Output ---
print("\n--- Shower Shape Observables ---")
print(f"Gamma Fit Parameters: a = {a_fit:.2f}, b = {b_fit:.4f}, scale = {scale_fit:.3f}")
print(f"Shower Maximum (z_max): {z_max:.2f} mm")
print(f"Shower Width (σ):       {shower_width:.2f} mm")

