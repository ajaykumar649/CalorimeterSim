import ROOT
import os

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# Open ROOT file
file = ROOT.TFile.Open("output.root")
if not file or file.IsZombie():
    raise IOError("Failed to open ROOT file")

# Create output directory
os.makedirs("plots", exist_ok=True)

# --- Total Energy ---
c1 = ROOT.TCanvas("c1", "Total Energy", 800, 600)
hTotal = file.Get("hTotal")
hTotal.SetLineColor(ROOT.kBlue)
hTotal.SetTitle("Total Energy Deposition;E_{dep} (MeV);Counts")
hTotal.Draw()
c1.SaveAs("plots/hTotal.png")

# --- Radial and Longitudinal ---
for hname, color, fname, title, xlabel in [
    ("hRadial", ROOT.kGreen+2, "hRadial.png", "Radial Profile", "Radius (mm)"),
    ("hLong", ROOT.kRed, "hLong.png", "Longitudinal Profile", "z (mm)")
]:
    c = ROOT.TCanvas(hname, hname, 800, 600)
    h = file.Get(hname)
    h.SetLineColor(color)
    h.SetTitle(f"{title};{xlabel};Counts")
    h.Draw()
    c.SaveAs(f"plots/{fname}")

# --- XY Profile ---
cXY = ROOT.TCanvas("cXY", "XY Profile", 800, 600)
hXY = file.Get("hXY")
hXY.SetTitle("XY Shower Profile;x (mm);y (mm)")
hXY.Draw("COLZ")
cXY.SaveAs("plots/hXY.png")

# --- Layer-wise Analysis ---
layer_means = []
layer_stddevs = []

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kOrange+7,
          ROOT.kViolet, ROOT.kCyan+1, ROOT.kMagenta+2, ROOT.kYellow+2]

cLayers = ROOT.TCanvas("cLayers", "Layer Energy", 1000, 800)
cLayers.SetLogy()
legend = ROOT.TLegend(0.65, 0.1, 0.9, 0.9)

maxLayer = 100
for i in range(maxLayer):
    hname = f"hLayer{i}"
    h = file.Get(hname)
    if not h:
        break

    h.SetLineColor(colors[i % len(colors)])
    h.SetLineWidth(2)
    h.SetTitle("Energy Deposition per Layer;E_{dep} (MeV);Counts")
    h.Draw("SAME" if i > 0 else "")
    legend.AddEntry(h, f"Layer {i}", "l")

    layer_means.append(h.GetMean())
    layer_stddevs.append(h.GetStdDev())

legend.Draw()
cLayers.SaveAs("plots/hLayers_overlay.png")

# --- Summary ---
print("\n📊 Calorimeter Layer Summary:")
shower_max_layer = max(range(len(layer_means)), key=lambda i: layer_means[i])
print(f" - Total Layers: {len(layer_means)}")
print(f" - Shower Max: Layer {shower_max_layer} with Mean = {layer_means[shower_max_layer]:.3f} MeV")

tail_leakage = sum(layer_means[shower_max_layer+1:])
print(f" - Tail Leakage (sum beyond max): {tail_leakage:.3f} MeV")

# Table-style output
print("\n Layer |   Mean (MeV)  |  StdDev (MeV)")
print("---------------------------------------")
for i, (mean, std) in enumerate(zip(layer_means, layer_stddevs)):
    print(f"  {i:3d}  |   {mean:10.3f}  |   {std:10.3f}")

# --- Optional: ntuple
tree = file.Get("hits")
if tree:
    cTree = ROOT.TCanvas("cTree", "Edep Tree", 800, 600)
    tree.Draw("edep>>htree(100,0,20)")
    cTree.SaveAs("plots/edep_from_tree.png")

print("\n✅ All plots and stats saved to ./plots/")

