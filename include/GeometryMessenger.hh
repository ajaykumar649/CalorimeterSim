#ifndef GEOMETRY_MESSENGER_HH
#define GEOMETRY_MESSENGER_HH

#include "G4UImessenger.hh"
#include "G4UIcmdWithAString.hh"

class DetectorConstruction;

class GeometryMessenger : public G4UImessenger {
public:
    GeometryMessenger(DetectorConstruction*);
    virtual ~GeometryMessenger();

    virtual void SetNewValue(G4UIcommand*, G4String);

private:
    DetectorConstruction* fDetector;
    G4UIcmdWithAString* fExportGDMLCmd;
};

#endif

