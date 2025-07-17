#include "RunAction.hh"
#include "RootIO.hh"

#include "G4Run.hh"
#include "G4SystemOfUnits.hh"
#include "G4ios.hh"

#include "TFile.h"
#include "TH1D.h"

// Static member initialization
TH1D* RunAction::hLongitudinal = nullptr;
TH1D* RunAction::hTotal = nullptr;
TH1D* RunAction::hRadial = nullptr;  // <-- Add this line
TFile* RunAction::rootFile = nullptr;
TH2D* RunAction::hXY = nullptr;


RunAction::RunAction() {}
RunAction::~RunAction() {}

void RunAction::BeginOfRunAction(const G4Run*) {
    G4cout << "### Run started" << G4endl;

    // Create ROOT file
    rootFile = new TFile("output.root", "RECREATE");

    // Set file in RootIO singleton
    RootIO::Instance()->SetFile(rootFile);

    // Book histograms
    hLongitudinal = new TH1D("hLong", "Energy Deposition per Layer", 40, 0, 40);
    hLongitudinal->GetXaxis()->SetTitle("Layer Number");
    hLongitudinal->GetYaxis()->SetTitle("Energy Deposition [MeV]");

    hTotal = new TH1D("hTotal", "Total Energy Deposition", 100, 0, 50);
    hTotal->GetXaxis()->SetTitle("E_{total} [MeV]");
    hTotal->GetYaxis()->SetTitle("Events");

    hRadial = new TH1D("hRadial", "Radial Energy Deposition", 100, 0, 100); // cm or mm
    hRadial->GetXaxis()->SetTitle("Radius [mm]");
    hRadial->GetYaxis()->SetTitle("Energy Deposition [MeV]");


    hXY = new TH2D("hXY", "XY Energy Deposition", 100, -100, 100, 100, -100, 100);
    hXY->GetXaxis()->SetTitle("X [mm]");
    hXY->GetYaxis()->SetTitle("Y [mm]");

}

void RunAction::EndOfRunAction(const G4Run*) {
    G4cout << "### Run ended, writing to ROOT file: output.root" << G4endl;

    // Write tree first
    RootIO::Instance()->Write();

    // Write histograms
    rootFile->cd();
    hLongitudinal->Write();
    hTotal->Write();
    hRadial->Write();	
    hXY->Write();

    // Close and cleanup
    rootFile->Close();
    delete rootFile;
    rootFile = nullptr;
}

