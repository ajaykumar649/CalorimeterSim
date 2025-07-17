# CalorimeterSim 🚀  
GEANT4 Sampling Calorimeter Simulation with ROOT Output

This repository contains the simulation code for a high-energy sampling calorimeter using [GEANT4](https://geant4.web.cern.ch/) and [ROOT](https://root.cern/). The simulation can be run inside a pre-built Docker container to simplify dependencies.

---

## 🧰 Features

- GEANT4-based calorimeter simulation.
- ROOT-based output (`.root` files with histograms & ntuples).
- Docker-based reproducible environment.
- Example analysis scripts and plots.

---

## 🔧 Getting Started

### 1. Clone this Repository

```bash
git clone https://github.com/ajaykumar649/CalorimeterSim.git
cd CalorimeterSim


2. Download or Transfer the Docker Image
If you received the Docker image calorimeter-dev-v1.1.tar (e.g. from USB):

# From your USB (assume it's mounted at /Volumes/CALO_USB)
cp /Volumes/CALO_USB/calorimeter-dev-v1.1.tar .
Or download it from Docker Hub (if available):

docker pull ajaykumar49/calorimeter-dev:v1.1
3. Load Docker Image (if using tar file)
docker load -i calorimeter-dev-v1.1.tar
4. Run the Container
Mount this folder (CalorimeterSim) into the container as /workspace:

docker run --rm -it \
  -v $(pwd):/workspace \
  ajaykumar49/calorimeter-dev:v1.1 \
  bash
This will start a bash shell inside the container with your code mounted at /workspace.

🧪 Inside the Container

Once inside:

cd /workspace
mkdir -p build
cd build
cmake ..
make -j$(nproc)
./CalorimeterSim
Output ROOT files (e.g., output.root) and histograms will be stored in build/.

📊 ROOT Analysis

Example analysis (outside or inside container):

root -l scripts/analyze.C
Or open the ROOT file interactively:

root -l build/output.root


CalorimeterSim/
├── CMakeLists.txt
├── src/                  # GEANT4 source code
├── include/              # Headers
├── macros/               # Optional macros
├── scripts/              # ROOT analysis scripts
├── Dockerfile            # Used to build the container
├── calorimeter-dev-v1.1.tar (optional) # Prebuilt container image
├── README.md


License

This project is licensed under the MIT License.

License

This project is licensed under the MIT License.
