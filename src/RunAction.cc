#include "RunAction.hh"
#include "RootIO.hh"
#include "G4Run.hh"
#include "G4ios.hh"

RunAction::RunAction() : G4UserRunAction() {}

RunAction::~RunAction() {}

void RunAction::BeginOfRunAction(const G4Run*) {
  G4cout << "### Run started" << G4endl;
  RootIO::Instance()->OpenFile("output.root");
}

void RunAction::EndOfRunAction(const G4Run*) {
  G4cout << "### Run ended, writing to ROOT file: output.root" << G4endl;
  RootIO::Instance()->Write();
}
