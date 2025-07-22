#include "PrimaryGeneratorAction.hh"
#include "G4ParticleTable.hh"
#include "G4Electron.hh"
#include "G4SystemOfUnits.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction() {
    fGun = new G4ParticleGun(1);
    fGun->SetParticleDefinition(G4Electron::Definition());
    // Set default values, overridden by macro /gun commands
    fGun->SetParticlePosition(G4ThreeVector(0, 0, -50 * cm));
    fGun->SetParticleEnergy(10 * MeV); // Default, overridden by /gun/energy
    fGun->SetParticleMomentumDirection(G4ThreeVector(0, 0, 1));
}

PrimaryGeneratorAction::~PrimaryGeneratorAction() {
    delete fGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event) {
    fGun->GeneratePrimaryVertex(event);
}
