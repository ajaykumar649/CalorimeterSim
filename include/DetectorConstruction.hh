#ifndef DETECTOR_CONSTRUCTION_HH
#define DETECTOR_CONSTRUCTION_HH

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"
#include "G4String.hh"

class G4VPhysicalVolume;

class DetectorConstruction : public G4VUserDetectorConstruction {
public:
    DetectorConstruction();
    virtual ~DetectorConstruction();
    virtual G4VPhysicalVolume* Construct();

    void SetMaterialName(const G4String& mat) { fMaterialName = mat; }
    void SetNumLayers(G4int n) { fNumLayers = n; }

    G4int GetNumLayers() const { return fNumLayers; }

private:
    G4String fMaterialName;
    G4int fNumLayers;
};

#endif

