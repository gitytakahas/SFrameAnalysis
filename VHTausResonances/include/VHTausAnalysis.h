// Dear emacs, this is -*- c++ -*-
// $Id: CycleCreators.py 344 2012-12-13 13:10:53Z krasznaa $
#ifndef VHTausAnalysis_H
#define VHTausAnalysis_H

// SFrame include(s):
#include "core/include/SCycleBase.h"

// ROOT include(s):
#include <TBits.h>
#include "TMatrixD.h"
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

class TH1D;
class TH2D;
class TRandom3;
class TBits;
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
class VHTausAnalysis : public SCycleBase {

public:
  
  /// Enumeration of all cut flags
  typedef enum {
    kBeforeCuts,            // C0
    kJSON,                  // C1
    kTrigger,               // C2
    kMetFilters,            // C3
    kMet,                   // C4
    kJet,                   // C5
    kTau,                   // C6
    kTauIsolation,          // C7
    kLepton,                // C8
    kLeptonDR,                // C9
    kMassWindow,            // C10
    kTau21,                 // C11
    kSubjetSingleTag,       // C12
    kSubjetDoubleTag,       // C13
    kNumCuts                // last!
  } SelectionCuts;
  
  /// static array of all cut names
  static const std::string kCutName[ kNumCuts ];
  
   /// Default constructor
   VHTausAnalysis();
   /// Default destructor
   ~VHTausAnalysis();

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
   virtual void clearBranches();
   
   /// Function to fill cut flow
   virtual void fillCutflow( const std::string histName, const std::string dirName, const TBits& cutmap, const Double_t weight );
   
   /// Function to book histograms
   virtual void bookHistograms( const TString& directory );
  /// Function GenFilter  to select Z to tautau events
  virtual void genFilterZtautau();
  
  /// Function to book histograms for trigger choice
  virtual void bookTriggerHistos(const TString& directory );
  virtual void checkTrigger(const TString& directory ,const std::string& channel);
  virtual void checkTriggerTurnOn();
  virtual void checkTriggerOfflineSelection(const TString& directory,  const UZH::Jet& Jet,const UZH::Tau& tau,const  TLorentzVector& lepton ,const  bool& ID , const  double& leptonIso,  const UZH::MissingEt& met,const std::string& channel ,const  double& HT );
 
  /// Function to book tree branches
  virtual void FillBranches(const std::string& channel,  const UZH::Jet& Jet, const double& Jet_tau21, const double& Jet_tau31, const double& Jet_tau32, const int& Jet_nTaggedSubjets, const double& Jet_subjet0_csv, const double& Jet_subjet1_csv, const double& ak8jet0_subjet01_dr,  const double& ak8jet0_subjet01_deta, const double& ak8jet0_subjet01_dphi, const double& b_weight, const double& b_weightGen,  const double& b_weightPU, const double& b_weightBtag,  const double& b_weightBtag_veto,  const double& b_runNumber, const double& b_eventNumber,const double& b_lumiBlock,  const UZH::Tau& tau, const  TLorentzVector& lepton, const UZH::MissingEt& met );
  
  virtual void passTrigger_branches(const std::string& channel);
  
  /// Function to fill histograms
  virtual void fillHistograms( const TString& directory, const UZH::Jet& vectorJet, const UZH::Jet& higgsJet, const TLorentzVector& diJet, const double& vJet_tau21, const double& vJet_tau31, const double& vJet_tau32, const int& vJet_nTaggedSubjets, const double& vJet_subjet0_csv, const double& vJet_subjet1_csv, const double& hJet_tau21, const double& hJet_tau31, const double& hJet_tau32, const int& hJet_nTaggedSubjets, const double& hJet_subjet0_csv, const double& hJet_subjet1_csv, const double& deta, const double& dphi, const double& dr );

private:
   //
   // Put all your private variables here
   //
  
  //
  // Input variable objects:
  //
  Ntuple::JetNtupleObject         m_jetAK4;            ///< jet container
  Ntuple::JetNtupleObject         m_jetAK8;            ///< jet container
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
  BTaggingScaleTool m_bTaggingScaleTool;
  ScaleFactorTool m_ScaleFactorTool;

  TLorentzVector applySVFitSemileptonic    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);
  TLorentzVector applySVFitHadronic    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);
  TLorentzVector applySVFitStandaloneSemileptonicEle    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);
  TLorentzVector applySVFitStandaloneSemileptonicMu    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);
  TLorentzVector applySVFitStandaloneHadronic    (float cov00, float cov10, float cov11, float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2);

  //
  // XML settings for VHAnalysis
  //
  // naming
  std::string m_recoTreeName;       ///< name of tree with reconstructed objects in ntuple
  // std::string m_outputTreeName;    ///< name of output tree
  std::vector<std::string> m_outputTreeName_ch_; ///< name of output trees for analysis
  std::vector<std::string> channels_;

  int m_ntupleLevel;               ///< cut at which branches for ntuple are written out
  std::string m_jetAK4Name;            ///< name of AK4 jet collection in tree with reconstructed objects
  std::string m_jetAK8Name;       ///< name of AK8 jet collection in tree with reconstructed objects
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
  double      m_mjjCut;           ///< cut on dijet mass
  double      m_jetDeltaEtaCut;   ///< cut on DeltaEta between selected jets
  // substructure cuts
  double      m_tau21HPCut;
  double      m_tau21LPCut;
  double      m_mVLowSidebandCut;
  double      m_mWLowerCut;
  double      m_mWUpperCut;
  double      m_mZLowerCut;
  double      m_mZUpperCut;
  double      m_mHLowerCut;
  double      m_mHUpperCut;
  // b-tagging
  double      m_csvMin;
  
  
  // electrons
  double         m_electronPtCut;
  double         m_electronEtaCut;

  // muons
  double         m_muonPtCut;
  double         m_muonEtaCut;
  
  // leptons=muons and electrons
  double         m_leptonPtCut;
  double         m_leptonEtaCut;

 // taus
  double         m_tauPtCut;
  double         m_tauEtaCut;
  bool           m_tauIsoCut;

  // MET
  double         m_metCut;
   
  // further settings
  std::string m_jsonName;
  std::string m_TrigSF_muonName;
  std::string m_IDSF_muonName;
  std::string m_IsoSF_muonName;
  std::string m_IDSF_eleName;

  // other variables needed
  std::vector<std::string> m_triggerNames;
  std::vector<std::string> m_catNames;
  
  int mu_tau;
  int ele_tau;
  

  int N_AK4;
  int taggedAK4_L;
  int taggedAK4_M;
  int taggedAK4_T;

  int N_tight_muons;
  int N_tight_electrons;

  ///
  /// branches
  ///
  double b_weight;
  double b_weightGen;
  double b_weightPU;
  double b_weightBtag;
  double b_weightBtag_veto;
  
  // event variables
  int b_runNumber;
  int b_eventNumber;
  int b_lumiBlock;
  
  // use flat variables for direct input in TMVA
  Double_t   b_ak8jet0_pt;
  Double_t   b_ak8jet0_phi;
  Double_t   b_ak8jet0_eta;
  Double_t   b_ak8jet0_e;
  Double_t   b_ak8jet0_tau21;
  Double_t   b_ak8jet0_m;
  Double_t   b_ak8jet0_mpruned;
  Double_t   b_ak8jet0_csv;
  Double_t   b_ak8jet1_pt;
  Double_t   b_ak8jet1_phi;
  Double_t   b_ak8jet1_eta;
  Double_t   b_ak8jet1_e;
  Double_t   b_ak8jet1_tau21;
  Double_t   b_ak8jet1_m;
  Double_t   b_ak8jet1_mpruned;
  Double_t   b_ak8jet1_csv;
  Double_t   b_ak8jet0_subjet01_dr;
  Double_t   b_ak8jet0_subjet01_deta;
  Double_t   b_ak8jet0_subjet01_dphi;
  Double_t   b_ak8jet0_subjet0_pt;
  Double_t   b_ak8jet0_subjet1_pt;
  Double_t   b_ak8jet0_subjet0_csv;
  Double_t   b_ak8jet0_subjet1_csv;
  Double_t   b_ak8jet1_subjet01_dr;
  Double_t   b_ak8jet1_subjet01_deta;
  Double_t   b_ak8jet1_subjet01_dphi;
  Double_t   b_ak8jet1_subjet0_pt;
  Double_t   b_ak8jet1_subjet1_pt;
  Double_t   b_ak8jet1_subjet0_csv;
  Double_t   b_ak8jet1_subjet1_csv;
  
  std::vector<Int_t>      b_selection_bits;
  std::vector<Int_t>      b_selection_lastcut;


 // use flat variables for direct input in analysis framework 
  /// branches
  ///
  std::map<std::string,Double_t> b_weight_;
  std::map<std::string,Double_t> b_weightGen_;
  std::map<std::string,Double_t> b_weightPU_;
  std::map<std::string,Double_t> b_weightBtag_;
  std::map<std::string,Double_t> b_weightBtag_veto_;
  std::map<std::string,Double_t> b_weightTrigSemi_;
  std::map<std::string,Double_t>  b_weightLepID_; 
  std::map<std::string,Double_t>  b_weightLepIso_; 
  
  // event variables
  std::map<std::string,int> b_runNumber_;
  std::map<std::string,int> b_eventNumber_;
  std::map<std::string,int> b_lumiBlock_;

  std::map<std::string,Double_t>   b_ak8jet0_pt_;
  std::map<std::string,Double_t>   b_ak8jet0_phi_;
  std::map<std::string,Double_t>   b_ak8jet0_eta_;
  std::map<std::string,Double_t>   b_ak8jet0_e_;
  std::map<std::string,Double_t>   b_ak8jet0_tau21_;
  std::map<std::string,Double_t>   b_ak8jet0_m_;
  std::map<std::string,Double_t>   b_ak8jet0_mpruned_;
  std::map<std::string,Double_t>   b_ak8jet0_msoftdrop_;
  std::map<std::string,Double_t>   b_ak8jet0_csv_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet01_dr_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet01_deta_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet01_dphi_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet0_pt_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet1_pt_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet0_csv_;
  std::map<std::string,Double_t>   b_ak8jet0_subjet1_csv_;


  std::map<std::string,Double_t> b_tau_pt_;
  std::map<std::string,Double_t> b_tau_eta_;
  std::map<std::string,Double_t> b_tau_phi_;
  std::map<std::string,Double_t> b_tau_Iso_;
  std::map<std::string,Double_t> b_tau_IsoRaw_;
  std::map<std::string,Double_t> b_tau_againstEle_;
  std::map<std::string,Double_t> b_tau_againstMu_;

  std::map<std::string,Double_t> b_seclepton_pt_;
  std::map<std::string,Double_t> b_seclepton_eta_;
  std::map<std::string,Double_t> b_seclepton_phi_;
  std::map<std::string,Double_t> b_met_;
  std::map<std::string,Double_t> b_met_phi_;
  std::map<std::string,Double_t> b_vis_mass_ll_;
  std::map<std::string,Double_t> b_dR_ll_;

  std::map<std::string,Double_t> b_H_Mass_SVFit_;
  std::map<std::string,Double_t> b_H_Pt_SVFit_;
  std::map<std::string,Double_t> b_H_Eta_SVFit_;
  std::map<std::string,Double_t> b_H_Phi_SVFit_;
  std::map<std::string,Double_t> b_X_Mass_SVFit_;
  std::map<std::string,Double_t> b_X_Pt_SVFit_;
  std::map<std::string,Double_t> b_X_Eta_SVFit_;
  std::map<std::string,Double_t> b_X_Phi_SVFit_;


  std::map<std::string,std::vector<TBits>>      b_selection_bits_;
  std::map<std::string,Int_t>      b_selection_lastcut_;

  std::map<std::string,bool> b_trig_HT800_;
  std::map<std::string,bool> b_trig_ak8Jet360_Trim30_;
  std::map<std::string,bool> b_trig_Ele22Loose_;
  std::map<std::string,bool> b_trig_Ele27Loose_;
  std::map<std::string,bool> b_trig_Ele27Tight_;
  std::map<std::string,bool> b_trig_Ele115_;
  std::map<std::string,bool> b_trig_Mu20_;
  std::map<std::string,bool> b_trig_Mu22_;
  std::map<std::string,bool> b_trig_Mu24_;
  std::map<std::string,bool> b_trig_Mu27_;
  std::map<std::string,bool> b_trig_Mu50_;


  std::map<std::string,int> b_N_AK4_;
  std::map<std::string,int> b_N_taggedAK4_L_;
  std::map<std::string,int> b_N_taggedAK4_M_;
  std::map<std::string,int> b_N_taggedAK4_T_;
  std::map<std::string,bool> b_isBoostedTau_;
  std::map<std::string,int> b_PV_N_;
  std::map<std::string,int> b_N_tight_muons_;
  std::map<std::string,int> b_N_tight_electrons_;
  
  std::map<std::string,bool> b_GenEvent_Htata_;
  std::map<std::string,bool> b_GenEvent_Ztata_;
  std::map<std::string,bool> b_GenEvent_Gammatata_;

  std::map<std::string,int> b_ChannelInt_; //0 mutau; 1 ele; 2 tautau



  ///
  /// branches for ntuples for analysis
  ///
  double weight;
  double weightGen;
  double weightPU;
  double weightBtag;
  double weightBtag_veto;
 
  // event variables
  int runNumber;
  int eventNumber;
  int lumiBlock;
 
  Double_t   ak8jet0_pt;
  Double_t   ak8jet0_phi;
  Double_t   ak8jet0_eta;
  Double_t   ak8jet0_e;
  Double_t   ak8jet0_tau21;
  Double_t   ak8jet0_m;
  Double_t   ak8jet0_mpruned;
  Double_t   ak8jet0_csv;
  Double_t   ak8jet1_pt;
  Double_t   ak8jet1_phi;
  Double_t   ak8jet1_eta;
  Double_t   ak8jet1_e;
  Double_t   ak8jet1_tau21;
  Double_t   ak8jet1_m;
  Double_t   ak8jet1_mpruned;
  Double_t   ak8jet1_csv;
  Double_t   ak8jet0_subjet01_dr;
  Double_t   ak8jet0_subjet01_deta;
  Double_t   ak8jet0_subjet01_dphi;
  Double_t   ak8jet0_subjet0_pt;
  Double_t   ak8jet0_subjet1_pt;
  Double_t   ak8jet0_subjet0_csv;
  Double_t   ak8jet0_subjet1_csv;
  Double_t   ak8jet1_subjet01_dr;
  Double_t   ak8jet1_subjet01_deta;
  Double_t   ak8jet1_subjet01_dphi;
  Double_t   ak8jet1_subjet0_pt;
  Double_t   ak8jet1_subjet1_pt;
  Double_t   ak8jet1_subjet0_csv;
  Double_t   ak8jet1_subjet1_csv;

  Double_t tau_pt;
  Double_t tau_eta;
  Double_t tau_phi;
  Double_t seclepton_pt;
  Double_t seclepton_eta;
  Double_t seclepton_phi;
  Double_t met;
  Double_t met_phi;
  Double_t HT;

  bool isBoostedTau;
  bool isBoostedTau_eletau;
  bool isBoostedTau_mutau;

  bool GenEvent_Htata_filter;
  bool GenEvent_Ztata_filter;
  bool GenEvent_Gammatata_filter;


  std::vector<Int_t>      branch_selection_bits;
  std::vector<Int_t>      branch_selection_lastcut;




   // Macro adding the functions for dictionary generation
   ClassDef( VHTausAnalysis, 0 );

}; // class VHAnalysis

#endif // VHAnalysis_H

