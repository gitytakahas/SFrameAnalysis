#include "../SVFit/include/NTFit.h"
// NTFit::NTFit( std::string iLikelihoodFile,int iType,NTFit::Options iOption,NTFit::CalcOptions iCalcOption,int iNEvents,bool iCorrectMet) { 
NTFit::NTFit(int iType, std::string iLikelihoodFile,NTFit::Options iOption,NTFit::CalcOptions iCalcOption,int iNEvents,bool iCorrectMet) { 
  f13Body = false;
  f23Body = false;
  if(iType == 1)  f13Body = true;
  if(iType == 2) {f13Body = true; f23Body = true;}
  if(iType == 3) f23Body = true;
  fNEvents    = iNEvents;
  fCorrectMet = iCorrectMet;

  fOption      = iOption;
  fCalcOption  = iCalcOption;
  //Initialize Basic Variables
  fX1      = 0;
  fX2      = 0;
  fPhi1    = 0;
  fPhi2    = 0;
  fCosPhi1 = 0;
  fCosPhi2 = 0;
  //Outputs
  fMass    = 0;
  fPt      = 0;
  fPhi     = 0;
  fEta     = 0;
  //fY       = 0;
  fMetSys  = 0;
  fM1Sys   = 0;
  fM2Sys   = 0;
  fW1Sys   = 0;
  fW2Sys   = 0;
  //Floating Weight variable
  fTotWeight = 0;  
  fMLep = 0.105;
  fMTau = 1.775;

  fTauL = 0.0000871;
  fResp = 1.;
  fTempWeight = 1.;
  //Basic ME for Tau decay + Useful Gaussian
  fF1   = new TF2("a","x*x*(3-2*x)-(2*x-1)*x*x*cos(y)",2.*fMLep/fMTau,1,0.,TMath::Pi()); 
  fF2   = new TF1("b","TMath::Pi()**2-x**2"                             ,0,TMath::Pi()); 
  fGaus = new TF1("g1","gaus",-100,100); 
  //Hard coded random seed
  fRand = new TRandom2(0xDEADBEEF); 
  //Tau kinematics
  fTau1.SetPtEtaPhiM(0,0,0,0);
  fTau2.SetPtEtaPhiM(0,0,0,0);
  
  //Load Angular Decay 
  fFile = new TFile(iLikelihoodFile.c_str()); 
  fY    = 0;
  f2D   = 0;
  fPHTau  = new TH1F*[6];
  fPHLep  = new TH2F*[6];
  
  fPZTau  = new TH1F*[6];
  fPZLep  = new TH2F*[6];
  
  fMHTau  = new TH1F*[6];
  fMHLep  = new TH2F*[6];
  
  fMZTau   = new TH1F*[6];
  fMZLep   = new TH2F*[6];

  fHX1        = new TH1F("tmpX1"     ,"tmpX1"     ,500, 0.,1.);
  fHX2        = new TH1F("tmpX2"     ,"tmpX2"     ,500, 0.,1.);
  fHCosPhi1   = new TH1F("tmpCosPhi1","tmpCosPhi1",500,-1.,1.);
  fHCosPhi2   = new TH1F("tmpCosPhi2","tmpCosPhi2",500,-1.,1.);
  //4 Vector
  fHMass      = new TH1F("tmpMass"   ,"tmpMass"    ,10000,  0.,5000.);
  fHPt        = new TH1F("tmpPt"     ,"tmpPt"      ,500  , 0.,1000.);
  fHPhi       = new TH1F("tmpHPhi"   ,"tmpHPhi"    ,500  ,-5.,5.);
  fHEta       = new TH1F("tmpHEta"   ,"tmpHEta"    ,500  ,-5.,5.);
  fCov = new TMatrixD(2,2);

  loadLikelihoodVariables();
 //  fFile.Close();
}
void NTFit::loadLikelihood(std::string iVar,TH1F **iZTau,TH2F **iZLep,TH1F **iHTau,TH2F **iHLep) { 
  for(int i0 = 0; i0 < 6; i0++) { 
    std::stringstream pName1,pName2;
    //pName0 <<  "cosc" << i0;
    pName1 << iVar <<  "cosx"  << i0;
    pName2 << iVar <<  "cos"  << i0;
    //Higgs 
    iZTau[i0] = (TH1F*) fFile->FindObjectAny(pName2.str().c_str()); 
    iZLep[i0] = (TH2F*) fFile->FindObjectAny(pName1.str().c_str()); 
    iHTau[i0] = (TH1F*) fFile->FindObjectAny(("h"+pName2.str()).c_str()); 
    iHLep[i0] = (TH2F*) fFile->FindObjectAny(("h"+pName1.str()).c_str()); 
  }
}
void NTFit::loadLikelihoodVariables() { 
  loadLikelihood("dphi"   ,fPZTau,fPZLep,fPHTau,fPHLep);
  loadLikelihood("mvamet" ,fMZTau,fMZLep,fMHTau,fMHLep);
}
void NTFit::computeLikelihoodFunction(double iPt,double iMet,double iFrac) {
  std::stringstream lPCrap0,lPCrap1,lMCrap0,lMCrap1; 
  lPCrap0 << "PZDCrap";
  lPCrap1 << "PZYCrap";
  lMCrap0 << "MZDCrap";
  lMCrap1 << "MZYCrap";

  //Determine the binning in the angle
  double lSlope = 0.1;
  double lConst = (TMath::Pi()-lSlope*6.*6.)/6.;
  int lPId   =  5.-int(sqrt(lConst*lConst-4*lSlope*(iPt-TMath::Pi()))/2./lSlope - lConst/2./lSlope); 
  //Determine the binning in MET
  int lMId = iMet/6.;
  if(lMId > 5) lMId = 5;
  if(lMId < 0) lMId = 0;
  //FIXME => no clones
  f2D       = (TH2F*) fPZLep[lPId]->Clone(lPCrap0.str().c_str()); f2D->Scale(1-iFrac); f2D->Add(fPHLep[lPId],iFrac);
  fY        = (TH1F*) fPZTau[lPId]->Clone(lPCrap1.str().c_str()); fY ->Scale(1-iFrac); fY ->Add(fPHTau[lPId],iFrac);
  
  TH2F* p2D = (TH2F*) fMZLep[lMId]->Clone(lMCrap0.str().c_str()); p2D->Scale(1-iFrac); p2D->Add(fMHLep[lMId]  ,iFrac);
  TH1F* pY  = (TH1F*) fMZTau[lMId]->Clone(lMCrap1.str().c_str()); pY ->Scale(1-iFrac); pY ->Add(fMHTau[lMId]  ,iFrac);
  
  f2D ->Multiply(p2D);
  fY  ->Multiply(pY);
  f2D->Scale(1./f2D->Integral());
  fY ->Scale(1./fY ->Integral());
}
//Sample from likelihoods
TLorentzVector NTFit::NeutrinoToy(TRandom2 &iRand,double &iX,double &iCosPhi,TLorentzVector &iTau,double iPt,double iPhi,double iEta,double iMLep,bool i3Body,double iXMin) { 
  TLorentzVector lVec; lVec.SetPtEtaPhiM(iPt,iEta,iPhi,iMLep);
  double lX     = 0;
  double lY     = 0;
  //Likelihood sampling (the key to this whole thing)
  if(fOption == kFlat) { 
    lX = iRand.Uniform(0.,1.);//2.*fX->GetRandom();//sqrt(iRand.Uniform(iXMin,1.0)); 
    lY = TMath::Pi()-TMath::Power(iRand.Uniform(0,TMath::Pi()*TMath::Pi()*TMath::Pi()),2.);
  }
  if(fOption == kFlat2) { 
    if( i3Body ) {lY=acos(iRand.Uniform(-1.,1.)); lX=iRand.Uniform(0.2,0.99);} //{f2D->GetRandom2(lX,lY); lX*=2.;}// lY = acos(lY);}
    if(!i3Body )  lY=acos(iRand.Uniform(-0.5,1.));
    if( i3Body ) fTempWeight *= f2D->GetBinContent(f2D->GetXaxis()->FindBin(lX/2.),f2D->GetYaxis()->FindBin(lY)); 
    if(!i3Body ) fTempWeight *= fY->GetBinContent(fY->GetXaxis()->FindBin(lY)); 
  }
  if(fOption == kME) { 
    if( i3Body )  fF1->GetRandom2(lX,lY); // lY = acos(lY);}
    if(!i3Body )  lY=fF2->GetRandom();
  }
  if(fOption == kHistLikelihood) { 
    if( i3Body ) {f2D->GetRandom2(lX,lY);    lX*=2.;  }
    if(!i3Body )  lY = fY->GetRandom();
  }
  if(fOption == kHistLikelihood2) { 
    if( i3Body ) {f2D->GetRandom2(lX,lY); lX*=2.;}// lY = acos(lY);}
    if(!i3Body )  lY=acos(iRand.Uniform(-0.5,1.));
  }
  //Sample Phi 
  double lPhi   = iRand.Uniform(0.,2.*TMath::Pi());
  //Compute  Kinematics
  double lMNN   = 0.; if(i3Body) lMNN = mass(lX,iMLep);
  double lTheta = lY; 
  //Compute variables in the rest frame
  iX      = lX/2.; if(!i3Body) iX *= 2.;
  iCosPhi = cos(lY);
  double lPRest  = restMomentum(lMNN,iMLep);
  double lGamma  = gamma       (lVec  ,lPRest,lTheta,iMLep);
  //Compute the energies
  double lETau = sqrt(lPRest*lPRest+iMLep*iMLep);
  double lENeu = sqrt(lPRest*lPRest+lMNN *lMNN );

  //Rest Frame 4 vectors
  TLorentzVector lXTau; lXTau.SetPxPyPzE( lPRest*cos(lTheta), lPRest*sin(lTheta)*cos(lPhi)            , lPRest*sin(lTheta)*sin(lPhi)            ,lETau); 
  TLorentzVector lXNeu; lXNeu.SetPxPyPzE(-lPRest*cos(lTheta), lPRest*sin(lTheta)*cos(lPhi+TMath::Pi()), lPRest*sin(lTheta)*sin(lPhi+TMath::Pi()),lENeu);  
  //Boost into lab frame
  double lBeta = beta(lGamma);
  TVector3 lBoost(lBeta,0,0); 
  lXTau.Boost(lBoost);                 
  lXNeu.Boost(lBoost);
  //Rotate in lab frame
  double lRPhi   = -lXTau.Phi();
  double lRTheta = -lXTau.Theta()-TMath::Pi()/2.;

  lXNeu.RotateZ(lRPhi);
  lXNeu.RotateY(lRTheta);
  lXTau.RotateZ(lRPhi);
  lXTau.RotateY(lRTheta);

  double lVPhi   = lVec.Phi();
  double lVTheta = lVec.Theta()+TMath::Pi()/2.;
  lXNeu.RotateY(lVTheta);
  lXNeu.RotateZ(lVPhi);
  lXTau.RotateY(lVTheta);
  lXTau.RotateZ(lVPhi);
  iTau = lVec+lXNeu;

  //Return the 4 vector
  return lXNeu;
}
void NTFit::calculateHist() { 
  fHMass->Fit("gaus","Q");
  fMass   = fHMass->GetFunction("gaus")->GetParameter(1); 
  //fMass = fHMass->GetXaxis()->GetBinCenter(fHMass->GetMaximumBin());
  
  fHPhi ->Fit("gaus","Q");
  fPhi = fHPhi->GetFunction("gaus")->GetParameter(1); 
  if(fabs(fPhi) > 2.*TMath::Pi()) fPhi = 0.;
  
  fHEta ->Fit("gaus","Q");
  fEta = fHEta->GetFunction("gaus")->GetParameter(1); 

  fHPt  ->Fit("gaus","Q");
  fPt = fHPt->GetFunction("gaus")->GetParameter(1); 
}
void NTFit::calculate() { 
  if(fCalcOption == kMean) divide();
  if(fCalcOption == kHist) calculateHist();
  fBoson.SetPtEtaPhiM(fPt, fPhi,fEta,fMass); 
  fUnc  .SetPtEtaPhiM(fHPt->GetRMS(),fHPhi->GetRMS(),fHEta->GetRMS(),fHMass->GetRMS()); //FIXME Use Quantiles
}  //if(fCalcOption == kHist) fBoson.SetPtEtaPhiM(fHPt->GetMean(),fHPhi->GetMean(),fHEta->GetMean(),fHMass->GetMean());

void NTFit::buildFourVector(int iNEvents,double iPt1,double iEta1,double iPhi1,double iM1,double iPt2,double iEta2,double iPhi2, double iM2, double iMEX,double iMEY,bool iClear) { 
  //Leptons and neutrino kinematics
  TLorentzVector lTau1,lTau2,lNu2,lNu1;
  TLorentzVector lLep1; lLep1.SetPtEtaPhiM(iPt1,iEta1,iPhi1,iM1);
  TLorentzVector lLep2; lLep2.SetPtEtaPhiM(iPt2,iEta2,iPhi2,iM2);

  //===> The Mass computation loop
  if(iClear) clearPars();
  for(int i0 = 0; i0 < iNEvents; i0++) {
    //Sample and compute the neutrinos
    lNu1 = NeutrinoToy(*fRand,fX1,fCosPhi1,lTau1,iPt1,iPhi1,iEta1,iM1,f13Body);
    lNu2 = NeutrinoToy(*fRand,fX2,fCosPhi2,lTau2,iPt2,iPhi2,iEta2,iM2,f23Body,0.);
    TLorentzVector       lSys = lTau1+lTau2;
    //Correct for MVA Met Response

  //   std::cout << "fCorrectMet " << fCorrectMet <<std::endl;
    if(fCorrectMet) { 
      double lK = (-2.8 + fResp*lSys.Pt())/lSys.Pt();
      lK = TMath::Max(lK,0.);
      lNu1 *= lK;
      lNu2 *= lK;
      lTau1 = lNu1 + lLep1;
      lTau2 = lNu2 + lLep2;
      lSys = lTau1+lTau2;
    }
    if(isnan((lNu1+lNu2).Px())) continue;
    
    //Compute MET Likelihood
    double pMEX         = (lNu1+lNu2).Px() - iMEX;
    double pMEY         = (lNu1+lNu2).Py() - iMEY;
    double lDiff        = (*fCov)(0,0)*pMEX*pMEX + (*fCov)(0,1)*pMEX*pMEY +  (*fCov)(1,0)*pMEX*pMEY + (*fCov)(1,1)*pMEY*pMEY;
    double lWeight      = fGaus->Eval(sqrt(lDiff)); 
    if(fOption == kFlat2) {lWeight *= fTempWeight; fTempWeight = 1.;}
    if(isnan(lWeight) || isinf(lWeight)) continue;
    if(fCalcOption == kMean) fillPars(lWeight,lSys);
    if(fCalcOption == kMax)  maxPars(lWeight,lSys);
    if(fCalcOption == kHist) histPars(lWeight,lSys);
  } //End of loop
  return;
}
TLorentzVector NTFit::NeutrinoToys(int iNProng,int iNJet,
				   double iD01,double iPt1,   double iPhi1,  double iEta1,double iM1,
				   double iD02,double iPt2,   double iPhi2,  double iEta2,double iM2,
				   double iMet,double iMetPhi,double iMCov00,double iMCov10,double iMCov01,double iMCov11) { 
  //Clear up stuff
  double   lMEX = iMet*cos(iMetPhi);
  double   lMEY = iMet*sin(iMetPhi);
  fGaus->SetParameter(0,1000); fGaus->SetParameter(1,0); fGaus->SetParameter(2,1.0);
  (*fCov)(0,0)  = iMCov00; (*fCov)(1,0)  = iMCov10; (*fCov)(0,1)  = iMCov01; (*fCov)(1,1)  = iMCov11;
  fCov->Invert();
  
  //Compute Some Random crap =>????
  TLorentzVector lU;    lU   .SetPtEtaPhiM(iMet,0,iMetPhi,0);
  TLorentzVector lLep1; lLep1.SetPtEtaPhiM(iPt1,0,iPhi1,  0);
  TLorentzVector lLep2; lLep2.SetPtEtaPhiM(iPt2,0,iPhi2,  0);
  lU+=lLep1; 
  lU+=lLep2;
  double lK =  lU.Pt()/(2.8 + 1.10*lU.Pt()); 
  fResp = 1;
  //   fResp = 0.9;
  //  if(iNJet == 1) fResp = 0.95;
  //   if(iNJet >  1) fResp = 1.0;
  
  fResp = 1.0;

  //double lMVis = (lLep1+lLep2).M();
  //double lFrac = TMath::Max(TMath::Min((lMVis-60.)/30.,1.),0.);  
  double lFrac = 0.;
  //Build the likelihood under higgs and Z hypothesis
  computeLikelihoodFunction(TMath::Min(fabs(iPhi1-iPhi2),2.*TMath::Pi()-fabs(iPhi1-iPhi2)),iMet,lFrac);
  buildFourVector(fNEvents,iPt1,iEta1,iPhi1,iM1,iPt2,iEta2,iPhi2,iM2,lMEX,lMEY);
  //lFrac = 1.;//TMath::Max(TMath::Min((fBoson.M()-90.)/30.,1.),0.);  
  //computeLikelihoodFunction(TMath::Min(fabs(iPhi1-iPhi2),2.*TMath::Pi()-fabs(iPhi1-iPhi2)),iMet,lFrac);
  //buildFourVector(fNEvents,iPt1,iEta1,iPhi1,iM1,iPt2,iEta2,iPhi2,iM2,lMEX,lMEY,true);
  //}
  //result?
  calculate();
  return fBoson;
}
TLorentzVector NTFit::uncVec() { 
  return fUnc;
}
///Tools
//Mass in the rest frame
double NTFit::mass(double iVal,double iMLep) { 
  double lM = sqrt(fMTau*fMTau+iMLep*iMLep-fMTau*sqrt(iVal*iVal*fMTau*fMTau+4*iMLep*iMLep));
  return lM;
} 
//Eta from theta
double NTFit::eta(double iTheta) { 
  if(iTheta >  TMath::Pi()) iTheta -= 2.*TMath::Pi();
  if(iTheta < -TMath::Pi()) iTheta += 2.*TMath::Pi();
  return -log(tan(fabs(iTheta)/2.));
}
//Momentum in the rest frame
double NTFit::restMomentum(double iMNN,double iMLep) {
  double lP = sqrt((fMTau*fMTau-(iMLep+iMNN)*(iMLep+iMNN))*(fMTau*fMTau-(iMLep-iMNN)*(iMLep-iMNN)))/2/fMTau;
  return lP;
} 
//Beta from Gamma
double NTFit::beta(double iGamma) { 
  return sqrt(iGamma*iGamma-1)/iGamma;
}
//Gamma from 4 vector with a partial approximation => b/c I'm lazy
double NTFit::gamma(TLorentzVector iVec,double iP,double iTheta,double iMLep) { 
  double lE = sqrt(iP*iP+iMLep*iMLep);
  double lGam = sqrt(iVec.P()*iVec.P()-iP*iP*sin(iTheta)*sin(iTheta))/(iP*cos(iTheta)+lE);
  lGam = sqrt(iVec.P()*iVec.P()-iP*iP*sin(iTheta)*sin(iTheta))/(iP*cos(iTheta)+beta(lGam)*lE);
  return lGam;
}

//sin Theta^2 of the energy in the restf frame
double NTFit::sinTheta2(double iGamma,double iP,double iTheta,double iM) { 
  double lE = sqrt(iP*iP+iM*iM);
  double lSin = (iP*sin(iTheta))/iGamma/(iP*cos(iTheta)+lE);
  return lSin;
}
//Momentum the lab frame
double NTFit::p         (double iGamma,double iP,double iTheta,double iM) { 
  double lE  = sqrt(iP*iP+iM*iM);
  double lPx = iGamma*(iP*cos(iTheta)+lE);
  double lPy = iP*sin(iTheta);
  return sqrt(lPx*lPx+lPy*lPy);
}
//Compute Neutrino decay from Vis vector
void NTFit::Nu(TLorentzVector &iVis,TLorentzVector &iNu,double iCos,double iPNu,double iMNN,double iPhi) { 
  double lEta = -log(tan(acos(iCos)/2.+TMath::Pi()/4.));
  iNu.SetPtEtaPhiM(iPNu*iCos,lEta,iPhi,iMNN);  iNu.SetTheta(acos(iCos));  
  iNu.RotateY(TMath::Pi()/2.);
  TVector3 lRotate = -iVis.Vect();
  iNu.RotateUz(lRotate);
}
//More stuff in labe frames
//Compute the kinematic variables
double NTFit::cosTheta(int iId,  double iPt1,double iPhi1,double iEta1,double iM1,double iPt2,double iPhi2,double iEta2,double iM2) { 
  TLorentzVector lLepVec;  lLepVec .SetPtEtaPhiM(iPt1 ,iEta1 ,iPhi1 ,0.105);
  TLorentzVector l2LepVec; l2LepVec.SetPtEtaPhiM(iPt2 ,iEta2 ,iPhi2 ,iM2);
  //Boost leptons into Tau frame
  lLepVec .Boost(-fTau1.BoostVector());
  l2LepVec.Boost(-fTau2.BoostVector());
  //double pCos1  = (lLepVec  .Px()*fTau1.Px()+lLepVec .Py()*fTau1.Py()+lLepVec .Pz()*fTau1.Pz())/fTau1.P()/lLepVec.P();
  //double pCos2  = (l2LepVec .Px()*fTau2.Px()+l2LepVec.Py()*fTau2.Py()+l2LepVec.Pz()*fTau2.Pz())/fTau2.P()/l2LepVec.P();

  //Rotate about Tau axis
  lLepVec .RotateZ(-fTau1.Phi()); 
  lLepVec .RotateY(-fTau1.Theta()-TMath::Pi()/2.); 
  l2LepVec.RotateZ(-fTau2.Phi()); 
  l2LepVec.RotateY(-fTau2.Theta()-TMath::Pi()/2.); 
  //Compute variables in Tau frame 
  double pCos1 = -lLepVec .Px()/lLepVec .P();
  double pCos2 = -l2LepVec.Px()/l2LepVec.P();
  if(iId == 0) return pCos1;
  if(iId == 1) return pCos2;
  if(iId == 2) return lLepVec .Phi();
  if(iId == 3) return l2LepVec.Phi();
  if(iId == 6) return l2LepVec.M();
  return lLepVec.P()/fMTau;
}
///////////Stupid Bookkeeping
void NTFit::fillPars(double iWeight, TLorentzVector &iSys) { 
  fTotWeight   += iWeight;
  //Usefull Polarization variables
  fX1          += iWeight*fX1;
  fX2          += iWeight*fX2;
  fCosPhi1     += iWeight*fCosPhi1; 
  fCosPhi2     += iWeight*fCosPhi2; 
  //4 Vector
  fMass        += iWeight*iSys.M();
  fPt          += iWeight*iSys.Pt();
  fPhi         += iWeight*iSys.Phi();
  fEta         += iWeight*iSys.Eta();
}
void NTFit::divide() { 
  //Usefull Polarization variables
  fX1     /=fTotWeight;
  fX2     /=fTotWeight;
  fCosPhi1/=fTotWeight;
  fCosPhi2/=fTotWeight;
  //4 Vector
  fMass   /=fTotWeight;
  fPt     /=fTotWeight;
  fPhi    /=fTotWeight;
  fEta    /=fTotWeight;
}
void NTFit::maxPars(double iWeight, TLorentzVector &iSys) { 
  if(iWeight < fTotWeight) return;
  fTotWeight   = iWeight;
  //Usefull Polarization variables
  fX1          = fX1;
  fX2          = fX2;
  fCosPhi1     = fCosPhi1; 
  fCosPhi2     = fCosPhi2; 
  //4 Vector
  fMass        = iSys.M();
  fPt          = iSys.Pt();
  fPhi         = iSys.Phi();
  fEta         = iSys.Eta();
}
void NTFit::histPars(double iWeight, TLorentzVector &iSys) { 
  //Usefull Polarization variables
  fHX1          ->Fill(fX1       ,iWeight);
  fHX2          ->Fill(fX2       ,iWeight);
  fHCosPhi1     ->Fill(fCosPhi1  ,iWeight);
  fHCosPhi2     ->Fill(fCosPhi2  ,iWeight); 
  //4 Vector
  fHMass        ->Fill(iSys.M()  ,iWeight);
  fHPt          ->Fill(iSys.Pt() ,iWeight);
  fHPhi         ->Fill(iSys.Phi(),iWeight);
  fHEta         ->Fill(iSys.Eta(),iWeight);
}
void NTFit::clear(TH1* iH) { 
  for(int i0 = 0; i0 < iH->GetNbinsX()+1; i0++) iH->SetBinContent(i0,0.);
}
void NTFit::clearPars() { 
  fTotWeight   = 0;
  //Usefull Polarization variables
  fX1          = 0;
  fX2          = 0;
  fCosPhi1     = 0;
  fCosPhi2     = 0;
  //4 Vector
  fMass        = 0;
  fPt          = 0;
  fPhi         = 0;
  fEta         = 0;
  //Histograms
  clear(fHX1);
  clear(fHX2);
  clear(fHCosPhi1);
  clear(fHCosPhi2);
  clear(fHMass);
  clear(fHPt);
  clear(fHPhi);
  clear(fHEta);
}
