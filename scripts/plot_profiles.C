void plot_profiles() {
    TFile* f = TFile::Open("output.root");
    TH1D* hLong = (TH1D*)f->Get("hLong");
    TH1D* hTot = (TH1D*)f->Get("hTotal");

    TCanvas* c1 = new TCanvas("c1", "Longitudinal Profile", 800, 600);
    hLong->SetXTitle("Layer");
    hLong->SetYTitle("Edep [MeV]");
    hLong->Draw("hist");
    c1->SaveAs("longitudinal_profile.png");

    TCanvas* c2 = new TCanvas("c2", "Total Energy", 800, 600);
    hTot->SetXTitle("Total Energy [MeV]");
    hTot->SetYTitle("Counts");
    hTot->Draw("hist");
    c2->SaveAs("total_energy.png");
}

