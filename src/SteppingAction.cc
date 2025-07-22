#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4TouchableHistory.hh"
#include "G4VPhysicalVolume.hh"
#include "RootIO.hh"
#include "G4SystemOfUnits.hh"

SteppingAction::SteppingAction() {}
SteppingAction::~SteppingAction() {}

void SteppingAction::UserSteppingAction(const G4Step* step) {
    auto edep = step->GetTotalEnergyDeposit();
    if (edep <= 0.) return;

    auto prePoint = step->GetPreStepPoint();
    auto touchable = static_cast<const G4TouchableHistory*>(prePoint->GetTouchable());

    G4int copyNo = touchable->GetReplicaNumber();
    auto pos = step->GetPreStepPoint()->GetPosition();
    G4double r = pos.perp();

    auto* rootIO = RootIO::Instance();
    rootIO->AddToLayer(copyNo, edep);
    rootIO->SaveHit(edep, pos);

    auto* analysisManager = G4AnalysisManager::Instance();
    analysisManager->FillH1(rootIO->GetHLongID(), copyNo, edep / MeV);
    analysisManager->FillH1(rootIO->GetHRadialID(), r, edep / MeV);
}

