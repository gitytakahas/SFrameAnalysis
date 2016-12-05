#ifndef ScaleFactorTool_h
#define ScaleFactorTool_h

#include "../interface/ScaleFactor.h"
#include "TROOT.h"
#include "TFile.h"
#include <iostream>
#include <map>
#include <cmath>
#include <string>

// SFrame include(s):
#include "core/include/SError.h"
#include "plug-ins/include/SToolBase.h"




class ScaleFactorTool : public SToolBase {
  
  
  
  public:
    
    ScaleFactorTool( SCycleBase* parent, const char* name = "ScaleFactorTool" );
    ~ScaleFactorTool();
    void BeginInputData( const SInputData& id ) throw( SError );
    
    // MUON
    double get_Efficiency_MuTrig(double, double);
    double get_ScaleFactor_MuId(double, double); 
    double get_ScaleFactor_MuIdIso(double, double);
    std::string m_Mu_TrigFile;
    std::string m_Mu_IdIsoFile;
    std::string m_Mu_IdFile;
    std::string m_Mu_IsoFile;
    
    // ELECTRON
    double get_Efficiency_EleTrig(double, double);
    double get_ScaleFactor_EleId(double, double);
    double get_ScaleFactor_EleIdIso(double, double);
    std::string m_Ele_TrigFile;
    std::string m_Ele_IdIsoFile;
    std::string m_Ele_IdFile;
    std::string m_Ele_IsoFile;
    
    bool verbose = true;
    
    
    
  private:
    
    std::string m_name;
    ScaleFactor* m_ScaleFactor_MuTrig;
    ScaleFactor* m_ScaleFactor_MuIdIso;
    ScaleFactor* m_ScaleFactor_MuId;
    ScaleFactor* m_ScaleFactor_MuIso;
    ScaleFactor* m_ScaleFactor_EleTrig;
    ScaleFactor* m_ScaleFactor_EleIdIso;
    ScaleFactor* m_ScaleFactor_EleId;
    ScaleFactor* m_ScaleFactor_EleIso;
    
    
    
};


#endif // ScaleFactorTool_h
