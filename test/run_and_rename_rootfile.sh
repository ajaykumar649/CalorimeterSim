#!/bin/bash

# ---- Default values from the macro file ----
DEFAULT_MAC="../macros/run_datacollection_final.mac"
TMP_MAC="tmp_run.mac"

# Extract defaults from macro if available
default_value() {
    grep "^$1" "$DEFAULT_MAC" | awk '{print $2}'
}

PARTICLE=${1:-$(default_value "/gun/particle")}
ENERGY=${2:-$(default_value "/gun/energy")}
NEVENTS=${3:-$(default_value "/run/beamOn")}

#ABSTHICK=${4:-$(default_value "/calor/setAbsThickness")}
#SCINTTHICK=${5:-$(default_value "/calor/setScintThickness")}

# Add units if user didn't supply them
if [[ "$4" =~ ^[0-9.]+$ ]]; then
  ABSTHICK="${4} mm"
else
  ABSTHICK=${4:-$(default_value "/calor/setAbsThickness")}
fi

if [[ "$5" =~ ^[0-9.]+$ ]]; then
  SCINTTHICK="${5} mm"
else
  SCINTTHICK=${5:-$(default_value "/calor/setScintThickness")}
fi


ABSMAT=${6:-$(default_value "/calor/setAbsMaterial")}

# Strip units for file name
ABSTHICK_VAL=${ABSTHICK//[!0-9.]/}
SCINTTHICK_VAL=${SCINTTHICK//[!0-9.]/}

echo "ℹ️ Using configuration:"
echo "   Particle     = $PARTICLE"
echo "   Energy       = $ENERGY GeV"
echo "   Events       = $NEVENTS"
echo "   Absorber     = $ABSTHICK ($ABSMAT)"
echo "   Scintillator = $SCINTTHICK"

# ---- Create modified macro file ----
cp "$DEFAULT_MAC" "$TMP_MAC"

sed -i "s|^/gun/particle .*|/gun/particle $PARTICLE|" "$TMP_MAC"
sed -i "s|^/gun/energy .*|/gun/energy ${ENERGY} GeV|" "$TMP_MAC"
sed -i "s|^/run/beamOn .*|/run/beamOn $NEVENTS|" "$TMP_MAC"
sed -i "s|^/calor/setAbsThickness .*|/calor/setAbsThickness $ABSTHICK|" "$TMP_MAC"
sed -i "s|^/calor/setScintThickness .*|/calor/setScintThickness $SCINTTHICK|" "$TMP_MAC"
sed -i "s|^/calor/setAbsMaterial .*|/calor/setAbsMaterial $ABSMAT|" "$TMP_MAC"

# ---- Run simulation ----
echo "🚀 Running Geant4 simulation..."
../build/CalorimeterSim "$TMP_MAC"

# ---- Output handling ----
OUTPUT_FILE="$PWD/output.root"
OUTPUT_DIR="$PWD/../Output"
RENAMED_FILE="$OUTPUT_DIR/${PARTICLE}_${ENERGY}GeV_${NEVENTS}evt_${ABSTHICK_VAL}mm_${ABSMAT}_${SCINTTHICK_VAL}mm.root"

mkdir -p "$OUTPUT_DIR"

if [ -f "$OUTPUT_FILE" ]; then
    mv "$OUTPUT_FILE" "$RENAMED_FILE"
    echo "✅ Renamed ROOT file to: $RENAMED_FILE"
else
    echo "❌ ROOT file not found after run."
fi

# ---- Cleanup ----
rm -f "$TMP_MAC"

