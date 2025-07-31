#!/bin/bash

MACRO="../macros/run_datacollection_final.mac"

# Extract values
PARTICLE=$(grep '^/gun/particle' "$MACRO" | awk '{print $2}')
ENERGY=$(grep '^/gun/energy' "$MACRO" | awk '{print $2 $3}' | sed 's/ //g')  # e.g., 10GeV

# Run Geant4
../build/./CalorimeterSim "$MACRO"

# Rename output.root
NEW_NAME="${PARTICLE}_${ENERGY}_output.root"
mv output.root "$NEW_NAME"

echo "Saved ROOT file as: $NEW_NAME"

