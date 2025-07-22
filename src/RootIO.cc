#include "RootIO.hh"
#include "G4SystemOfUnits.hh"
#include "G4AnalysisManager.hh"
#include "G4ThreeVector.hh"

RootIO* RootIO::fInstance = nullptr;

RootIO* RootIO::Instance() {
    if (!fInstance)
        fInstance = new RootIO();
    return fInstance;
}

RootIO::RootIO() : fAnalysisManager(nullptr) {}

RootIO::~RootIO() {
    delete fAnalysisManager;
}

void RootIO::SetNumLayers(G4int n) {
    fLayerEdep.resize(n, 0.);
}

void RootIO::AddToLayer(G4int layer, G4double edep) {
    if (layer >= 0 && layer < (G4int)fLayerEdep.size())
        fLayerEdep[layer] += edep;
}

void RootIO::ClearEvent() {
    fEdep.clear();
    fPos.clear();
    std::fill(fLayerEdep.begin(), fLayerEdep.end(), 0.);
}

void RootIO::SaveHit(G4double edep, const G4ThreeVector& pos) {
    fEdep.push_back(edep);
    fPos.push_back(pos);

    fAnalysisManager->FillH1(hRadialID, pos.perp());
    fAnalysisManager->FillH1(hLongID, pos.z());
    fAnalysisManager->FillH2(hXYID, pos.x(), pos.y());
}

void RootIO::FillEvent() {
    G4double totalEdep = 0.;
    for (size_t i = 0; i < fEdep.size(); ++i) {
        fAnalysisManager->FillNtupleDColumn(0, fEdep[i] / MeV);
        fAnalysisManager->FillNtupleDColumn(1, fPos[i].x() / mm);
        fAnalysisManager->FillNtupleDColumn(2, fPos[i].y() / mm);
        fAnalysisManager->FillNtupleDColumn(3, fPos[i].z() / mm);
        fAnalysisManager->AddNtupleRow();
        totalEdep += fEdep[i];
    }

    fAnalysisManager->FillH1(hTotalID, totalEdep / MeV);

    for (size_t i = 0; i < fLayerEdep.size(); ++i) {
        fAnalysisManager->FillH1(hLayerIDs[i], fLayerEdep[i] / MeV);
    }
}

void RootIO::OpenFile(const G4String& filename) {
    fAnalysisManager = G4AnalysisManager::Instance();
    fAnalysisManager->SetVerboseLevel(1);
    fAnalysisManager->OpenFile(filename);

    hTotalID  = fAnalysisManager->CreateH1("hTotal",  "Total Energy Deposition (MeV)", 101, 0., 101.);
    hRadialID = fAnalysisManager->CreateH1("hRadial", "Radial Profile (mm)",           100, 0., 50.);
    hLongID   = fAnalysisManager->CreateH1("hLong",   "Longitudinal Profile (mm)",      100, -100., 100.);
    hXYID     = fAnalysisManager->CreateH2("hXY",     "XY Shower Profile (mm)",         100, -50., 50., 100, -50., 50.);

    for (size_t i = 0; i < fLayerEdep.size(); ++i) {
        G4String name = "hLayer" + std::to_string(i);
        G4String title = "Energy deposition in Layer " + std::to_string(i);
        hLayerIDs.push_back(fAnalysisManager->CreateH1(name, title, 100, 0., 10.));
    }

    fAnalysisManager->CreateNtuple("hits", "Energy and Position");
    fAnalysisManager->CreateNtupleDColumn("edep");
    fAnalysisManager->CreateNtupleDColumn("x");
    fAnalysisManager->CreateNtupleDColumn("y");
    fAnalysisManager->CreateNtupleDColumn("z");
    fAnalysisManager->FinishNtuple();
}

void RootIO::CloseFile() {
    if (fAnalysisManager) {
        fAnalysisManager->Write();
        fAnalysisManager->CloseFile();
    }
}

void RootIO::Write() {
    if (fAnalysisManager) {
        fAnalysisManager->Write();
        fAnalysisManager->CloseFile();
    }
}

