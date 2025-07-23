#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "FTFP_BERT.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4PhysicalVolumeStore.hh"
#include "G4Material.hh"
#include <iostream>

#include "DetectorConstruction.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

int main(int argc, char** argv) {
    // Initialize interactive session only if no macro provided
    G4UIExecutive* ui = nullptr;
    if (argc == 1) {
        ui = new G4UIExecutive(argc, argv);
    }

    // Run Manager
    G4RunManager* runManager = new G4RunManager();

    // User Initialization
    runManager->SetUserInitialization(new DetectorConstruction());
    runManager->SetUserInitialization(new FTFP_BERT);

    // User Actions
    runManager->SetUserAction(new PrimaryGeneratorAction());
    runManager->SetUserAction(new RunAction());
    runManager->SetUserAction(new EventAction());
    runManager->SetUserAction(new SteppingAction());

    // Visualization manager
    G4VisManager* visManager = new G4VisExecutive();
    visManager->Initialize();

    // Get UI manager
    G4UImanager* UImanager = G4UImanager::GetUIpointer();

    if (argc > 1) {
        // Batch mode: execute macro before initialization
        G4String macroFile = argv[1];
        UImanager->ApplyCommand("/control/execute " + macroFile);
        runManager->Initialize();
    } else {
        // Interactive mode: initialize and dump geometry
        runManager->Initialize();
        G4LogicalVolumeStore* lvs = G4LogicalVolumeStore::GetInstance();
        G4PhysicalVolumeStore* pvs = G4PhysicalVolumeStore::GetInstance();
        std::cout << "Listing all logical and physical volumes:" << std::endl;
        for (auto* lv : *lvs) {
            std::cout << "Logical Volume: " << lv->GetName() << ", Material: " << lv->GetMaterial()->GetName();
            for (auto* pv : *pvs) {
                if (pv->GetLogicalVolume() == lv) {
                    std::cout << ", Position: " << pv->GetTranslation() << std::endl;
                    break;
                }
            }
        }
        ui->SessionStart();
    }

    // Cleanup
    delete visManager;
    delete runManager;
    if (ui) delete ui;
    return 0;
}
