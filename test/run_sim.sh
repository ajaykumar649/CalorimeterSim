#!/bin/bash

# === Input Parameters ===
PARTICLE="$1"
ENERGY="$2"
NEVENTS="$3"

if [ -z "$PARTICLE" ] || [ -z "$ENERGY" ] || [ -z "$NEVENTS" ]; then
  echo "❌ Usage: $0 <particle> <energy in GeV> <nEvents>"
  echo "Example: $0 e- 10 10000"
  exit 1
fi

# === Paths ===
MACRO_TEMPLATE="../macros/run_datacollection_template.mac"
MACRO="../macros/run_temp.mac"
BINARY="../build/CalorimeterSim"
ROOTDIR="../build"
OUTPUTDIR="../Output"

# === Validate Files ===
if [ ! -f "$MACRO_TEMPLATE" ]; then
  echo "❌ Template macro file not found at $MACRO_TEMPLATE"
  exit 1
fi

if [ ! -x "$BINARY" ]; then
  echo "❌ Simulation binary not found or not executable at $BINARY"
  exit 1
fi

# === Create Temporary Macro with Substituted Values ===
cp "$MACRO_TEMPLATE" "$MACRO"

# macOS-compatible sed (note the '' after -i)
sed -i '' "s|^/gun/particle .*|/gun/particle $PARTICLE|" "$MACRO"
sed -i '' "s|^/gun/energy .*|/gun/energy ${ENERGY} GeV|" "$MACRO"
sed -i '' "s|^/run/beamOn .*|/run/beamOn $NEVENTS|" "$MACRO"

# === Run Simulation ===
"$BINARY" "$MACRO" || { echo "❌ Simulation failed"; exit 1; }

# === Move Output ===
RAW_FILE="$ROOTDIR/output.root"
NEW_NAME="${PARTICLE}_${ENERGY}GeV_${NEVENTS}evt.root"
TARGET_FILE="$OUTPUTDIR/$NEW_NAME"

mkdir -p "$OUTPUTDIR"

if [ -f "$RAW_FILE" ]; then
  mv "$RAW_FILE" "$TARGET_FILE"
  echo "✅ ROOT file saved as: $TARGET_FILE"
else
  echo "❌ ROOT file not found at $RAW_FILE"
  exit 1
fi

