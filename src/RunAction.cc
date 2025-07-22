#include "RunAction.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "RootIO.hh"
#include "DetectorConstruction.hh"

RunAction::RunAction() {}
RunAction::~RunAction() {}

void RunAction::BeginOfRunAction(const G4Run*) {
    G4RunManager::GetRunManager()->SetRandomNumberStore(false);

    // Retrieve number of layers dynamically
    auto* det = const_cast<DetectorConstruction*>(
        static_cast<const DetectorConstruction*>(G4RunManager::GetRunManager()->GetUserDetectorConstruction()));

    RootIO::Instance()->SetNumLayers(det->GetNumLayers());
    RootIO::Instance()->OpenFile("output.root");
}

void RunAction::EndOfRunAction(const G4Run* run) {
    RootIO::Instance()->Write();

    G4cout << "### Run ended. Events processed: " << run->GetNumberOfEvent() << G4endl;
    G4cout << "### ROOT file 'output.root' written." << G4endl;
}

