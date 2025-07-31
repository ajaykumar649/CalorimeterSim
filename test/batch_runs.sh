#!/bin/bash
# batch_runs.sh

PARTICLES=("e-" "pi-" "proton")
ENERGIES=(1 5 10)  # in GeV
ABS_THICKS=(6 8)   # in mm
SCINT_THICKS=(2 4) # in mm
MATERIALS=("G4_Pb" "G4_Fe")

for P in "${PARTICLES[@]}"; do
  for E in "${ENERGIES[@]}"; do
    for ABS in "${ABS_THICKS[@]}"; do
      for SCINT in "${SCINT_THICKS[@]}"; do
        for MAT in "${MATERIALS[@]}"; do
          ./run_and_rename_rootfile.sh "$P" "$E" 100 "$ABS" "$SCINT" "$MAT"
        done
      done
    done
  done
done

