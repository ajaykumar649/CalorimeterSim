#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"

class G4VPhysicalVolume;
class G4LogicalVolume;
class CalorimeterMessenger;

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    virtual ~DetectorConstruction();

    virtual G4VPhysicalVolume* Construct();

    G4LogicalVolume* GetScoringVolume() const;
    G4int GetNumLayers() const;

    void SetNumLayers(G4int num);
    void SetAbsThickness(G4double thick);
    void SetScintThickness(G4double thick);
    void SetAbsMaterial(const G4String& material);

private:
    G4LogicalVolume* fScoringVolume;
    G4int fNumLayers;
    G4double fAbsThickness;
    G4double fScintThickness;
    G4String fAbsMaterial;
    CalorimeterMessenger* fMessenger;
};

#endif
