#ifndef SVFitTool_h
#define SVFitTool_h

//#include "../interface/SVFitTool.h"
#include "../interface/SVfitStandaloneAlgorithm.h"
#include "../interface/SVfitStandaloneLikelihood.h"
#include "../interface/SVfitStandaloneMarkovChainIntegrator.h"
#include "../interface/svFitStandaloneAuxFunctions.h"

#include "TROOT.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include <TString.h>
#include <iostream>
#include <map>
#include <cmath>
#include <string>
#include <assert.h>

// SFrame include(s):
#include "core/include/SError.h"
#include "plug-ins/include/SToolBase.h"




class SVFitTool : public SToolBase {
  
  
  
  public:
    
    SVFitTool( SCycleBase* parent, const char* name = "SVFitTool" );
    ~SVFitTool();
    void BeginInputData( const SInputData& id ) throw( SError );
    
    void addMeasuredLeptonTau( const std::string& channel, const TLorentzVector lep, const TLorentzVector tau, int tauDecayMode );
    //void addMeasuredElectronTau( const TLorentzVector ele,   const TLorentzVector tau );
    //void addMeasuredMuonTau(     const TLorentzVector mu,    const TLorentzVector tau );
//     void addMeasuredTauToElectron( const double pt, const double eta, const double phi );
//     void addMeasuredTauToMuon(     const double pt, const double eta, const double phi );
//     void addMeasuredTauToHadrons(  const double pt, const double eta, const double phi, const double mass );
    double getSVFitMass( const double measuredMETx, const double measuredMETy,
                         const double covMET00, const double covMET01, const double covMET11,
                         unsigned int verbosity = 0 );
    void getSVFitMassAndPT( double& mass, double& pt,
                            const double measuredMETx, const double measuredMETy,
                            const double covMET00, const double covMET01, const double covMET11,
                            unsigned int verbosity = 0 );
    
    bool verbose = true;
    TFile* m_ResoFile;
    std::string m_ResoFilePath;
    //TString m_ResoFilePath;
    
    
    
  private:
    
    std::string m_name;
    std::vector<svFitStandalone::MeasuredTauLepton> m_measuredTauLeptons;


      
};


#endif // SVFitTool_h
