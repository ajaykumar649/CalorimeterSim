/*#include "EventAction.hh"
#include "G4Event.hh"
#include "G4RunManager.hh"

EventAction::EventAction() {}
EventAction::~EventAction() {}

void EventAction::BeginOfEventAction(const G4Event*) {
    // Optional: Add something
}

void EventAction::EndOfEventAction(const G4Event*) {
    // Optional: Add something
}
*/
#include "EventAction.hh"
#include "G4Event.hh"
#include "G4RunManager.hh"
#include "RootIO.hh"

EventAction::EventAction() {}
EventAction::~EventAction() {}

void EventAction::BeginOfEventAction(const G4Event*) {
    RootIO::Instance()->ClearEvent();
}

void EventAction::EndOfEventAction(const G4Event*) {
    RootIO::Instance()->FillEvent();
}
