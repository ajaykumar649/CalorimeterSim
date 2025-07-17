// RootIO.hh
#ifndef ROOTIO_HH
#define ROOTIO_HH

#include "globals.hh"
#include "G4ThreeVector.hh"
#include <vector>
#include <map>

class TFile;
class TTree;
class TH1D;
class TH2D;

class RootIO {
public:
    static RootIO* Instance();
    ~RootIO();

    void SetFile(TFile* file);
    void SaveHit(G4double edep, G4ThreeVector pos);
    void FillEvent();
    void ClearEvent();
    void Write();

private:
    RootIO();
    static RootIO* fInstance;

    TFile* fFile;
    TTree* fTree;
    std::vector<G4double> fEdepVec, fXVec, fYVec, fZVec;

    TH1D* hRadial;
    TH1D* hLong;
    TH1D* hTotal;
    TH2D* hXY;
    std::map<int, TH2D*> hLayerXY;
};

#endif

