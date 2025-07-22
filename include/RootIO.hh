#ifndef ROOTIO_HH
#define ROOTIO_HH

#include "globals.hh"
#include "G4ThreeVector.hh"
#include "G4SystemOfUnits.hh"
#include "G4String.hh"
#include "G4AnalysisManager.hh"

#include <vector>

class RootIO {
public:
    static RootIO* Instance();
    ~RootIO();

    void OpenFile(const G4String& filename);
    void CloseFile();
    void Write();

    void SaveHit(G4double edep, const G4ThreeVector& pos);
    void FillEvent();
    void ClearEvent();

    void SetNumLayers(G4int n);
    void AddToLayer(G4int layer, G4double edep);

    G4int GetHTotalID() const { return hTotalID; }
    G4int GetHLongID() const { return hLongID; }
    G4int GetHRadialID() const { return hRadialID; }

private:
    RootIO();
    static RootIO* fInstance;

    G4AnalysisManager* fAnalysisManager;

    std::vector<G4double> fLayerEdep;
    std::vector<G4double> fEdep;
    std::vector<G4ThreeVector> fPos;

    G4int hTotalID, hRadialID, hLongID, hXYID;
    std::vector<G4int> hLayerIDs;
};

#endif

