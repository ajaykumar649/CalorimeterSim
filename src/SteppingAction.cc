#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4VPhysicalVolume.hh"
#include "RootIO.hh"
#include "G4SystemOfUnits.hh"

SteppingAction::SteppingAction() {}
SteppingAction::~SteppingAction() {}

void SteppingAction::UserSteppingAction(const G4Step* step) {
    auto edep = step->GetTotalEnergyDeposit();
    if (edep <= 0.) return;

    auto prePoint = step->GetPreStepPoint();
    auto volume = prePoint->GetPhysicalVolume()->GetName();

    // Only record energy in scintillator (Active) layers
    if (volume.find("Active") != G4String::npos) {
        G4int copyNo = prePoint->GetTouchableHandle()->GetCopyNumber();
        auto pos = prePoint->GetPosition();
        G4double z = pos.z();
        G4double r = pos.perp();

        // [MODIFIED] Validate copyNo using RootIO's actual layer count
        auto* rootIO = RootIO::Instance();
        if (copyNo < 0 || copyNo >= rootIO->GetNumLayers()) {
            //G4cout << "Warning: Invalid CopyNo = " << copyNo
            //       << " at z = " << z / mm << " mm in volume " << volume << G4endl;
            return;
        }

        // Debug output
        //G4cout << "Step in Volume: " << volume << ", CopyNo: " << copyNo
        //       << ", Edep: " << edep / MeV << " MeV, z = " << z / mm << " mm" << G4endl;

        rootIO->AddToLayer(copyNo, edep);
        rootIO->SaveHit(edep, pos);

        auto* analysisManager = G4AnalysisManager::Instance();
        analysisManager->FillH1(rootIO->GetHLongID(), copyNo, edep / MeV);
        analysisManager->FillH1(rootIO->GetHRadialID(), r, edep / MeV);
    }
}

