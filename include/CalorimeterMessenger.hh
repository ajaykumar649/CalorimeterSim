#ifndef CalorimeterMessenger_h
#define CalorimeterMessenger_h 1

#include "G4UImessenger.hh"
#include "globals.hh"

class DetectorConstruction;
class G4UIdirectory;
class G4UIcmdWithAnInteger;
class G4UIcmdWithADoubleAndUnit;
class G4UIcmdWithAString;

class CalorimeterMessenger : public G4UImessenger
{
public:
    CalorimeterMessenger(DetectorConstruction*);
    virtual ~CalorimeterMessenger();

    virtual void SetNewValue(G4UIcommand*, G4String);

private:
    DetectorConstruction* fDetector;
    G4UIdirectory* fDirectory;
    G4UIcmdWithAnInteger* fSetLayersCmd;
    G4UIcmdWithADoubleAndUnit* fSetAbsThicknessCmd;
    G4UIcmdWithADoubleAndUnit* fSetScintThicknessCmd;
    G4UIcmdWithAString* fSetAbsMaterialCmd;
};

#endif
