// RootIO.cc
#include "RootIO.hh"
#include "G4SystemOfUnits.hh"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TAxis.h"
#include <cmath>
#include <sstream>

RootIO* RootIO::fInstance = nullptr;

RootIO* RootIO::Instance() {
    if (!fInstance) {
        fInstance = new RootIO();
    }
    return fInstance;
}

RootIO::RootIO()
    : fFile(nullptr), fTree(nullptr), hRadial(nullptr), hLong(nullptr), hTotal(nullptr), hXY(nullptr) {
    hRadial = new TH1D("hRadial", "Radial Energy Deposition", 100, 0, 100);
    hRadial->GetXaxis()->SetTitle("Radius [mm]");
    hRadial->GetYaxis()->SetTitle("Energy [MeV]");

    hLong = new TH1D("hLong", "Energy Deposition per Layer", 100, 0, 100);
    hLong->GetXaxis()->SetTitle("Z [mm]");
    hLong->GetYaxis()->SetTitle("Energy [MeV]");

    hTotal = new TH1D("hTotal", "Total Energy Deposition", 1, 0, 1);

    hXY = new TH2D("hXY", "XY Energy Deposition", 100, -50, 50, 100, -50, 50);
    hXY->SetDirectory(nullptr);
    hXY->GetXaxis()->SetTitle("X [mm]");
    hXY->GetYaxis()->SetTitle("Y [mm]");
}

RootIO::~RootIO() {
    Write();
    delete hRadial;
    delete hLong;
    delete hTotal;
    delete hXY;
    for (auto& kv : hLayerXY) delete kv.second;
    if (fFile) {
        fFile->Close();
        delete fFile;
    }
}

void RootIO::SetFile(TFile* file) {
    fFile = file;
    if (!fFile) return;
    fFile->cd();
    fTree = new TTree("Hits", "Per-event hit information");
    fTree->Branch("edep", &fEdepVec);
    fTree->Branch("x", &fXVec);
    fTree->Branch("y", &fYVec);
    fTree->Branch("z", &fZVec);
}

void RootIO::SaveHit(G4double edep, G4ThreeVector pos) {
    fEdepVec.push_back(edep);
    fXVec.push_back(pos.x() / mm);
    fYVec.push_back(pos.y() / mm);
    fZVec.push_back(pos.z() / mm);

    double x = pos.x() / mm;
    double y = pos.y() / mm;
    double z = pos.z() / mm;
    double r = std::sqrt(x * x + y * y);

    if (hXY)     hXY->Fill(x, y, edep);
    if (hRadial) hRadial->Fill(r, edep);
    if (hLong)   hLong->Fill(z, edep);
    if (hTotal)  hTotal->Fill(0.5, edep);

    int layer = static_cast<int>(z / 10); // Assuming 10mm per layer
    if (!hLayerXY[layer]) {
        std::ostringstream name;
        name << "hXY_layer" << layer;
        hLayerXY[layer] = new TH2D(name.str().c_str(), name.str().c_str(), 100, -50, 50, 100, -50, 50);
        hLayerXY[layer]->GetXaxis()->SetTitle("X [mm]");
        hLayerXY[layer]->GetYaxis()->SetTitle("Y [mm]");
        hLayerXY[layer]->SetDirectory(nullptr);
    }
    hLayerXY[layer]->Fill(x, y, edep);
}

void RootIO::FillEvent() {
    if (fTree) fTree->Fill();
}

void RootIO::ClearEvent() {
    fEdepVec.clear();
    fXVec.clear();
    fYVec.clear();
    fZVec.clear();
}

void RootIO::Write() {
    if (!fFile) return;
    fFile->cd();
    if (fTree) fTree->Write("", TObject::kOverwrite);
    if (hXY)   hXY->Write("", TObject::kOverwrite);
    if (hRadial) hRadial->Write("", TObject::kOverwrite);
    if (hLong)   hLong->Write("", TObject::kOverwrite);
    if (hTotal)  hTotal->Write("", TObject::kOverwrite);
    for (auto& kv : hLayerXY) kv.second->Write("", TObject::kOverwrite);
}

