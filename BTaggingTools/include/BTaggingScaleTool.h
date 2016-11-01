#ifndef __BTAGGINGSCALETOOL_H__
#define __BTAGGINGSCALETOOL_H__

// SFrame include(s):
#include "core/include/SError.h"
#include "plug-ins/include/SToolBase.h"

#include <TH2.h>

#include "../NtupleVariables/include/Jet.h"

#include "../include/BTagCalibrationStandalone.h"

class BTaggingScaleTool : public SToolBase {
  
  //
  // Follow examples in https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagCalibration
  // 
  //
  
 public:
  /// constructor
  BTaggingScaleTool( SCycleBase* parent, const char* name = "BTaggingScaleTool" );

  /// destructor
  ~BTaggingScaleTool();

  /// function booking histograms
  void BeginInputData( const SInputData& id ) throw( SError );
  
  double getScaleFactor( const double& pt, const double& eta, const int& flavour, bool isTagged, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory = "jet" );

  double getScaleFactor( const UZH::Jet& jet, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory = "jet");
  
  double getSoftdropSubjetScaleFactor( const UZH::Jet& jet, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory = "subjet_softdrop" );

  double getScaleFactor( const UZH::JetVec& vJets, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory = "jet" );
  
  double getSoftdropSubjetScaleFactor( const UZH::JetVec& vJets, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory = "subjet_softdrop" );
 
  /// function for veto
  double getScaleFactor_veto( const double& pt, const double& eta, const int& flavour, bool isTagged, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory_veto = "jet_ak4" );

  double getScaleFactor_veto( const UZH::Jet& jet, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory_veto = "jet_ak4");

  double getScaleFactor_veto( const UZH::JetVec& vJets, const double& sigma_bc = 0., const double& sigma_udsg = 0., const TString& jetCategory_veto = "jet_ak4" );
  


  /// function to book histograms for efficiencies
  void bookHistograms();
  
  /// function to fill jet b-tagging efficiencies
  void fillEfficiencies( const UZH::JetVec& vJets );
 
  /// function to fill jet b-tagging efficiencies for veto
  void fillEfficiencies_veto( const UZH::JetVec& vJets );
  
  /// function to fill subjet b-tagging efficiencies
  void fillSoftdropSubjetEfficiencies( const UZH::JetVec& vJets );
  
  /// function to read in b-tagging efficiencies
  void readEfficiencies();
  
  /// function to return b-tagging efficiency for individual jet
  double getEfficiency( const double& pt, const double& eta, const int& flavour, const TString& jetCategory = "jet" );
  
  /// function to convert flavor integer to TString
  TString flavourToString( const int& flavour );
  
  /// helper function to check if jet is b-tagged
  bool isTagged( const UZH::Jet& jet );
  
  /// helper function to check if jet is b-tagged passing CSV value directly
  bool isTagged( const double& csv );
  
  /// helper function to check if jet is b-tagged for veto
  bool isTagged_veto( const UZH::Jet& jet );
  
  /// helper function to check if jet is b-tagged passing CSV value directly for veto
  bool isTagged_veto( const double& csv );
  

 private:

  std::string m_name;                 ///< name of the tool
  std::string m_tagger;
  std::string m_tagger_veto ;
  std::string m_workingPoint;
  std::string m_workingPoint_veto;
  std::string m_csvFile;
  std::string m_csvFile_veto;
  std::string m_measurementType_udsg;
  std::string m_measurementType_bc;
  std::string Clemens;
  std::string m_measurementType_veto_udsg;
  std::string m_measurementType_veto_bc;
  std::string m_effHistDirectory;
  std::string m_effFile;
  std::string m_effFile_veto;
  std::vector<TString> m_jetCategories;
  std::vector<TString> m_jetCategories_veto;
  std::vector<TString> m_flavours;
  
  std::map<std::string, double> wpCuts; // could have a function to set these

  double currentWorkingPointCut;
  double currentWorkingPointCut_veto;

  std::map< std::string, TH2F > m_effMaps;
  std::map< std::string, TH2F > m_effMaps_veto;

  std::unique_ptr<BTagCalibrationReader> m_reader;
  std::unique_ptr<BTagCalibrationReader> m_reader_up;
  std::unique_ptr<BTagCalibrationReader> m_reader_down;

  std::unique_ptr<BTagCalibrationReader> m_reader_veto;
  std::unique_ptr<BTagCalibrationReader> m_reader_veto_up;
  std::unique_ptr<BTagCalibrationReader> m_reader_veto_down;

};


#endif //  __BTAGGINGSCALETOOL_H__
