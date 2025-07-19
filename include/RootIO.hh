#ifndef RootIO_h
#define RootIO_h 1

#include "G4ThreeVector.hh"
#include "G4RootAnalysisManager.hh"
#include <mutex>

class RootIO {
public:
  static RootIO* Instance();
  void OpenFile(const G4String& fileName);
  void SaveHit(G4double edep, G4ThreeVector pos);
  void FillEvent();
  void ClearEvent();
  void Write();

  G4int GetHRadialID() const { return hRadialID; }
  G4int GetHLongID() const { return hLongID; }
  G4int GetHTotalID() const { return hTotalID; }
  G4int GetHXYID() const { return hXYID; }

private:
  RootIO();
  ~RootIO();
  static RootIO* fInstance;
  static std::mutex fMutex;

  G4RootAnalysisManager* fAnalysisManager;
  G4int hRadialID;
  G4int hLongID;
  G4int hTotalID;
  G4int hXYID;
  std::map<int, G4int> hLayerXYIDs;

  std::vector<double> fEdepVec;
  std::vector<double> fXVec;
  std::vector<double> fYVec;
  std::vector<double> fZVec;
};

#endif
