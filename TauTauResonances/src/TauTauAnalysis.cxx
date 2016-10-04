// $Id: CycleCreators.py 344 2012-12-13 13:10:53Z krasznaa $

// Local include(s):
#include "../include/TauTauAnalysis.h"
// External include(s):
#include "../GoodRunsLists/include/TGoodRunsListReader.h"

#include <TMath.h>

ClassImp( TauTauAnalysis );


// define cut names

const std::string TauTauAnalysis::kCutName[ TauTauAnalysis::kNumCuts ] = {
  "BeforeCuts",            // C0
  "JSON",                  // C1
  "Trigger",               // C2
  "MetFilters",            // C3
  "Lepton",                // C4
  "LepTau",                // C6
};

TauTauAnalysis::TauTauAnalysis()
   : SCycleBase()
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
   , m_ScaleFactorTool( this )
{

   m_logger << INFO << "Hello!" << SLogger::endmsg;
   SetLogName( GetName() );
   
   // read configuration details from XML file
   DeclareProperty("RecoTreeName", m_recoTreeName = "physics" );

   // channels
   channels_.push_back("mutau");
   channels_.push_back("eletau");


   DeclareProperty( "JetAK4Name",               m_jetAK4Name               = "jetAK4" );
   DeclareProperty( "ElectronName",             m_electronName             = "el" );
   DeclareProperty( "MuonName",                 m_muonName                 = "mu" );
   DeclareProperty( "TauName",                  m_tauName                  = "tau" );
   DeclareProperty( "MissingEtName",            m_missingEtName            = "MET" );
   DeclareProperty( "GenParticleName",          m_genParticleName          = "genParticle" );
   
   DeclareProperty( "IsData",                   m_isData                   = false );
   DeclareProperty( "doSVFit",                  m_doSVFit                  = false );
   DeclareProperty( "IsSignal",                 m_isSignal                 = false );
   
   DeclareProperty( "AK4JetPtCut",              m_AK4jetPtCut           = 20.);
   DeclareProperty( "AK4JetEtaCut",             m_AK4jetEtaCut          = 4.7);

   DeclareProperty( "ElectronPtCut",                 m_electronPtCut              = 26. );
   DeclareProperty( "ElectronEtaCut",                m_electronEtaCut             = 2.1 );
   DeclareProperty( "ElectronD0Cut",                m_electronD0Cut             = 0.045 );
   DeclareProperty( "ElectronDzCut",                m_electronDzCut             = 0.2 );
   DeclareProperty( "ElectronIsoCut",                m_electronIsoCut             = 0.1 );
   
   DeclareProperty( "MuonPtCut",                 m_muonPtCut              = 23. );
   DeclareProperty( "MuonEtaCut",                m_muonEtaCut             = 2.1 );
   DeclareProperty( "MuonD0Cut",                m_muonD0Cut             = 0.045 );
   DeclareProperty( "MuonDzCut",                m_muonDzCut             = 0.2 );
   DeclareProperty( "MuonIsoCut",                m_muonIsoCut             = 0.15 );

   DeclareProperty( "TauPtCut",                 m_tauPtCut           = 20 );
   DeclareProperty( "TauEtaCut",                m_tauEtaCut          = 2.3  );
   DeclareProperty( "TauDzCut",                m_tauDzCut          = 0.2  );

   DeclareProperty( "JSONName",                 m_jsonName             = std::string (std::getenv("SFRAME_DIR")) + "/../GoodRunsLists/JSON/Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt" );

   //   DeclareProperty( "TrigSF_muonName",                 m_TrigSF_muonName             = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.root" ); 
   //   DeclareProperty( "IDSF_muonName",                  m_IDSF_muonName            = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/MuonID_Z_RunBCD_prompt80X_7p65.root" );
   //   DeclareProperty( "IsoSF_muonName",                  m_IsoSF_muonName            = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/MuonIso_Z_RunBCD_prompt80X_7p65.root" );
   //   DeclareProperty( "IDSF_eleName",                  m_IDSF_eleName            = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Electron/egammaEffi.txt_SF2D.root" );
  
   
}

TauTauAnalysis::~TauTauAnalysis() {

  for(int channel = 0; channel < (int)channels_.size(); channel++){
    file[channel]->Write();
    file[channel]->Close();
  }    

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
  m_triggerNames_mutau.push_back("HLT_IsoMu22_v"); // OR
  m_triggerNames_mutau.push_back("HLT_IsoTkMu22_v");
//  m_triggerNames_mutau.push_back("HLT_IsoMu18_v");
//  m_triggerNames_mutau.push_back("HLT_IsoMu20_v4");
//  m_triggerNames_mutau.push_back("HLT_IsoMu22_v3");
//  m_triggerNames_mutau.push_back("HLT_IsoMu22_eta2p1_v2");
//  m_triggerNames_mutau.push_back("HLT_IsoMu24_v2");
//  m_triggerNames_mutau.push_back("HLT_IsoMu27_v4");
//  m_triggerNames_mutau.push_back("HLT_IsoTkMu18_v3");
//  m_triggerNames_mutau.push_back("HLT_IsoTkMu20_v5");
//  m_triggerNames_mutau.push_back("HLT_IsoTkMu22_eta2p1_v2");
//  m_triggerNames_mutau.push_back("HLT_IsoTkMu22_v3");
//  m_triggerNames_mutau.push_back("HLT_IsoTkMu24_v2");
//  m_triggerNames_mutau.push_back("HLT_IsoTkMu27_v4");
//  m_triggerNames_mutau.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v5");
//  m_triggerNames_mutau.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v5");
//  m_triggerNames_mutau.push_back("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2");
//  m_triggerNames_mutau.push_back("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2");
//  m_triggerNames_mutau.push_back("HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v2");

  // electron triggers
  m_triggerNames_eletau.push_back("HLT_Ele25_eta2p1_WPTight_Gsf_v");
//  m_triggerNames_eletau.push_back("HLT_Ele23_WPLoose_Gsf_v4");
//  m_triggerNames_eletau.push_back("HLT_Ele24_eta2p1_WPLoose_Gsf_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele25_WPTight_Gsf_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele25_eta2p1_WPLoose_Gsf_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele25_eta2p1_WPTight_Gsf_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele27_WPLoose_Gsf_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele27_WPTight_Gsf_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele27_eta2p1_WPLoose_Gsf_v3");
//  m_triggerNames_eletau.push_back("HLT_Ele27_eta2p1_WPTight_Gsf_v3");
//  m_triggerNames_eletau.push_back("HLT_Ele32_eta2p1_WPTight_Gsf_v3");
//  m_triggerNames_eletau.push_back("HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v3");
//  m_triggerNames_eletau.push_back("HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2");
//  m_triggerNames_eletau.push_back("HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2");


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
      return lep_pt > another.lep_pt;
    if (tau_iso != another.tau_iso)
      return tau_iso > another.tau_iso; // note that tau isolation is better if we have higher value ! 
    if (tau_pt != another.tau_pt)
      return tau_pt > another.tau_pt;
    return ilepton < another.ilepton;
  }

};




void TauTauAnalysis::EndCycle() throw( SError ) {
   std::cout << "events in mu_tau " <<mu_tau <<std::endl;
   std::cout << "events in ele_tau " <<ele_tau <<std::endl;
   return;
}

void TauTauAnalysis::BeginInputData( const SInputData& id ) throw( SError ) {

  m_logger << INFO << "RecoTreeName:         " <<             m_recoTreeName << SLogger::endmsg;
  m_logger << INFO << "JetAK4Name:           " <<             m_jetAK4Name << SLogger::endmsg;
  m_logger << INFO << "ElectronName:         " <<             m_electronName << SLogger::endmsg;
  m_logger << INFO << "MuonName:             " <<             m_muonName << SLogger::endmsg;
  m_logger << INFO << "TauName:             " <<             m_tauName << SLogger::endmsg;
  m_logger << INFO << "GenParticleName:      " <<             m_genParticleName << SLogger::endmsg;
  
  m_logger << INFO << "IsData:           " <<                   (m_isData ? "TRUE" : "FALSE") << SLogger::endmsg;
  m_logger << INFO << "IsSignal:           " <<                 (m_isSignal ? "TRUE" : "FALSE") << SLogger::endmsg;
  m_logger << INFO << "doSVFit:           " <<                   (m_doSVFit ? "TRUE" : "FALSE") << SLogger::endmsg;
  m_logger << INFO << "ElectronPtCut:           " <<                 m_electronPtCut << SLogger::endmsg;
  m_logger << INFO << "ElectronEtaCut:           " <<                m_electronEtaCut << SLogger::endmsg;
  m_logger << INFO << "ElectronD0Cut:           " <<                 m_electronD0Cut << SLogger::endmsg;
  m_logger << INFO << "ElectronDzCut:           " <<                m_electronDzCut << SLogger::endmsg;
  m_logger << INFO << "ElectronIsoCut:           " <<                m_electronIsoCut << SLogger::endmsg;
  
  m_logger << INFO << "MuonPtCut:           " <<                 m_muonPtCut << SLogger::endmsg;
  m_logger << INFO << "MuonEtaCut:           " <<                m_muonEtaCut << SLogger::endmsg;
  m_logger << INFO << "MuonD0Cut:           " <<                m_muonD0Cut << SLogger::endmsg;
  m_logger << INFO << "MuonDzCut:           " <<                m_muonDzCut << SLogger::endmsg;
  m_logger << INFO << "MuonIsoCut:           " <<                m_muonIsoCut << SLogger::endmsg;
  
  m_logger << INFO << "TauPtCut:           " <<                 m_tauPtCut << SLogger::endmsg;
  m_logger << INFO << "TauEtaCut:           " <<                m_tauEtaCut << SLogger::endmsg;
  m_logger << INFO << "TauDzCut:           " <<                m_tauDzCut << SLogger::endmsg;
  
  
  m_logger << INFO << "JSONName:           " <<                 m_jsonName << SLogger::endmsg;
  //  m_logger << INFO << "TrigSF_muonName:           " <<                 m_TrigSF_muonName << SLogger::endmsg;
  //  m_logger << INFO << "IDSF_muonName:           " <<                 m_IDSF_muonName << SLogger::endmsg;
  //  m_logger << INFO << "IsoSF_muonName:           " <<                 m_IsoSF_muonName << SLogger::endmsg;
  //  m_logger << INFO << "IDSF_eleName:           " <<                 m_IDSF_eleName << SLogger::endmsg;


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


  for(int channel = 0; channel < (int)channels_.size(); channel++){

    TString filename = "Myroot_" + channels_[channel];
    filename += ".root";
    file[channel] = new TFile(filename, "recreate");

    tree[channel] = new TTree("tree", "tree");

    tree[channel]->Branch("weight", &b_weight, "weight/F");
    tree[channel]->Branch("genweightGen", &b_genweight, "genweight/F");
    tree[channel]->Branch("puweight", &b_puweight, "puweight/F");

    tree[channel]->Branch("run", &b_run, "run/I");
    tree[channel]->Branch("evt", &b_evt, "evt/I");
    tree[channel]->Branch("lumi", &b_lum, "lumi/I");

    tree[channel]->Branch("is_data", &b_isData, "is_data/I");
    tree[channel]->Branch("npv", &b_npv, "npv/I");
    tree[channel]->Branch("channel", &b_channel, "channel/I");


    tree[channel]->Branch("pt_1", &b_pt_1, "pt_1/F");
    tree[channel]->Branch("eta_1", &b_eta_1, "eta_1/F");
    tree[channel]->Branch("phi_1", &b_phi_1, "phi_1/F");
    tree[channel]->Branch("m_1", &b_m_1, "m_1/F");
    tree[channel]->Branch("q_1", &b_q_1, "q_1/I");
    tree[channel]->Branch("d0_1", &b_d0_1, "d0_1/F");
    tree[channel]->Branch("dz_1", &b_dz_1, "dz_1/F");
    tree[channel]->Branch("mt_1", &b_mt_1, "mt_1/F");
    tree[channel]->Branch("pfmt_1", &b_pfmt_1, "pfmt_1/F");
    tree[channel]->Branch("puppimt_1", &b_puppimt_1, "puppimt_1/F");
    tree[channel]->Branch("iso_1", &b_iso_1, "iso_1/F");
    tree[channel]->Branch("id_e_mva_nt_loose_1", &b_id_e_mva_nt_loose_1, "id_e_mva_nt_loose_1/F");
    tree[channel]->Branch("gen_match_1", &b_gen_match_1, "gen_match_1/I");
    tree[channel]->Branch("trigweight_1", &b_trigweight_1, "trigweight_1/F");
    tree[channel]->Branch("isoweight_1", &b_isoweight_1, "isoweight_1/F");

    tree[channel]->Branch("pt_2", &b_pt_2, "pt_2/F");
    tree[channel]->Branch("eta_2", &b_eta_2, "eta_2/F");
    tree[channel]->Branch("phi_2", &b_phi_2, "phi_2/F");
    tree[channel]->Branch("m_2", &b_m_2, "m_2/F");
    tree[channel]->Branch("q_2", &b_q_2, "q_2/I");
    tree[channel]->Branch("d0_2", &b_d0_2, "d0_2/F");
    tree[channel]->Branch("dz_2", &b_dz_2, "dz_2/F");
    tree[channel]->Branch("mt_2", &b_mt_2, "mt_2/F");
    tree[channel]->Branch("pfmt_2", &b_pfmt_2, "pfmt_2/F");
    tree[channel]->Branch("puppimt_2", &b_puppimt_2, "puppimt_2/F");
    tree[channel]->Branch("iso_2", &b_iso_2, "iso_2/F");
    tree[channel]->Branch("gen_match_2", &b_gen_match_2, "gen_match_2/I");
    tree[channel]->Branch("idisoweight_2", &b_idisoweight_2, "idisoweight_2/F");
    
    tree[channel]->Branch("jpt_1",  &b_jpt_1, "jpt_1/F");
    tree[channel]->Branch("jeta_1", &b_jeta_1, "jeta_1/F");
    tree[channel]->Branch("jphi_1", &b_jphi_1, "jphi_1/F");
    
    tree[channel]->Branch("jpt_2",  &b_jpt_2, "jpt_2/F");
    tree[channel]->Branch("jeta_2", &b_jeta_2, "jeta_2/F");
    tree[channel]->Branch("jphi_2", &b_jphi_2, "jphi_2/F");
    
    tree[channel]->Branch("bpt_1",  &b_bpt_1, "bpt_1/F");
    tree[channel]->Branch("beta_1", &b_beta_1, "beta_1/F");
    tree[channel]->Branch("bphi_1", &b_bphi_1, "bphi_1/F");
    
    tree[channel]->Branch("againstElectronVLooseMVA6_2", &b_againstElectronVLooseMVA6_2, "againstElectronVLooseMVA6_2/I");
    tree[channel]->Branch("againstElectronLooseMVA6_2", &b_againstElectronLooseMVA6_2, "againstElectronLooseMVA6_2/I");
    tree[channel]->Branch("againstElectronMediumMVA6_2", &b_againstElectronMediumMVA6_2, "againstElectronMediumMVA6_2/I");
    tree[channel]->Branch("againstElectronTightMVA6_2", &b_againstElectronTightMVA6_2, "againstElectronTightMVA6_2/I");
    tree[channel]->Branch("againstElectronVTightMVA6_2", &b_againstElectronVTightMVA6_2, "againstElectronVTightMVA6_2/I");
    tree[channel]->Branch("againstMuonLoose3_2", &b_againstMuonLoose3_2, "againstMuonLoose3_2/I");
    tree[channel]->Branch("againstMuonTight3_2", &b_againstMuonTight3_2, "againstMuonTight3_2/I");
    tree[channel]->Branch("byCombinedIsolationDeltaBetaCorrRaw3Hits_2", &b_byCombinedIsolationDeltaBetaCorrRaw3Hits_2, "byCombinedIsolationDeltaBetaCorrRaw3Hits_2/I");
    tree[channel]->Branch("byIsolationMVA3newDMwLTraw_2", &b_byIsolationMVA3newDMwLTraw_2, "byIsolationMVA3newDMwLTraw_2/F");
    tree[channel]->Branch("byIsolationMVA3oldDMwLTraw_2", &b_byIsolationMVA3oldDMwLTraw_2, "byIsolationMVA3oldDMwLTraw_2/F");
    tree[channel]->Branch("chargedIsoPtSum_2", &b_chargedIsoPtSum_2, "chargedIsoPtSum_2/F");
    tree[channel]->Branch("neutralIsoPtSum_2", &b_neutralIsoPtSum_2, "neutralIsoPtSum_2/F");
    tree[channel]->Branch("puCorrPtSum_2", &b_puCorrPtSum_2, "puCorrPtSum_2/F");
    tree[channel]->Branch("decayModeFindingOldDMs_2", &b_decayModeFindingOldDMs_2, "decayModeFindingOldDMs_2/I");
    tree[channel]->Branch("decayMode_2", &b_decayMode_2, "decayMode_2/I");

    tree[channel]->Branch("met", &b_met, "met/F");
    tree[channel]->Branch("metphi", &b_metphi, "metphi/F");
    tree[channel]->Branch("metcov00", &b_metcov00, "metcov00/F");
    tree[channel]->Branch("metcov01", &b_metcov01, "metcov01/F");
    tree[channel]->Branch("metcov10", &b_metcov10, "metcov10/F");
    tree[channel]->Branch("metcov11", &b_metcov11, "metcov11/F");
    tree[channel]->Branch("mvacov00", &b_mvacov00, "mvacov00/F");
    tree[channel]->Branch("mvacov01", &b_mvacov01, "mvacov01/F");
    tree[channel]->Branch("mvacov10", &b_mvacov10, "mvacov10/F");
    tree[channel]->Branch("mvacov11", &b_mvacov11, "mvacov11/F");
    tree[channel]->Branch("puppimet", &b_puppimet, "puppimet/F");
    tree[channel]->Branch("puppimetphi", &b_puppimetphi, "puppimetphi/F");
    tree[channel]->Branch("mvamet", &b_mvamet, "mvamet/F");
    tree[channel]->Branch("mvametphi", &b_mvametphi, "mvametphi/F");

    tree[channel]->Branch("m_vis", &b_m_vis, "m_vis/F");
    tree[channel]->Branch("m_sv", &b_m_sv, "m_sv/F");
    tree[channel]->Branch("m_sv_pfmet", &b_m_sv_pfmet, "m_sv_pfmet/F");

    tree[channel]->Branch("mt_tot", &b_mt_tot, "mt_tot/F");
    tree[channel]->Branch("dR_ll", &b_dR_ll, "dR_ll/F");
    tree[channel]->Branch("pt_tt", &b_pt_tt, "pt_tt/F");
    tree[channel]->Branch("njets", &b_njets, "njets/I");
    tree[channel]->Branch("ncjets", &b_ncjets, "ncjets/I");
    tree[channel]->Branch("nfjets", &b_nfjets, "nfjets/I");
    tree[channel]->Branch("njetspt20", &b_njetspt20, "n_njetspt20/I");
    tree[channel]->Branch("nbtag", &b_nbtag, "nbtag/I");
    tree[channel]->Branch("ncbtag", &b_ncbtag, "ncbtag/I");
    tree[channel]->Branch("nfbtag", &b_nfbtag, "nfbtag/I");
    tree[channel]->Branch("NUP", &b_NUP, "NUP/I");
    tree[channel]->Branch("rho", &b_rho, "rho/F");
    tree[channel]->Branch("npu", &b_npu, "npu/I");
    tree[channel]->Branch("weightLepID", &b_weightLepID_, "weightLepID/F");
    tree[channel]->Branch("weightLepIso", &b_weightLepIso_, "weightLepIso/F");

  }
  
  for (auto ch: channels_){
    TString hname = "cutflow_" + ch;
    TString dirname = "histogram_" + ch;
    std::cout << hname << " " << dirname << std::endl;
    Book( TH1F(hname, hname, 20, 0.5, 20.5 ), dirname); 
  }

  //  m_bTaggingScaleTool.BeginInputData( id );
  m_ScaleFactorTool.BeginInputData( id );

  return;

}

void TauTauAnalysis::EndInputData( const SInputData& ) throw( SError ) {
//   std::cout << "EndInputData" << std::endl;

  //
  // Final analysis of cut flow
  //
  
  for(auto ch: channels_){
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

  m_logger << INFO << "Connecting input variables" << SLogger::endmsg;
  if (m_isData) {
    m_jetAK4.ConnectVariables(       m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis, (m_jetAK4Name + "_").c_str() );
    m_eventInfo.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters, "" );
  }
  else {
    m_jetAK4.ConnectVariables(       m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis|Ntuple::JetTruth, (m_jetAK4Name + "_").c_str() );
    m_eventInfo.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::EventInfoBasic|Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters|Ntuple::EventInfoTruth, "" );
    m_genParticle.ConnectVariables(  m_recoTreeName.c_str(), Ntuple::GenParticleBasic|Ntuple::GenParticleTauDecayAnalysis, (m_genParticleName + "_").c_str() );
  }
  m_electron.ConnectVariables(     m_recoTreeName.c_str(), Ntuple::ElectronBasic|Ntuple::ElectronID|Ntuple::ElectronAdvancedID|Ntuple::ElectronBoostedIsolation, (m_electronName + "_").c_str() );
  m_muon.ConnectVariables(         m_recoTreeName.c_str(), Ntuple::MuonBasic|Ntuple::MuonID|Ntuple::MuonIsolation|Ntuple::MuonTrack|Ntuple::MuonBoostedIsolation, (m_muonName + "_").c_str() );
  m_tau.ConnectVariables(         m_recoTreeName.c_str(), Ntuple::TauBasic|Ntuple::TauID|Ntuple::TauAdvancedID, (m_tauName + "_").c_str() );

  m_missingEt.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::MissingEtBasic|Ntuple::MissingEtAnalysis|Ntuple::MissingEtCovAnalysis , (m_missingEtName + "_").c_str() );
  m_puppimissingEt.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::MissingEtBasic, (m_missingEtName + "_puppi_").c_str() );
  m_mvamissingEt.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::MissingEtBasic|Ntuple::MissingEtMVAAnalysis|Ntuple::MissingEtCovAnalysis, (m_missingEtName + "_mva_").c_str() );
  
  m_logger << INFO << "Connecting input variables completed" << SLogger::endmsg;

   return;

}

void TauTauAnalysis::ExecuteEvent( const SInputData&, Double_t ) throw( SError ) {

  
  m_logger << VERBOSE << "ExecuteEvent" << SLogger::endmsg;

  b_evt = m_eventInfo.eventNumber;
  b_run = m_eventInfo.runNumber;
  b_lum = m_eventInfo.lumiBlock;
  b_npv = m_eventInfo.PV_N;
  b_isData = (Int_t) m_isData;
  b_weight = 1.;

  //  UZH::GenParticle lhe( &m_lhe, 0);

  //  std::cout << lhe.V_mass() << " " << lhe.V_pt() << " " << lhe.Nj() << std::endl;
  //  std::cout << "event = " << m_eventInfo.eventNumber << " " << m_eventInfo.rho << std::endl;
  //  std::cout << (*m_eventInfo.nPuVtxTrue)[0]  << std::endl;

  b_NUP = m_eventInfo.lheNj;
  b_rho = m_eventInfo.rho;

  if (m_isData) {b_npu = -1;}
  else {b_npu = (*m_eventInfo.actualIntPerXing)[0];}

  // Cut 0: No cuts
  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kBeforeCuts, 1);
  }

  // Cut 1: check for data if run/lumiblock in JSON
  if (m_isData) {
    if(!(isGoodEvent(m_eventInfo.runNumber, m_eventInfo.lumiBlock))) throw SError( SError::SkipEvent );
  }else{
    getEventWeight();
    genFilterZtautau();
  }

  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kJSON, 1);
  }
  
  // Cut 2: pass trigger
//   TString trigger_result = passTrigger();
// 
//  if(trigger_result != "none"){
//    m_logger << VERBOSE << "Trigger pass" << SLogger::endmsg;
//  }else{
//    throw SError( SError::SkipEvent );
//  }




  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kTrigger, 1);
  }


  // Cut 3: pass MET filters
 if (passMETFilters()){
   m_logger << VERBOSE << "passMETFilters" << SLogger::endmsg;
 }else{
   throw SError( SError::SkipEvent );
 }

  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kMetFilters, 1);
  }


  // Cut 4: muon
  std::vector<UZH::Muon> goodMuons;
  
  for( int i = 0; i < m_muon.N; ++i ){
    UZH::Muon mymuon( &m_muon, i );


    if (mymuon.pt() < m_muonPtCut) continue;
    if (fabs(mymuon.eta()) > m_muonEtaCut) continue;
    if (fabs(mymuon.d0_allvertices()) > m_muonD0Cut) continue;
    if (fabs(mymuon.dz_allvertices()) > m_muonDzCut) continue;
    if (mymuon.isMediumMuon() < 0.5) continue;
    //    if (mymuon.SemileptonicPFIso() / mymuon.pt() > m_muonIsoCut) continue;

    goodMuons.push_back(mymuon);
  }



  // Cut 5: electron
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
    //    if (myelectron.SemileptonicPFIso() / myelectron.pt() > m_electronIsoCut) continue;

	  
    goodElectrons.push_back(myelectron);
      
  }



  if(goodMuons.size()!=0){
    fillCutflow("cutflow_mutau", "histogram_mutau", kLepton, 1);
  }else if(goodElectrons.size()!=0){
    fillCutflow("cutflow_eletau", "histogram_eletau", kLepton, 1);
  }else{
    throw SError( SError::SkipEvent );
  }




  // Cut 6: taus
  std::vector<UZH::Tau> goodTaus;
 
  for ( int i = 0; i <   (m_tau.N); ++i ) {
    UZH::Tau mytau( &m_tau, i );
    if(mytau.TauType()!=1) continue;
    if(mytau.pt() < m_tauPtCut) continue;
    if(fabs(mytau.eta()) > m_tauEtaCut) continue;
    if(fabs(mytau.dz()) > m_tauDzCut) continue;
    if(mytau.decayModeFinding() < 0.5) continue;
    if(fabs(mytau.charge()) != 1) continue;

//    if(event_channel=="mutau"){
//      if(mytau.againstMuonTight3() < 0.5) continue;
//      if(mytau.againstElectronVLooseMVA6() < 0.5) continue;
//    }else if(event_channel=="eletau"){
//      if(mytau.againstMuonLoose3() < 0.5) continue;
//      if(mytau.againstElectronTightMVA6() < 0.5) continue;
//    }
//
//    if(mytau.byTightIsolationMVArun2v1DBoldDMwLT() < 0.5) continue;

    goodTaus.push_back(mytau);
  }
  

  if(goodTaus.size()==0) throw SError( SError::SkipEvent );
  
  // Cut 7: Pair selection
  // First, select muon with highest isolation, and then, highest pT

  std::vector<ltau_pair> mutau_pair;

  // For mu-tau
  for(int imuon=0; imuon < (int)goodMuons.size(); imuon++){
    for(int itau=0; itau < (int)goodTaus.size(); itau++){

      if(goodMuons[imuon].tlv().DeltaR(goodTaus[itau].tlv()) < 0.5) continue; 

      // need to include trigger matching here 
      //      if(trigger_result == "ele") continue;

      Float_t mupt = goodMuons[imuon].pt();
      Float_t reliso = goodMuons[imuon].SemileptonicPFIso() / mupt;
      Float_t taupt = goodTaus[itau].pt();
      Float_t tauiso = goodTaus[itau].byIsolationMVArun2v1DBoldDMwLTraw();
      ltau_pair pair = {imuon, reliso, mupt, itau, tauiso, taupt};
      mutau_pair.push_back(pair);
    }
  }

  std::vector<ltau_pair> eletau_pair;

  // For ele-tau
  for(int ielectron=0; ielectron < (int)goodElectrons.size(); ielectron++){
    for(int itau=0; itau < (int)goodTaus.size(); itau++){

      if(goodElectrons[ielectron].tlv().DeltaR(goodTaus[itau].tlv()) < 0.5) continue; 

      // need to include trigger matching here 
      //      if(trigger_result == "mu") continue;


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



  /// This depends on the channel


  UZH::Muon dummyMuon;
  UZH::Electron dummyElectron;

  if(mutau_pair.size()!=0){
    fillCutflow("cutflow_mutau", "histogram_mutau", kLepTau, 1);
    sort(mutau_pair.begin(), mutau_pair.end());


    // selecting mva met
    UZH::MissingEt MvaMet;

    for ( int i = 0; i < (Met.Nmva()); ++i ) {
      UZH::MissingEt myMvaMet( &m_mvamissingEt, i );

      //      std::cout << i << " mt : missing (et, phi) = " << myMvaMet.et() << " " << myMvaMet.phi() << std::endl;
      
      bool flag_lep = false;
      bool flag_tau = false;
      
      
    for(int ipf=0; ipf < (int) myMvaMet.recoil_pt().size(); ipf++){
	Float_t recoil_pt = myMvaMet.recoil_pt().at(ipf);
	Float_t recoil_eta = myMvaMet.recoil_eta().at(ipf);
	Float_t recoil_phi = myMvaMet.recoil_phi().at(ipf);
	Int_t recoil_pdgId = abs(myMvaMet.recoil_pdgId().at(ipf));

	//	std::cout << "\t" << ipf << " recoil pt,eta,phi,M,charge = " << recoil_pt << " " << recoil_eta << " " << recoil_phi << " " << recoil_pdgId << std::endl;

	if(recoil_pt == goodMuons[mutau_pair[0].ilepton].pt() && 
	   recoil_eta == goodMuons[mutau_pair[0].ilepton].eta() && 
	   recoil_phi == goodMuons[mutau_pair[0].ilepton].phi() &&
	   recoil_pdgId == 13
	   ){

	  flag_lep = true;

	}
	
	if(recoil_pt == goodTaus[mutau_pair[0].itau].pt() && 
	   recoil_eta == goodTaus[mutau_pair[0].itau].eta() && 
	   recoil_phi == goodTaus[mutau_pair[0].itau].phi() && 
	   recoil_pdgId == 15
	   ){

	  flag_tau = true;

	}
      }
      
      if(flag_lep==true && flag_tau==true){
	//	std::cout << "====> THIS IS mu-tau MATCHED !!" << std::endl;
//	std::cout << "muon pt,eta,phi = " << goodMuons[mutau_pair[0].ilepton].pt() << " "
//		  << goodMuons[mutau_pair[0].ilepton].eta() << " "
//		  << goodMuons[mutau_pair[0].ilepton].phi() << std::endl;
//	std::cout << "tau pt,eta,phi = " << goodTaus[mutau_pair[0].itau].pt() << " " 
//		  << goodTaus[mutau_pair[0].itau].eta() << " " 
//		  << goodTaus[mutau_pair[0].itau].phi() << std::endl;

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
      if (!myjetak4.IDLoose()) continue;
      
      goodJetsAK4.push_back(myjetak4);
    }

   
    FillBranches( "mutau", goodJetsAK4, goodTaus[mutau_pair[0].itau], goodMuons[mutau_pair[0].ilepton], dummyElectron, Met, PuppiMet, MvaMet);
    mu_tau++;

 }



  if(eletau_pair.size()!=0){
    fillCutflow("cutflow_eletau", "histogram_eletau", kLepTau, 1);
    sort(eletau_pair.begin(), eletau_pair.end());

    UZH::MissingEt MvaMet;


    for ( int i = 0; i < (Met.Nmva()); ++i ) {
      UZH::MissingEt myMvaMet( &m_mvamissingEt, i );
      
      //      std::cout << i << " et : missing (et, phi) = " << myMvaMet.et() << " " << myMvaMet.phi() << std::endl;

      bool flag_lep = false;
      bool flag_tau = false;


      for(int ipf=0; ipf < (int) myMvaMet.recoil_pt().size(); ipf++){
	Float_t recoil_pt = myMvaMet.recoil_pt().at(ipf);
	Float_t recoil_eta = myMvaMet.recoil_eta().at(ipf);
	Float_t recoil_phi = myMvaMet.recoil_phi().at(ipf);
	Int_t recoil_pdgId = abs(myMvaMet.recoil_pdgId().at(ipf));

	//	std::cout << "\t" << ipf << " recoil pt,eta,phi,M,charge = " << recoil_pt << " " << recoil_eta << " " << recoil_phi << " " << recoil_pdgId << std::endl;

	if(recoil_pt == goodElectrons[eletau_pair[0].ilepton].pt() && 
	   recoil_eta == goodElectrons[eletau_pair[0].ilepton].eta() && 
	   recoil_phi == goodElectrons[eletau_pair[0].ilepton].phi() && 
	   recoil_pdgId == 11
	   ){

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
//	std::cout << "====> THIS IS ele-tau MATCHED !!" << std::endl;
//	std::cout << "electron pt,eta,phi = " << goodElectrons[eletau_pair[0].ilepton].pt() << " "
//		  << goodElectrons[eletau_pair[0].ilepton].eta() << " "
//		  << goodElectrons[eletau_pair[0].ilepton].phi() << std::endl;
//	std::cout << "tau pt,eta,phi = " << goodTaus[eletau_pair[0].itau].pt() << " " 
//		  << goodTaus[eletau_pair[0].itau].eta() << " " 
//		  << goodTaus[eletau_pair[0].itau].phi() << std::endl;

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
      if (!myjetak4.IDLoose()) continue;
      
      goodJetsAK4.push_back(myjetak4);
    }

    FillBranches( "eletau", goodJetsAK4, goodTaus[eletau_pair[0].itau], dummyMuon, goodElectrons[eletau_pair[0].ilepton], Met, PuppiMet, MvaMet);
    ele_tau++;



  }


  return;
}
  


bool TauTauAnalysis::isGoodEvent(int runNumber, int lumiSection) {

  //std::cout << "isGoodEvent" << std::endl;
  
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
  
  //std::cout << "TauTauAnalysis" << std::endl;
  
  bool flag_mu_trigger = false;
  bool flag_ele_trigger = false;

  for (std::map<std::string,bool>::iterator it = (m_eventInfo.trigDecision)->begin(); it != (m_eventInfo.trigDecision)->end(); ++it){
    for (unsigned int t = 0; t < m_triggerNames_mutau.size(); ++t ){
      if ((it->first).find(m_triggerNames_mutau[t]) != std::string::npos) {
        if (it->second == true) {
          m_logger << VERBOSE << "Trigger pass: " << (it->first) << SLogger::endmsg;

	  flag_mu_trigger = true;
	  //	  return true;
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
	  //	  return true;
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
  
  //std::cout << "passMETFilters" << std::endl;
  
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
  //std::cout << "getEventWeight" << std::endl;
  
  double weight = 1.;
  for( unsigned int v = 0; v < (m_eventInfo.actualIntPerXing)->size(); ++v ){
    
    if ( (*m_eventInfo.bunchCrossing)[v] == 0 ) {
      b_puweight = m_pileupReweightingTool.getPileUpweight( (*m_eventInfo.actualIntPerXing)[v] );
      m_logger << VERBOSE << "Weight: " << b_puweight << " for true: " << (*m_eventInfo.actualIntPerXing)[v] << SLogger::endmsg;
      //std::cout << "Weight: " << b_weightPU << " for true: " << (*m_eventInfo.actualIntPerXing)[v] <<std::endl;
      break;
    }
  }
  
  
  //TString infile = TString(this->GetHistInputFile()->GetName());
  //std::cout << infile << std::endl;
  //cross_section_weight = getLumiWeight( infile )
  
  b_genweight = (m_eventInfo.genEventWeight < 0) ? -1 : 1; 
  b_weight *= b_puweight*b_genweight;
  
}


void TauTauAnalysis::fillCutflow(TString histName, TString dirName, const Int_t id, const Double_t weight){

  //  std::cout << "\t" << histName << " "<<dirName << " " << id << " " << weight << std::endl;
  //  Hist( histName.c_str(), dirName.c_str() )->Fill( id+1, weight );
  Hist( histName, dirName )->Fill( id+1, weight );
}


//void TauTauAnalysis::FillBranches(const std::string& channel,  const std::vector<UZH::Jet> &Jet, const UZH::Tau& tau, const TLorentzVector& lepton, const UZH::MissingEt& met ){

//void TauTauAnalysis::FillBranches(const std::string& channel,  const std::vector<UZH::Jet> &Jet, const UZH::Tau& tau, const UZH::Muon& lepton, const UZH::MissingEt& met ){

void TauTauAnalysis::FillBranches(const std::string& channel,  const std::vector<UZH::Jet> &Jet, const UZH::Tau& tau, const UZH::Muon& muon, const UZH::Electron& electron,  const UZH::MissingEt& met, const UZH::MissingEt& puppimet, const UZH::MissingEt& mvamet){
  //std::cout << "FillBranches" << std::endl;
  
  b_njetspt20 = Jet.size();

  Int_t njets = 0;
  Int_t nfjets = 0;
  Int_t ncjets = 0;
  Int_t nfbtag = 0;
  Int_t ncbtag = 0;
  Int_t nbtag = 0;
  Int_t ibjet = -1;

  for ( int ijet = 0; ijet < (int)Jet.size(); ++ijet) {

    if(Jet.at(ijet).pt() > 30) njets++;
    if(fabs(Jet.at(ijet).eta()) < 2.4 && Jet.at(ijet).csv() > 0.8) {
      nbtag++;
      if(ibjet < 0) ibjet = ijet;
    }
    if(Jet.at(ijet).pt() > 30 && fabs(Jet.at(ijet).eta()) < 2.4 && Jet.at(ijet).csv() > 0.8) ncbtag++;
    if(Jet.at(ijet).pt() > 30 && fabs(Jet.at(ijet).eta()) > 2.4 && Jet.at(ijet).csv() > 0.8) nfbtag++;
    if(Jet.at(ijet).pt() > 30 && fabs(Jet.at(ijet).eta()) < 2.4) ncjets++;
    if(Jet.at(ijet).pt() > 30 && fabs(Jet.at(ijet).eta()) > 2.4) nfjets++;
  }

  if(b_njetspt20 >= 2){
    b_jpt_1  = Jet.at(0).pt();
    b_jeta_1 = Jet.at(0).eta();
    b_jphi_1 = Jet.at(0).phi();
    b_jpt_2  = Jet.at(1).pt();
    b_jeta_2 = Jet.at(1).eta();
    b_jphi_2 = Jet.at(1).phi();
  }else if(b_njetspt20 == 1){
    b_jpt_1  = Jet.at(0).pt();
    b_jeta_1 = Jet.at(0).eta();
    b_jphi_1 = Jet.at(0).phi();
    b_jpt_2  = -1;
    b_jeta_2 = -9;
    b_jphi_2 = -9;
  }else{
    b_jpt_1  = -1;
    b_jeta_1 = -9;
    b_jphi_1 = -9;
    b_jpt_2  = -1;
    b_jeta_2 = -9;
    b_jphi_2 = -9;
  }
  
  if(ibjet > 0){
    b_bpt_1  = Jet.at(ibjet).pt();
    b_beta_1 = Jet.at(ibjet).eta();
    b_bphi_1 = Jet.at(ibjet).phi();
  }else{
    b_bpt_1  = -1;
    b_beta_1 = -9;
    b_bphi_1 = -9;
  }
  
  b_ncjets = ncjets;
  b_njets = njets;
  b_nfjets = nfjets;
  b_nbtag = nbtag;
  b_ncbtag = ncbtag;
  b_nfbtag = nfbtag;



  // For taus 
  b_pt_2 = tau.tlv().Pt();
  b_eta_2 = tau.tlv().Eta();
  b_phi_2 = tau.tlv().Phi();
  b_m_2 = tau.tlv().M();
  b_q_2 = tau.charge();
  b_d0_2 = tau.d0();
  b_dz_2 = tau.dz();
  b_iso_2 = tau.byTightIsolationMVArun2v1DBoldDMwLT();
  b_againstElectronVLooseMVA6_2 = tau.againstElectronVLooseMVA6();
  b_againstElectronLooseMVA6_2 = tau.againstElectronLooseMVA6();
  b_againstElectronMediumMVA6_2 = tau.againstElectronMediumMVA6();
  b_againstElectronTightMVA6_2 = tau.againstElectronTightMVA6();
  b_againstElectronVTightMVA6_2 = tau.againstElectronVTightMVA6();
  b_againstMuonLoose3_2 = tau.againstMuonLoose3();
  b_againstMuonTight3_2 = tau.againstMuonTight3();
  b_byCombinedIsolationDeltaBetaCorrRaw3Hits_2 = tau.byCombinedIsolationDeltaBetaCorrRaw3Hits();
  b_byIsolationMVA3newDMwLTraw_2 = tau.byIsolationMVArun2v1DBnewDMwLTraw();
  b_byIsolationMVA3oldDMwLTraw_2 = tau.byIsolationMVArun2v1DBoldDMwLTraw();
  b_chargedIsoPtSum_2 = tau.chargedIsoPtSum();
  b_neutralIsoPtSum_2 = tau.neutralIsoPtSum();
  b_puCorrPtSum_2 = tau.puCorrPtSum();
  b_decayModeFindingOldDMs_2 = tau.decayModeFinding();
  if (m_isData) {b_gen_match_2 = -1;}
  else {b_gen_match_2 = genMatch(b_eta_2, b_phi_2);}
  b_decayMode_2 = tau.decayMode();

  TLorentzVector lep_lv;

  if(channel=="mutau"){
    b_pt_1 = muon.tlv().Pt();
    b_eta_1 = muon.tlv().Eta();
    b_phi_1 = muon.tlv().Phi();
    b_m_1 = muon.tlv().M();
    b_q_1 = muon.charge();
    b_d0_1 = muon.d0();
    b_dz_1 = muon.dz();
    b_iso_1 = muon.SemileptonicPFIso() / muon.pt();
    b_id_e_mva_nt_loose_1 = -1;
    lep_lv.SetPtEtaPhiM(b_pt_1, b_eta_1, b_phi_1, b_m_1);
    b_channel = 0; 

    if (!m_isData) b_weightLepID_= m_ScaleFactorTool.get_ScaleFactor_IDMuIchep(lep_lv.Pt(),fabs(lep_lv.Eta()));
    if (!m_isData) b_weightLepIso_= m_ScaleFactorTool.get_ScaleFactor_IsoMuIchep(lep_lv.Pt(),fabs(lep_lv.Eta()));


  }else{
    b_pt_1 = electron.tlv().Pt();
    b_eta_1 = electron.tlv().Eta();
    b_phi_1 = electron.tlv().Phi();
    b_m_1 = electron.tlv().M();
    b_q_1 = electron.charge();
    b_d0_1 = electron.d0();
    b_dz_1 = electron.dz();
    b_iso_1 = electron.SemileptonicPFIso() / electron.pt();
    b_id_e_mva_nt_loose_1 = electron.nonTrigMVA();
    lep_lv.SetPtEtaPhiM(b_pt_1, b_eta_1, b_phi_1, b_m_1);
    b_channel = 1; 

    if (!m_isData) b_weightLepID_= m_ScaleFactorTool.get_ScaleFactor_IDEleIchep(lep_lv.Pt(),fabs(lep_lv.Eta()));
  }

  if (m_isData) {b_gen_match_1 = -1;}
  else {b_gen_match_1 = genMatch(b_eta_1, b_phi_1);}
  b_id_e_mva_nt_loose_1 = -1;
  b_trigweight_1 = 1.;
  b_isoweight_1 = 1.;

  b_met = met.et();
  b_metphi = met.phi();
  b_puppimet = puppimet.et();
  b_puppimetphi = puppimet.phi();
  b_mvamet = mvamet.et();
  b_mvametphi = mvamet.phi();
  b_metcov00 = met.cov00();
  b_metcov01 = met.cov10(); // not typo. This is same for 10
  b_metcov10 = met.cov10();
  b_metcov11 = met.cov11();
  b_mvacov00 = mvamet.cov00();
  b_mvacov01 = mvamet.cov10(); // not typo. This is same for 10
  b_mvacov10 = mvamet.cov10();
  b_mvacov11 = mvamet.cov11();

  b_mt_1 = TMath::Sqrt(2*lep_lv.Pt()*mvamet.et()*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), mvamet.phi()))));
  b_pfmt_1 = TMath::Sqrt(2*lep_lv.Pt()*met.et()*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), met.phi()))));
  b_puppimt_1 = TMath::Sqrt(2*lep_lv.Pt()*puppimet.et()*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), puppimet.phi()))));

  b_mt_2 = TMath::Sqrt(2*b_pt_2*mvamet.et()*(1-TMath::Cos(deltaPhi(b_phi_2, mvamet.phi()))));
  b_pfmt_2 = TMath::Sqrt(2*b_pt_2*met.et()*(1-TMath::Cos(deltaPhi(b_phi_2, met.phi()))));
  b_puppimt_2 = TMath::Sqrt(2*b_pt_2*puppimet.et()*(1-TMath::Cos(deltaPhi(b_phi_2, puppimet.phi()))));


  b_m_vis = (lep_lv + tau.tlv()).M();
  b_dR_ll = tau.tlv().DeltaR(lep_lv);

  b_mt_tot = TMath::Sqrt(TMath::Power(b_mt_1,2) + TMath::Power(b_mt_2,2) + 2*lep_lv.Pt()*b_pt_2*(1-TMath::Cos(deltaPhi(lep_lv.Phi(), b_phi_2))));


  TLorentzVector lmet; 
  lmet.SetPxPyPzE(met.et()*TMath::Cos(met.phi()), met.et()*TMath::Sin(met.phi()), 0, met.et());

//  NSVfitStandalone::Vector measuredMET(met *TMath::Cos(met_phi), met *TMath::Sin(met_phi), 0); 

  b_pt_tt = (lep_lv + tau.tlv() + lmet).Pt();

  
  //  bool doSVfit= false;
  if (m_doSVFit){
    //  if (true){
    std::cout << "mvamet" << std::endl;
    //    TLorentzVector dilepton;
    //    dilepton.SetPtEtaPhiM(0,0,0,0);
    //    dilepton = applySVFitSemileptonic(mvamet.cov00(),mvamet.cov10(),mvamet.cov11(),mvamet.et(),mvamet.phi(),tau.tlv(),lep_lv);  

    b_m_sv = applySVFit(mvamet.cov00(),mvamet.cov10(),mvamet.cov11(),mvamet.et(),mvamet.phi(),lep_lv, tau.tlv(), channel);

    //    b_m_sv = dilepton.M();
    //    b_pt_sv = dilepton.Pt();
    //    b_eta_sv = dilepton.Eta();
    //    b_phi_sv = dilepton.Phi();

    std::cout << "pfmet" << std::endl;
    //    TLorentzVector dilepton_pf;
    //    dilepton_pf.SetPtEtaPhiM(0,0,0,0);

    //    dilepton_pf = applySVFitSemileptonic(met.cov00(),met.cov10(),met.cov11(),met.et(),met.phi(),tau.tlv(),lep_lv);  
    b_m_sv_pfmet = applySVFit(met.cov00(),met.cov10(),met.cov11(),met.et(),met.phi(),lep_lv, tau.tlv(), channel);  

    //    b_m_sv_pfmet = dilepton_pf.M();
  }

  if(channel=="mutau") tree[0]->Fill();
  if(channel=="eletau") tree[1]->Fill();


}



//TLorentzVector TauTauAnalysis::applySVFitSemileptonic(float cov00, float cov10, float cov11,  float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2){
//
//  std::cout << cov00 << " " <<  cov10<< " " <<  cov11 << " " << met << " " << met_phi << " " << lep1.Pt() << " " << lep1.Eta() << " " << lep1.Phi() << " " << lep2.Pt() << " " << lep2.Eta() << " " << lep2.Phi() << std::endl;
//  
//  TLorentzVector   lBoson4;
//  lBoson4.SetPtEtaPhiE(0,0,0,0);
//
//  TMatrixD covMETraw(2,2);
//  covMETraw[0][0]=  cov00;
//  covMETraw[1][0]=  cov10;
//  covMETraw[0][1]=  cov10;
//  covMETraw[1][1]=  cov11;
//
//  float lcov00 =  cov00;
//  float lcov10 =  cov10;
//  float lcov01 =  cov10;
//  float lcov11 =  cov11;
//  
//  
//  TLorentzVector   nullo;
//  nullo.SetPtEtaPhiE(0,0,0,0);
//  if(lcov00*lcov11-lcov01*lcov01 == 0) {
//    std::cout<<"covMat det null "<<std::endl;
//    return nullo;
//  }
//  
//
//  NSVfitStandalone::Vector measuredMET(met *TMath::Cos(met_phi), met *TMath::Sin(met_phi), 0); 
//  // setup measure tau lepton vectors 
//  NSVfitStandalone::LorentzVector l1(lep1.Px(), lep1.Py(), lep1.Pz(), TMath::Sqrt(lep1.M()*lep1.M()+lep1.Px()*lep1.Px()+lep1.Py()*lep1.Py()+lep1.Pz()*lep1.Pz()));
//  NSVfitStandalone::LorentzVector l2(lep2.Px(), lep2.Py(), lep2.Pz(), TMath::Sqrt(lep2.M()*lep2.M()+lep2.Px()*lep2.Px()+lep2.Py()*lep2.Py()+lep2.Pz()*lep2.Pz()));
//  std::vector<NSVfitStandalone::MeasuredTauLepton> measuredTauLeptons;
//  measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kHadDecay, l1));
//  measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kLepDecay, l2));
//
//  // construct the class object from the minimal necesarry information
//  NSVfitStandaloneAlgorithm algo(measuredTauLeptons, measuredMET, covMETraw, 0);
//
//  // apply customized configurations if wanted (examples are given below)
//  algo.addLogM(false);
//
//  // integration by markov chain MC
//  algo.integrateMarkovChain();
//  if(algo.isValidSolution()){
//   
//    lBoson4.SetPtEtaPhiM( algo.pt(), algo.eta(), algo.phi(), algo.getMass());
//  }
//  else{
//    std::cout << "sorry -- status of NLL is not valid [" << algo.isValidSolution() << "]" << std::endl;
//   lBoson4.SetPtEtaPhiM( 0.,0,0,0);
//  }
//  
//  measuredTauLeptons.clear();
//  return   lBoson4 ;
//  
//}




//////////////////
// I HAVE TO WORK FROM HERE TOMORROW !!! 
//////////////////

float TauTauAnalysis::applySVFit(float cov00, float cov10, float cov11,  float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2, const std::string& channel){

  std::cout << "enter SVFit calculation : " << cov00 << " " <<  cov10<< " " <<  cov11 << " " << met << " " << met_phi << " " << lep1.Pt() << " " << lep1.Eta() << " " << lep1.Phi() << " " << lep2.Pt() << " " << lep2.Eta() << " " << lep2.Phi() << std::endl;
  
  //  TLorentzVector   lBoson4;
  //  lBoson4.SetPtEtaPhiE(0,0,0,0);

////  TMatrixD covMET(2,2);
////  covMET[0][0]=  cov00;
////  covMET[1][0]=  cov10;
////  covMET[0][1]=  cov10;
////  covMET[1][1]=  cov11;

//  float lcov00 =  cov00;
//  float lcov10 =  cov10;
//  float lcov01 =  cov10;
//  float lcov11 =  cov11;
  
  
//  TLorentzVector   nullo;
//  nullo.SetPtEtaPhiE(0,0,0,0);
//  if(lcov00*lcov11-lcov01*lcov01 == 0) {
//    std::cout<<"covMat det null "<<std::endl;
//    return nullo;
//  }
  

//  NSVfitStandalone::Vector measuredMET(met *TMath::Cos(met_phi), met *TMath::Sin(met_phi), 0); 
  // setup measure tau lepton vectors 
  //  NSVfitStandalone::LorentzVector l1(lep1.Px(), lep1.Py(), lep1.Pz(), TMath::Sqrt(lep1.M()*lep1.M()+lep1.Px()*lep1.Px()+lep1.Py()*lep1.Py()+lep1.Pz()*lep1.Pz()));
  //  NSVfitStandalone::LorentzVector l2(lep2.Px(), lep2.Py(), lep2.Pz(), TMath::Sqrt(lep2.M()*lep2.M()+lep2.Px()*lep2.Px()+lep2.Py()*lep2.Py()+lep2.Pz()*lep2.Pz()));

////  std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons;
////  //  std::vector<NSVfitStandalone::MeasuredTauLepton> measuredTauLeptons;
////  //  measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kHadDecay, l1));
////  //  measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kLepDecay, l2));
////
////  if(channel=="mutau"){
////    measuredTauLeptons.push_back(svFitStandalone::MeasuredTauLepton(svFitStandalone::kTauToMuDecay, lep1.Pt(), lep1.Eta(), lep1.Phi(), lep1.M())); // tau -> electron decay (Pt, eta, phi, mass)
////  }else if(channel=="eletau"){
////    measuredTauLeptons.push_back(svFitStandalone::MeasuredTauLepton(svFitStandalone::kTauToElecDecay, lep1.Pt(), lep1.Eta(), lep1.Phi(), lep1.M())); // tau -> electron decay (Pt, eta, phi, mass)
////  }
////
////  std::cout << "check1 "<<std::endl;
////
////  measuredTauLeptons.push_back(svFitStandalone::MeasuredTauLepton(svFitStandalone::kTauToHadDecay,  lep2.Pt(), lep2.Eta(), lep2.Phi(), lep2.M(), 0)); 
////
////  std::cout << "check2 "<<std::endl;
////  SVfitStandaloneAlgorithm algo(measuredTauLeptons, met*TMath::Cos(met_phi), met*TMath::Sin(met_phi), covMET, 0);
////
////  std::cout << "check3 "<<std::endl;
////  algo.addLogM(false);  
////
////  std::cout << "check4 "<<std::endl;
////  algo.integrateMarkovChain();
////
////  std::cout << "check5 "<<std::endl;
////
////  float mass = algo.getMass(); // Full SVFit mass - return value is in units of GeV
////  //  float transverse_mass = algo.getTransverseMass(); // Transverse SVFit mass
////
////  std::cout << "check6 "<<std::endl;
////
////  if ( algo.isValidSolution() ) {
////    std::cout << "found mass = " << mass << std::endl;
////  } else {
////    std::cout << "sorry -- status of NLL is not valid [" << algo.isValidSolution() << "]" << std::endl;
////  }

////  return mass;
  return 1;

//  // construct the class object from the minimal necesarry information
//  NSVfitStandaloneAlgorithm algo(measuredTauLeptons, measuredMET, covMET, 0);
//
//  // apply customized configurations if wanted (examples are given below)
//  algo.addLogM(false);
//
//  // integration by markov chain MC
//  algo.integrateMarkovChain();
//  if(algo.isValidSolution()){
//   
//    lBoson4.SetPtEtaPhiM( algo.pt(), algo.eta(), algo.phi(), algo.getMass());
//  }
//  else{
//    std::cout << "sorry -- status of NLL is not valid [" << algo.isValidSolution() << "]" << std::endl;
//   lBoson4.SetPtEtaPhiM( 0.,0,0,0);
//  }
//  
//  measuredTauLeptons.clear();
//  return   lBoson4 ;
  
}






void TauTauAnalysis::genFilterZtautau() {
//   std::cout << "genFilterZtautau" << std::endl;
  
  //  std::vector<UZH::GenParticle> goodGenPart;
  
  for ( int p = 0; p <   (m_genParticle.N) ; ++p ) {
    UZH::GenParticle mygoodGenPart( &m_genParticle, p );

    if( fabs(mygoodGenPart.pdgId()) == 15 ){
      if ( mygoodGenPart.mother()[0]==25){
	// std::cout << " Inside H : mygoodGenPart.pdgId() " <<mygoodGenPart.pdgId() << " mygoodGenPart.mother()[0] " << (mygoodGenPart.mother())[0] << std::endl;
	GenEvent_Htata_filter= true;
      }
      if( mygoodGenPart.mother()[0]==23){
	// std::cout << " Inside Z : mygoodGenPart.pdgId() " <<mygoodGenPart.pdgId() << " mygoodGenPart.mother()[0] " << (mygoodGenPart.mother())[0] << std::endl;
	GenEvent_Ztata_filter= true;
      }
    } 
  }
}



int TauTauAnalysis::genMatch(Float_t lep_eta, Float_t lep_phi) {
//   std::cout << "genMatch" << std::endl;

  Float_t min_dR = 1000;

  UZH::GenParticle closestGen;
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


    // From here, re-calculate tau visible 4 momentum
//    if(pdgId==15){
//      if(isPrompt==0) continue;
//      if(mygoodGenPart.taudecay()!=4) continue;
//      //std::cout << "TAU flag " << " " << isPrompt << " " << isDirectPromptTauDecayProduct << std::endl;
//      
//      TLorentzVector tau;
//      tau.SetPtEtaPhiM(mygoodGenPart.tauvispt(), mygoodGenPart.tauviseta(), mygoodGenPart.tauvisphi(), mygoodGenPart.tauvismass());
//
//      pt = tau.Pt();
//      eta = tau.Pt();
//      phi = tau.Phi();
//    }

    if(! ((pdgId==11 || pdgId==13) && (isPrompt || isDirectPromptTauDecayProduct) && pt > 8)) continue;

//    if(! 
//       ( || ( pdgId==15 && isPrompt && pt > 15))
//       ) continue;
    

    Float_t dr = deltaR(lep_eta - eta, deltaPhi(lep_phi, phi));
    if(dr < min_dR){
      min_dR = dr;
      //      closestGen = mygoodGenPart;

      if( pdgId==11 && isPrompt) id = 1;
      if( pdgId==13 && isPrompt) id = 2;
      if( pdgId==11 && isDirectPromptTauDecayProduct) id = 3;
      if( pdgId==13 && isDirectPromptTauDecayProduct) id = 4;
      
    }
  }



  // check for tau matching
  for ( int p = 0; p <  (int)m_genParticle.tauvispt->size() ; ++p ) {
    float taupt = m_genParticle.tauvispt->at(p);
    float taueta = m_genParticle.tauviseta->at(p);
    float tauphi = m_genParticle.tauvisphi->at(p);
    int taudecay = m_genParticle.taudecay->at(p);
    
    if(taupt < 15) continue;
    if(taudecay != 4) continue;
    
    Float_t dr = deltaR(lep_eta - taueta, deltaPhi(lep_phi, tauphi));
    if(dr < min_dR){
      min_dR = dr;
      
      id = 5;
      
    }
  }


  return id;

}



Float_t TauTauAnalysis::deltaPhi(Float_t p1, Float_t p2){

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
  
  return TMath::Sqrt(TMath::Power(deta,2) + TMath::Power(dphi,2));

}
