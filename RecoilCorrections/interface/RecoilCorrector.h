#ifndef RecoilCorrector_h
#define RecoilCorrector_h

#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TLorentzVector.h"
#include "TAxis.h"
#include "TGraphAsymmErrors.h"
#include <TString.h>
#include <TRandom.h>
#include <TMath.h>
#include <assert.h>
#include <iostream>
#include <map>
#include <cmath>
#include <string>
// SFrame include(s):
#include "core/include/SError.h"
#include "plug-ins/include/SToolBase.h"






/// Main class that reads files and processes the input
class RecoilCorrector {
  
  public:
    RecoilCorrector(TString fileName);
    //void init_RecoilCorrector(TString fileName);
    ~RecoilCorrector();

    void Correct( float MetPx,        float MetPy,
	              float genZPx,       float genZPy,
	              float diLepPx,      float diLepPy,
	              int njets,
	              float & MetCorrPx,  float & MetCorrPy);

    void CorrectByMeanResolution( float MetPx,        float MetPy,
			                      float genZPx,       float genZPy,
			                      float diLepPx,       float diLepPy,
			                      int njets,
			                      float & MetCorrPx,  float & MetCorrPy);
			                    
    TLorentzVector CorrectByMeanResolution(     float MetPx,    float MetPy,
					                            float genVPx,   float genVPy,
					                            float visVPx,   float visVPy,
                                                int njets);


  
  private:
  
    int binNumber(float x, const std::vector<float> bins) const
    {
      for (size_t iB=0; iB<bins.size(); ++iB)
        if (x>=bins[iB]&&x<bins[iB+1])
	      return iB;
      return 0;
    }

    int binNumber(float x, int nbins, const float * bins) {
      int binN = 0;
      for (int iB=0; iB<nbins; ++iB) {
        if (x>=bins[iB]&&x<bins[iB+1]) {
	      binN = iB;
	      break;
        }
      }
    return binN;
    }

    TString _fileName;

    void InitMEtWeights(TFile * file,
	  	                TString  _perpZStr,
		                TString  _paralZStr,
		                int nZPtBins,
		                float * ZPtBins,
		                TString * _ZPtStr,
		                int nJetsBins,
		                TString * _nJetsStr);

    void InitMEtWeights(TFile * file,
		                const std::vector<float>& ZPtBins,
		                const std::string _perpZStr,
		                const std::string _paralZStr,
		                const std::vector<std::string>& _ZPtStr,
		                const std::vector<std::string>& _nJetsStr);

    void CalculateU1U2FromMet(  float MetPx,    float MetPy,
			                    float genZPx,   float genZPy,
			                    float diLepPx,  float diLepPy,
			                    float & U1,     float & U2,
			                    float & metU1,  float & metU2);

    void CalculateMetFromU1U2(  float U1,       float U2,
			                    float genZPx,   float genZPy,
			                    float diLepPx,  float diLepPy,
			                    float & metPx,  float & metPy);

    void  U1U2CorrectionsByWidth(   float & U1, float & U2,
			                        int nZptBin,
			                        int njets);

    float CorrectionsBySampling(float x, TF1 * funcMC, TF1 * funcData);

    float rescale(    float x,  float meanData,         float meanMC,
		                        float resolutionData,   float resolutionMC);
    

    //float * _ZPtBins;
    std::vector<float> _ZPtBins;

    Double_t 	_epsrel;
    Double_t 	_epsabs;
    Double_t   	_error;
    float _range;

    int _nZPtBins;
    int _nJetsBins;

    TF1 * _metZParalData[5][3];
    TF1 * _metZPerpData[5][3];
    TF1 * _metZParalMC[5][3];
    TF1 * _metZPerpMC[5][3];

    TH1F * _metZParalDataHist[5][3];
    TH1F * _metZPerpDataHist[5][3];
    TH1F * _metZParalMCHist[5][3];
    TH1F * _metZPerpMCHist[5][3];

    float _meanMetZParalData[5][3];
    float _meanMetZParalMC[5][3];
    float _meanMetZPerpData[5][3];
    float _meanMetZPerpMC[5][3];

    float _rmsMetZParalData[5][3];
    float _rmsLeftMetZParalData[5][3];
    float _rmsRightMetZParalData[5][3];

    float _rmsMetZParalMC[5][3];
    float _rmsLeftMetZParalMC[5][3];
    float _rmsRightMetZParalMC[5][3];

    float _rmsMetZPerpData[5][3];
    float _rmsLeftMetZPerpData[5][3];
    float _rmsRightMetZPerpData[5][3];

    float _rmsMetZPerpMC[5][3];
    float _rmsLeftMetZPerpMC[5][3];
    float _rmsRightMetZPerpMC[5][3];

    float _xminMetZPerp[5][3];
    float _xmaxMetZPerp[5][3];

    float _xminMetZPerpData[5][3];
    float _xmaxMetZPerpData[5][3];

    float _xminMetZPerpMC[5][3];
    float _xmaxMetZPerpMC[5][3];

    float _xminMetZParal[5][3];
    float _xmaxMetZParal[5][3];

    float _xminMetZParalData[5][3];
    float _xmaxMetZParalData[5][3];

    float _xminMetZParalMC[5][3];
    float _xmaxMetZParalMC[5][3];

};





/// Class to call from SFrame
/// This class should contain
///  - RecoilCorrector objects and
///  - methods to call them separately
/// This is done to make the code shorter in the main script
class RecoilCorrectorTool : public SToolBase {

  public:
  
    RecoilCorrectorTool(SCycleBase* parent, const char* name = "RecoilCorrector");
    void BeginInputData( const SInputData& id ) throw( SError );
    ~RecoilCorrectorTool();
                                                
    // PF MET
    TLorentzVector CorrectPFMETByMeanResolution(    float MetPx,    float MetPy,
					                                float genVPx,   float genVPy,
					                                float visVPx,   float visVPy,
                                                    int njets);
	
	// MVA MET
    TLorentzVector CorrectMVAMETByMeanResolution(   float MetPx,    float MetPy,
     					                            float genVPx,   float genVPy,
					                                float visVPx,   float visVPy,
                                                    int njets);
	
	// Z pt corrections
    float ZptWeight( float genVM, float genVPt );

    std::string m_name;
    std::string m_PFMETFile;
    std::string m_MVAMETFile;
    std::string m_ZPTFile;
  
  
                                   
  private:
  
    RecoilCorrector* m_PFMETCorrector;
    RecoilCorrector* m_MVAMETCorrector;
    TH1F* m_ZPTHist;
    
};

#endif
