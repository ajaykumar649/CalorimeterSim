#include "RootIO.hh"
#include "G4SystemOfUnits.hh"
#include <sstream>

RootIO* RootIO::fInstance = nullptr;
std::mutex RootIO::fMutex;

RootIO* RootIO::Instance() {
  std::lock_guard<std::mutex> lock(fMutex);
  if (!fInstance) {
    fInstance = new RootIO();
  }
  return fInstance;
}

RootIO::RootIO()
    : fAnalysisManager(G4RootAnalysisManager::Instance()),
      hRadialID(0), hLongID(0), hTotalID(0), hXYID(0) {
  // Defer file creation to OpenFile
}

RootIO::~RootIO() {
  Write();
}

void RootIO::OpenFile(const G4String& fileName) {
  fAnalysisManager->SetFileName(fileName);
  fAnalysisManager->OpenFile();
  hRadialID = fAnalysisManager->CreateH1("hRadial", "Radial Energy Deposition", 100, 0, 100);
  fAnalysisManager->SetH1XAxisTitle(hRadialID, "Radius [mm]");
  fAnalysisManager->SetH1YAxisTitle(hRadialID, "Energy [MeV]");

  hLongID = fAnalysisManager->CreateH1("hLong", "Energy Deposition per Layer", 100, 0, 100);
  fAnalysisManager->SetH1XAxisTitle(hLongID, "Z [mm]");
  fAnalysisManager->SetH1YAxisTitle(hLongID, "Energy [MeV]");

  hTotalID = fAnalysisManager->CreateH1("hTotal", "Total Energy Deposition", 1, 0, 1);

  hXYID = fAnalysisManager->CreateH2("hXY", "XY Energy Deposition", 100, -50, 50, 100, -50, 50);
  fAnalysisManager->SetH2XAxisTitle(hXYID, "X [mm]");
  fAnalysisManager->SetH2YAxisTitle(hXYID, "Y [mm]");

  fAnalysisManager->CreateNtuple("Hits", "Per-event hit information");
  fAnalysisManager->CreateNtupleDColumn("edep");
  fAnalysisManager->CreateNtupleDColumn("x");
  fAnalysisManager->CreateNtupleDColumn("y");
  fAnalysisManager->CreateNtupleDColumn("z");
  fAnalysisManager->FinishNtuple();
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

  fAnalysisManager->FillH1(hRadialID, r, edep);
  fAnalysisManager->FillH1(hLongID, z, edep);
  fAnalysisManager->FillH1(hTotalID, 0.5, edep);
  fAnalysisManager->FillH2(hXYID, x, y, edep);

  int layer = static_cast<int>(z / 10); // Assuming 10mm per layer
  if (hLayerXYIDs.find(layer) == hLayerXYIDs.end()) {
    std::ostringstream name;
    name << "hXY_layer" << layer;
    hLayerXYIDs[layer] = fAnalysisManager->CreateH2(name.str().c_str(), name.str().c_str(), 100, -50, 50, 100, -50, 50);
    fAnalysisManager->SetH2XAxisTitle(hLayerXYIDs[layer], "X [mm]");
    fAnalysisManager->SetH2YAxisTitle(hLayerXYIDs[layer], "Y [mm]");
  }
  fAnalysisManager->FillH2(hLayerXYIDs[layer], x, y, edep);
}

void RootIO::FillEvent() {
  for (size_t i = 0; i < fEdepVec.size(); ++i) {
    fAnalysisManager->FillNtupleDColumn(0, fEdepVec[i]);
    fAnalysisManager->FillNtupleDColumn(1, fXVec[i]);
    fAnalysisManager->FillNtupleDColumn(2, fYVec[i]);
    fAnalysisManager->FillNtupleDColumn(3, fZVec[i]);
    fAnalysisManager->AddNtupleRow();
  }
}

void RootIO::ClearEvent() {
  fEdepVec.clear();
  fXVec.clear();
  fYVec.clear();
  fZVec.clear();
}

void RootIO::Write() {
  fAnalysisManager->Write();
  fAnalysisManager->CloseFile();
}
