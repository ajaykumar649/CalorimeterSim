#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "FTFP_BERT.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "DetectorConstruction.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

int main(int argc, char** argv) {
    G4UIExecutive* ui = new G4UIExecutive(argc, argv);
    G4RunManager* runManager = new G4RunManager();
    runManager->SetUserInitialization(new DetectorConstruction());
    runManager->SetUserInitialization(new FTFP_BERT);
    runManager->SetUserAction(new PrimaryGeneratorAction());
    runManager->SetUserAction(new RunAction());
    runManager->SetUserAction(new EventAction());
    runManager->SetUserAction(new SteppingAction());
    runManager->Initialize();

    G4VisManager* vis = new G4VisExecutive();
    vis->Initialize();

    G4UImanager::GetUIpointer()->ApplyCommand("/control/execute macros/vis.mac");
    ui->SessionStart();

    delete vis;
    delete runManager;
    delete ui;
    return 0;
}

