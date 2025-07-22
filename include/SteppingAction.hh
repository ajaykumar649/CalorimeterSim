#ifndef STEPPINGACTION_HH
#define STEPPINGACTION_HH

#include "G4UserSteppingAction.hh"

class SteppingAction : public G4UserSteppingAction {
public:
    SteppingAction();              // declaration only
    virtual ~SteppingAction();     // declaration only

    virtual void UserSteppingAction(const G4Step*);
};

#endif

