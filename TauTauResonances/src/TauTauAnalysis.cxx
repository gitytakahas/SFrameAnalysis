// $Id: CycleCreators.py 344 2012-12-13 13:10:53Z krasznaa $

// Local include(s):
#include "../include/TauTauAnalysis.h"
// External include(s):
#include "../GoodRunsLists/include/TGoodRunsListReader.h"

#include <TMath.h>
#include "TRandom3.h"

ClassImp( TauTauAnalysis );





// define cut names
const std::string TauTauAnalysis::kCutName[ TauTauAnalysis::kNumCuts ] = {
  "BeforeCuts",            // C0
  "JSON",                  // C1
  "Trigger",               // C2
  "MetFilters",            // C3
  "Lepton",                // C4
  "LepTau",                // C6
  "BeforeCutsWeighted",    // C7
};





TauTauAnalysis::TauTauAnalysis() : SCycleBase()
   , m_jetAK4( this )
   , m_eventInfo( this )
   , m_electron( this )
   , m_muon( this )
   , m_tau( this )
   , m_missingEt( this )
   , m_puppimissingEt( this )
   , m_mvamissingEt( this )
   , m_genParticle( this )
   , m_pileupReweightingTool( this )
   , m_bTaggingScaleTool( this )
   , m_ScaleFactorTool( this )
   , m_RecoilCorrector( this )
{

  m_logger << INFO << "Hello!" << SLogger::endmsg;
  SetLogName( GetName() );
  
  // read configuration details from XML file
  DeclareProperty("RecoTreeName", m_recoTreeName = "physics" );

  // channels
  channels_.push_back("mutau");
  channels_.push_back("eletau");
  
  for(unsigned int ch=0;ch< channels_.size();ch++){
    m_outputTreeName_ch_.push_back("");
  }
  
  DeclareProperty( "OutputTreeName_mutau" , m_outputTreeName_ch_[0]);
  DeclareProperty( "OutputTreeName_eletau" , m_outputTreeName_ch_[1]);

  DeclareProperty( "JetAK4Name",           m_jetAK4Name            = "jetAK4" );
  DeclareProperty( "ElectronName",         m_electronName          = "el" );
  DeclareProperty( "MuonName",             m_muonName              = "mu" );
  DeclareProperty( "TauName",              m_tauName               = "tau" );
  DeclareProperty( "MissingEtName",        m_missingEtName         = "MET" );
  DeclareProperty( "GenParticleName",      m_genParticleName       = "genParticle" );
  
  DeclareProperty( "IsData",               m_isData                = false );
  DeclareProperty( "doSVFit",              m_doSVFit               = false );
  DeclareProperty( "IsSignal",             m_isSignal              = false );
  DeclareProperty( "doRecoilCorr",         m_doRecoilCorr          = false );
  
  // for SUSY https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016
  // for comparison https://twiki.cern.ch/twiki/bin/viewauth/CMS/MSSMAHTauTauSummer2016#Baseline
  // for us https://twiki.cern.ch/twiki/bin/view/CMS/SMTauTau2016#Baseline_sync_selection
  DeclareProperty( "AK4JetPtCut",          m_AK4jetPtCut           = 20.   );
  DeclareProperty( "AK4JetEtaCut",         m_AK4jetEtaCut          = 4.7   );
  DeclareProperty( "CSVWorkingPoint",      m_CSVWorkingPoint       = 0.8   ); // 0.8 is Medium

  DeclareProperty( "ElectronPtCut",        m_electronPtCut         = 26.   );
  DeclareProperty( "ElectronEtaCut",       m_electronEtaCut        = 2.1   );
  DeclareProperty( "ElectronD0Cut",        m_electronD0Cut         = 0.045 );
  DeclareProperty( "ElectronDzCut",        m_electronDzCut         = 0.2   );
  DeclareProperty( "ElectronIsoCut",       m_electronIsoCut        = 0.1   );
  
  DeclareProperty( "MuonPtCut",            m_muonPtCut             = 23.   );
  DeclareProperty( "MuonEtaCut",           m_muonEtaCut            = 2.4   ); // 2.4; 2.1
  DeclareProperty( "MuonD0Cut",            m_muonD0Cut             = 0.045 );
  DeclareProperty( "MuonDzCut",            m_muonDzCut             = 0.2   );
  DeclareProperty( "MuonIsoCut",           m_muonIsoCut            = 0.15  );

  DeclareProperty( "TauPtCut",             m_tauPtCut              = 20   ); // 20; 30
  DeclareProperty( "TauEtaCut",            m_tauEtaCut             = 2.3  );
  DeclareProperty( "TauDzCut",             m_tauDzCut              = 0.2  );

  // ICHEP: https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2689.html
//   DeclareProperty( "JSONName",             m_jsonName              = std::string (std::getenv("SFRAME_DIR")) + "/../GoodRunsLists/JSON/Cert_271036-280385_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt" );
  DeclareProperty( "JSONName",             m_jsonName              = std::string (std::getenv("SFRAME_DIR")) + "/../GoodRunsLists/JSON/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_ICHEP.txt" );
  
}





TauTauAnalysis::~TauTauAnalysis() {
  
  m_logger << INFO << "Tschoe!" << SLogger::endmsg;
  
}





void TauTauAnalysis::BeginCycle() throw( SError ) {
  
  m_logger << INFO << "BeginCycle ... " << SLogger::endmsg;
  
  mu_tau=0;
  ele_tau=0;

  // Load GRL:
  if (m_isData) {
    m_logger << INFO << "Loading GoodRunsList from file: " << m_jsonName << SLogger::endmsg;
    Root::TGoodRunsListReader reader( TString( m_jsonName.c_str() ) );
    if( ! reader.Interpret() ) {
      m_logger << FATAL << "Couldn't read in the GRL!" << SLogger::endmsg;
      throw SError( ( "Couldn't read in file: " + m_jsonName ).c_str(), SError::SkipCycle );
    }
    m_grl = reader.GetMergedGoodRunsList();
    m_grl.Summary();
    m_grl.SetName( "MyGoodRunsList" );
    
    AddConfigObject( &m_grl );
  }
  
  m_triggerNames_mutau.clear();
  m_triggerNames_eletau.clear();
	
	
  // muon triggers
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016
  m_triggerNames_mutau.push_back("HLT_IsoMu22_v");   // HTT OR
  m_triggerNames_mutau.push_back("HLT_IsoTkMu22_v"); // HTT
//   m_triggerNames_mutau.push_back("HLT_IsoMu18_v");
//   m_triggerNames_mutau.push_back("HLT_IsoMu20_v4");
//   m_triggerNames_mutau.push_back("HLT_IsoMu22_v3");
//   m_triggerNames_mutau.push_back("HLT_IsoMu22_eta2p1_v2");
//   m_triggerNames_mutau.push_back("HLT_IsoMu24_v"); // not pre-scaled
//   m_triggerNames_mutau.push_back("HLT_IsoMu27_v4");
//   m_triggerNames_mutau.push_back("HLT_IsoTkMu18_v3");
//   m_triggerNames_mutau.push_back("HLT_IsoTkMu20_v5");
//   m_triggerNames_mutau.push_back("HLT_IsoTkMu22_eta2p1_v2");
//   m_triggerNames_mutau.push_back("HLT_IsoTkMu22_v3");
//   m_triggerNames_mutau.push_back("HLT_IsoTkMu24_v"); // not pre-scaled
//   m_triggerNames_mutau.push_back("HLT_IsoTkMu27_v4");
//   m_triggerNames_mutau.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v5");
//   m_triggerNames_mutau.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v5");
//   m_triggerNames_mutau.push_back("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2");
//   m_triggerNames_mutau.push_back("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2");
//   m_triggerNames_mutau.push_back("HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v2");


  // electron triggers
  m_triggerNames_eletau.push_back("HLT_Ele25_eta2p1_WPTight_Gsf_v");
//   m_triggerNames_eletau.push_back("HLT_Ele23_WPLoose_Gsf_v4");
//   m_triggerNames_eletau.push_back("HLT_Ele24_eta2p1_WPLoose_Gsf_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele25_WPTight_Gsf_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele25_eta2p1_WPLoose_Gsf_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele25_eta2p1_WPTight_Gsf_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele27_WPLoose_Gsf_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele27_WPTight_Gsf_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele27_eta2p1_WPLoose_Gsf_v3");
//   m_triggerNames_eletau.push_back("HLT_Ele27_eta2p1_WPTight_Gsf_v3");
//   m_triggerNames_eletau.push_back("HLT_Ele32_eta2p1_WPTight_Gsf_v3");
//   m_triggerNames_eletau.push_back("HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v3");
//   m_triggerNames_eletau.push_back("HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2");
//   m_triggerNames_eletau.push_back("HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2");


  return;

}





struct ltau_pair
{
  Int_t ilepton;
  Float_t lep_iso;
  Float_t lep_pt;
  Int_t itau;
  Float_t tau_iso;
  Float_t tau_pt;

  //overload comparators
  bool operator<(const ltau_pair& another) const {
    if (lep_iso != another.lep_iso)
      return lep_iso < another.lep_iso;
    if (lep_pt != another.lep_pt)
      return lep_pt > another.lep_pt; // take highest pt
    if (tau_iso != another.tau_iso)
      return tau_iso > another.tau_iso; // note that tau isolation is better if we have higher value ! 
    if (tau_pt != another.tau_pt)
      return tau_pt > another.tau_pt; // take highest pt
    return ilepton < another.ilepton;
  }

};





void TauTauAnalysis::EndCycle() throw( SError ) {
   std::cout << "events in mu_tau " <<mu_tau <<std::endl;
   std::cout << "events in ele_tau " <<ele_tau <<std::endl;
   return;
}





void TauTauAnalysis::BeginInputData( const SInputData& id ) throw( SError ) {
//   std::cout << "BeginInputData" << std::endl;

  m_logger << INFO << "RecoTreeName:         " <<             m_recoTreeName << SLogger::endmsg;
  m_logger << INFO << "JetAK4Name:           " <<             m_jetAK4Name << SLogger::endmsg;
  m_logger << INFO << "ElectronName:         " <<             m_electronName << SLogger::endmsg;
  m_logger << INFO << "MuonName:             " <<             m_muonName << SLogger::endmsg;
  m_logger << INFO << "TauName:              " <<             m_tauName << SLogger::endmsg;
  m_logger << INFO << "GenParticleName:      " <<             m_genParticleName << SLogger::endmsg;
  
  m_logger << INFO << "IsData:               " <<             (m_isData ? "TRUE" : "FALSE") << SLogger::endmsg;
  m_logger << INFO << "IsSignal:             " <<             (m_isSignal ? "TRUE" : "FALSE") << SLogger::endmsg;
  m_logger << INFO << "doSVFit:              " <<             (m_doSVFit ? "TRUE" : "FALSE") << SLogger::endmsg;
  m_logger << INFO << "doRecoilCorr:         " <<             (m_doRecoilCorr ? "TRUE" : "FALSE") << SLogger::endmsg;
  
  m_logger << INFO << "ElectronPtCut:        " <<             m_electronPtCut << SLogger::endmsg;
  m_logger << INFO << "ElectronEtaCut:       " <<             m_electronEtaCut << SLogger::endmsg;
  m_logger << INFO << "ElectronD0Cut:        " <<             m_electronD0Cut << SLogger::endmsg;
  m_logger << INFO << "ElectronDzCut:        " <<             m_electronDzCut << SLogger::endmsg;
  m_logger << INFO << "ElectronIsoCut:       " <<             m_electronIsoCut << SLogger::endmsg;
  
  m_logger << INFO << "MuonPtCut:            " <<             m_muonPtCut << SLogger::endmsg;
  m_logger << INFO << "MuonEtaCut:           " <<             m_muonEtaCut << SLogger::endmsg;
  m_logger << INFO << "MuonD0Cut:            " <<             m_muonD0Cut << SLogger::endmsg;
  m_logger << INFO << "MuonDzCut:            " <<             m_muonDzCut << SLogger::endmsg;
  m_logger << INFO << "MuonIsoCut:           " <<             m_muonIsoCut << SLogger::endmsg;
  
  m_logger << INFO << "TauPtCut:             " <<             m_tauPtCut << SLogger::endmsg;
  m_logger << INFO << "TauEtaCut:            " <<             m_tauEtaCut << SLogger::endmsg;
  m_logger << INFO << "TauDzCut:             " <<             m_tauDzCut << SLogger::endmsg;
    
  m_logger << INFO << "JSONName:             " <<             m_jsonName << SLogger::endmsg;
  

  if (!m_isData) m_pileupReweightingTool.BeginInputData( id );

 
  if (m_isData) {
    TObject* grl;
    if( ! ( grl = GetConfigObject( "MyGoodRunsList" ) ) ) {
      m_logger << FATAL << "Can't access the GRL!" << SLogger::endmsg;
      throw SError( "Can't access the GRL!", SError::SkipCycle );
    }
    m_grl = *( dynamic_cast< Root::TGoodRunsList* >( grl ) );
  }
  
  
  std::cout << " declaring variables" << std::endl;
  for(int ch = 0; ch < (int)channels_.size(); ch++){
  
    const char* treeName = m_outputTreeName_ch_[ch].c_str();
    
    DeclareVariable( b_weight[channels_[ch]],         "weight",         treeName);
    DeclareVariable( b_genweight[channels_[ch]],      "genweight",      treeName);
    DeclareVariable( b_puweight[channels_[ch]],       "puweight",       treeName);
    DeclareVariable( b_weightbtag[channels_[ch]],     "weightbtag",     treeName);
    DeclareVariable( b_channel[channels_[ch]],        "channel",        treeName);
    DeclareVariable( b_isData[channels_[ch]],         "isData",         treeName);
    DeclareVariable( b_run[channels_[ch]],            "run",            treeName);
    DeclareVariable( b_evt[channels_[ch]],            "evt",            treeName);
    DeclareVariable( b_lum[channels_[ch]],            "lum",            treeName);
    
    DeclareVariable( b_npv[channels_[ch]],            "npv",            treeName);
    DeclareVariable( b_npu[channels_[ch]],            "npu",            treeName);
    DeclareVariable( b_NUP[channels_[ch]],            "NUP",            treeName);
    DeclareVariable( b_rho[channels_[ch]],            "rho",            treeName);
    
    DeclareVariable( b_njets[channels_[ch]],          "njets",          treeName);
    DeclareVariable( b_nfjets[channels_[ch]],         "nfjets",         treeName);
    DeclareVariable( b_ncjets[channels_[ch]],         "ncjets",         treeName);
    DeclareVariable( b_nbtag[channels_[ch]],          "nbtag",          treeName);
    DeclareVariable( b_nfbtag[channels_[ch]],         "nfbtag",         treeName);
    DeclareVariable( b_ncbtag[channels_[ch]],         "ncbtag",         treeName);
    DeclareVariable( b_njets20[channels_[ch]],        "njets20",        treeName);
    DeclareVariable( b_nfjets20[channels_[ch]],       "nfjets20",       treeName);
    DeclareVariable( b_ncjets20[channels_[ch]],       "ncjets20",       treeName);
    DeclareVariable( b_nbtag20[channels_[ch]],        "nbtag20",        treeName);
    DeclareVariable( b_nfbtag20[channels_[ch]],       "nfbtag20",       treeName);
    DeclareVariable( b_ncbtag20[channels_[ch]],       "ncbtag20",       treeName);
    
    DeclareVariable( b_pt_1[channels_[ch]],           "pt_1",           treeName);
    DeclareVariable( b_eta_1[channels_[ch]],          "eta_1",          treeName);
    DeclareVariable( b_phi_1[channels_[ch]],          "phi_1",          treeName);
    DeclareVariable( b_m_1[channels_[ch]],            "m_1",            treeName);
    DeclareVariable( b_q_1[channels_[ch]],            "q_1",            treeName);
    DeclareVariable( b_d0_1[channels_[ch]],           "d0_1",           treeName);
    DeclareVariable( b_dz_1[channels_[ch]],           "dz_1",           treeName);
    DeclareVariable( b_mt_1[channels_[ch]],           "mt_1",           treeName);
    DeclareVariable( b_pfmt_1[channels_[ch]],         "pfmt_1",         treeName);
    DeclareVariable( b_puppimt_1[channels_[ch]],      "puppimt_1",      treeName);
    DeclareVariable( b_iso_1[channels_[ch]],          "iso_1",          treeName);
    DeclareVariable( b_id_e_mva_nt_loose_1[channels_[ch]],  "id_e_mva_nt_loose_1",  treeName);
    DeclareVariable( b_gen_match_1[channels_[ch]],    "gen_match_1",    treeName);
    DeclareVariable( b_trigweight_1[channels_[ch]],   "trigweight_1",   treeName);
    DeclareVariable( b_idisoweight_1[channels_[ch]],  "idisoweight_1",  treeName);
    
    DeclareVariable( b_pt_2[channels_[ch]],           "pt_2",           treeName);
    DeclareVariable( b_eta_2[channels_[ch]],          "eta_2",          treeName);
    DeclareVariable( b_phi_2[channels_[ch]],          "phi_2",          treeName);
    DeclareVariable( b_m_2[channels_[ch]],            "m_2",            treeName);
    DeclareVariable( b_q_2[channels_[ch]],            "q_2",            treeName);
    DeclareVariable( b_d0_2[channels_[ch]],           "d0_2",           treeName);
    DeclareVariable( b_dz_2[channels_[ch]],           "dz_2",           treeName);
    DeclareVariable( b_mt_2[channels_[ch]],           "mt_2",           treeName);
    DeclareVariable( b_pfmt_2[channels_[ch]],         "pfmt_2",         treeName);
    DeclareVariable( b_puppimt_2[channels_[ch]],      "puppimt_2",      treeName);
    DeclareVariable( b_iso_2[channels_[ch]],          "iso_2",          treeName);
    DeclareVariable( b_gen_match_2[channels_[ch]],    "gen_match_2",    treeName);
    DeclareVariable( b_trigweight_2[channels_[ch]],   "trigweight_2",   treeName);
    DeclareVariable( b_idisoweight_2[channels_[ch]],  "idisoweight_2",  treeName);
    DeclareVariable( b_pol_2[channels_[ch]],          "pol_2",          treeName);
    
    DeclareVariable( b_againstElectronVLooseMVA6_2[channels_[ch]],  "againstElectronVLooseMVA6_2",  treeName);
    DeclareVariable( b_againstElectronLooseMVA6_2[channels_[ch]],   "againstElectronLooseMVA6_2",   treeName);
    DeclareVariable( b_againstElectronMediumMVA6_2[channels_[ch]],  "againstElectronMediumMVA6_2",  treeName);
    DeclareVariable( b_againstElectronTightMVA6_2[channels_[ch]],   "againstElectronTightMVA6_2",   treeName);
    DeclareVariable( b_againstElectronVTightMVA6_2[channels_[ch]],  "againstElectronVTightMVA6_2",  treeName);
    DeclareVariable( b_againstMuonLoose3_2[channels_[ch]],          "againstMuonLoose3_2",          treeName);
    DeclareVariable( b_againstMuonTight3_2[channels_[ch]],          "againstMuonTight3_2",          treeName);
    DeclareVariable( b_byCombinedIsolationDeltaBetaCorrRaw3Hits_2[channels_[ch]], "byCombinedIsolationDeltaBetaCorrRaw3Hits_2", treeName);
    DeclareVariable( b_byIsolationMVA3newDMwLTraw_2[channels_[ch]], "byIsolationMVA3newDMwLTraw_2", treeName);
    DeclareVariable( b_byIsolationMVA3oldDMwLTraw_2[channels_[ch]], "byIsolationMVA3oldDMwLTraw_2", treeName);
    DeclareVariable( b_chargedIsoPtSum_2[channels_[ch]],            "chargedIsoPtSum_2",            treeName);
    DeclareVariable( b_neutralIsoPtSum_2[channels_[ch]],            "neutralIsoPtSum_2",            treeName);
    DeclareVariable( b_puCorrPtSum_2[channels_[ch]],                "puCorrPtSum_2",                treeName);
    DeclareVariable( b_decayModeFindingOldDMs_2[channels_[ch]],     "decayModeFindingOldDMs_2",     treeName);
    DeclareVariable( b_decayMode_2[channels_[ch]],                  "decayMode_2",                treeName);
    
    DeclareVariable( b_dilepton_veto[channels_[ch]],                "dilepton_veto",                treeName);
    DeclareVariable( b_extraelec_veto[channels_[ch]],               "extraelec_veto",               treeName);
    DeclareVariable( b_extramuon_veto[channels_[ch]],               "extramuon_veto",               treeName);
    
    DeclareVariable( b_jpt_1[channels_[ch]],        "jpt_1",            treeName);
    DeclareVariable( b_jeta_1[channels_[ch]],       "jeta_1",           treeName);
    DeclareVariable( b_jphi_1[channels_[ch]],       "jphi_1",           treeName);
    DeclareVariable( b_jpt_2[channels_[ch]],        "jpt_2",            treeName);
    DeclareVariable( b_jeta_2[channels_[ch]],       "jeta_2",           treeName);
    DeclareVariable( b_jphi_2[channels_[ch]],       "jphi_2",           treeName);
    
    DeclareVariable( b_bpt_1[channels_[ch]],        "bpt_1",            treeName);
    DeclareVariable( b_beta_1[channels_[ch]],       "beta_1",           treeName);
    DeclareVariable( b_bphi_1[channels_[ch]],       "bphi_1",           treeName);
    DeclareVariable( b_bcsv_1[channels_[ch]],       "bcsv_1",           treeName);
    DeclareVariable( b_bpt_2[channels_[ch]],        "bpt_2",            treeName);
    DeclareVariable( b_beta_2[channels_[ch]],       "beta_2",           treeName);
    DeclareVariable( b_bphi_2[channels_[ch]],       "bphi_2",           treeName);
    DeclareVariable( b_bcsv_2[channels_[ch]],       "bcsv_2",           treeName);
    
    DeclareVariable( b_met[channels_[ch]],          "met",              treeName);
    DeclareVariable( b_met_old[channels_[ch]],      "met_old",          treeName);
    DeclareVariable( b_metphi[channels_[ch]],       "metphi",           treeName);
    DeclareVariable( b_puppimet[channels_[ch]],     "puppimet",         treeName);
    DeclareVariable( b_puppimetphi[channels_[ch]],  "puppimetphi",      treeName);
    DeclareVariable( b_mvamet[channels_[ch]],       "mvamet",           treeName);
    DeclareVariable( b_mvamet_old[channels_[ch]],   "mvamet_old",       treeName);
    DeclareVariable( b_mvametphi[channels_[ch]],    "mvametphi",        treeName);
    
    DeclareVariable( b_metcov00[channels_[ch]],     "metcov00",         treeName);
    DeclareVariable( b_metcov01[channels_[ch]],     "metcov01",         treeName);
    DeclareVariable( b_metcov10[channels_[ch]],     "metcov10",         treeName);
    DeclareVariable( b_metcov11[channels_[ch]],     "metcov11",         treeName);
    DeclareVariable( b_mvacov00[channels_[ch]],     "mvacov00",         treeName);
    DeclareVariable( b_mvacov01[channels_[ch]],     "mvacov01",         treeName);
    DeclareVariable( b_mvacov10[channels_[ch]],     "mvacov10",         treeName);
    DeclareVariable( b_mvacov11[channels_[ch]],     "mvacov11",         treeName);
    
    DeclareVariable( b_m_vis[channels_[ch]],        "m_vis",            treeName);
    DeclareVariable( b_m_sv[channels_[ch]],         "m_sv",             treeName);
    DeclareVariable( b_m_sv_pfmet[channels_[ch]],   "m_sv_pfmet",       treeName);
    DeclareVariable( b_dR_ll[channels_[ch]],        "dR_ll",            treeName);
    DeclareVariable( b_dphi_ll_bj[channels_[ch]],   "dphi_ll_bj",       treeName);
    DeclareVariable( b_pt_tt[channels_[ch]],        "pt_tt",            treeName);
    DeclareVariable( b_mt_tot[channels_[ch]],       "mt_tot",           treeName);
    DeclareVariable( b_ht[channels_[ch]],           "ht",               treeName);
    
    DeclareVariable( b_pzetamiss[channels_[ch]],    "pzetamiss",        treeName);
    DeclareVariable( b_pzetavis[channels_[ch]],     "pzetavis",         treeName);
    DeclareVariable( b_pzeta_disc[channels_[ch]],   "pzeta_disc",       treeName);

  }
  
  for (auto ch: channels_){
    TString hname = "cutflow_" + ch;
    TString dirname = "histogram_" + ch;
    std::cout << hname << " " << dirname << std::endl;
    Book( TH1F(hname, hname, 20, 0.5, 20.5 ), dirname);
  }
  
  // Checks
  Book( TH1F("pt_gentaus",      "gen taus pt",      150, 0, 150 ), "checks");
  Book( TH1F("pt_gentau1",      "gen tau 1 pt",     150, 0, 150 ), "checks");
  Book( TH1F("pt_gentau2",      "gen tau 2 pt",     150, 0, 150 ), "checks");
  Book( TH1F("pt_muon",         "gen muon pt",      100, 0, 100 ), "checks");
  Book( TH1F("DeltaR_tautau",   "DeltaR_tautau",    100, 0,   5 ), "checks");

  m_bTaggingScaleTool.BeginInputData( id );
  m_ScaleFactorTool.BeginInputData( id );
  m_RecoilCorrector.BeginInputData( id );

  return;

}





void TauTauAnalysis::EndInputData( const SInputData& ) throw( SError ) {
//   std::cout << "EndInputData" << std::endl;

  
  for(auto ch: channels_) {
    m_logger << INFO << "cut flow for " << ch << SLogger::endmsg;
    m_logger << INFO << Form( "Cut\t%25.25s\tEvents\tRelEff\tAbsEff", "Name" ) << SLogger::endmsg;
  
    TString hname = "cutflow_" + ch;
    TString dirname = "histogram_" + ch;

    Double_t ntot = Hist(hname, dirname)->GetBinContent( 1 );
    m_logger << INFO << Form( "\t%25.25s\t%6.0f", "start", ntot ) << SLogger::endmsg;

    for( Int_t ibin = 2; ibin <= kNumCuts; ++ibin ) {
      Int_t    icut    = ibin - 1;
      Double_t nevents = Hist(hname, dirname)->GetBinContent( ibin );
      Double_t releff  = 100. * nevents / Hist(hname, dirname)->GetBinContent( ibin-1 );
      Double_t abseff  = 100. * nevents / ntot;
      m_logger << INFO  << Form( "C%d\t%25.25s\t%6.0f\t%6.2f\t%6.2f", icut-1, kCutName[icut].c_str(), nevents, releff, abseff ) << SLogger::endmsg;
    }

    std::cout << std::endl;
  }

   return;

}





void TauTauAnalysis::BeginInputFile( const SInputData& ) throw( SError ) {
//   std::cout << "BeginInputFile" << std::endl;

  m_logger << INFO << "Connecting input variables" << SLogger::endmsg;
  if (m_isData) {
    m_jetAK4.ConnectVariables(      m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis, (m_jetAK4Name + "_").c_str() );
    m_eventInfo.ConnectVariables(   m_recoTreeName.c_str(), Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters, "" );
  }
  else {
    m_jetAK4.ConnectVariables(      m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis|Ntuple::JetTruth, (m_jetAK4Name + "_").c_str() );
    m_eventInfo.ConnectVariables(   m_recoTreeName.c_str(), Ntuple::EventInfoBasic|Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters|Ntuple::EventInfoTruth, "" );
    m_genParticle.ConnectVariables( m_recoTreeName.c_str(), Ntuple::GenParticleBasic|Ntuple::GenParticleTauDecayAnalysis, (m_genParticleName + "_").c_str() );
  }
  m_electron.ConnectVariables(      m_recoTreeName.c_str(), Ntuple::ElectronBasic|Ntuple::ElectronID|Ntuple::ElectronAdvancedID|Ntuple::ElectronBoostedIsolation|Ntuple::ElectronSuperCluster, (m_electronName + "_").c_str() );
  m_muon.ConnectVariables(          m_recoTreeName.c_str(), Ntuple::MuonBasic|Ntuple::MuonID|Ntuple::MuonIsolation|Ntuple::MuonTrack|Ntuple::MuonBoostedIsolation, (m_muonName + "_").c_str() );
  m_tau.ConnectVariables(           m_recoTreeName.c_str(), Ntuple::TauBasic|Ntuple::TauID|Ntuple::TauAdvancedID, (m_tauName + "_").c_str() );

  m_missingEt.ConnectVariables(         m_recoTreeName.c_str(), Ntuple::MissingEtBasic|Ntuple::MissingEtAnalysis|Ntuple::MissingEtCovAnalysis , (m_missingEtName + "_").c_str() );
  m_puppimissingEt.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::MissingEtBasic, (m_missingEtName + "_puppi_").c_str() );
  m_mvamissingEt.ConnectVariables(      m_recoTreeName.c_str(), Ntuple::MissingEtBasic|Ntuple::MissingEtMVAAnalysis|Ntuple::MissingEtCovAnalysis, (m_missingEtName + "_mva_").c_str() );
  
  m_logger << INFO << "Connecting input variables completed" << SLogger::endmsg;
  
  return;

}





void TauTauAnalysis::ExecuteEvent( const SInputData&, Double_t ) throw( SError ) {
//   std::cout << "ExecuteEvent" << std::endl;
  m_logger << VERBOSE << "ExecuteEvent" << SLogger::endmsg;
  
  b_weight_     =  1.;
  b_genweight_  =  1.;
  b_npu_        = -1.;
  //b_weight["mutau"]  = 1.;
  //b_weight["eletau"] = 1.;
  
    
  
  // Cut 0: no cuts
  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kBeforeCuts, 1);
    b_channel[ch] = 0;
  }
  if (m_isSignal) checks(); // checks
  
  
  // Cut 1: check for data if run/lumiblock in JSON
  if (m_isData) {
    if(!(isGoodEvent(m_eventInfo.runNumber, m_eventInfo.lumiBlock))) throw SError( SError::SkipEvent );
  }
  else{
    getEventWeight();
    genFilterZtautau(); // checks Z-tautau not cut away
    if(m_doRecoilCorr) setGenBosonTLVs();
  }
  
  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kJSON, 1);
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kBeforeCutsWeighted, b_genweight_);
  }
  
  

  // Cut 2: pass trigger
  TString trigger_result = "both";
  if(m_isData) trigger_result = passTrigger();
  if(trigger_result != "none") m_logger << VERBOSE << "Trigger pass" << SLogger::endmsg;
  else throw SError( SError::SkipEvent );
  
  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kTrigger, 1);
  }
  
  
  
  // Cut 3: pass MET filters
//   if (passMETFilters()) m_logger << VERBOSE << "passMETFilters" << SLogger::endmsg;
//   else throw SError( SError::SkipEvent );
  
  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kMetFilters, 1);
  }
  
  
  
  // Cut 4: lepton (muon)
  std::vector<UZH::Muon> goodMuons;
  for( int i = 0; i < m_muon.N; ++i ){
    UZH::Muon mymuon( &m_muon, i );
    
    if (mymuon.pt() < m_muonPtCut) continue;
    if (fabs(mymuon.eta()) > m_muonEtaCut) continue;
    if (fabs(mymuon.d0_allvertices()) > m_muonD0Cut) continue;
    if (fabs(mymuon.dz_allvertices()) > m_muonDzCut) continue;
    if (mymuon.isMediumMuon() < 0.5) continue;
    //if (mymuon.SemileptonicPFIso() / mymuon.pt() > m_muonIsoCut) continue;
    
    goodMuons.push_back(mymuon);
  }
  
  // Cut 4: lepton (electron)
  std::vector<UZH::Electron> goodElectrons;
  for ( int i = 0; i < m_electron.N; ++i ) {
    UZH::Electron myelectron( &m_electron, i );

    if (myelectron.pt() < m_electronPtCut) continue;
    if (fabs(myelectron.eta()) > m_electronEtaCut) continue;
    if (fabs(myelectron.d0_allvertices()) > m_electronD0Cut) continue;
    if (fabs(myelectron.dz_allvertices()) > m_electronDzCut) continue;
    if (myelectron.passConversionVeto()!=1) continue;
    if (myelectron.expectedMissingInnerHits()>1) continue;
    if (myelectron.nonTrigMVAID() < 0.5) continue;
    //if (myelectron.SemileptonicPFIso() / myelectron.pt() > m_electronIsoCut) continue;
	
    goodElectrons.push_back(myelectron);
  }
  
  
  if(goodMuons.size()!=0){
    fillCutflow("cutflow_mutau", "histogram_mutau", kLepton, 1);
  }
  if(goodElectrons.size()!=0){
    fillCutflow("cutflow_eletau", "histogram_eletau", kLepton, 1);
  }
  else if(goodMuons.size()==0) throw SError( SError::SkipEvent );
  
  
  
  // Cut 6: lepton - tau pair
  
  // For tau
  std::vector<UZH::Tau> goodTaus;
  for ( int i = 0; i <   (m_tau.N); ++i ) {
    UZH::Tau mytau( &m_tau, i );
    if(mytau.TauType()!=1) continue;
    if(mytau.pt() < m_tauPtCut) continue;
    if(fabs(mytau.eta()) > m_tauEtaCut) continue;
    if(fabs(mytau.dz()) > m_tauDzCut) continue;
    if(mytau.decayModeFinding() < 0.5) continue;
    if(fabs(mytau.charge()) != 1) continue;
    //if(mytau.byTightIsolationMVArun2v1DBoldDMwLT() < 0.5) continue;

//     if(event_channel=="mutau"){
//       if(mytau.againstMuonTight3() < 0.5) continue;
//       if(mytau.againstElectronVLooseMVA6() < 0.5) continue;
//     }else if(event_channel=="eletau"){
//       if(mytau.againstMuonLoose3() < 0.5) continue;
//       if(mytau.againstElectronTightMVA6() < 0.5) continue;
//    }

    goodTaus.push_back(mytau);
  }

  if(goodTaus.size()==0) throw SError( SError::SkipEvent );
  
  
  // First, select muon with highest isolation, and then, highest pT
    
  // For mu-tau
  std::vector<ltau_pair> mutau_pair;
  for(int imuon=0; imuon < (int)goodMuons.size(); imuon++){
    if(trigger_result == "ele") break; // trigger
    for(int itau=0; itau < (int)goodTaus.size(); itau++){

      if(goodMuons[imuon].tlv().DeltaR(goodTaus[itau].tlv()) < 0.5) continue;
      
      Float_t mupt = goodMuons[imuon].pt();
      Float_t reliso = goodMuons[imuon].SemileptonicPFIso() / mupt;
      Float_t taupt = goodTaus[itau].pt();
      Float_t tauiso = goodTaus[itau].byIsolationMVArun2v1DBoldDMwLTraw();
      ltau_pair pair = {imuon, reliso, mupt, itau, tauiso, taupt};
      mutau_pair.push_back(pair);
    }
  }
  
  // For ele-tau
  std::vector<ltau_pair> eletau_pair;
  for(int ielectron=0; ielectron < (int)goodElectrons.size(); ielectron++){
    if(trigger_result == "mu") break; // trigger
    for(int itau=0; itau < (int)goodTaus.size(); itau++){
      
      if(goodElectrons[ielectron].tlv().DeltaR(goodTaus[itau].tlv()) < 0.5) continue;
      
      Float_t elept = goodElectrons[ielectron].pt();
      Float_t reliso = goodElectrons[ielectron].SemileptonicPFIso() / elept;
      Float_t taupt = goodTaus[itau].pt();
      Float_t tauiso = goodTaus[itau].byIsolationMVArun2v1DBoldDMwLTraw();
      ltau_pair pair = {ielectron, reliso, elept, itau, tauiso, taupt};
      eletau_pair.push_back(pair);
    }
  }
  
  
  if(mutau_pair.size()==0 && eletau_pair.size()==0){
    throw SError( SError::SkipEvent );
  }
  
  
  UZH::MissingEt Met( &m_missingEt, 0 );
  UZH::MissingEt PuppiMet( &m_puppimissingEt, 0 );
  
  // This depends on the channel
  UZH::Muon dummyMuon;
  UZH::Electron dummyElectron;
  
  // For mu-tau
  if(mutau_pair.size()!=0){
    
    fillCutflow("cutflow_mutau", "histogram_mutau", kLepTau, 1);
    sort(mutau_pair.begin(), mutau_pair.end());
    
    UZH::MissingEt MvaMet;
    for ( int i = 0; i < (Met.Nmva()); ++i ) {
      UZH::MissingEt myMvaMet( &m_mvamissingEt, i );
      
      bool flag_lep = false;
      bool flag_tau = false;
      
      for(int ipf=0; ipf < (int) myMvaMet.recoil_pt().size(); ipf++){
        Float_t recoil_pt = myMvaMet.recoil_pt().at(ipf);
        Float_t recoil_eta = myMvaMet.recoil_eta().at(ipf);
        Float_t recoil_phi = myMvaMet.recoil_phi().at(ipf);
        Int_t recoil_pdgId = abs(myMvaMet.recoil_pdgId().at(ipf));
        
        if(recoil_pt == goodMuons[mutau_pair[0].ilepton].pt() && 
           recoil_eta == goodMuons[mutau_pair[0].ilepton].eta() && 
           recoil_phi == goodMuons[mutau_pair[0].ilepton].phi() &&
           recoil_pdgId == 13){
            flag_lep = true;
        }
        
        if(recoil_pt == goodTaus[mutau_pair[0].itau].pt() && 
           recoil_eta == goodTaus[mutau_pair[0].itau].eta() && 
           recoil_phi == goodTaus[mutau_pair[0].itau].phi() && 
           recoil_pdgId == 15){
            flag_tau = true;
        }
      }
      
      if(flag_lep==true && flag_tau==true){
        MvaMet = myMvaMet;
      }
      
    }
    
    // For Jets
    std::vector<UZH::Jet> goodJetsAK4;
    for ( int i = 0; i < (m_jetAK4.N); ++i ) {
      UZH::Jet myjetak4( &m_jetAK4, i );
      
      Float_t dr_mj = deltaR(myjetak4.eta() - goodMuons[mutau_pair[0].ilepton].eta(), 
                      deltaPhi(myjetak4.phi(), goodMuons[mutau_pair[0].ilepton].phi()));
      if(dr_mj < 0.5) continue;
      
      Float_t dr_tj = deltaR(myjetak4.eta() - goodTaus[mutau_pair[0].itau].eta(), 
			          deltaPhi(myjetak4.phi(), goodTaus[mutau_pair[0].itau].phi()));
      if(dr_tj < 0.5) continue;
      
      if (fabs(myjetak4.eta()) > m_AK4jetEtaCut) continue;
      if (myjetak4.pt() < m_AK4jetPtCut) continue;
      if (!LooseJetID(myjetak4)) continue; // !myjetak4.IDLoose()
      
      goodJetsAK4.push_back(myjetak4);
    }
    
    FillBranches( "mutau", goodJetsAK4, goodTaus[mutau_pair[0].itau], goodMuons[mutau_pair[0].ilepton], dummyElectron, Met, PuppiMet, MvaMet);
    mu_tau++;
  
  }
  
  
  // For ele-tau
  if(eletau_pair.size()!=0){
    fillCutflow("cutflow_eletau", "histogram_eletau", kLepTau, 1);
    sort(eletau_pair.begin(), eletau_pair.end());
    
    UZH::MissingEt MvaMet;
    for ( int i = 0; i < (Met.Nmva()); ++i ) {
      UZH::MissingEt myMvaMet( &m_mvamissingEt, i );
      
      bool flag_lep = false;
      bool flag_tau = false;
      
      for(int ipf=0; ipf < (int) myMvaMet.recoil_pt().size(); ipf++){
        Float_t recoil_pt = myMvaMet.recoil_pt().at(ipf);
        Float_t recoil_eta = myMvaMet.recoil_eta().at(ipf);
        Float_t recoil_phi = myMvaMet.recoil_phi().at(ipf);
        Int_t recoil_pdgId = abs(myMvaMet.recoil_pdgId().at(ipf));
        
        if(recoil_pt == goodElectrons[eletau_pair[0].ilepton].pt() && 
           recoil_eta == goodElectrons[eletau_pair[0].ilepton].eta() && 
           recoil_phi == goodElectrons[eletau_pair[0].ilepton].phi() && 
           recoil_pdgId == 11){
            flag_lep = true;
        }
        
        if(recoil_pt == goodTaus[eletau_pair[0].itau].pt() && 
           recoil_eta == goodTaus[eletau_pair[0].itau].eta() && 
           recoil_phi == goodTaus[eletau_pair[0].itau].phi() && 
           recoil_pdgId == 15){
            flag_tau = true;
        }
      }
      
      if(flag_lep==true && flag_tau==true){
        MvaMet = myMvaMet; 
      }
    
    }
    
    
    // For Jets
    std::vector<UZH::Jet> goodJetsAK4;
    for ( int i = 0; i < (m_jetAK4.N); ++i ) {
      UZH::Jet myjetak4( &m_jetAK4, i );
      
      Float_t dr_ej = deltaR(myjetak4.eta() - goodElectrons[eletau_pair[0].ilepton].eta(), 
			          deltaPhi(myjetak4.phi(), goodElectrons[eletau_pair[0].ilepton].phi()));
      if(dr_ej < 0.5) continue;
      
      Float_t dr_tj = deltaR(myjetak4.eta() - goodTaus[eletau_pair[0].itau].eta(), 
			          deltaPhi(myjetak4.phi(), goodTaus[eletau_pair[0].itau].phi()));
      if(dr_tj < 0.5) continue;
      
      if (fabs(myjetak4.eta()) > m_AK4jetEtaCut) continue;
      if (myjetak4.pt() < m_AK4jetPtCut) continue;
      if (!LooseJetID(myjetak4)) continue;
      
      goodJetsAK4.push_back(myjetak4);
    }
    
    FillBranches( "eletau", goodJetsAK4, goodTaus[eletau_pair[0].itau], dummyMuon, goodElectrons[eletau_pair[0].ilepton], Met, PuppiMet, MvaMet);
    ele_tau++;
    
  }
  
  return;
  
}





bool TauTauAnalysis::isGoodEvent(int runNumber, int lumiSection) {
//   std::cout << "isGoodEvent" << std::endl;
  
  bool isGood = true;
  if (m_isData) {
    isGood = m_grl.HasRunLumiBlock( runNumber, lumiSection );
    if( !isGood ) {
      m_logger << WARNING << "Bad event! Run: " << runNumber <<  " - Lumi Section: " << lumiSection << SLogger::endmsg;
      // throw SError( SError::SkipEvent );
    }
    else m_logger << VERBOSE << "Good event! Run: " << runNumber <<  " - Lumi Section: " << lumiSection << SLogger::endmsg;
  }
  
  return isGood;
  
}





TString TauTauAnalysis::passTrigger() {
//   std::cout << "TauTauAnalysis" << std::endl;
  
  bool flag_mu_trigger = false;
  bool flag_ele_trigger = false;

  for (std::map<std::string,bool>::iterator it = (m_eventInfo.trigDecision)->begin(); it != (m_eventInfo.trigDecision)->end(); ++it){
    for (unsigned int t = 0; t < m_triggerNames_mutau.size(); ++t ){
      if ((it->first).find(m_triggerNames_mutau[t]) != std::string::npos) {
        if (it->second == true) {
          m_logger << VERBOSE << "Trigger pass: " << (it->first) << SLogger::endmsg;
          flag_mu_trigger = true;
          //return true;
        }
      }
    }
  }

  for (std::map<std::string,bool>::iterator it = (m_eventInfo.trigDecision)->begin(); it != (m_eventInfo.trigDecision)->end(); ++it){
    for (unsigned int t = 0; t < m_triggerNames_eletau.size(); ++t ){
      if ((it->first).find(m_triggerNames_eletau[t]) != std::string::npos) {
        if (it->second == true) {
          m_logger << VERBOSE << "Trigger pass: " << (it->first) << SLogger::endmsg;
	      flag_ele_trigger = true;
	      //return true;
        }
      }
    }
  }

  if(flag_mu_trigger == true && flag_ele_trigger == true) return "both";
  if(flag_mu_trigger == true && flag_ele_trigger == false) return "mu";
  if(flag_mu_trigger == false && flag_ele_trigger == true) return "ele";

  return "none";
  
}





bool TauTauAnalysis::passMETFilters() {
//   std::cout << "passMETFilters" << std::endl;
  
  bool passMetFilters = true;
  
  // using only what's recommended in https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
  if( !(m_eventInfo.PV_filter) ) {
    passMetFilters = false;
    m_logger << VERBOSE << "PV_filter" << SLogger::endmsg;
  }
  if( !(m_eventInfo.passFilter_CSCHalo) ) {
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_CSCHalo" << SLogger::endmsg;
  }
  if( !(m_eventInfo.passFilter_HBHELoose) ) {
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_HBHELoose" << SLogger::endmsg;
  }
  if( !(m_eventInfo.passFilter_HBHEIso) ) {
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_HBHEIso" << SLogger::endmsg;
  }
  if( !(m_eventInfo.passFilter_EEBadSc) ) {
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_EEBadSc" << SLogger::endmsg;
  }
 
  if( !(m_eventInfo.passFilter_globalTightHalo2016) ){
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_EEBadSc" << SLogger::endmsg;
  }

  if( !(m_eventInfo.passFilter_chargedHadronTrackResolution) ){
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_EEBadSc" << SLogger::endmsg;
  }

  if( !(m_eventInfo.passFilter_muonBadTrack) ) {        
    passMetFilters = false;
    m_logger << VERBOSE << "passFilter_EEBadSc" << SLogger::endmsg;
  } 
  
  return passMetFilters;
  
}





void TauTauAnalysis::getEventWeight() {
//   std::cout << "getEventWeight" << std::endl;
  
  double weight = 1.;
  b_npu_ = -1.;
  for( unsigned int v = 0; v < (m_eventInfo.actualIntPerXing)->size(); ++v ){
    
    if ( (*m_eventInfo.bunchCrossing)[v] == 0 ) {
      b_npu_ = (*m_eventInfo.actualIntPerXing)[v]; // averageIntPerXing
      b_puweight_ = m_pileupReweightingTool.getPileUpweight( b_npu_ );
      m_logger << VERBOSE << "Weight: " << b_puweight_ << " for true: " << b_npu_ << SLogger::endmsg;
      break;
    }
  }
  
  b_genweight_ = (m_eventInfo.genEventWeight < 0) ? -1 : 1; 
  b_weight_ *= b_puweight_*b_genweight_;
  
}





void TauTauAnalysis::fillCutflow(TString histName, TString dirName, const Int_t id, const Double_t weight){
//   std::cout << "fillCutflow" << std::endl;

  Hist( histName, dirName )->Fill( id+1, weight );

}





void TauTauAnalysis::FillBranches(const std::string& channel, const std::vector<UZH::Jet> &Jet,
                                  const UZH::Tau& tau, const UZH::Muon& muon, const UZH::Electron& electron,
                                  const UZH::MissingEt& met, const UZH::MissingEt& puppimet, const UZH::MissingEt& mvamet){
//   std::cout << "FillBranches" << std::endl;
  
  const char* ch = channel.c_str();
  b_weightbtag_ = 1.;
  
  b_weight[ch]      = b_weight_;
  b_genweight[ch]   = b_genweight_;
  b_puweight[ch]    = b_puweight_;
  b_evt[ch]         = m_eventInfo.eventNumber;
  b_run[ch]         = m_eventInfo.runNumber;
  b_lum[ch]         = m_eventInfo.lumiBlock;
  b_isData[ch]      = (Int_t) m_isData;
  
  b_npu[ch]         = b_npu_; // for MC defined in getEventWeight
  b_npv[ch]         = m_eventInfo.PV_N;
  b_NUP[ch]         = m_eventInfo.lheNj;
  b_rho[ch]         = m_eventInfo.rho;
  
  Int_t njets       =  0;
  Int_t nfjets      =  0;
  Int_t ncjets      =  0;
  Int_t nbtag       =  0;
  Int_t nfbtag      =  0;
  Int_t ncbtag      =  0;
  Int_t njets20     =  0;
  Int_t nfjets20    =  0;
  Int_t ncjets20    =  0;
  Int_t nbtag20     =  0;
  Int_t nfbtag20    =  0;
  Int_t ncbtag20    =  0;
  Int_t ibjet1      = -1;
  Int_t ibjet2      = -1;
  Int_t icjet1      = -1; // central jet that is not the same as leading b jet for dphi_ll_bj
  Float_t ht        =  0; // total scalar energy HT
  
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#Other_common_selections
  for( int ijet = 0; ijet < (int)Jet.size(); ++ijet ){
    ht += Jet.at(ijet).e();
    bool isBTagged = getBTagWeight_promote_demote(Jet.at(ijet)); // (Jet.at(ijet).csv()) > 0.8 //csv > 0.8 is medium
    if(Jet.at(ijet).pt() > 30) njets++;
    if(fabs(Jet.at(ijet).eta()) < 2.4 && isBTagged){
      nbtag++;
      if      (ibjet1 < 0) ibjet1 = ijet;
      else if (ibjet2 < 0) ibjet2 = ijet;
    }
    if(fabs(Jet.at(ijet).eta()) < 2.4){         // CENTRAL 20 GeV
      if(isBTagged) ncbtag20++;                 //  btag
      ncjets20++;                               //  jets
      if(icjet1 < 0 && (icjet1 != ibjet1 || ibjet1 < 0 )) icjet1 = ijet;
      if(Jet.at(ijet).pt() > 30){               // CENTRAL 30 GeV
        if(isBTagged) ncbtag++;                 //  btag
        ncjets++;                               //  jets
      }
    }
    else if(fabs(Jet.at(ijet).eta()) > 2.4){    // FORWARD 20 GeV
      if(isBTagged) nfbtag20++;                 //  btag
      nfjets20++;                               //  jets
      if(Jet.at(ijet).pt() > 30){               // FORWARD 30 GeV
        if(isBTagged) nfbtag++;                 //  btag
        nfjets++;                               //  jets
      }
    }
  }
  njets20 = ncjets20 + nfjets20;
  nbtag20 = ncbtag20 + nfbtag20;
  njets = ncjets + nfjets;
  nbtag = ncbtag + nfbtag;
  
  if(njets20 > 1){
    b_jpt_1[ch]     = Jet.at(0).pt();
    b_jeta_1[ch]    = Jet.at(0).eta();
    b_jphi_1[ch]    = Jet.at(0).phi();
    b_jpt_2[ch]     = Jet.at(1).pt();
    b_jeta_2[ch]    = Jet.at(1).eta();
    b_jphi_2[ch]    = Jet.at(1).phi();
  }
  else if(njets20 == 1){
    b_jpt_1[ch]     = Jet.at(0).pt();
    b_jeta_1[ch]    = Jet.at(0).eta();
    b_jphi_1[ch]    = Jet.at(0).phi();
    b_jpt_2[ch]     = -1;
    b_jeta_2[ch]    = -9;
    b_jphi_2[ch]    = -9;
  }
  else{
    b_jpt_1[ch]     = -1;
    b_jeta_1[ch]    = -9;
    b_jphi_1[ch]    = -9;
    b_jpt_2[ch]     = -1;
    b_jeta_2[ch]    = -9;
    b_jphi_2[ch]    = -9;
  }
  
  if(ibjet1 < 0){
    b_bpt_1[ch]     = -1;
    b_beta_1[ch]    = -9;
    b_bphi_1[ch]    = -9;
    b_bcsv_1[ch]    = -1;
  }else{
    b_bpt_1[ch]     = Jet.at(ibjet1).pt();
    b_beta_1[ch]    = Jet.at(ibjet1).eta();
    b_bphi_1[ch]    = Jet.at(ibjet1).phi();
    b_bcsv_1[ch]    = Jet.at(ibjet1).csv();
  }
  if (ibjet2 < 0){
    b_bpt_2[ch]     = -1;
    b_beta_2[ch]    = -9;
    b_bphi_2[ch]    = -9;
    b_bcsv_2[ch]    = -1;
  }
  else{
    b_bpt_2[ch]     = Jet.at(ibjet2).pt();
    b_beta_2[ch]    = Jet.at(ibjet2).eta();
    b_bphi_2[ch]    = Jet.at(ibjet2).phi();
    b_bcsv_2[ch]    = Jet.at(ibjet2).csv();
  }
  
  b_njets[ch]       = njets;
  b_nfjets[ch]      = nfjets;
  b_ncjets[ch]      = ncjets;
  b_nbtag[ch]       = nbtag;
  b_nfbtag[ch]      = nfbtag;
  b_ncbtag[ch]      = ncbtag;
  b_njets20[ch]     = njets20;
  b_nfjets20[ch]    = nfjets20;
  b_ncjets20[ch]    = ncjets20;
  b_nbtag20[ch]     = nbtag20;
  b_nfbtag20[ch]    = nfbtag20;
  b_ncbtag20[ch]    = ncbtag20;

  // For taus
  b_pt_2[ch]        = tau.tlv().Pt();
  b_eta_2[ch]       = tau.tlv().Eta();
  b_phi_2[ch]       = tau.tlv().Phi();
  b_m_2[ch]         = tau.tlv().M();
  b_q_2[ch]         = tau.charge();
  b_d0_2[ch]        = tau.d0();
  b_dz_2[ch]        = tau.dz();
  b_iso_2[ch]       = tau.byTightIsolationMVArun2v1DBoldDMwLT();
  
  b_pol_2[ch]       = -9;
  if (tau.chargedPionPt() > 0 && tau.neutralPionPt() > 0)
    b_pol_2[ch]       = (tau.chargedPionPt() - tau.neutralPionPt()) / (tau.chargedPionPt() + tau.neutralPionPt());
  
  b_againstElectronVLooseMVA6_2[ch]     = tau.againstElectronVLooseMVA6();
  b_againstElectronLooseMVA6_2[ch]      = tau.againstElectronLooseMVA6();
  b_againstElectronMediumMVA6_2[ch]     = tau.againstElectronMediumMVA6();
  b_againstElectronTightMVA6_2[ch]      = tau.againstElectronTightMVA6();
  b_againstElectronVTightMVA6_2[ch]     = tau.againstElectronVTightMVA6();
  b_againstMuonLoose3_2[ch]             = tau.againstMuonLoose3();
  b_againstMuonTight3_2[ch]             = tau.againstMuonTight3();
  b_byCombinedIsolationDeltaBetaCorrRaw3Hits_2[ch] = tau.byCombinedIsolationDeltaBetaCorrRaw3Hits();
  b_byIsolationMVA3newDMwLTraw_2[ch]    = tau.byIsolationMVArun2v1DBnewDMwLTraw();
  b_byIsolationMVA3oldDMwLTraw_2[ch]    = tau.byIsolationMVArun2v1DBoldDMwLTraw();
  b_chargedIsoPtSum_2[ch]               = tau.chargedIsoPtSum();
  b_neutralIsoPtSum_2[ch]               = tau.neutralIsoPtSum();
  b_puCorrPtSum_2[ch]                   = tau.puCorrPtSum();
  b_decayModeFindingOldDMs_2[ch]        = tau.decayModeFinding();
  if (m_isData)  b_gen_match_2[ch]      = -1;
  else{
    b_gen_match_2[ch]                   = genMatch(b_eta_2[ch], b_phi_2[ch]);
    b_genmatchweight[ch]                = genMatchSF(b_gen_match_2[ch],b_eta_2[ch]); // leptons faking taus and real taus ID eff
    b_weight[ch]                        = b_weight[ch]*b_genmatchweight[ch];
  }
  b_decayMode_2[ch]                     = tau.decayMode();
  
  extraLeptonVetos(channel, muon, electron);
  b_dilepton_veto[ch]                   = (int) b_dilepton_veto_;
  b_extraelec_veto[ch]                  = (int) b_extraelec_veto_;
  b_extramuon_veto[ch]                  = (int) b_extramuon_veto_;
  
  TLorentzVector lep_lv;
  b_trigweight_1[ch]                    = 1.;
  b_trigweight_2[ch]                    = 1.;
  b_idisoweight_1[ch]                   = 1.;
  b_idisoweight_2[ch]                   = 1.;
  if(channel=="mutau"){
    b_pt_1[ch]      = muon.tlv().Pt();
    b_eta_1[ch]     = muon.tlv().Eta();
    b_phi_1[ch]     = muon.tlv().Phi();
    b_m_1[ch]       = muon.tlv().M();
    b_q_1[ch]       = muon.charge();
    b_d0_1[ch]      = muon.d0();
    b_dz_1[ch]      = muon.dz();
    b_iso_1[ch]     = muon.SemileptonicPFIso() / muon.pt();
    b_id_e_mva_nt_loose_1[ch]   = -1;
    lep_lv.SetPtEtaPhiM(b_pt_1[ch], b_eta_1[ch], b_phi_1[ch], b_m_1[ch]);
    b_channel[ch]   = 1;
    if (!m_isData){
      b_trigweight_1[ch]    = m_ScaleFactorTool.get_Efficiency_MuTrig(lep_lv.Pt(),fabs(lep_lv.Eta()));
      b_idisoweight_1[ch]   = m_ScaleFactorTool.get_ScaleFactor_MuIdIso(lep_lv.Pt(),fabs(lep_lv.Eta()));
    }
  }
  else{
    b_pt_1[ch]      = electron.tlv().Pt();
    b_eta_1[ch]     = electron.tlv().Eta();
    b_phi_1[ch]     = electron.tlv().Phi();
    b_m_1[ch]       = electron.tlv().M();
    b_q_1[ch]       = electron.charge();
    b_d0_1[ch]      = electron.d0();
    b_dz_1[ch]      = electron.dz();
    b_iso_1[ch]     = electron.SemileptonicPFIso() / electron.pt();
    b_id_e_mva_nt_loose_1[ch]           = electron.nonTrigMVA();
    lep_lv.SetPtEtaPhiM(b_pt_1[ch], b_eta_1[ch], b_phi_1[ch], b_m_1[ch]);
    b_channel[ch]       = 2;
    if (!m_isData){
      b_trigweight_1[ch]    = m_ScaleFactorTool.get_Efficiency_EleTrig(lep_lv.Pt(),fabs(lep_lv.Eta()));
      b_idisoweight_1[ch]   = m_ScaleFactorTool.get_ScaleFactor_EleIdIso(lep_lv.Pt(),fabs(lep_lv.Eta()));
    }
  }
  
  b_weightbtag[ch] = 1.;
  if (m_isData) b_gen_match_1[ch]  = -1;
  else{
    b_weightbtag[ch]    = b_weightbtag_; // do not apply b tag weight when using promote-demote method !!!
    //b_weightbtag[ch]    = m_bTaggingScaleTool.getScaleFactor_veto(Jet); // getScaleFactor_veto for AK4, getScaleFactor for AK8
    b_weight[ch]        = b_weight[ch] * b_trigweight_1[ch] * b_idisoweight_1[ch] * b_idisoweight_2[ch]; // * b_weightbtag[ch]
    b_gen_match_1[ch]   = genMatch(b_eta_1[ch], b_phi_1[ch]);
  }
  
  b_id_e_mva_nt_loose_1[ch] = -1;
  
  TLorentzVector lmet;
  TLorentzVector lmvamet;
  float fmet      = met.et();        float fmetphi      = met.phi();
  float fmvamet   = mvamet.et();     float fmvametphi   = mvamet.phi();
  float fpuppimet = puppimet.et();   float fpuppimetphi = puppimet.phi();
  lmet.SetPxPyPzE(fmet*TMath::Cos(fmetphi), fmet*TMath::Sin(fmetphi), 0, fmet);
  lmvamet.SetPxPyPzE(fmvamet*TMath::Cos(fmvametphi), fmvamet*TMath::Sin(fmvametphi), 0, fmvamet);
  TLorentzVector lmetCorr;
  TLorentzVector lmvametCorr;
  if(m_doRecoilCorr){
    lmetCorr    =  m_RecoilCorrector.CorrectPFMETByMeanResolution(  lmet.Px(),          lmet.Py(),
					                                                boson_tlv.Px(),     boson_tlv.Py(),
					                                                boson_tlv_vis.Px(), boson_tlv_vis.Py(),
					                                                m_jetAK4.N ); //m_eventInfo.lheNj
    lmvametCorr = m_RecoilCorrector.CorrectMVAMETByMeanResolution(  lmvamet.Px(),       lmvamet.Py(),
    					                                            boson_tlv.Px(),     boson_tlv.Py(),
					                                                boson_tlv_vis.Px(), boson_tlv_vis.Py(),
					                                                m_jetAK4.N ); //m_eventInfo.lheNj
    fmet    = lmetCorr.E();         fmetphi = lmetCorr.Phi();
    fmvamet = lmvametCorr.E();   fmvametphi = lmvametCorr.Phi();
  }
  
  b_met[ch]         = fmet;
  b_metphi[ch]      = fmetphi;
  b_puppimet[ch]    = fpuppimet;
  b_puppimetphi[ch] = fpuppimetphi;
  b_mvamet[ch]      = fmvamet;
  b_mvametphi[ch]   = fmvametphi;
  b_met_old[ch]     = met.et();
  b_mvamet_old[ch]  = mvamet.et();
  b_metcov00[ch]    = met.cov00();
  b_metcov01[ch]    = met.cov10(); // not typo. This is same for 10
  b_metcov10[ch]    = met.cov10();
  b_metcov11[ch]    = met.cov11();
  b_mvacov00[ch]    = mvamet.cov00();
  b_mvacov01[ch]    = mvamet.cov10(); // not typo. This is same for 10
  b_mvacov10[ch]    = mvamet.cov10();
  b_mvacov11[ch]    = mvamet.cov11();
  
  b_mt_1[ch]        = TMath::Sqrt(2*lep_lv.Pt()*fmvamet*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), fmvametphi))));
  b_pfmt_1[ch]      = TMath::Sqrt(2*lep_lv.Pt()*fmet*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), fmetphi))));
  b_puppimt_1[ch]   = TMath::Sqrt(2*lep_lv.Pt()*fpuppimet*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), fpuppimetphi))));
  
  b_mt_2[ch]        = TMath::Sqrt(2*b_pt_2[ch]*fmvamet*(1-TMath::Cos(deltaPhi(b_phi_2[ch], fmvametphi))));
  b_pfmt_2[ch]      = TMath::Sqrt(2*b_pt_2[ch]*fmet*(1-TMath::Cos(deltaPhi(b_phi_2[ch], fmetphi))));
  b_puppimt_2[ch]   = TMath::Sqrt(2*b_pt_2[ch]*fpuppimet*(1-TMath::Cos(deltaPhi(b_phi_2[ch], fpuppimetphi))));
  
//  NSVfitStandalone::Vector measuredMET(fmet *TMath::Cos(met_phi), fmet *TMath::Sin(met_phi), 0);
  b_m_vis[ch]       = (lep_lv + tau.tlv()).M();
  b_dR_ll[ch]       = tau.tlv().DeltaR(lep_lv);
  b_mt_tot[ch]      = TMath::Sqrt(TMath::Power(b_mt_1[ch],2) + TMath::Power(b_mt_2[ch],2) + 2*lep_lv.Pt()*b_pt_2[ch]*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), b_phi_2[ch]))));
  b_pt_tt[ch]       = (lep_lv + tau.tlv() + lmet).Pt();
  b_ht[ch]          = ht + lep_lv.E() + tau.tlv().E();
  
  // Delta phi( lep+tau, bj+j ) if there is one central b jet and on central jet
  if(icjet1 != -1 && ibjet1 != -1)
    b_dphi_ll_bj[ch] = fabs(deltaPhi( (lep_lv+tau.tlv()).Phi(), (Jet.at(ibjet1).tlv()+Jet.at(icjet1).tlv()).Phi() ));
  else
    b_dphi_ll_bj[ch] = -1;
  
  TVector3 leg1(lep_lv.Px(), lep_lv.Py(), 0.);
  TVector3 leg2(tau.tlv().Px(), tau.tlv().Py(), 0.);
  TVector3 metleg(lmet.Px(), lmet.Py(), 0.);
  TVector3 zetaAxis = (leg1.Unit() + leg2.Unit()).Unit();
  Float_t pZetaVis_ = leg1*zetaAxis + leg2*zetaAxis;
  Float_t pZetaMET_ = metleg*zetaAxis;
  b_pzetamiss[ch]   = pZetaMET_;
  b_pzetavis[ch]    = pZetaVis_;
  b_pzeta_disc[ch]  = pZetaMET_ - 0.5*pZetaVis_;
  
  bool doSVfit= false;
  if (m_doSVFit){
    //  if (true){
    std::cout << "mvamet" << std::endl;
    //    TLorentzVector dilepton;
    //    dilepton.SetPtEtaPhiM(0,0,0,0);
    //    dilepton = applySVFitSemileptonic(mvamet.cov00(),mvamet.cov10(),mvamet.cov11(),fmvamet,fmvametphi,tau.tlv(),lep_lv);  
    
    b_m_sv[ch]      = applySVFit(mvamet.cov00(),mvamet.cov10(),mvamet.cov11(),fmvamet,fmvametphi,lep_lv, tau.tlv(), channel);
    
    //    b_m_sv = dilepton.M();
    //    b_pt_sv = dilepton.Pt();
    //    b_eta_sv = dilepton.Eta();
    //    b_phi_sv = dilepton.Phi();
    
    std::cout << "pfmet" << std::endl;
    //    TLorentzVector dilepton_pf;
    //    dilepton_pf.SetPtEtaPhiM(0,0,0,0);
    //    dilepton_pf = applySVFitSemileptonic(met.cov00(),met.cov10(),met.cov11(),fmet,fmetphi,tau.tlv(),lep_lv);  
    b_m_sv_pfmet[ch] = applySVFit(met.cov00(),met.cov10(),met.cov11(),fmet,fmetphi,lep_lv, tau.tlv(), channel);  
    
    //    b_m_sv_pfmet = dilepton_pf.M();
  }

}





float TauTauAnalysis::applySVFit(float cov00, float cov10, float cov11,  float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2, const std::string& channel){
//   std::cout << "applySVFit" << std::endl;

  return 1;
  
}





void TauTauAnalysis::genFilterZtautau() {
//   std::cout << "genFilterZtautau" << std::endl;
    
  for ( int p = 0; p <   (m_genParticle.N) ; ++p ) {
    UZH::GenParticle mygoodGenPart( &m_genParticle, p );

    if( fabs(mygoodGenPart.pdgId()) == 15 ){
      if( mygoodGenPart.mother()[0]==25 ){ GenEvent_Htata_filter = true; }
      if( mygoodGenPart.mother()[0]==23 ){ GenEvent_Ztata_filter = true; }
    } 
  }
}





void TauTauAnalysis::setGenBosonTLVs(){
//   std::cout << "recoilCorrection" << std::endl;
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#Computation_of_generator_Z_W_Hig
// TODO: check case of more than one boson
  
  boson_tlv     = TLorentzVector();
  boson_tlv_vis = TLorentzVector();
  
  for ( int p = 0; p < (m_genParticle.N); ++p ) {
    UZH::GenParticle mygoodGenPart( &m_genParticle, p );
    float pdg = fabs(mygoodGenPart.pdgId());
    bool isNeutrino = (pdg == 12 || pdg == 14 || pdg == 16);
    
    if( (mygoodGenPart.fromHardProcessFinalState() && (pdg == 11 || pdg == 13 || isNeutrino)) ||
        mygoodGenPart.isDirectHardProcessTauDecayProductFinalState() ){
      boson_tlv += mygoodGenPart.tlv();
      if(!isNeutrino)
        boson_tlv_vis += mygoodGenPart.tlv();
    }
  }
  
  //std::cout << ">>> recoilCorrection: boson_tlv.E() " << boson_tlv.E() << std::endl;
  //std::cout << ">>> recoilCorrection: boson_tlv.P() " << boson_tlv.P() << std::endl;
  
}





int TauTauAnalysis::genMatch(Float_t lep_eta, Float_t lep_phi) {
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_Matching
//  1: prompt electron
//  2: prompt muon
//  3: tau -> e
//  4. tau -> mu
//  5: tau -> hadr.
//  6: fake jet / PU

  Float_t min_dR = 1000;
  int id = 6;

  // check for lepton matching, first
  for ( int p = 0; p <   (m_genParticle.N) ; ++p ) {
    UZH::GenParticle mygoodGenPart( &m_genParticle, p );
    
    Float_t pt = mygoodGenPart.pt();
    Float_t eta = mygoodGenPart.eta();
    Float_t phi = mygoodGenPart.phi();
    Int_t pdgId = abs(mygoodGenPart.pdgId());
    Int_t isPrompt = mygoodGenPart.isPrompt();
    Int_t isDirectPromptTauDecayProduct = mygoodGenPart.isDirectPromptTauDecayProduct();
    
    if(mygoodGenPart.status()!=1) continue;
    
    if(! ((pdgId==11 || pdgId==13) && (isPrompt > 0.5 || isDirectPromptTauDecayProduct > 0.5) && pt > 8) ) continue;
    
    Float_t dr = deltaR(lep_eta - eta, deltaPhi(lep_phi, phi));
    if(dr < min_dR){
      min_dR = dr;
      if( pdgId==11 && isPrompt > 0.5) id = 1;
      if( pdgId==13 && isPrompt > 0.5) id = 2;
      if( pdgId==11 && isDirectPromptTauDecayProduct > 0.5) id = 3;
      if( pdgId==13 && isDirectPromptTauDecayProduct > 0.5) id = 4;
      
    }
  }
  
  // Retrieve visible pT of the taus ! 
  // Should be done in Ntuplizer level from next time.
  std::map<int, TLorentzVector> gennus;
  std::map<int, TLorentzVector> gentaus;
  for ( int p = 0; p <   (m_genParticle.N) ; ++p ) {
    UZH::GenParticle mygoodGenPart( &m_genParticle, p );
    
    Float_t pt = mygoodGenPart.pt();
    Float_t eta = mygoodGenPart.eta();
    Float_t phi = mygoodGenPart.phi();
    Float_t energy = mygoodGenPart.e();
    Int_t pdgId = mygoodGenPart.pdgId();
    Int_t abspdgId = abs(mygoodGenPart.pdgId());
    Int_t isPrompt = mygoodGenPart.isPrompt();

    Int_t mother = -999;
    if(mygoodGenPart.nMoth() !=0){
      mother = abs(mygoodGenPart.mother()[0]);
    }

    // save gen tau neutrino
    if(mygoodGenPart.status()==1 && abspdgId==16 && mother==15){
      TLorentzVector genNeutrino;
      genNeutrino.SetPtEtaPhiE(pt,eta,phi,energy);
      gennus[pdgId] = genNeutrino;
      //std::cout << "Neutrino : " << pdgId << " " << genNeutrino.Pt() << std::endl;
    }

    // skip if not tau
    if(!(mygoodGenPart.status()==2 && abspdgId==15 && isPrompt > 0.5)) continue;

    bool isleptonic = false;
    for(int daughter=0; daughter < (int)mygoodGenPart.nDau(); daughter++){
      //std::cout << "\t" << "parent " << pdgId << "(pt = " << pt << ") daughter : " << mygoodGenPart.dau()[daughter] << std::endl;
      Int_t daughter_pdgId = abs(mygoodGenPart.dau()[daughter]);
      if(daughter_pdgId==11 || daughter_pdgId==13) isleptonic = true;
      if(daughter_pdgId==15){
        std::cout << "Tau decays into taus !!!" << std::endl;
        isleptonic = true;
      }
    }

    if(isleptonic==false){
      TLorentzVector genPt;
      genPt.SetPtEtaPhiE(pt,eta,phi,energy);
      gentaus[pdgId] = genPt;
    }
  }
  
  
  // if tau decays hadronically: loop over gentaus, gennus
  // substract gennu pt from gentau pt
  for(std::map<int, TLorentzVector>::iterator it = gentaus.begin(); it!=gentaus.end(); ++it){
    Int_t pdg = (*it).first;
    for(std::map<int, TLorentzVector>::iterator itn = gennus.begin(); itn!=gennus.end(); ++itn){
      Int_t nu = (*itn).first;
      if(pdg==15){
        if(nu==16) (*it).second -= (*itn).second;
      }else if(pdg==-15){
        if(nu==-16) (*it).second -= (*itn).second;
      }else{
	  std::cout << "Impossible !!!" << std::endl;
      }
    }
  }
  
  
  // match lepton gentaus
  for(std::map<int, TLorentzVector>::iterator it = gentaus.begin(); it!=gentaus.end(); ++it){
    //    Int_t pdg = (*it).first;
    Float_t dr = deltaR(lep_eta - (*it).second.Eta(), 
			            deltaPhi(lep_phi, (*it).second.Phi()));
    if(dr < min_dR){
      min_dR = dr;
      id = 5;
    }
    //    std::cout << "Last Tau = " << pdg << " " << (*it).second.Pt() << std::endl;
  }

  if(min_dR > 0.2) id = 6;
  
  return id;

}





Float_t TauTauAnalysis::deltaPhi(Float_t p1, Float_t p2){
// std::cout << "deltaPhi" << std::endl;

  Float_t res = p1 - p2;
  while(res > TMath::Pi()){
    res -= 2*TMath::Pi();
  }
  while(res < -TMath::Pi()){
    res += 2*TMath::Pi();
  }
  
  return res;

}





Float_t TauTauAnalysis::deltaR(Float_t deta, Float_t dphi){
//   std::cout << "deltaR" << std::endl;
  
  return TMath::Sqrt(TMath::Power(deta,2) + TMath::Power(dphi,2));

}





bool TauTauAnalysis::isNonTrigElectronID(const UZH::Electron& electron)
{
//   std::cout << "isNonTrigElectronID" << std::endl;
// 90% efficiency working point
// https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#Non_triggering_electron_MVA_deta
// https://github.com/gitytakahas/EXOVVNtuplizerRunII/blob/80X_ntuplizer/Ntuplizer/plugins/ElectronsNtuplizer.cc#L66-L98
  Float_t eta = fabs(electron.superCluster_eta());
  Float_t pt  = electron.pt();
  Float_t mva = electron.nonTrigMVAID();

  // assume pt > 5.0 GeV
  if(pt <= 10.){
    if(eta < 0.8)           return mva > -0.083313;
    else if(eta < 1.479)    return mva > -0.235222;
    else                    return mva > -0.67099;
  }
  else if(pt > 10.){
    if(eta < 0.8)           return mva > 0.913286;
    else if(eta < 1.479)    return mva > 0.805013;
    else                    return mva > 0.358969;
  }
  else{
    std::cout << ">>> Does not happen" << std::endl;
    return false;
  } 
}





bool TauTauAnalysis::LooseJetID(const UZH::Jet& jet)
{
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID#Recommendations_for_13_TeV_data
  Float_t eta = fabs(jet.eta());
  Float_t NHF  = jet.nhf();  //neutralHadronEnergyFraction();
  Float_t NEMF = jet.nemf(); //neutralEmEnergyFraction();
  Float_t NM   = jet.nm();   //neutralMultiplicity();
  Float_t CM   = jet.cm();   //chargedMultiplicity();

  if(eta <= 2.4){      // eta < 2.4
    Float_t CHF  = jet.chf();  //chargedHadronEnergyFraction();
    Float_t CEMF = jet.cemf(); //chargedEmEnergyFraction();
    return NHF < 0.99 && NEMF < 0.99 && NM+CM > 1 &&
           CHF > 0    && CEMF < 0.99 &&    CM > 0;
  }
  else if(eta <= 2.7){ // eta < 2.7  
    return NHF < 0.99 && NEMF < 0.99 && NM+CM > 1;
  }
  else if(eta <= 3.0){ // eta < 3.0  
    return NEMF < 0.90 && NM > 2;
  }
  else if(eta  < 4.7){ // eta < 4.7 = m_AK4jetEtaCut  
    return NEMF < 0.90 && NM > 10;
  } 
  return false;
}





float TauTauAnalysis::genMatchSF(const int genmatch_2, const float tau_eta){
  //std::cout << "genMatchSF" << std::endl;
  //https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_Matching
  //https://indico.cern.ch/event/563239/contributions/2279020/attachments/1325496/1989607/lepTauFR_tauIDmeeting_20160822.pdf
  
  float eta = fabs(tau_eta);
  
  // electron -> tau    for VLoose
  if      (genmatch_2 == 3) {
    if      ( eta < 1.46  ) return 1.292;
    else if ( eta > 1.558 ) return 1.536;
  }
  // muon -> tau        for Tight
  else if (genmatch_2 == 4) {
    if      ( eta < 0.4 ) return 1.418;
    else if ( eta < 0.8 ) return 1.134;  
    else if ( eta < 1.2 ) return 1.260;  
    else if ( eta < 1.7 ) return 1.660;  
    else                  return 1.205;
  }
  // real tau
  else if (genmatch_2 == 5) {
    return 0.90;
  }
  
  return 1.0;
}





void TauTauAnalysis::extraLeptonVetos(const std::string& channel, const UZH::Muon& muon, const UZH::Electron& electron){
  //std::cout << "extraLeptonVetos" << std::endl;
  
  b_dilepton_veto_  = false;
  b_extraelec_veto_ = false;
  b_extramuon_veto_ = false;
  
  // extra leptons
  // https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2016#Baseline_mu_tau_h
  // https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2016#Baseline_e_tau_h
  // https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2016#Third_lepton_vetoes
  
  std::vector<UZH::Muon> passedMuons;
  for( int i = 0; i < m_muon.N; ++i ){
    UZH::Muon mymuon( &m_muon, i );  
    
    if(mymuon.pt() < 10) continue;
    if(fabs(mymuon.eta()) > 2.4) continue;
    if(fabs(mymuon.dz_allvertices()) > 0.2) continue;
    if(fabs(mymuon.d0_allvertices()) > 0.045) continue;
    if(mymuon.SemileptonicPFIso() / mymuon.pt() > 0.3) continue;

    // extra muon veto
    if(mymuon.isMediumMuon() > 0.5 && channel=="mutau"){
	  if(mymuon.eta() != muon.eta() && mymuon.pt() != muon.pt() && mymuon.phi() != muon.phi())
	    b_extramuon_veto_ = true;
      //else continue;
    }
    
    if( mymuon.pt() > 15 && mymuon.isGlobalMuon()
                         && mymuon.isTrackerMuon() 
                         && mymuon.isPFMuon() ){
      passedMuons.push_back(mymuon);
    }    
  }
  
  std::vector<UZH::Electron> passedElectrons;
  for( int i = 0; i < m_electron.N; ++i ){
    UZH::Electron myelectron( &m_electron, i );
    
    if(myelectron.pt() < 10) continue;
    if(fabs(myelectron.eta()) > 2.5) continue;
    if(fabs(myelectron.dz_allvertices()) > 0.2) continue;
    if(fabs(myelectron.d0_allvertices()) > 0.045) continue;
    if(myelectron.SemileptonicPFIso() / myelectron.pt() > 0.3) continue;
    
    // extra electron veto
    if(myelectron.passConversionVeto() &&
       isNonTrigElectronID(myelectron) && 
       myelectron.expectedMissingInnerHits() <= 1 &&
       channel=="eletau"){
      if( myelectron.pt() != electron.pt() && myelectron.eta() != electron.eta() && myelectron.phi() != electron.phi())
        b_extraelec_veto_ = true;
      //else continue;
    }
    
    if(myelectron.pt() > 15 && fabs(myelectron.nonTrigMVAID() > 0.5)) // TODO: change to equivalent POG Spring15 25ns cut-based "Veto" ID    
      passedElectrons.push_back(myelectron);
  }
  
  
  // dilepton veto
  if(channel=="mutau"){
    bool _flag = false;
    for(int imuon = 0; imuon < (int)passedMuons.size(); imuon++){
      for(int jmuon = 0; jmuon < (int)passedMuons.size(); jmuon++){
        if(imuon < jmuon) continue;
        if(passedMuons[imuon].charge() * passedMuons[jmuon].charge() < 0 &&
           passedMuons[imuon].tlv().DeltaR(passedMuons[jmuon].tlv()) > 0.15)
          b_dilepton_veto_ = true; 
      }
    }
  }
  else if(channel=="eletau"){
    bool _flag = false;
    for(int ielectron = 0; ielectron < (int)passedElectrons.size(); ielectron++){
      for(int jelectron = 0; jelectron < (int)passedElectrons.size(); jelectron++){
        if(ielectron < jelectron) continue;
	    if(passedElectrons[ielectron].charge() * passedElectrons[jelectron].charge() < 0 &&
	       passedElectrons[ielectron].tlv().DeltaR(passedElectrons[jelectron].tlv()) > 0.15)
          b_dilepton_veto_ = true; 
      }
    }
  }
}





bool TauTauAnalysis::getBTagWeight_promote_demote( const UZH::Jet& jet ) {
  //std::cout << "getBTagSF_promote_demote" << std::endl;
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#B_tag_scale_factors
  // example: https://github.com/rappoccio/usercode/blob/Dev_53x/EDSHyFT/plugins/BTagSFUtil_tprime.h
  //
  // instead of calculating the event weights,
  // scale factors are used to update the b-tagging status on a jet-by-jet basis
  // advantage: 1) no need to apply event weights
  //            2) reproducibility with seed
  
  bool isBTagged = (jet.csv() > m_CSVWorkingPoint);
  if (m_isData) return isBTagged;
  
  //if (isBTagged) std::cout << "Jet b tagged" << std::endl;
  //else           std::cout << "Jet b not tagged" << std::endl;
  
  TRandom3* generator = new TRandom3( (int) ((jet.eta()+5)*100000) );
  double rand = generator->Uniform(1.);
  
  double BTag_SF  = m_bTaggingScaleTool.getScaleFactor_noWeight(jet);
  double BTag_eff = m_bTaggingScaleTool.getEfficiency(jet,"jet_ak4");
  double BTag_SFweight  = m_bTaggingScaleTool.getScaleFactor_veto(jet);
  b_weightbtag_ *= BTag_SFweight;
  
  if (BTag_SF == 1) return isBTagged; // no correction
  else if(BTag_SF > 1){
    if(isBTagged) return isBTagged;
    float mistagPercentage = (1.0 - BTag_SF) / (1.0 - (1.0/BTag_eff)); // fraction of jets to be promoted
    if( rand < mistagPercentage ) isBTagged = true; // PROMOTE
  }
  else{//(BTag_SF < 1)
    if(!isBTagged) return isBTagged;
    if( rand < 1 - BTag_SF ) isBTagged = false; // DEMOTE: 1-SF fraction of jets to be demoted
  }
  
  return isBTagged;
}





void TauTauAnalysis::checks() {
  //std::cout << "checks" << std::endl;

  /// GEN TAUS
  std::vector<UZH::GenParticle> taus;
  std::vector<UZH::GenParticle> muons;
  for ( int p = 0; p < (m_genParticle.N); ++p ) {
    UZH::GenParticle mygoodGenPart( &m_genParticle, p );
    Int_t pdgID = fabs(mygoodGenPart.pdgId());
    if( pdgID == 15 && fabs(mygoodGenPart.mother()[0]) != 15){ // X -> TT 7000021
      taus.push_back(mygoodGenPart);
      
      /// GEN MUON
      //for(int daughter=0; daughter < (int)mygoodGenPart.nDau(); daughter++){
      //  Int_t daughter_pdgId = abs(mygoodGenPart.dau()[daughter]);
      //  if(daughter_pdgId==13){ muons.push_back(mygoodGenPart); break; }
      //}
    }
    else if ( pdgID == 13 && mygoodGenPart.isDirectPromptTauDecayProduct()){
      muons.push_back(mygoodGenPart);
    }
  }
  
  if(taus.size() < 2)      std::cout << "Warning: taus.size() < 2" << std::endl;
  else{
    //else std::cout << "taus.size() = 2" << std::endl;
    float pt_tau1 = taus.at(0).pt();
    float pt_tau2 = taus.at(1).pt();
    if(pt_tau1 < pt_tau2){
      float pt = pt_tau1;
      pt_tau1 = pt_tau2;
      pt_tau2 = pt;
    }
    
    Hist("pt_gentaus", "checks" )->Fill( pt_tau1 );
    Hist("pt_gentaus", "checks" )->Fill( pt_tau2 );
    Hist("pt_gentau1", "checks" )->Fill( pt_tau1 );
    Hist("pt_gentau2", "checks" )->Fill( pt_tau2 );
    Hist("DeltaR_tautau", "checks" )->Fill( taus.at(0).tlv().DeltaR(taus.at(1).tlv()) );
    
    for( int i = 0; i < (int)muons.size(); ++i ){
      Hist("pt_muon", "checks" )->Fill( muons.at(i).pt() );
    }
    
  }

//   /// RECO MUON
//   //UZH::Muon muon;
//   for( int i = 0; i < m_muon.N; ++i ){
//     UZH::Muon mymuon( &m_muon, i );
//     
//     //if (mymuon.pt() < m_muonPtCut) continue;
//     //if (fabs(mymuon.eta()) > m_muonEtaCut) continue;
//     //if (fabs(mymuon.d0_allvertices()) > m_muonD0Cut) continue;
//     //if (fabs(mymuon.dz_allvertices()) > m_muonDzCut) continue;
//     //if (mymuon.isMediumMuon() < 0.5) continue;
//     
//     //for ( int p = 0; p < (m_genParticle.N); ++p ) {
//     //  UZH::GenParticle mygoodGenPart( &m_genParticle, p );
//     //  if deltaR(mymuon.tlv(),);
//     //  muon = mymuon;
//     //  break;
//     //}
//     
//     //muon = mymuon;
//     Hist("pt_muon", "checks" )->Fill( mymuon.pt() );
//     break;
//   }

}





