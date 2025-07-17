#include "G4VUserDetectorConstruction.hh"

class DetectorConstruction : public G4VUserDetectorConstruction {
public:
    DetectorConstruction();
    virtual ~DetectorConstruction();
    virtual G4VPhysicalVolume* Construct();
    void SetMaterialName(const G4String& mat) { fMaterialName = mat; }
private:
    G4String fMaterialName;
};

