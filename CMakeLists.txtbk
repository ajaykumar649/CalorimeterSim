cmake_minimum_required(VERSION 3.10)
project(CalorimeterSim)

# --- Find packages ---
find_package(Geant4 REQUIRED)
find_package(ROOT REQUIRED)

# --- Include paths ---
include(${Geant4_USE_FILE})
include_directories(
  ${ROOT_INCLUDE_DIRS}
  ${Geant4_INCLUDE_DIR}
  ${PROJECT_SOURCE_DIR}/include
)

# --- Source files ---
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

# --- Executable target ---
add_executable(CalorimeterSim CalorimeterSim.cc ${sources} ${headers})

# --- Link libraries ---
target_link_libraries(CalorimeterSim ${Geant4_LIBRARIES} ${ROOT_LIBRARIES})

# --- Set C++ standard ---
set_property(TARGET CalorimeterSim PROPERTY CXX_STANDARD 17)

# --- Optional: Enable compile flags (debugging etc.) ---
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -Wall")

