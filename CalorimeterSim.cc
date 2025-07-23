#include "G4RunManager.hh"
#include "G4UImanager.hh"
//#include "FTFP_BERT.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4PhysicalVolumeStore.hh"
#include "G4Material.hh"
#include "G4Gamma.hh"
#include "G4ProcessManager.hh"
#include "G4ProcessVector.hh"
#include <iostream>

#include "DetectorConstruction.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

#include "MyPhysicsList.hh"

void RemovePhotonNuclear() {
    auto gamma = G4Gamma::Gamma();
    G4ProcessManager* pmanager = gamma->GetProcessManager();
    G4ProcessVector* pvect = pmanager->GetProcessList();

    for (G4int i = 0; i < pvect->size(); ++i) {
        G4VProcess* proc = (*pvect)[i];
        if (proc->GetProcessName() == "photonNuclear") {
            pmanager->RemoveProcess(proc);
            G4cout << "✅ Removed photonNuclear process from gamma" << G4endl;
            break;
        }
    }
}

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
    //runManager->SetUserInitialization(new FTFP_BERT);
    runManager->SetUserInitialization(new MyPhysicsList());
    
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
        G4String macroFile = argv[1];
        UImanager->ApplyCommand("/control/execute " + macroFile);
        runManager->Initialize();
        RemovePhotonNuclear(); // ✅ Moved here after initialization
    } else {
        runManager->Initialize();
        RemovePhotonNuclear(); // ✅ Moved here after initialization

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

