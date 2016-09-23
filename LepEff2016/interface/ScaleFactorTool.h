#ifndef ScaleFactorTool_h
#define ScaleFactorTool_h

#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TAxis.h"
#include "TGraphAsymmErrors.h"
#include <iostream>
#include <map>
#include <cmath>
#include <string>
// SFrame include(s):
#include "core/include/SError.h"
#include "plug-ins/include/SToolBase.h"




class ScaleFactorTool  : public SToolBase   {

	private: 
        std::string m_name; 
	std::map<std::string, TGraphAsymmErrors *> eff_data;
	std::map<std::string, TGraphAsymmErrors *> eff_mc;
	std::map<std::string, TGraphAsymmErrors *> eff_data_IDMu;
	std::map<std::string, TGraphAsymmErrors *> eff_mc_IDMu;
	std::map<std::string, TGraphAsymmErrors *> eff_data_IDEle;
	std::map<std::string, TGraphAsymmErrors *> eff_mc_IDEle;

	TH1D * etaBinsH_IDMu;	
	TH2D * etaptBinsH_IDMu;	TH2D * etaptBinsH_IsoMu;
	TH1D * etaBinsH_IDEle; 
	TH2D * etaptBinsH_IDEle;
	TH1D * etaBinsH;
	TH2D * etaptBinsH_TrigMu;

	void  SetAxisBins(TGraphAsymmErrors*);
	bool  check_SameBinning(TGraphAsymmErrors*, TGraphAsymmErrors*);
	std::string FindEtaLabel(double);
	std::string FindEtaLabel_IDMu(double);
	std::string FindEtaLabel_IDEle(double);
        int FindPtBin( std::map<std::string, TGraphAsymmErrors *>, std::string, double);

	public:
	/* ScaleFactor(){}; */
	/* ~ ScaleFactor(){}; */
	/* ///	constructor */
	ScaleFactorTool( SCycleBase* parent, const char* name = "ScaleFactorTool" );
	/* /// destructor */
	~ScaleFactorTool(); 

	void BeginInputData( const SInputData& id ) throw( SError );
	 
	void init_ScaleFactor(TString);
	void init_ScaleFactor(TString,std::string);

	double get_EfficiencyData(double, double); //pt, eta
	double get_EfficiencyMC(double, double);
	double get_ScaleFactor(double, double); 
	double get_EfficiencyDataError(double, double);
	double get_EfficiencyMCError(double, double);
	double get_ScaleFactorError(double, double);
	double get_EfficiencyData_IDMu(double, double); //pt, eta
	double get_EfficiencyMC_IDMu(double, double);
	double get_ScaleFactor_IDMu(double, double); 
	double get_EfficiencyDataError_IDMu(double, double);
	double get_EfficiencyMCError_IDMu(double, double);
	double get_ScaleFactorError_IDMu(double, double);
	double get_EfficiencyData_IDEle(double, double); //pt, eta
	double get_EfficiencyMC_IDEle(double, double);
	double get_ScaleFactor_IDEle(double, double); 
	double get_EfficiencyDataError_IDEle(double, double);
	double get_EfficiencyMCError_IDEle(double, double);
	double get_ScaleFactorError_IDEle(double, double);

	double get_EfficiencyTrigMu(double, double);
	double get_ScaleFactor_IDEleIchep(double, double);
	double get_ScaleFactor_IDMuIchep(double, double); 
	double get_ScaleFactor_IsoMuIchep(double, double); 

	bool verbose =true; 
	std::string m_TrigFile;
	std::string m_Mu_IDSFFile;
	std::string m_Mu_IsoSFFile;
	std::string m_Ele_IDSFFile;


};


#endif //  ScaleFactor_h


