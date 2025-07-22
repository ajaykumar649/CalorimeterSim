# CalorimeterSim

A Geant4-based simulation of electromagnetic showers in a sampling calorimeter, designed for high-energy physics studies. The project simulates a 10 GeV electron interacting with a 10-layer lead-scintillator calorimeter, with energy deposition analyzed using ROOT and Python.

---

## 📦 Prerequisites

- **Docker**: For reproducible environment (`ajaykumar49/calorimeter-dev:v1.3`)
- **Geant4**: Version compatible with the Docker image
- **ROOT**: For data analysis
- **Python 3**: With `uproot`, `numpy`, `matplotlib` (see `requirements.txt`)
- **CMake**: For building the simulation

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ajaykumar649/CalorimeterSim.git
cd CalorimeterSim
2. Docker Setup
Pull the Docker image:

docker pull ajaykumar49/calorimeter-dev:v1.3
Or load locally:

docker load -i ~/calorimeter-dev_v1.3.tar
3. Launch Container
docker run -it \
  --env DISPLAY=$DISPLAY \
  --volume $PWD:/home/ajay/CalorimeterSim \
  --workdir /home/ajay/CalorimeterSim \
  ajaykumar49/calorimeter-dev:v1.3
4. Build Simulation
source /opt/geant4/bin/geant4.sh
mkdir -p build
cd build
cmake ..
make -j$(nproc)
🚀 Usage

Run Simulation
./CalorimeterSim ../macros/vis.mac
Outputs output.root with energy deposition data.

📊 Analyze Data

Generate Plots
cd  scripts
python3 "name of python script"
Install Python Dependencies

python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

