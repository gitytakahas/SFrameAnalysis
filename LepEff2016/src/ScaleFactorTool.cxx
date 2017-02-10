#include "../interface/ScaleFactorTool.h"
#include <cstdlib>
#include <limits>
#include <TFile.h>



ScaleFactorTool::ScaleFactorTool(SCycleBase* parent, const char* name ):
 SToolBase( parent ), m_name( name ) 
{
  SetLogName( name );
  DeclareProperty( m_name+"Mu_TrigFile ",   m_Mu_TrigFile       = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/Run2016BtoH/Muon_IsoMu24_OR_TkIsoMu24_2016BtoH_eff.root" ); 
  DeclareProperty( m_name+"Mu_IdIsoFil",    m_Mu_IdIsoFile      = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p15_2016BtoH_eff.root" );
  //  DeclareProperty( m_name+"Mu_TrigFile ",   m_Mu_TrigFile       = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/Run2016BCD/Muon_IsoMu22_OR_TkIsoMu22_eff.root" ); 
  //  DeclareProperty( m_name+"Mu_IdIsoFil",    m_Mu_IdIsoFile      = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/Run2016BCD/Muon_IdIso0p15_eff.root" );
  //DeclareProperty( m_name+"Mu_IdFile",      m_Mu_IdFile         = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/MuonIso_Z_RunBCD_prompt80X_7p65.root" );
  //DeclareProperty( m_name+"Mu_IsoFile",     m_Mu_IsoFile        = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/MuonIso_Z_RunBCD_prompt80X_7p65.root" );
  DeclareProperty( m_name+"EleTrigFile",    m_Ele_TrigFile      = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Electron/Run2016BtoH/Electron_Ele25_eta2p1_WPTight_eff.root" ); //Electron_Ele25eta2p1WPTight_eff.root
  DeclareProperty( m_name+"EleIdIsoName",   m_Ele_IdIsoFile     = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p1_eff.root" );
  //DeclareProperty( m_name+"Ele_IdFile",     m_Ele_IdFile        = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Electron/egammaEffi_txt_SF2D.root" );
  //DeclareProperty( m_name+"Ele_IsoFile",    m_Ele_IsoFile       = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Electron/egammaEffi_txt_SF2D.root" );
}



void ScaleFactorTool::BeginInputData( const SInputData& ) throw( SError ) {

  m_logger << INFO << "Initializing ScaleFactor for lepons" << SLogger::endmsg;
  m_logger << INFO << "Efficiency file Mu Trig: "   << m_Mu_TrigFile    << SLogger::endmsg;
  m_logger << INFO << "Efficiency file Mu IdIso: "  << m_Mu_IdIsoFile   << SLogger::endmsg;
  //m_logger << INFO << "Efficiency file Mu Id: "     << m_Mu_IdFile      << SLogger::endmsg;
  //m_logger << INFO << "Efficiency file Mu Iso: "    << m_Mu_IsoFile     << SLogger::endmsg;
  m_logger << INFO << "Efficiency file Ele Trig: "  << m_Ele_TrigFile   << SLogger::endmsg;
  m_logger << INFO << "Efficiency file Ele IdIso: " << m_Ele_IdIsoFile  << SLogger::endmsg;
  //m_logger << INFO << "Efficiency file Ele Id: "    << m_Ele_IdFile     << SLogger::endmsg;
  //m_logger << INFO << "Efficiency file Ele Iso: "   << m_Ele_IsoFile    << SLogger::endmsg;

  m_ScaleFactor_MuTrig  = new ScaleFactor( m_Mu_TrigFile );
  m_logger << INFO << "Scale factor Mu Trig initialised" << SLogger:: endmsg;

  m_ScaleFactor_MuIdIso = new ScaleFactor( m_Mu_IdIsoFile );
  m_logger << INFO << "Scale factor Mu IdIsp initialised" << SLogger:: endmsg;

  //m_ScaleFactor_MuId    = new ScaleFactor( m_Mu_IdFile );
  //m_logger << INFO << "Scale factor Mu Id initialised" << SLogger:: endmsg;
  
  //m_ScaleFactor_MuIso   = new ScaleFactor( m_Mu_IsoFile );
  //m_logger << INFO << "Scale factor Mu Iso initialised" << SLogger:: endmsg;

  m_ScaleFactor_EleTrig   = new ScaleFactor( m_Ele_TrigFile );
  m_logger << INFO << "Scale factor Ele Id initialised" << SLogger:: endmsg;

  m_ScaleFactor_EleIdIso = new ScaleFactor( m_Ele_IdIsoFile );
  m_logger << INFO << "Scale factor Ele IdIso initialised" << SLogger:: endmsg;

  //m_ScaleFactor_EleId   = new ScaleFactor( m_Ele_IdFile );
  //m_logger << INFO << "Scale factor Ele Id initialised" << SLogger:: endmsg;
  
  //m_ScaleFactor_EleIso    = new ScaleFactor( m_Ele_IsoFile );
  //m_logger << INFO << "Scale factor Ele Iso initialised" << SLogger:: endmsg;
  
  return;
}



ScaleFactorTool::~ScaleFactorTool(){
  //delete  eff_mc[etaLabel]; delete eff_data[etaLabel]
}



double ScaleFactorTool::get_Efficiency_MuTrig(double pt, double eta){
    return m_ScaleFactor_MuTrig->get_EfficiencyData(pt,eta);
}



double ScaleFactorTool::get_ScaleFactor_MuId(double pt, double eta){
    return m_ScaleFactor_MuId->get_ScaleFactor(pt,eta);
}



double ScaleFactorTool::get_ScaleFactor_MuIdIso(double pt, double eta){
    return m_ScaleFactor_MuIdIso->get_ScaleFactor(pt,eta);
}



double ScaleFactorTool::get_Efficiency_EleTrig(double pt, double eta){
    return m_ScaleFactor_EleTrig->get_EfficiencyData(pt,eta);
}



double ScaleFactorTool::get_ScaleFactor_EleId(double pt, double eta){
    return m_ScaleFactor_EleId->get_ScaleFactor(pt,eta);
}



double ScaleFactorTool::get_ScaleFactor_EleIdIso(double pt, double eta){
    return m_ScaleFactor_EleIdIso->get_ScaleFactor(pt,eta);
}





