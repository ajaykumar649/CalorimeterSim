#include "CalorimeterMessenger.hh"
#include "DetectorConstruction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcmdWithAnInteger.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4UIcmdWithAString.hh"

CalorimeterMessenger::CalorimeterMessenger(DetectorConstruction* detector)
    : fDetector(detector)
{
    fDirectory = new G4UIdirectory("/calor/");
    fDirectory->SetGuidance("Calorimeter control");

    fSetLayersCmd = new G4UIcmdWithAnInteger("/calor/setLayers", this);
    fSetLayersCmd->SetGuidance("Set number of layers in calorimeter.");
    fSetLayersCmd->SetParameterName("numLayers", false);
    fSetLayersCmd->AvailableForStates(G4State_PreInit, G4State_Idle);

    fSetAbsThicknessCmd = new G4UIcmdWithADoubleAndUnit("/calor/setAbsThickness", this);
    fSetAbsThicknessCmd->SetGuidance("Set absorber layer thickness.");
    fSetAbsThicknessCmd->SetParameterName("absThickness", false);
    fSetAbsThicknessCmd->SetUnitCategory("Length");
    fSetAbsThicknessCmd->AvailableForStates(G4State_PreInit, G4State_Idle);

    fSetScintThicknessCmd = new G4UIcmdWithADoubleAndUnit("/calor/setScintThickness", this);
    fSetScintThicknessCmd->SetGuidance("Set scintillator layer thickness.");
    fSetScintThicknessCmd->SetParameterName("scintThickness", false);
    fSetScintThicknessCmd->SetUnitCategory("Length");
    fSetScintThicknessCmd->AvailableForStates(G4State_PreInit, G4State_Idle);

    fSetAbsMaterialCmd = new G4UIcmdWithAString("/calor/setAbsMaterial", this);
    fSetAbsMaterialCmd->SetGuidance("Set absorber material (e.g., G4_Pb, G4_W).");
    fSetAbsMaterialCmd->SetParameterName("absMaterial", false);
    fSetAbsMaterialCmd->AvailableForStates(G4State_PreInit, G4State_Idle);
}

CalorimeterMessenger::~CalorimeterMessenger()
{
    delete fSetLayersCmd;
    delete fSetAbsThicknessCmd;
    delete fSetScintThicknessCmd;
    delete fSetAbsMaterialCmd;
    delete fDirectory;
}

void CalorimeterMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
    if (command == fSetLayersCmd) {
        G4int num = fSetLayersCmd->GetNewIntValue(newValue);
        fDetector->SetNumLayers(num);
    }
    else if (command == fSetAbsThicknessCmd) {
        G4double thick = fSetAbsThicknessCmd->GetNewDoubleValue(newValue);
        fDetector->SetAbsThickness(thick);
    }
    else if (command == fSetScintThicknessCmd) {
        G4double thick = fSetScintThicknessCmd->GetNewDoubleValue(newValue);
        fDetector->SetScintThickness(thick);
    }
    else if (command == fSetAbsMaterialCmd) {
        fDetector->SetAbsMaterial(newValue);
    }
}
