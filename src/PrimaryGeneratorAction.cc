#include "PrimaryGeneratorAction.hh"
#include "G4ParticleTable.hh"
#include "G4Electron.hh"
#include "G4SystemOfUnits.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction() {
    fGun = new G4ParticleGun(1);
    fGun->SetParticleDefinition(G4Electron::Definition());
    fGun->SetParticlePosition(G4ThreeVector(0,0,-50*cm));
    fGun->SetParticleMomentumDirection(G4ThreeVector(0,0,1));
}
PrimaryGeneratorAction::~PrimaryGeneratorAction() { delete fGun; }
void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event) {
    auto* gun = fGun;
    auto* pt = G4ParticleTable::GetParticleTable();
    gun->SetParticleEnergy(energy*GeV); // energy from UI macro
    gun->GeneratePrimaryVertex(event);
}

