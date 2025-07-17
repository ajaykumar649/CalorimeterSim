#ifndef RUNACTION_HH
#define RUNACTION_HH

#include "G4UserRunAction.hh"
#include "globals.hh"
#include "TH2D.h"  // <-- ADD THIS LINE

class TH1D;
class TFile;

class RunAction : public G4UserRunAction {
public:
    RunAction();
    virtual ~RunAction();

    virtual void BeginOfRunAction(const G4Run*);
    virtual void EndOfRunAction(const G4Run*);

    // Static access to histograms (used in SteppingAction)
    static TH1D* hLongitudinal;
    static TH1D* hTotal;
    static TH1D* hRadial;	
    static TH2D* hXY;  // Add this line

private:
    static TFile* rootFile;
};

#endif

