#include "DetectorConstruction.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"

DetectorConstruction::DetectorConstruction()
    : fMaterialName("G4_Pb"), fNumLayers(40) {}

DetectorConstruction::~DetectorConstruction() {}

G4VPhysicalVolume* DetectorConstruction::Construct() {
    auto* nist = G4NistManager::Instance();
    auto* worldMat = nist->FindOrBuildMaterial("G4_AIR");
    auto* absorber = nist->FindOrBuildMaterial(fMaterialName);
    auto* scint = nist->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");

    G4Box* solidW = new G4Box("World", 1*m, 1*m, 1*m);
    auto* logicW = new G4LogicalVolume(solidW, worldMat, "World");
    new G4PVPlacement(0, {}, logicW, "World", nullptr, false, 0);

    G4double dz = fNumLayers * (1.5 + 4.) * mm;
    G4double z0 = -dz / 2;
    for (int i = 0; i < fNumLayers; ++i) {
        G4double zPb = z0 + i * (1.5 + 4.) * mm + 0.75 * mm;
        G4Box* sPb = new G4Box("Pb", 5 * cm, 5 * cm, 0.75 * mm);
        auto* lPb = new G4LogicalVolume(sPb, absorber, "Pb");
        new G4PVPlacement(0, G4ThreeVector(0, 0, zPb), lPb, "Pb", logicW, false, i);

        G4double zSc = zPb + 0.75 * mm + 2 * mm;
        G4Box* sSc = new G4Box("Sc", 5 * cm, 5 * cm, 2 * mm);
        auto* lSc = new G4LogicalVolume(sSc, scint, "Sc");
        new G4PVPlacement(0, G4ThreeVector(0, 0, zSc), lSc, "Sc", logicW, false, i);
    }

    return new G4PVPlacement(0, {}, logicW, "WorldPhys", nullptr, false, 0);
}

