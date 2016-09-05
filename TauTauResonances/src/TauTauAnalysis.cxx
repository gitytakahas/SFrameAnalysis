// $Id: CycleCreators.py 344 2012-12-13 13:10:53Z krasznaa $

// Local include(s):
#include "../include/TauTauAnalysis.h"
// External include(s):
#include "../GoodRunsLists/include/TGoodRunsListReader.h"

//#include <TMath.h>

ClassImp( TauTauAnalysis );


// define cut names

const std::string TauTauAnalysis::kCutName[ TauTauAnalysis::kNumCuts ] = {
  "BeforeCuts",            // C0
  "JSON",                  // C1
  "Trigger",               // C2
  "MetFilters",            // C3
  "Lepton",                // C4
  "LepTau",              // C6
};

TauTauAnalysis::TauTauAnalysis()
   : SCycleBase()
   , m_jetAK4( this )
   , m_eventInfo( this )
   , m_electron( this )
   , m_muon( this )
   , m_tau( this )
   , m_missingEt( this )
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
   DeclareProperty( "IsSignal",                 m_isSignal                 = false );
   
   DeclareProperty( "AK4JetPtCut",              m_AK4jetPtCut           = 20.);
   DeclareProperty( "AK4JetEtaCut",             m_AK4jetEtaCut          = 4.7);

   DeclareProperty( "ElectronPtCut",                 m_electronPtCut              = 26. );
   DeclareProperty( "ElectronEtaCut",                m_electronEtaCut             = 2.1 );
   DeclareProperty( "ElectronD0Cut",                m_electronD0Cut             = 0.045 );
   DeclareProperty( "ElectronDzCut",                m_electronDzCut             = 0.2 );
   DeclareProperty( "ElectronIsoCut",                m_electronIsoCut             = 0.1 );
   
   DeclareProperty( "MuonPtCut",                 m_muonPtCut              = 20. );
   DeclareProperty( "MuonEtaCut",                m_muonEtaCut             = 2.1 );
   DeclareProperty( "MuonD0Cut",                m_muonD0Cut             = 0.045 );
   DeclareProperty( "MuonDzCut",                m_muonDzCut             = 0.2 );
   DeclareProperty( "MuonIsoCut",                m_muonIsoCut             = 0.15 );

   DeclareProperty( "TauPtCut",                 m_tauPtCut           = 30 );
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
  //  m_triggerNames_eletau.clear();
	
  // muon triggers
  m_triggerNames_mutau.push_back("HLT_IsoMu18_v");
  m_triggerNames_mutau.push_back("HLT_IsoMu20_v4");
  m_triggerNames_mutau.push_back("HLT_IsoMu22_v3");
  m_triggerNames_mutau.push_back("HLT_IsoMu22_eta2p1_v2");
  m_triggerNames_mutau.push_back("HLT_IsoMu24_v2");
  m_triggerNames_mutau.push_back("HLT_IsoMu27_v4");
  m_triggerNames_mutau.push_back("HLT_IsoTkMu18_v3");
  m_triggerNames_mutau.push_back("HLT_IsoTkMu20_v5");
  m_triggerNames_mutau.push_back("HLT_IsoTkMu22_eta2p1_v2");
  m_triggerNames_mutau.push_back("HLT_IsoTkMu22_v3");
  m_triggerNames_mutau.push_back("HLT_IsoTkMu24_v2");
  m_triggerNames_mutau.push_back("HLT_IsoTkMu27_v4");
  m_triggerNames_mutau.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v5");
  m_triggerNames_mutau.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v5");
  m_triggerNames_mutau.push_back("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2");
  m_triggerNames_mutau.push_back("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2");
  m_triggerNames_mutau.push_back("HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v2");

  // electron triggers
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

    tree[channel]->Branch("weight", &b_weight_, "weight/F");
    tree[channel]->Branch("weightGen", &b_weightGen_, "weightGen/F");
    tree[channel]->Branch("puweight", &b_weightPU_, "puweight/F");

    tree[channel]->Branch("run", &b_runNumber_, "run/I");
    tree[channel]->Branch("evt", &b_eventNumber_, "evt/I");
    tree[channel]->Branch("lumi", &b_lumiBlock_, "lumi/I");
    tree[channel]->Branch("is_data", &b_isData_, "is_data/I");
    tree[channel]->Branch("npu", &b_npu_, "npu/I");
    
    tree[channel]->Branch("tau_pt", &b_tau_pt_, "tau_pt/F");
    tree[channel]->Branch("tau_eta", &b_tau_eta_, "tau_eta/F");
    tree[channel]->Branch("tau_phi", &b_tau_phi_, "tau_phi/F");
    tree[channel]->Branch("tau_iso", &b_tau_iso_, "tau_iso/I");
    tree[channel]->Branch("tau_iso_raw", &b_tau_iso_raw_, "tau_iso_raw/F");
    tree[channel]->Branch("tau_againstEle", &b_tau_againstEle_, "tau_againstEle/I");
    tree[channel]->Branch("tau_againstMu", &b_tau_againstMu_, "tau_againstMu/I");
    
    tree[channel]->Branch("l2_pt", &b_l2_pt_, "l2_pt/F");
    tree[channel]->Branch("l2_eta", &b_l2_eta_, "l2_eta/F");
    tree[channel]->Branch("l2_phi", &b_l2_phi_, "l2_phi/F");
    tree[channel]->Branch("met", &b_met_, "met/F");
    tree[channel]->Branch("met_phi", &b_met_phi_, "met_phi/F");
    tree[channel]->Branch("m_vis", &b_vis_mass_ll_, "m_vis/F");
    tree[channel]->Branch("dR_ll", &b_dR_ll_, "dR_ll/F");
    tree[channel]->Branch("n_jets", &b_njets_, "n_jets/I");
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
    //    m_eventInfo.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters, "" );
    m_eventInfo.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::EventInfoMETFilters, "" );
  }
  else {
    m_jetAK4.ConnectVariables(       m_recoTreeName.c_str(), Ntuple::JetBasic|Ntuple::JetAnalysis|Ntuple::JetTruth, (m_jetAK4Name + "_").c_str() );
    //    m_eventInfo.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::EventInfoBasic|Ntuple::EventInfoTrigger|Ntuple::EventInfoMETFilters|Ntuple::EventInfoTruth, "" );
    m_eventInfo.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::EventInfoBasic|Ntuple::EventInfoMETFilters|Ntuple::EventInfoTruth, "" );
    m_genParticle.ConnectVariables(  m_recoTreeName.c_str(), Ntuple::GenParticleBasic, (m_genParticleName + "_").c_str() );
  }
  m_electron.ConnectVariables(     m_recoTreeName.c_str(), Ntuple::ElectronBasic|Ntuple::ElectronID|Ntuple::ElectronAdvancedID|Ntuple::ElectronBoostedIsolation, (m_electronName + "_").c_str() );
  m_muon.ConnectVariables(         m_recoTreeName.c_str(), Ntuple::MuonBasic|Ntuple::MuonID|Ntuple::MuonIsolation|Ntuple::MuonTrack|Ntuple::MuonBoostedIsolation, (m_muonName + "_").c_str() );
  m_tau.ConnectVariables(         m_recoTreeName.c_str(), Ntuple::TauBasic|Ntuple::TauID|Ntuple::TauAdvancedID, (m_tauName + "_").c_str() );

  m_missingEt.ConnectVariables(    m_recoTreeName.c_str(), Ntuple::MissingEtBasic|Ntuple::MissingEtAnalysis , (m_missingEtName + "_").c_str() );
  
  m_logger << INFO << "Connecting input variables completed" << SLogger::endmsg;

   return;

}

void TauTauAnalysis::ExecuteEvent( const SInputData&, Double_t ) throw( SError ) {

  m_logger << VERBOSE << "ExecuteEvent" << SLogger::endmsg;

  b_eventNumber_ = m_eventInfo.eventNumber;
  b_runNumber_ = m_eventInfo.runNumber;
  b_lumiBlock_ = m_eventInfo.lumiBlock;
  b_npu_ = m_eventInfo.PV_N;

  // Cut 0: No cuts
  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kBeforeCuts, 1);
  }

  
  
  // Cut 1: check for data if run/lumiblock in JSON
  if (m_isData) {
    if(!(isGoodEvent(m_eventInfo.runNumber, m_eventInfo.lumiBlock))) throw SError( SError::SkipEvent );
  }else{
    b_weight_ = getEventWeight();
    genFilterZtautau();
  }


  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kJSON, 1);
  }
  

  // Cut 2: pass trigger
//  if(passTrigger()){
//    m_logger << VERBOSE << "Trigger pass" << SLogger::endmsg;
//  }else{
//    throw SError( SError::SkipEvent );
//  }



  for (auto ch: channels_){
    fillCutflow("cutflow_" + ch, "histogram_" + ch, kTrigger, 1);
  }


  // Cut 3: pass MET filters
//  if (passMETFilters()){
//    m_logger << VERBOSE << "passMETFilters" << SLogger::endmsg;
//  }else{
//    throw SError( SError::SkipEvent );
//  }

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

    //    std::cout << "electron nonTrigMVA = "<< myelectron.nonTrigMVA() << std::endl;

    if(     b_eventNumber_ == 1027000){


      std::cout << "electron pT = "<< myelectron.pt() << std::endl;
      std::cout << "electron eta = "<< myelectron.eta() << std::endl;
      std::cout << "electron d0 = "<< myelectron.d0() << std::endl;
      std::cout << "electron dz = "<< myelectron.dz() << std::endl;
      std::cout << "electron passConvVeto = "<< myelectron.passConversionVeto() << std::endl;
      std::cout << "electron expMissingHits = "<< myelectron.expectedMissingInnerHits() << std::endl;
      std::cout << "electron nonTrigMVAID = "<< myelectron.nonTrigMVAID() << std::endl;
      std::cout << "electron nonTrigMVA = "<< myelectron.nonTrigMVA() << std::endl;
    }

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

  if(     b_eventNumber_ == 102700)
    std::cout << b_eventNumber_ << " check 2" << std::endl;



  if(goodMuons.size()!=0){
    fillCutflow("cutflow_mutau", "histogram_mutau", kLepton, 1);
  }else if(goodElectrons.size()!=0){
    fillCutflow("cutflow_eletau", "histogram_eletau", kLepton, 1);
  }else{
    throw SError( SError::SkipEvent );
  }


  if(     b_eventNumber_ == 102700)
    std::cout << b_eventNumber_ << " check 3" << std::endl;



  // Make sure that there is no events with good muon and good electron at the same time

//  TString event_type = "none";
//
//  if(goodMuons.size()==1 && goodElectrons.size()==0){
//    event_type = "mutau";
//  }else if(goodMuons.size()==0 && goodElectrons.size()==1){
//    event_type = "eletau";
//  }else{
//    throw SError( SError::SkipEvent );
//  }

  

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


  if(     b_eventNumber_ == 102700)
    std::cout << b_eventNumber_ << " check 4" << std::endl;


  //  if(goodTaus.size()!=1) throw SError( SError::SkipEvent );



  UZH::MissingEt goodMet( &m_missingEt, 0 );

  std::vector<UZH::Jet> goodJetsAK4;
  
  for ( int i = 0; i < (m_jetAK4.N); ++i ) {
    UZH::Jet myjetak4( &m_jetAK4, i );
    if (fabs(myjetak4.eta()) > m_AK4jetEtaCut) continue;
    if (myjetak4.pt() < m_AK4jetPtCut) continue;
    if (myjetak4.IDTight()) goodJetsAK4.push_back(myjetak4);

    goodJetsAK4.push_back(myjetak4);
  }

  
  // Cut 7: Pair selection
  // First, select muon with highest isolation, and then, highest pT

//  int iGood_muon = 0;
//  
//  if(goodMuons.size()>1){
//    Float_t min_iso = 100000;
//
//    for(int imuon=0; imuon < goodMuons.size(); imuon++){
//      Float_t reliso = goodMuons[imuon].SemileptonicPFIso() / goodMuons[imuon].pt();
//      if(min_iso > reliso) min_iso = reliso;
//    }
//
//    Float_t max_pt =　0;
//
//    for(int imuon=0; imuon < goodMuons.size(); imuon++){
//      Float_t reliso = goodMuons[imuon].SemileptonicPFIso() / mpt; 
//      if(reliso == min_iso){
//	if(max_pt < goodMuons[imuon].pt()){
//	  max_pt = goodMuons[imuon].pt();
//	  iGood_muon = imuon;
//	}
//      }
//    }
//  }
//
//  std::cout << "Muon choice : " << iGood_muon << std::endl;

  std::vector<ltau_pair> mutau_pair;

  // For mu-tau
  for(int imuon=0; imuon < (int)goodMuons.size(); imuon++){
    for(int itau=0; itau < (int)goodTaus.size(); itau++){
      if(goodMuons[imuon].tlv().DeltaR(goodTaus[itau].tlv()) < 0.5) continue; 

      // need to include trigger matching here 

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

      if(     b_eventNumber_ == 102700){

	std::cout << "(ielectron, itau, dR) = " << ielectron << " " << itau << " e pT, eta, phi = " << goodElectrons[ielectron].pt() << " " << goodElectrons[ielectron].eta() << " " << goodElectrons[ielectron].phi() << " tau pT, eta, phi = " << goodTaus[itau].pt() << " " << goodTaus[itau].eta() << " " << goodTaus[itau].phi() << " dR = " << goodElectrons[ielectron].tlv().DeltaR(goodTaus[itau].tlv()) << std::endl;
      }

      if(goodElectrons[ielectron].tlv().DeltaR(goodTaus[itau].tlv()) < 0.5) continue; 

      // need to include trigger matching here 



      Float_t elept = goodElectrons[ielectron].pt();
      Float_t reliso = goodElectrons[ielectron].SemileptonicPFIso() / elept;
      Float_t taupt = goodTaus[itau].pt();
      Float_t tauiso = goodTaus[itau].byIsolationMVArun2v1DBoldDMwLTraw();
      ltau_pair pair = {ielectron, reliso, elept, itau, tauiso, taupt};
      eletau_pair.push_back(pair);
    }
  }


  if(     b_eventNumber_ == 102700){
    std::cout << b_eventNumber_ << " check 5 " << mutau_pair.size() << " " << eletau_pair.size()  << std::endl;
  }


  if(mutau_pair.size()==0 && eletau_pair.size()==0){
    throw SError( SError::SkipEvent );
  }

  if(mutau_pair.size()!=0){
    fillCutflow("cutflow_mutau", "histogram_mutau", kLepTau, 1);
    sort(mutau_pair.begin(), mutau_pair.end());

    FillBranches( "mutau", goodJetsAK4, goodTaus[mutau_pair[0].itau], goodMuons[mutau_pair[0].ilepton].tlv(), goodMet);
    mu_tau++;


  }
  if(eletau_pair.size()!=0){
    fillCutflow("cutflow_eletau", "histogram_eletau", kLepTau, 1);
    sort(eletau_pair.begin(), eletau_pair.end());

    FillBranches( "eletau", goodJetsAK4, goodTaus[eletau_pair[0].itau], goodElectrons[eletau_pair[0].ilepton].tlv(), goodMet);
    ele_tau++;

  }



//  for (int i = 0; i < (int)mutau_pair.size(); i++){
//
//    std::cout << "\t imuon = " <<  mutau_pair[i].imuon 
//	      << " muon pT = " << mutau_pair[i].lep_pt 
//	      << " muon iso = " << mutau_pair[i].lep_iso 
//	      << " itau = " << mutau_pair[i].itau 
//	      << " tau pT = " << mutau_pair[i].tau_pt 
//	      << " tau iso = " << mutau_pair[i].tau_iso << std::endl;
//  }










  return;
}
  


bool TauTauAnalysis::isGoodEvent(int runNumber, int lumiSection) {
  
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



bool TauTauAnalysis::passTrigger() {
  
  for (std::map<std::string,bool>::iterator it = (m_eventInfo.trigDecision)->begin(); it != (m_eventInfo.trigDecision)->end(); ++it){
    for (unsigned int t = 0; t < m_triggerNames_mutau.size(); ++t ){
      if ((it->first).find(m_triggerNames_mutau[t]) != std::string::npos) {
        if (it->second == true) {
          m_logger << VERBOSE << "Trigger pass: " << (it->first) << SLogger::endmsg;
	  return true;
        }
      }
    }
  }
  
  return false;
  
}


bool TauTauAnalysis::passMETFilters() {
  
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


double TauTauAnalysis::getEventWeight() {
  
  double weight = 1.;
  for( unsigned int v = 0; v < (m_eventInfo.actualIntPerXing)->size(); ++v ){
    
    if ( (*m_eventInfo.bunchCrossing)[v] == 0 ) {
      b_weightPU_ = m_pileupReweightingTool.getPileUpweight( (*m_eventInfo.actualIntPerXing)[v] );
      m_logger << VERBOSE << "Weight: " << b_weightPU_ << " for true: " << (*m_eventInfo.actualIntPerXing)[v] << SLogger::endmsg;
      //std::cout << "Weight: " << b_weightPU << " for true: " << (*m_eventInfo.actualIntPerXing)[v] <<std::endl;
      break;
    }
  }
  b_weightGen_ = (m_eventInfo.genEventWeight < 0) ? -1 : 1; 
  weight *= b_weightPU_*b_weightGen_;
  
  return weight;
  
}


void TauTauAnalysis::fillCutflow(TString histName, TString dirName, const Int_t id, const Double_t weight){

  //  std::cout << "\t" << histName << " "<<dirName << " " << id << " " << weight << std::endl;
  //  Hist( histName.c_str(), dirName.c_str() )->Fill( id+1, weight );
  Hist( histName, dirName )->Fill( id+1, weight );
}


void TauTauAnalysis::FillBranches(const std::string& channel,  const std::vector<UZH::Jet> &Jet, const UZH::Tau& tau, const TLorentzVector& lepton, const UZH::MissingEt& met ){

  b_isData_ = (Int_t) m_isData;
  
  b_tau_pt_=tau.tlv().Pt();
  b_tau_eta_=tau.tlv().Eta();
  b_tau_phi_=tau.tlv().Phi();
  b_tau_iso_raw_ = tau.byIsolationMVArun2v1PWnewDMwLTraw();
  b_tau_iso_ = tau.byVLooseIsolationMVArun2v1PWnewDMwLT();
  b_tau_againstEle_=tau.againstElectronVLooseMVA6();
  b_tau_againstMu_=tau.againstMuonLoose3();

  b_l2_pt_=lepton.Pt();
  b_l2_eta_=lepton.Eta();// FIX 
  b_l2_phi_=lepton.Phi();// FIX 
  
  b_vis_mass_ll_=(lepton +tau.tlv()).M();
  b_dR_ll_= lepton.DeltaR(tau.tlv());

  b_met_ =met.et();
  b_met_phi_ =met.phi();
  b_njets_ = Jet.size();

  if (channel=="mutau") { 
    b_ChannelInt_ = 0; 
    if (!m_isData) {
      
      b_weightLepID_= m_ScaleFactorTool.get_ScaleFactor_IDMuIchep(lepton.Pt(),fabs(lepton.Eta()));
      b_weightLepIso_= m_ScaleFactorTool.get_ScaleFactor_IsoMuIchep(lepton.Pt(),fabs(lepton.Eta()));
    
    }
  }
  if (channel=="eletau")  {   
    b_ChannelInt_ = 1;
    
    if (!m_isData) {  
      b_weightLepID_= m_ScaleFactorTool.get_ScaleFactor_IDEleIchep(lepton.Pt(),fabs(lepton.Eta()));
    }
  }


    
  
  bool doSVfit= false;
  if (doSVfit){
    TLorentzVector H_ll;
    H_ll.SetPtEtaPhiM(0,0,0,0);
  
    H_ll=applySVFitSemileptonic(met.cov00(),met.cov10(),met.cov11(),met.et(),met.phi(),tau.tlv(),lepton);

    b_H_Mass_SVFit_=H_ll.M();
    b_H_Pt_SVFit_=H_ll.Pt();
    b_H_Eta_SVFit_=H_ll.Eta();
    b_H_Phi_SVFit_=H_ll.Phi();
  }

  if (!m_isData){
  
    b_GenEvent_Htata_ = GenEvent_Htata_filter ;
    b_GenEvent_Ztata_ = GenEvent_Ztata_filter ;
   }


  if(channel=="mutau") tree[0]->Fill();
  if(channel=="eletau") tree[1]->Fill();


}



TLorentzVector TauTauAnalysis::applySVFitSemileptonic(float cov00, float cov10, float cov11,  float met, float met_phi, TLorentzVector lep1 , TLorentzVector lep2){
  // std::cout<<"inside applySVFitSemileptonic "<<std::endl;
  
  TLorentzVector   lBoson4;
  lBoson4.SetPtEtaPhiE(0,0,0,0);

  TMatrixD covMETraw(2,2);
  covMETraw[0][0]=  cov00;
  covMETraw[1][0]=  cov10;
  covMETraw[0][1]=  cov10;
  covMETraw[1][1]=  cov11;

  float lcov00 =  cov00;
  float lcov10 =  cov10;
  float lcov01 =  cov10;
  float lcov11 =  cov11;
  
  
  TLorentzVector   nullo;
  nullo.SetPtEtaPhiE(0,0,0,0);
  if(lcov00*lcov11-lcov01*lcov01 == 0) {
    std::cout<<"covMat det null "<<std::endl;
    return nullo;
  }
  

  NSVfitStandalone::Vector measuredMET(met *TMath::Cos(met_phi), met *TMath::Sin(met_phi), 0); 
  // setup measure tau lepton vectors 
  NSVfitStandalone::LorentzVector l1(lep1.Px(), lep1.Py(), lep1.Pz(), TMath::Sqrt(lep1.M()*lep1.M()+lep1.Px()*lep1.Px()+lep1.Py()*lep1.Py()+lep1.Pz()*lep1.Pz()));
  NSVfitStandalone::LorentzVector l2(lep2.Px(), lep2.Py(), lep2.Pz(), TMath::Sqrt(lep2.M()*lep2.M()+lep2.Px()*lep2.Px()+lep2.Py()*lep2.Py()+lep2.Pz()*lep2.Pz()));
  std::vector<NSVfitStandalone::MeasuredTauLepton> measuredTauLeptons;
  measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kHadDecay, l1));
  measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kLepDecay, l2));

  // construct the class object from the minimal necesarry information
  NSVfitStandaloneAlgorithm algo(measuredTauLeptons, measuredMET, covMETraw, 0);

  // apply customized configurations if wanted (examples are given below)
  algo.addLogM(false);

  // integration by markov chain MC
  algo.integrateMarkovChain();
  if(algo.isValidSolution()){
   
    lBoson4.SetPtEtaPhiM( algo.pt(), algo.eta(), algo.phi(), algo.getMass());
  }
  else{
    std::cout << "sorry -- status of NLL is not valid [" << algo.isValidSolution() << "]" << std::endl;
   lBoson4.SetPtEtaPhiM( 0.,0,0,0);
  }
  
  measuredTauLeptons.clear();
  return   lBoson4 ;
  
}


void TauTauAnalysis::genFilterZtautau() {
  
  std::vector<UZH::GenParticle> goodGenPart;
  
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
