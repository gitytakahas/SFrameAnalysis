#include "include/LumiWeight.h"

#include <iostream>

//==============================================================================================
LumiWeight::LumiWeight( void ){

}

//==============================================================================================
LumiWeight::~LumiWeight( void ){

}

//==============================================================================================
double LumiWeight::getLumiWeight( TString sample ){

  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#MC_and_data_samples
  // https://cmsweb.cern.ch/das/request?input=dataset%3D%2FZZ_TuneCUETP8M1_13TeV-pythia8%2FRunIISummer15GS-MCRUN2_71_V1-v1%2FGEN-SIM&instance=prod%2Fglobal

  xSec_ = 1.;
  genEvents_ = 1.;
  
  if( sample.Contains("Spring16")){
    
    if( sample.Contains( "TT" )){
      if( sample.Contains("powheg-pythia8")){
        xSec_ = 831.76;
        genEvents_ = 32103976.;
      }
      else if( sample.Contains("madgraphMLM-pythia8")){
        xSec_ = 831.76;
        genEvents_ = 10259851.; 
      }
      else if( sample.Contains("herwig")){
        xSec_ = 831.76;
        genEvents_ = 19797004.; 
      }
    }
    
    else if( sample.Contains( "DYJetsToLL" )){
      if( sample.Contains("M-10to50_TuneCUETP8M1")){
        xSec_ = 18610.0;
        genEvents_ = 1.;
      }
      else if( sample.Contains("M-50_TuneCUETP8M1")){
        xSec_ =  5765.4;
        genEvents_ = 1.;
      }
    }
    
    else if( sample.Contains( "ST" )){
      if( sample.Contains("tW_top_5f_NoFullyHadronicDecays")){
        xSec_ = 1.;
        genEvents_ = 1.;
      }
      else if( sample.Contains("tW_top_5f_inclusiveDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("tW_antitop_5f_NoFullyHadronicDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("tW_antitop_5f_inclusiveDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("s-channel_4f_leptonDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("t-channel_top_4f_inclusiveDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("t-channel_top_4f_leptonDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("t-channel_antitop_4f_inclusiveDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("t-channel_antitop_4f_leptonDecays")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
    }
    
    else if( sample.Contains( "WW" )){
      if( sample.Contains("powheg-pythia8")){
        xSec_ = 1.;
        genEvents_ = 1.;
      }
      else if( sample.Contains("madgraphMLM-pythia8")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
      else if( sample.Contains("herwig")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
    }
    
    else if( sample.Contains( "WJets" )){
      if( sample.Contains("ToLNu_TuneCUETP8M1")){
        xSec_ = 61526.7;
        genEvents_ = 1.;
      }
    }
    
    else if( sample.Contains( "WZ" )){
      if( sample.Contains("TuneCUETP8M1")){
        xSec_ = 1.;
        genEvents_ = 1.;
      }
    }
    
    else if( sample.Contains( "WW" )){
      if( sample.Contains("powheg-pythia8")){
        xSec_ = 1.;
        genEvents_ = 1.;
      }
      else if( sample.Contains("madgraphMLM")){
        xSec_ = 1.;
        genEvents_ = 1.; 
      }
    }
    
    else if( sample.Contains( "ZZ" )){
      if( sample.Contains("powheg-pythia8")){
        xSec_ = 1.;
        genEvents_ = 1.;
      }
    }
    
    
    
    
    
    
  }
  
  // std::cout<< "Crosssection = " << xSec_ << "genEvents = " << genEvents_ << "Weight = " << xSec_/genEvents_ <<std::endl;
  return xSec_/genEvents_;

      
}
