#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4VTouchable.hh"
#include "G4TouchableHandle.hh"
#include "G4SystemOfUnits.hh"
#include "RunAction.hh"
#include "RootIO.hh"

void SteppingAction::UserSteppingAction(const G4Step* step) {
    auto edep = step->GetTotalEnergyDeposit();
    if (edep <= 0) return;

    // Save to ROOT
    RootIO::Instance()->SaveHit(edep, step->GetPreStepPoint()->GetPosition());

    auto prePoint = step->GetPreStepPoint();
    auto touchable = prePoint->GetTouchable();

    G4int copyNo = touchable->GetCopyNumber();
    G4ThreeVector pos = prePoint->GetPosition();
    G4double r = std::sqrt(pos.x() * pos.x() + pos.y() * pos.y());

    RunAction::hLongitudinal->Fill(copyNo, edep / MeV);
    RunAction::hTotal->Fill(edep / MeV);

    if (edep > 0.1 * MeV && r < 100.0) {
        RunAction::hRadial->Fill(r, edep / MeV);
    }
}

