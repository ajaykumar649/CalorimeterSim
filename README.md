CalorimeterSim
A Geant4-based simulation of electromagnetic showers in a sampling calorimeter, designed for high-energy physics studies. The project simulates a 10 GeV electron interacting with a 10-layer lead-scintillator calorimeter, with energy deposition analyzed using ROOT and Python.
Prerequisites

Docker: For reproducible environment (ajaykumar49/calorimeter-dev:v1.3).
Geant4: Version compatible with the Docker image.
ROOT: For data analysis.
Python 3: With uproot, numpy, matplotlib (see requirements.txt).
CMake: For building the simulation.

Setup

Clone the Repository:
git clone https://github.com/ajaykumar649/CalorimeterSim.git
cd CalorimeterSim


Docker Setup:

Pull the Docker image:docker pull ajaykumar49/calorimeter-dev:v1.3


Or load locally:docker load -i ~/calorimeter-dev_v1.3.tar




Launch Container:
docker run -it --env DISPLAY=$DISPLAY --volume $PWD:/home/ajay/CalorimeterSim \
  --workdir /home/ajay/CalorimeterSim ajaykumar49/calorimeter-dev:v1.3


Build Simulation:
source /opt/geant4/bin/geant4.sh
mkdir -p build
cd build
cmake ..
make -j$(nproc)



Usage

Run Simulation:
./CalorimeterSim ../macros/vis.mac


Outputs output.root with energy deposition data.


Analyze Data:

Use scripts/plot_profiles.py to generate visualizations:python3 scripts/plot_profiles.py


Install dependencies:pip install -r requirements.txt





Key Files

CalorimeterSim.cc: Main simulation executable.
include/, src/: Geant4 classes for detector construction, actions, and ROOT I/O.
macros/vis.mac: Visualization macro for Geant4.
scripts/plot_profiles.py: Python script for analyzing output.root and plotting energy profiles.

Notes

Prepared on July 19, 2025, by Dr. Ajay Kumar (ajaykumar49@bhu.ac.in).
Visualization outputs (e.g., PNGs) are excluded via .gitignore to reduce repository size.
For issues, contact the repository owner or open an issue on GitHub.
