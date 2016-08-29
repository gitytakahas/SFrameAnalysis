// Dear emacs, this is -*- c++ -*-
// $Id: CycleCreators.py 344 2012-12-13 13:10:53Z krasznaa $
#ifndef TauTauAnalysis_H
#define TauTauAnalysis_H

// SFrame include(s):
#include "core/include/SCycleBase.h"

// ROOT include(s):
//#include <TBits.h>
//#include "TMatrixD.h"
// External include(s):
#include "../NtupleVariables/include/JetNtupleObject.h"
#include "../NtupleVariables/include/Jet.h"
#include "../NtupleVariables/include/EventInfoNtupleObject.h"
#include "../NtupleVariables/include/ElectronNtupleObject.h"
#include "../NtupleVariables/include/Electron.h"
#include "../NtupleVariables/include/MuonNtupleObject.h"
#include "../NtupleVariables/include/Muon.h"
#include "../NtupleVariables/include/TauNtupleObject.h"
#include "../NtupleVariables/include/Tau.h"
#include "../NtupleVariables/include/MissingEtNtupleObject.h"
#include "../NtupleVariables/include/MissingEt.h"
#include "../NtupleVariables/include/GenParticleNtupleObject.h"
#include "../NtupleVariables/include/GenParticle.h"
#include "../GoodRunsLists/include/TGoodRunsList.h"
#include "../PileupReweightingTool/include/PileupReweightingTool.h"
#include "../BTaggingTools/include/BTaggingScaleTool.h"
#include "../SVFit/include/NSVfitStandaloneAlgorithm.h"
//#include "../SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"
#include "../LepEff2016/interface/ScaleFactorTool.h"

//class TH1D;
//class TH2D;
//class TRandom3;
//class TBits;

#include <TFile.h>
#include <TTree.h>
#include <TMath.h>

namespace UZH {
  class Jet;
  class Electron;
  class Muon;
  class Tau;
  class MissingEt;
  class GenParticle;
}

/**
 *   @short Put short description of class here
 *
 *          Put a longer description over here...
 *
 *  @author Put your name here
 * @version $Revision: 344 $
 */
class TauTauAnalysis : public SCycleBase {

public:
  
  /// Enumeration of all cut flags
  typedef enum {
    kBeforeCuts,            // C0
    kJSON,                  // C1
    kTrigger,               // C2
    kMetFilters,            // C3
    kLepton,                // C4
    kTau,                   // C5
    kLeptonDR,              // C6
    kNumCuts                // last!
  } SelectionCuts;
  
  /// static array of all cut names
  static const std::string kCutName[ kNumCuts ];
  
   /// Default constructor
   TauTauAnalysis();
   /// Default destructor
   ~TauTauAnalysis();

   /// Function called at the beginning of the cycle
   virtual void BeginCycle() throw( SError );
   /// Function called at the end of the cycle
   virtual void EndCycle() throw( SError );

   /// Function called at the beginning of a new input data
   virtual void BeginInputData( const SInputData& ) throw( SError );
   /// Function called after finishing to process an input data
   virtual void EndInputData  ( const SInputData& ) throw( SError );

   /// Function called after opening each new input file
   virtual void BeginInputFile( const SInputData& ) throw( SError );

   /// Function called for every event
   virtual void ExecuteEvent( const SInputData&, Double_t ) throw( SError );
   
   /// Function to check good lumi section
   virtual bool isGoodEvent(int runNumber, int lumiSection);
   
   /// Function to check for trigger pass
   virtual bool passTrigger();
   
   /// Function to check for MET filters pass
   virtual bool passMETFilters();
   
   /// Function to obtain event weights for MC
   virtual double getEventWeight();
   
   /// Function to clear/reset all output branches
  //   virtual void clearBranches();
   
  /// Function to fill cut flow
  //  virtual void fillCutflow( const std::string histName, const std::string dirName, const Int_t id, const Double_t weight = 1.);
  virtual void fillCutflow(TString histName, TString dirName, const Int_t id, const Double_t weight);
   
  /// Function GenFilter  to select Z to tautau events
  virtual void genFilterZtautau();
  
  /// Function to book tree branches
  virtual void FillBranches(const std::string& channel,  const std::vector<UZH::Jet>& Jet, const UZH::Tau& tau, const  TLorentzVector& lepton, const UZH::MissingEt& met );
  
  /// Function to fill histograms

private:
   //
   // Put all your private variables here
   //
  
  //
  // Input variable objects:
  //
  Ntuple::JetNtupleObject         m_jetAK4;            ///< jet container
  Ntuple::EventInfoNtupleObject   m_eventInfo; ///< event info container
  Ntuple::ElectronNtupleObject    m_electron;            ///< electron container
  Ntuple::MuonNtupleObject        m_muon;            ///< muon container
  Ntuple::TauNtupleObject         m_tau;            ///< tau container
  Ntuple::MissingEtNtupleObject   m_missingEt;            ///< missing E_T container
  Ntuple::GenParticleNtupleObject m_genParticle;            ///< gen particle container
  
  
  //
  // Further objects
  //
  Root::TGoodRunsList m_grl;
  PileupReweightingTool m_pileupReweightingTool;
  //  BTaggingScaleTool m_bTaggingScaleTool;
  ScaleFactorTool m_ScaleFactorTool;

  TLorentzVector applySVFitSemileptonic    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);
  TLorentzVector applySVFitHadronic    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);

  //
  // XML settings for TauTauAnalysis
  //
  // naming
  std::string m_recoTreeName;       ///< name of tree with reconstructed objects in ntuple
  // std::string m_outputTreeName;    ///< name of output tree
  std::vector<std::string> m_outputTreeName_ch_; ///< name of output trees for analysis
  std::vector<std::string> channels_;

  int m_ntupleLevel;               ///< cut at which branches for ntuple are written out
  std::string m_jetAK4Name;            ///< name of AK4 jet collection in tree with reconstructed objects
  std::string m_electronName;       ///< name of electron collection in tree with reconstructed objects
  std::string m_muonName;       ///< name of muon collection in tree with reconstructed objects
  std::string m_tauName;       ///< name of tau collection in tree with reconstructed objects
  std::string m_missingEtName;       ///< name of missing E_T collection in tree with reconstructed objects
  std::string m_genParticleName;       ///< name of gen particle collection in tree with reconstructed objects
  
  // flags
  bool        m_isData;
  bool        m_isSignal;
  bool        m_applyMETFilters;
  
  bool m_FillHist;

  // cuts
  // jets
  double      m_jetPtCut;         ///< cut on jet pT
  double      m_jetEtaCut;        ///< cut on jet eta
  double      m_AK4jetPtCut;         ///< cut on jet pT
  double      m_AK4jetEtaCut;        ///< cut on jet eta
  // substructure cuts
  // b-tagging
  double      m_csvMin;
  
  
  // electrons
  double         m_electronPtCut;
  double         m_electronEtaCut;
  double         m_electronD0Cut;
  double         m_electronDzCut;
  double         m_electronIsoCut;

  // muons
  double         m_muonPtCut;
  double         m_muonEtaCut;
  double         m_muonD0Cut;
  double         m_muonDzCut;
  double         m_muonIsoCut;
  
  // leptons=muons and electrons
  double         m_leptonPtCut;
  double         m_leptonEtaCut;

 // taus
  double         m_tauPtCut;
  double         m_tauEtaCut;
  double         m_tauDzCut;

  // MET
  double         m_metCut;
   
  // further settings
  std::string m_jsonName;
  std::string m_TrigSF_muonName;
  std::string m_IDSF_muonName;
  std::string m_IsoSF_muonName;
  std::string m_IDSF_eleName;

  // other variables needed
  std::vector<std::string> m_triggerNames_mutau;
  std::vector<std::string> m_triggerNames_eletau;
  
  int mu_tau;
  int ele_tau;
  

  ///
  /// branches
  ///

  //  double b_weightBtag;
  //  double b_weightBtag_veto;
  
  Float_t b_weight_;
  Float_t b_weightGen_;
  Float_t b_weightPU_;
  Float_t  b_weightLepID_; 
  Float_t  b_weightLepIso_; 
  Int_t b_runNumber_;
  Int_t b_eventNumber_;
  Int_t b_lumiBlock_;

  Float_t b_tau_pt_;
  Float_t b_tau_eta_;
  Float_t b_tau_phi_;
  Int_t b_tau_iso_;
  Float_t b_tau_iso_raw_;
  Int_t b_tau_againstEle_;
  Int_t b_tau_againstMu_;

  Float_t b_l2_pt_;
  Float_t b_l2_eta_;
  Float_t b_l2_phi_;
  Float_t b_met_;
  Float_t b_met_phi_;
  Float_t b_vis_mass_ll_;
  Float_t b_dR_ll_;

  Float_t b_H_Mass_SVFit_;
  Float_t b_H_Pt_SVFit_;
  Float_t b_H_Eta_SVFit_;
  Float_t b_H_Phi_SVFit_;

  Int_t b_njets_;
  Int_t b_npu_; 
  bool b_GenEvent_Htata_;
  bool b_GenEvent_Ztata_;
  Int_t b_ChannelInt_; //0 mutau; 1 ele; 2 tautau

  Int_t b_isData_;

  TTree *tree[2];
  TFile *file[2];

  bool GenEvent_Htata_filter;
  bool GenEvent_Ztata_filter;


   // Macro adding the functions for dictionary generation
   ClassDef( TauTauAnalysis, 0 );

}; // class TauTauAnalysis

#endif // TauTauAnalysis_H

