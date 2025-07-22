#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "FTFP_BERT.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "G4LogicalVolumeStore.hh"  // For logical volumes
#include "G4PhysicalVolumeStore.hh" // For physical volumes
#include "G4Material.hh"            // To fix G4Material incomplete type
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
  runManager->SetUserAction(new PrimaryGeneratorAction());  // gun will be configured from macros
  runManager->SetUserAction(new RunAction());
  runManager->SetUserAction(new EventAction());
  runManager->SetUserAction(new SteppingAction());

  // Initialize
  runManager->Initialize();

  // Visualization manager
  G4VisManager* visManager = new G4VisExecutive();
  visManager->Initialize();

  // Get UI manager and apply macro (if any)
  G4UImanager* UImanager = G4UImanager::GetUIpointer();

  if (argc > 1) {
    // Batch mode: execute macro file passed as argument
    G4String macroFile = argv[1];
    UImanager->ApplyCommand("/control/execute " + macroFile);
  } else {
    // Interactive idle mode: dump geometry and launch UI
    UImanager->ApplyCommand("/run/initialize");
    // Custom geometry dump
    G4LogicalVolumeStore* lvs = G4LogicalVolumeStore::GetInstance();
    G4PhysicalVolumeStore* pvs = G4PhysicalVolumeStore::GetInstance();
    std::cout << "Listing all logical and physical volumes:" << std::endl;
    for (auto* lv : *lvs) {
        std::cout << "Logical Volume: " << lv->GetName() << ", Material: " << lv->GetMaterial()->GetName();
        // Find associated physical volume(s)
        for (auto* pv : *pvs) {
            if (pv->GetLogicalVolume() == lv) {
                std::cout << ", Position: " << pv->GetTranslation() << std::endl;
                break; // Assume one physical volume per logical for simplicity
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
