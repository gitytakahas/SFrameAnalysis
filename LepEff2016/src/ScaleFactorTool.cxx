#include "../interface/ScaleFactorTool.h"
#include <cstdlib>
#include <limits>

#include <TFile.h>
ScaleFactorTool::ScaleFactorTool(SCycleBase* parent, 
			 const char* name ):
 SToolBase( parent ), m_name( name ) 
{
  SetLogName( name );
  DeclareProperty( m_name+"TrigMuName",                 m_TrigFile             = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.root" ); 
  DeclareProperty(  m_name+"MuIDSFName",                  m_Mu_IDSFFile            = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/MuonID_Z_RunBCD_prompt80X_7p65.root" );
  DeclareProperty(  m_name+"MuIsoSFName",                  m_Mu_IsoSFFile            = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Muon/MuonIso_Z_RunBCD_prompt80X_7p65.root" );
  DeclareProperty(  m_name+"EleIDSFName",                  m_Ele_IDSFFile            = std::string (std::getenv("SFRAME_DIR")) + "/../LepEff2016/data/Electron/egammaEffi_txt_SF2D.root" );

}
void ScaleFactorTool::BeginInputData( const SInputData& ) throw( SError ) {

 
  
  m_logger << INFO << "Initializing ScaleFactor for lepons" << SLogger::endmsg;
  m_logger << INFO << "Efficiency file Trig: " << m_TrigFile << SLogger::endmsg;
  m_logger << INFO << "Efficiency file MuSF: " << m_Mu_IDSFFile << SLogger::endmsg;
  m_logger << INFO << "Efficiency file eleSF: " << m_Ele_IDSFFile << SLogger::endmsg;

  init_ScaleFactor( m_TrigFile);
  m_logger << INFO <<"Scale factor Mu trig  initialised"<< SLogger:: endmsg;

  init_ScaleFactor( m_Mu_IDSFFile);
  m_logger << INFO <<"Scale factor Mu ID initialised"<< SLogger:: endmsg;
  init_ScaleFactor( m_Mu_IsoSFFile);
  m_logger << INFO <<"Scale factor Mu Iso initialised"<< SLogger:: endmsg;

  init_ScaleFactor( m_Ele_IDSFFile);
  m_logger << INFO <<"Scale factor Ele ID initialised"<< SLogger:: endmsg;
  return;
}

ScaleFactorTool::~ScaleFactorTool(){
  //delete  eff_mc[etaLabel]; delete eff_data[etaLabel]
}
void ScaleFactorTool::init_ScaleFactor(TString inputRootFile){
  
  // if (inputRootFile.Contains("Electron_IdIso")){
  //     //std::cout <<"  Got the input file .root " << inputRootFile <<std::endl;
  //     TFile * fileIn = new TFile(inputRootFile, "read");
  //     // if root file not found
  //     if (fileIn->IsZombie() ) {
  // 	if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
  // 	exit(1); };
	
  //     std::string HistoBaseName = "ZMass";
  //     etaBinsH_IDEle = (TH1D*)fileIn->Get("etaBinsH"); 
  //     etaBinsH_IDEle->SetDirectory(0);
  //     std::string etaLabel, GraphName;
  //     int nEtaBins = etaBinsH_IDEle->GetNbinsX();
  //     for (int iBin=0; iBin<nEtaBins; iBin++){    
  // 	etaLabel = etaBinsH_IDEle->GetXaxis()->GetBinLabel(iBin+1);
  // 	GraphName = HistoBaseName+etaLabel+"_Data";
  // 	eff_data_IDEle[etaLabel] = (TGraphAsymmErrors*)fileIn->Get(TString(GraphName)); 
  // 	// eff_data[etaLabel]->SetDirectory(0);
  // 	SetAxisBins(eff_data_IDEle[etaLabel]);
  // 	GraphName = HistoBaseName+etaLabel+"_MC";
  // 	eff_mc_IDEle[etaLabel] = (TGraphAsymmErrors*)fileIn->Get(TString(GraphName));
  // 	// eff_mc[etaLabel]->SetDirectory(0);
  // 	SetAxisBins(eff_mc_IDEle[etaLabel]); 
  // 	bool sameBinning = check_SameBinning(eff_data_IDEle[etaLabel], eff_mc_IDEle[etaLabel]);
  // 	if (!sameBinning) { 
  // 	  if (verbose)std::cout<< "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from LepEffInterface/src/ScaleFactor.cc . Can not proceed because ScaleFactor::check_SameBinning returned different pT binning for data and MC for eta label " << etaLabel << std::endl;
  // 	  exit(1); }; 
  //     }
  //     fileIn->Close();
  //   }

  // else  if (inputRootFile.Contains("Muon_IdIso")){
  //     //std::cout <<"  Got the input file .root " << inputRootFile <<std::endl;
  //     TFile * fileIn = new TFile(inputRootFile, "read");
  //     // if root file not found
  //     if (fileIn->IsZombie() ) {
  // 	if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
  // 	exit(1); };
	
  //     std::string HistoBaseName = "ZMass";
  //     etaBinsH_IDMu = (TH1D*)fileIn->Get("etaBinsH"); 
  //     etaBinsH_IDMu->SetDirectory(0);
  //     std::string etaLabel, GraphName;
  //     int nEtaBins = etaBinsH_IDMu->GetNbinsX();
  //     for (int iBin=0; iBin<nEtaBins; iBin++){    
  // 	etaLabel = etaBinsH_IDMu->GetXaxis()->GetBinLabel(iBin+1);
  // 	GraphName = HistoBaseName+etaLabel+"_Data";
  // 	eff_data_IDMu[etaLabel] = (TGraphAsymmErrors*)fileIn->Get(TString(GraphName)); 
  // 	// eff_data[etaLabel]->SetDirectory(0);
  // 	SetAxisBins(eff_data_IDMu[etaLabel]);
  // 	GraphName = HistoBaseName+etaLabel+"_MC";
  // 	eff_mc_IDMu[etaLabel] = (TGraphAsymmErrors*)fileIn->Get(TString(GraphName));
  // 	// eff_mc[etaLabel]->SetDirectory(0);
  // 	SetAxisBins(eff_mc_IDMu[etaLabel]); 
  // 	bool sameBinning = check_SameBinning(eff_data_IDMu[etaLabel], eff_mc_IDMu[etaLabel]);
  // 	if (!sameBinning) { 
  // 	  if (verbose)std::cout<< "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from LepEffInterface/src/ScaleFactor.cc . Can not proceed because ScaleFactor::check_SameBinning returned different pT binning for data and MC for eta label " << etaLabel << std::endl;
  // 	  exit(1); }; 
  //     }
  //     fileIn->Close();
  //   }
  // else  if( inputRootFile.Contains("Muon_IsoMu22")){
  //     //std::cout <<"  Got the input file .root " << inputRootFile <<std::endl;
  //     TFile * fileIn = new TFile(inputRootFile, "read");
  //     // if root file not found
  //     if (fileIn->IsZombie() ) {
  // 	if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
  // 	exit(1); };
	
  //     std::string HistoBaseName = "ZMass";
  //     etaBinsH = (TH1D*)fileIn->Get("etaBinsH"); 
  //     etaBinsH->SetDirectory(0);
  //     std::string etaLabel, GraphName;
  //     int nEtaBins = etaBinsH->GetNbinsX();
  //     for (int iBin=0; iBin<nEtaBins; iBin++){    
  // 	etaLabel = etaBinsH->GetXaxis()->GetBinLabel(iBin+1);
  // 	GraphName = HistoBaseName+etaLabel+"_Data";
  // 	eff_data[etaLabel] = (TGraphAsymmErrors*)fileIn->Get(TString(GraphName)); 
  // 	// eff_data[etaLabel]->SetDirectory(0);
  // 	SetAxisBins(eff_data[etaLabel]);
  // 	GraphName = HistoBaseName+etaLabel+"_MC";
  // 	eff_mc[etaLabel] = (TGraphAsymmErrors*)fileIn->Get(TString(GraphName));
  // 	// eff_mc[etaLabel]->SetDirectory(0);
  // 	SetAxisBins(eff_mc[etaLabel]); 
  // 	bool sameBinning = check_SameBinning(eff_data[etaLabel], eff_mc[etaLabel]);
  // 	if (!sameBinning) { 
  // 	  if (verbose)std::cout<< "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from LepEffInterface/src/ScaleFactor.cc . Can not proceed because ScaleFactor::check_SameBinning returned different pT binning for data and MC for eta label " << etaLabel << std::endl;
  // 	  exit(1); }; 
  //     }
  //     fileIn->Close();
  //   }


  std::cout <<" Want the input file .root " << inputRootFile <<std::endl;

  if (inputRootFile.Contains("egamma")){
    auto fileIn = TFile::Open(inputRootFile// .c_str()
			      );// TFile * fileIn = new TFile(inputRootFile, "read");
    if (fileIn->IsZombie() ) {
      if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
      exit(1); 
    }
    etaptBinsH_IDEle = (TH2D*)fileIn->Get("EGamma_SF2D");
    etaptBinsH_IDEle->SetDirectory(0);
    fileIn->Close();

  }

  else  if (inputRootFile.Contains("MuonID")){
     auto fileIn = TFile::Open(inputRootFile// .c_str()
			       );
    if (fileIn->IsZombie() ) {
      if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
      exit(1); 
    }
    etaptBinsH_IDMu = (TH2D*)fileIn->Get("MC_NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio");
    etaptBinsH_IDMu->SetDirectory(0);
    fileIn->Close();
    
  }
  else  if (inputRootFile.Contains("MuonIso")){
  auto fileIn = TFile::Open(inputRootFile// .c_str()
			    );
    if (fileIn->IsZombie() ) {
      if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
      exit(1); 
    }
    etaptBinsH_IsoMu = (TH2D*)fileIn->Get("MC_NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1/pt_abseta_ratio");
    
    etaptBinsH_IsoMu->SetDirectory(0);
   
   fileIn->Close();

  }

  else  if (inputRootFile.Contains("SingleMuonTrigger")){
    auto fileIn = TFile::Open(inputRootFile// .c_str()
			      );
    if (fileIn->IsZombie() ) {
      if (verbose)std::cout << "ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from NTupleMaker/src/ScaleFactor.cc : ‎File " <<inputRootFile << " does not exist. Please check. " <<std::endl; 
      exit(1); 
    }
    etaptBinsH_TrigMu = (TH2D*)fileIn->Get("IsoMu22_OR_IsoTkMu22_PtEtaBins_Run274094_to_276097/efficienciesDATA/pt_abseta_DATA"); 
    etaptBinsH_TrigMu->SetDirectory(0);
    fileIn->Close();

  }


  else {if (verbose)std::cout<< "File Notfound " << inputRootFile << std::endl;}

  //  delete eff_mc[etaLabel]; delete eff_data[etaLabel];
 return;
}




void ScaleFactorTool::SetAxisBins(TGraphAsymmErrors* graph) {

	int NPOINTS = graph->GetN(); 
	double AXISBINS [NPOINTS+1] = {};
	for (int i=0; i<NPOINTS; i++) { AXISBINS[i] = (graph->GetX()[i] - graph->GetErrorXlow(i)); }
	AXISBINS[NPOINTS] = (graph->GetX()[NPOINTS-1] + graph->GetErrorXhigh(NPOINTS-1));
	graph->GetXaxis()->Set(NPOINTS, AXISBINS);
	return;
}

bool ScaleFactorTool::check_SameBinning(TGraphAsymmErrors* graph1, TGraphAsymmErrors* graph2){
	bool haveSameBins = false;
	int n1 = graph1->GetXaxis()->GetNbins();
	int n2 = graph2->GetXaxis()->GetNbins();
	if (n1 != n2 ) {return false;}
	else {
		haveSameBins = true;
		const int nbins = n1;
		double x1, x2;
		for (int i=0; i<nbins; i++){ 
			x1 = (graph1->GetXaxis()->GetXbins())->GetArray()[i];
			x2 = (graph2->GetXaxis()->GetXbins())->GetArray()[i]; 
			haveSameBins = haveSameBins and (x1== x2) ;
		}
	}

	return haveSameBins;
}


std::string ScaleFactorTool::FindEtaLabel(double Eta){
	Eta = fabs(Eta);
	int binNumber = etaBinsH->GetXaxis()->FindFixBin(Eta);
	std::string EtaLabel = etaBinsH->GetXaxis()->GetBinLabel(binNumber);
	std::map<std::string, TGraphAsymmErrors*>::iterator it;
	it =  eff_data.find(EtaLabel);
	if ( it == eff_data.end()) { 
	  if (verbose)	std::cout << "ERROR in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : no object corresponding to eta label "<< EtaLabel << " for data " << std::endl; exit(1);
	}
	else return EtaLabel;
}
std::string ScaleFactorTool::FindEtaLabel_IDMu(double Eta){
	Eta = fabs(Eta);
	int binNumber = etaBinsH_IDMu->GetXaxis()->FindFixBin(Eta);
	std::string EtaLabel = etaBinsH_IDMu->GetXaxis()->GetBinLabel(binNumber);
	std::map<std::string, TGraphAsymmErrors*>::iterator it;
	it =  eff_data_IDMu.find(EtaLabel);
	if ( it == eff_data_IDMu.end()) { 
	  if (verbose)	std::cout << "ERROR in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : no object corresponding to eta label "<< EtaLabel << " for data " << std::endl; exit(1);
	}
	else return EtaLabel;
}

std::string ScaleFactorTool::FindEtaLabel_IDEle(double Eta){
	Eta = fabs(Eta);
	int binNumber = etaBinsH_IDEle->GetXaxis()->FindFixBin(Eta);
	std::string EtaLabel = etaBinsH_IDEle->GetXaxis()->GetBinLabel(binNumber);
	std::map<std::string, TGraphAsymmErrors*>::iterator it;
	it =  eff_data_IDEle.find(EtaLabel);
	if ( it == eff_data_IDEle.end()) { 
	  if (verbose)	std::cout << "ERROR in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : no object corresponding to eta label "<< EtaLabel << " for data " << std::endl; exit(1);
	}
	else return EtaLabel;
}

int ScaleFactorTool::FindPtBin( std::map<std::string, TGraphAsymmErrors *> eff_map, std::string EtaLabel, double Pt){

        int Npoints = eff_map[EtaLabel]->GetN();
	double ptMAX = (eff_map[EtaLabel]->GetX()[Npoints-1])+(eff_map[EtaLabel]->GetErrorXhigh(Npoints-1));
	double ptMIN = (eff_map[EtaLabel]->GetX()[0])-(eff_map[EtaLabel]->GetErrorXlow(0));
	// if pt is overflow, return last pt bin
 	if (Pt >= ptMAX ) return Npoints; 
	// if pt is underflow, return nonsense number and warning
	else if (Pt < ptMIN){ 
	  if (verbose)	std::cout<< "WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: pT too low (pt = " << Pt << "), min value is " << ptMIN << ". Returned efficiency =1. Weight will be 1. " << std::endl;
	return -99;}
	// if pt is in range
	else {return eff_map[EtaLabel]->GetXaxis()->FindFixBin(Pt);} 
	}


double ScaleFactorTool::get_EfficiencyData(double pt, double eta){

        double eff;
	std::string label = FindEtaLabel(eta);

	int ptbin = FindPtBin(eff_data, label, pt); 
	if (ptbin == -99){eff =1;} // if pt is underflow 
	else eff = eff_data[label]->GetY()[ptbin-1];

	if (eff > 1.) { if (verbose)std::cout<< "WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: Returned efficiency in data > 1. " << std::endl;} 
	if (eff < 0 ) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: Returned negative efficiency in data" <<std::endl;}
	return eff;
	
}
double ScaleFactorTool::get_EfficiencyData_IDMu(double pt, double eta){

        double eff;
	std::string label = FindEtaLabel_IDMu(eta);

	int ptbin = FindPtBin(eff_data_IDMu, label, pt); 
	if (ptbin == -99){eff =1;} // if pt is underflow 
	else eff = eff_data_IDMu[label]->GetY()[ptbin-1];

	if (eff > 1.) { if (verbose)std::cout<< "WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: Returned efficiency in data > 1. " << std::endl;} 
	if (eff < 0 ) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: Returned negative efficiency in data" <<std::endl;}
	return eff;
	
}
double ScaleFactorTool::get_EfficiencyData_IDEle(double pt, double eta){

        double eff;
	std::string label = FindEtaLabel_IDEle(eta);

	int ptbin = FindPtBin(eff_data_IDEle, label, pt); 
	if (ptbin == -99){eff =1;} // if pt is underflow 
	else eff = eff_data_IDEle[label]->GetY()[ptbin-1];

	if (eff > 1.) { if (verbose)std::cout<< "WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: Returned efficiency in data > 1. " << std::endl;} 
	if (eff < 0 ) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: Returned negative efficiency in data" <<std::endl;}
	return eff;
	
}


double ScaleFactorTool::get_EfficiencyMC(double pt, double eta) {

	double eff;		
	std::string label = FindEtaLabel(eta);

	int ptbin = FindPtBin(eff_mc, label, pt); 
	if (ptbin == -99){eff =1;} // if pt is underflow 
	else eff= eff_mc[label]->GetY()[ptbin-1];

	if (eff > 1. ) { if (verbose)std::cout << "WARNING in ScaleFactor::get_EfficiencyMC(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : Returned efficiency in MC > 1. " << std::endl;} 		
	if (eff < 0 ) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_EfficiencyMC(double pt, double eta) from LepEffIntrface/src/ScaleFactor.cc : Returned negative efficiency in MC. " <<std::endl;}
	

	return eff;

}

double ScaleFactorTool::get_EfficiencyTrigMu(double pt, double eta) {

  double eff;double eff_unc;		
  
  double ptmax =etaptBinsH_TrigMu->GetXaxis()->GetXmax();
  double ptmin =etaptBinsH_TrigMu->GetXaxis()->GetXmin();
  
  if (pt >= ptmax) pt = ptmax - 0.01;
  if (pt <= ptmin) pt = ptmin + 0.001;
  if (fabs(eta)>2.4) eff=0;
  else{
    int pt_bin = etaptBinsH_TrigMu->GetXaxis()->FindBin(pt);
    int eta_bin = etaptBinsH_TrigMu->GetYaxis()->FindBin(fabs(eta));
 

    eff= etaptBinsH_TrigMu-> GetBinContent(pt_bin, eta_bin);
    eff_unc= etaptBinsH_TrigMu-> GetBinError(pt_bin,eta_bin);
  }
  
  // std::cout << "later mu pt "<< pt << " eta " <<  eta <<std::endl;
  // std::cout << "mu Trig eff "<<eff<< " pm "<<eff_unc<<  std::endl;
  return eff;
}

double ScaleFactorTool::get_ScaleFactor_IDEleIchep(double pt, double eta) {

  double eff;double eff_unc;		
  // std::cout << "first ele pt "<< pt << " eta " <<  eta <<std::endl;
  double ptmax = etaptBinsH_IDEle->GetYaxis()->GetXmax();
  double ptmin = etaptBinsH_IDEle->GetYaxis()->GetXmin();
  // std::cout << " ele ptmax  "<< ptmax <<" ele ptmin  "<< ptmin  <<std::endl;

  if (pt >= ptmax) pt = ptmax - 0.01;
  if (pt <= ptmin) pt = ptmin + 0.001;
  if (fabs(eta)>=2.5) eff=0;

  int pt_bin = etaptBinsH_IDEle->GetYaxis()->FindBin(pt);
  int eta_bin = etaptBinsH_IDEle->GetXaxis()->FindBin(fabs(eta));
 

  if ((fabs(eta)<2.4)){
    eff= etaptBinsH_IDEle-> GetBinContent( eta_bin,pt_bin);
    eff_unc=  etaptBinsH_IDEle-> GetBinError( eta_bin,pt_bin);
  }
  // std::cout << "later ele pt "<< pt << " eta " <<  eta <<std::endl;
    // std::cout << "ele ID SF "<<eff<< " pm "<<eff_unc<<  std::endl;
  
  return eff;
}
double ScaleFactorTool::get_ScaleFactor_IDMuIchep(double pt, double eta) {

  double eff;double eff_unc;		
  // std::cout << "mu pt "<< pt << " eta " <<  eta <<std::endl;
  double ptmax = etaptBinsH_IDMu->GetXaxis()->GetXmax();
  double ptmin = etaptBinsH_IDMu->GetXaxis()->GetXmin();
  
  if (pt >= ptmax) pt = ptmax - 0.01;
  if (pt <= ptmin) pt = ptmin + 0.001;
  if (fabs(eta)>=2.4) eff=0;
  int pt_bin = etaptBinsH_IDMu->GetXaxis()->FindBin(pt);
  int  eta_bin = etaptBinsH_IDMu->GetYaxis()->FindBin(fabs(eta));
 

  if ((fabs(eta)<2.4)){
    
    eff= etaptBinsH_IDMu-> GetBinContent(pt_bin, eta_bin);
    eff_unc=  etaptBinsH_IDMu-> GetBinError(pt_bin, eta_bin);
  }
  // std::cout << "mu pt "<< pt << " eta " <<  eta <<std::endl;
  // std::cout << "mu ID SF "<<eff<<  " pm "<<eff_unc<<  std::endl;
  
  
  return eff;
}
double ScaleFactorTool::get_ScaleFactor_IsoMuIchep(double pt, double eta) {

  double eff;double eff_unc;		
  // std::cout << "mu pt "<< pt << " eta " <<  eta <<std::endl;
  double ptmax = etaptBinsH_IsoMu->GetXaxis()->GetXmax();
  double ptmin = etaptBinsH_IsoMu->GetXaxis()->GetXmin();
  
  if (pt >= ptmax) pt = ptmax - 0.01;
  if (pt <= ptmin) pt = ptmin + 0.001;
  
  if (fabs(eta)>=2.4) eff=0;
 int pt_bin = etaptBinsH_IsoMu->GetXaxis()->FindBin(pt);
 int eta_bin = etaptBinsH_IsoMu->GetYaxis()->FindBin(fabs(eta));
 

  if ((fabs(eta)<2.4)){
    eff= etaptBinsH_IsoMu-> GetBinContent(pt_bin, eta_bin);
    eff_unc=  etaptBinsH_IsoMu-> GetBinError(pt_bin, eta_bin);
  }
  // std::cout << "mu pt "<< pt << " eta " <<  eta <<std::endl;
  // std::cout << "mu Iso SF "<<eff<<  " pm "<<eff_unc<<  std::endl;
  
  return eff;
}

double ScaleFactorTool::get_EfficiencyMC_IDMu(double pt, double eta) {

	double eff;		
	std::string label = FindEtaLabel_IDMu(eta);

	int ptbin = FindPtBin(eff_mc_IDMu, label, pt); 
	if (ptbin == -99){eff =1;} // if pt is underflow 
	else eff= eff_mc_IDMu[label]->GetY()[ptbin-1];

	if (eff > 1. ) { if (verbose)std::cout << "WARNING in ScaleFactor::get_EfficiencyMC(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : Returned efficiency in MC > 1. " << std::endl;} 		
	if (eff < 0 ) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_EfficiencyMC(double pt, double eta) from LepEffIntrface/src/ScaleFactor.cc : Returned negative efficiency in MC. " <<std::endl;}
	

	return eff;

}

double ScaleFactorTool::get_EfficiencyMC_IDEle(double pt, double eta) {

	double eff;		
	std::string label = FindEtaLabel_IDEle(eta);

	int ptbin = FindPtBin(eff_mc_IDEle, label, pt); 
	if (ptbin == -99){eff =1;} // if pt is underflow 
	else eff= eff_mc_IDEle[label]->GetY()[ptbin-1];

	if (eff > 1. ) { if (verbose)std::cout << "WARNING in ScaleFactor::get_EfficiencyMC(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : Returned efficiency in MC > 1. " << std::endl;} 		
	if (eff < 0 ) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_EfficiencyMC(double pt, double eta) from LepEffIntrface/src/ScaleFactor.cc : Returned negative efficiency in MC. " <<std::endl;}
	

	return eff;

}


double ScaleFactorTool::get_ScaleFactor(double pt, double eta){
	
	double efficiency_data = get_EfficiencyData(pt, eta);
	if (verbose) 	std::cout << " efficiency_data "<<  efficiency_data <<std::endl;

	double efficiency_mc = get_EfficiencyMC(pt, eta);
	if (verbose) 	std::cout << " efficiency_mc "<<  efficiency_mc <<std::endl;

	double SF;

	if ( efficiency_mc != 0) {SF = efficiency_data/efficiency_mc;}
	else {
	  SF=0.; 
	  if (verbose)  std::cout <<  "WARNING in ScaleFactor::get_ScaleFactor(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : MC efficiency = 0. Scale Factor set to 0. ";
	}
	if (verbose) std::cout <<" for pt " <<pt<< " eta " <<eta << ": SF "<<SF <<std::endl; 
       	return SF;	

}
double ScaleFactorTool::get_ScaleFactor_IDMu(double pt, double eta){
	
	double efficiency_data = get_EfficiencyData_IDMu(pt, eta);
	if (verbose) 	std::cout << " efficiency_data "<<  efficiency_data <<std::endl;

	double efficiency_mc = get_EfficiencyMC_IDMu(pt, eta);
	if (verbose) 	std::cout << " efficiency_mc "<<  efficiency_mc <<std::endl;

	double SF;

	if ( efficiency_mc != 0) {SF = efficiency_data/efficiency_mc;}
	else {
	  SF=0.; 
	  if (verbose)  std::cout <<  "WARNING in ScaleFactor::get_ScaleFactor(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : MC efficiency = 0. Scale Factor set to 0. ";
	}
	if (verbose) std::cout <<" for pt " <<pt<< " eta " <<eta << ": SF "<<SF <<std::endl; 
       	return SF;	

}
double ScaleFactorTool::get_ScaleFactor_IDEle(double pt, double eta){
	
	double efficiency_data = get_EfficiencyData_IDEle(pt, eta);
	if (verbose) 	std::cout << " efficiency_data "<<  efficiency_data <<std::endl;

	double efficiency_mc = get_EfficiencyMC_IDEle(pt, eta);
	if (verbose) 	std::cout << " efficiency_mc "<<  efficiency_mc <<std::endl;

	double SF;

	if ( efficiency_mc != 0) {SF = efficiency_data/efficiency_mc;}
	else {
	  SF=0.; 
	  if (verbose)  std::cout <<  "WARNING in ScaleFactor::get_ScaleFactor(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : MC efficiency = 0. Scale Factor set to 0. ";
	}
	if (verbose) std::cout <<" for pt " <<pt<< " eta " <<eta << ": SF "<<SF <<std::endl; 
       	return SF;	

}


double ScaleFactorTool::get_EfficiencyDataError(double pt, double eta){

	double eff_error;
	std::string label = FindEtaLabel(eta);
	int ptbin = FindPtBin(eff_data, label, pt); 
	if (ptbin == -99){eff_error =0.;} // if pt is underflow 
	else eff_error= eff_data[label]->GetErrorYhigh(ptbin-1); 
        // errors are supposed to be symmetric, can use GetErrorYhigh or GetErrorYlow

	double effData = get_EfficiencyData(pt,eta);
	if (eff_error > effData) eff_error = 0.5*effData;
	return eff_error;
}
	
double ScaleFactorTool::get_EfficiencyDataError_IDMu(double pt, double eta){

	double eff_error;
	std::string label = FindEtaLabel_IDMu(eta);
	int ptbin = FindPtBin(eff_data_IDMu, label, pt); 
	if (ptbin == -99){eff_error =0.;} // if pt is underflow 
	else eff_error= eff_data_IDMu[label]->GetErrorYhigh(ptbin-1); 
        // errors are supposed to be symmetric, can use GetErrorYhigh or GetErrorYlow

	double effData = get_EfficiencyData_IDMu(pt,eta);
	if (eff_error > effData) eff_error = 0.5*effData;
	return eff_error;
}
	
double ScaleFactorTool::get_EfficiencyDataError_IDEle(double pt, double eta){

	double eff_error;
	std::string label = FindEtaLabel_IDEle(eta);
	int ptbin = FindPtBin(eff_data_IDEle, label, pt); 
	if (ptbin == -99){eff_error =0.;} // if pt is underflow 
	else eff_error= eff_data_IDEle[label]->GetErrorYhigh(ptbin-1); 
        // errors are supposed to be symmetric, can use GetErrorYhigh or GetErrorYlow

	double effData = get_EfficiencyData_IDEle(pt,eta);
	if (eff_error > effData) eff_error = 0.5*effData;
	return eff_error;
}
	
	

double ScaleFactorTool::get_EfficiencyMCError(double pt, double eta){

	double eff_error;
	std::string label = FindEtaLabel(eta);
	int ptbin = FindPtBin(eff_mc, label, pt); 
	if (ptbin == -99){eff_error =0.;} // if pt is underflow 
	else eff_error= eff_mc[label]->GetErrorYhigh(ptbin-1); 
	// errors are supposed to be symmetric, can use GetErrorYhigh or GetErrorYlow

	double effMC = get_EfficiencyMC(pt,eta);
	if (eff_error > effMC ) eff_error = 0.5*effMC;
	return eff_error;
}
double ScaleFactorTool::get_EfficiencyMCError_IDMu(double pt, double eta){

	double eff_error;
	std::string label = FindEtaLabel_IDMu(eta);
	int ptbin = FindPtBin(eff_mc_IDMu, label, pt); 
	if (ptbin == -99){eff_error =0.;} // if pt is underflow 
	else eff_error= eff_mc_IDMu[label]->GetErrorYhigh(ptbin-1); 
	// errors are supposed to be symmetric, can use GetErrorYhigh or GetErrorYlow

	double effMC = get_EfficiencyMC(pt,eta);
	if (eff_error > effMC ) eff_error = 0.5*effMC;
	return eff_error;
}
double ScaleFactorTool::get_EfficiencyMCError_IDEle(double pt, double eta){

	double eff_error;
	std::string label = FindEtaLabel_IDEle(eta);
	int ptbin = FindPtBin(eff_mc_IDEle, label, pt); 
	if (ptbin == -99){eff_error =0.;} // if pt is underflow 
	else eff_error= eff_mc_IDEle[label]->GetErrorYhigh(ptbin-1); 
	// errors are supposed to be symmetric, can use GetErrorYhigh or GetErrorYlow

	double effMC = get_EfficiencyMC_IDEle(pt,eta);
	if (eff_error > effMC ) eff_error = 0.5*effMC;
	return eff_error;
}

double ScaleFactorTool::get_ScaleFactorError(double pt, double eta){

	double SF_error = 0.;
	
	double effData = get_EfficiencyData(pt, eta);
	double effMC = get_EfficiencyMC(pt, eta);
	double errData = get_EfficiencyDataError(pt, eta);
	double errMC =  get_EfficiencyMCError(pt, eta);

	if (errData == 0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: uncertainty on data point = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (errMC ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: uncertainty on MC = 0, can not calculate uncerttainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (effData ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: efficiency in data = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (effMC ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: efficiency in MC = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	else {	
	SF_error = pow((errData/effData),2) + pow((errMC/effMC),2);
	SF_error = pow(SF_error, 0.5)*(effData/effMC);
	}
	return SF_error;
}
	
double ScaleFactorTool::get_ScaleFactorError_IDMu(double pt, double eta){

	double SF_error = 0.;
	
	double effData = get_EfficiencyData_IDMu(pt, eta);
	double effMC = get_EfficiencyMC_IDMu(pt, eta);
	double errData = get_EfficiencyDataError_IDMu(pt, eta);
	double errMC =  get_EfficiencyMCError_IDMu(pt, eta);

	if (errData == 0) { if (verbose)std::cout<<"WARNING in ScaleFactorTool::get_ScaleFactorToolError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: uncertainty on data point = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (errMC ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: uncertainty on MC = 0, can not calculate uncerttainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (effData ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: efficiency in data = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (effMC ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: efficiency in MC = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	else {	
	SF_error = pow((errData/effData),2) + pow((errMC/effMC),2);
	SF_error = pow(SF_error, 0.5)*(effData/effMC);
	}
	return SF_error;
}
	
double ScaleFactorTool::get_ScaleFactorError_IDEle(double pt, double eta){

	double SF_error = 0.;
	
	double effData = get_EfficiencyData_IDEle(pt, eta);
	double effMC = get_EfficiencyMC_IDEle(pt, eta);
	double errData = get_EfficiencyDataError_IDEle(pt, eta);
	double errMC =  get_EfficiencyMCError_IDEle(pt, eta);

	if (errData == 0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: uncertainty on data point = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (errMC ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: uncertainty on MC = 0, can not calculate uncerttainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (effData ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: efficiency in data = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	if (effMC ==0) { if (verbose)std::cout<<"WARNING in ScaleFactor::get_ScaleFactorError(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: efficiency in MC = 0, can not calculate uncertainty on scale factor. Uncertainty set to 0." << std::endl;}
	else {	
	SF_error = pow((errData/effData),2) + pow((errMC/effMC),2);
	SF_error = pow(SF_error, 0.5)*(effData/effMC);
	}
	return SF_error;
}
	

