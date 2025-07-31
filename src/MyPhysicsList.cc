// src/MyPhysicsList.cc
#include "MyPhysicsList.hh"
#include "G4EmStandardPhysics.hh"
#include "G4Gamma.hh"
#include "G4ProcessManager.hh"

MyPhysicsList::MyPhysicsList() {
    RegisterPhysics(new G4EmStandardPhysics());
}

void MyPhysicsList::ConstructProcess() {
    G4VModularPhysicsList::ConstructProcess();

    // Remove photonNuclear process from gamma
    auto gamma = G4Gamma::Gamma();
    G4ProcessManager* pmanager = gamma->GetProcessManager();
    for (int i = 0; i < pmanager->GetProcessListLength(); ++i) {
        G4VProcess* proc = (*pmanager->GetProcessList())[i];
        if (proc->GetProcessName() == "photonNuclear") {
            pmanager->RemoveProcess(proc);
            G4cout << "✅ Removed photonNuclear process from gamma" << G4endl;
            break;
        }
    }
}

