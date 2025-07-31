#include "GeometryMessenger.hh"
#include "DetectorConstruction.hh"
#include "G4UIcmdWithAString.hh"

GeometryMessenger::GeometryMessenger(DetectorConstruction* det)
    : fDetector(det) {
    // Disabled to avoid linker issues
    // fExportGDMLCmd = new G4UIcmdWithAString("/geometry/exportGDML", this);
    // fExportGDMLCmd->SetGuidance("Export the geometry to a GDML file.");
    // fExportGDMLCmd->SetParameterName("filename", false);
}

GeometryMessenger::~GeometryMessenger() {
    // delete fExportGDMLCmd;
}

void GeometryMessenger::SetNewValue(G4UIcommand* command, G4String newValue) {
    // Disabled
    // if (command == fExportGDMLCmd) {
    //     fDetector->ExportGDML(newValue);
    // }
}
