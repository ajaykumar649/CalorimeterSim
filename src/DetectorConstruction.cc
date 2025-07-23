#include "DetectorConstruction.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4Material.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4SDManager.hh"
#include "G4RunManager.hh"
#include "CalorimeterMessenger.hh"
#include "G4coutDestination.hh"
#include "RootIO.hh"  // [MODIFIED]

#include "G4Gamma.hh"
#include "G4ProcessManager.hh"
#include "G4ProcessVector.hh"  // <-- [PATCH ADDED]

DetectorConstruction::DetectorConstruction()
    : fScoringVolume(nullptr),
      fNumLayers(20),
      fAbsThickness(8.0 * mm),
      fScintThickness(4.0 * mm),
      fAbsMaterial("G4_Pb"),
      fMessenger(nullptr)
{
    fMessenger = new CalorimeterMessenger(this);
}

DetectorConstruction::~DetectorConstruction() {
    delete fMessenger;
}

// [PATCH ADDED] Local helper to remove photonNuclear process
static void RemovePhotonNuclear() {
    auto gamma = G4Gamma::Gamma();
    G4ProcessManager* pman = gamma->GetProcessManager();
    G4ProcessVector* pvect = pman->GetProcessList();

    for (G4int i = 0; i < pvect->size(); ++i) {
        G4VProcess* proc = (*pvect)[i];
        if (proc->GetProcessName() == "photonNuclear") {
            pman->RemoveProcess(proc);
            G4cout << "✅ Removed photonNuclear from gamma" << G4endl;
            break;
        }
    }
}

G4VPhysicalVolume* DetectorConstruction::Construct() {
    G4NistManager* nist = G4NistManager::Instance();

    // Materials
    G4Material* worldMat = nist->FindOrBuildMaterial("G4_AIR");
    G4Material* absorberMat = nist->FindOrBuildMaterial(fAbsMaterial);
    G4Material* activeMat = nist->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");

    // World volume
    G4double worldSizeXY = 1.0 * m;
    G4double worldSizeZ = 2.0 * m;

    G4Box* solidWorld = new G4Box("World", worldSizeXY / 2, worldSizeXY / 2, worldSizeZ / 2);
    G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, worldMat, "World");
    G4VPhysicalVolume* physWorld = new G4PVPlacement(
        nullptr, {}, logicWorld, "World", nullptr, false, 0, true);

    // Layer parameters
    G4double layerXY = 50.0 * cm;
    G4double totalLayerThickness = fAbsThickness + fScintThickness;
    G4double totalThickness = fNumLayers * totalLayerThickness;

    G4Box* solidAbsorber = new G4Box("Absorber", layerXY / 2, layerXY / 2, fAbsThickness / 2);
    G4Box* solidActive = new G4Box("Active", layerXY / 2, layerXY / 2, fScintThickness / 2);

    G4LogicalVolume* logicAbsorber = new G4LogicalVolume(solidAbsorber, absorberMat, "Absorber");
    G4LogicalVolume* logicActive = new G4LogicalVolume(solidActive, activeMat, "Active");

    for (int i = 0; i < fNumLayers; ++i) {
        // Center of the i-th layer
        G4double layerZCenter = -0.5 * totalThickness + (i + 0.5) * totalLayerThickness;

        // Place scintillator and absorber relative to layer center
        G4double scintZ = layerZCenter - 0.5 * fAbsThickness;
        G4double absZ   = layerZCenter + 0.5 * fScintThickness;

        new G4PVPlacement(nullptr, G4ThreeVector(0, 0, scintZ),
                          logicActive, "Active" + std::to_string(i), logicWorld, false, i, true);

        new G4PVPlacement(nullptr, G4ThreeVector(0, 0, absZ),
                          logicAbsorber, "Absorber" + std::to_string(i), logicWorld, false, i, true);
    }

    // [MODIFIED] Let RootIO know how many layers were built
    RootIO::Instance()->SetNumLayers(fNumLayers);

    // [PATCH] Suppress fatal crash from photonNuclear
    //RemovePhotonNuclear();

    return physWorld;
}

void DetectorConstruction::SetNumLayers(G4int num) {
    fNumLayers = num;
    G4RunManager::GetRunManager()->ReinitializeGeometry();
}

void DetectorConstruction::SetAbsThickness(G4double thick) {
    fAbsThickness = thick;
    G4RunManager::GetRunManager()->ReinitializeGeometry();
}

void DetectorConstruction::SetScintThickness(G4double thick) {
    fScintThickness = thick;
    G4RunManager::GetRunManager()->ReinitializeGeometry();
}

void DetectorConstruction::SetAbsMaterial(const G4String& material) {
    fAbsMaterial = material;
    G4RunManager::GetRunManager()->ReinitializeGeometry();
}

G4LogicalVolume* DetectorConstruction::GetScoringVolume() const {
    return fScoringVolume;
}

G4int DetectorConstruction::GetNumLayers() const {
    return fNumLayers;
}

