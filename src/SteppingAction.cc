#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4VTouchable.hh"
#include "G4TouchableHandle.hh"
#include "G4SystemOfUnits.hh"
#include "RootIO.hh"
#include "G4RootAnalysisManager.hh"

void SteppingAction::UserSteppingAction(const G4Step* step) {
  auto edep = step->GetTotalEnergyDeposit();
  if (edep <= 0) return;

  // Save to ROOT
  RootIO* rootIO = RootIO::Instance();
  rootIO->SaveHit(edep, step->GetPreStepPoint()->GetPosition());

  auto prePoint = step->GetPreStepPoint();
  auto touchable = prePoint->GetTouchable();
  G4int copyNo = touchable->GetCopyNumber();

  // Fill histograms via RootIO using G4RootAnalysisManager
  G4RootAnalysisManager* analysisManager = G4RootAnalysisManager::Instance();
  analysisManager->FillH1(rootIO->GetHLongID(), copyNo, edep / MeV);
  if (edep > 0.1 * MeV) {
    G4ThreeVector pos = prePoint->GetPosition();
    G4double r = std::sqrt(pos.x() * pos.x() + pos.y() * pos.y());
    if (r < 100.0) {
      analysisManager->FillH1(rootIO->GetHRadialID(), r, edep / MeV);
    }
  }
}
