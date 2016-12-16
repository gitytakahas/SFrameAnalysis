//#if !defined(__CINT__) || defined(__MAKECINT__)
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <TBenchmark.h>
#include <TSystem.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <TLorentzVector.h>
#include <assert.h>
	     //#endif

#include "GenStructDefs.hh"
TGenData data;

Float_t deltaPhi(Float_t p1, Float_t p2){
  Float_t res = p1 - p2;
  while(res > TMath::Pi()){
    res -= 2*TMath::Pi();
  }
  while(res < -TMath::Pi()){
    res += 2*TMath::Pi();
  }

  return res;
}


Float_t deltaR(Float_t de, Float_t dp){
  return TMath::Sqrt(de*de + dp*dp);
}


void parselhe(//const char *infile="GF8TeV.mjj200.alpha0.00.part06.lhe",
	      TString infile="lhe_files/HTT_11_pythia.lhe",
	      TString ofile="Myroot.root",
	      UInt_t entries=50000)
{
  std::cout << ">>> " << infile << std::endl;
  std::cout << ">>> input  file = " << infile << std::endl;
  std::cout << ">>> output file = " << ofile << std::endl;

  gBenchmark->Start("readlhe");

  ifstream ifs;
  ifs.open(infile);
  assert(ifs.is_open());
  string line;

  // skip the intro up until <init>
  do {
    getline(ifs,line);
  } while (line.compare("<init>") != 0);

  //  std::cout << "Read LHE files end." << std::endl;
  TFile *outfile = new TFile(ofile,"recreate");
  TTree* tree = new TTree("Events","Events");  
  tree->Branch("Events",&data,
	       "njet/i:scalePdf/F:weight:vmass:vpt:vy:vphi:vpx:vpy:vpz:x_1:x_2:id_1/I:id_2/I:aqcd/F:aqed:jetpt_1:jeteta_1:jetphi_1:jetpt_2:jeteta_2:jetphi_2:mjj/F:dphi/F:deta/F:dR/F"); //:dR_tm 

  // get the info in <init>
  getline(ifs,line);
  stringstream ssinit1(line);
  int idbmup1, idbmup2; 
  double ebmup1, ebmup2; 
  int pdfgup1, pdfgup2, pdfsup1, pdfsup2, idwtup, nprup;
  ssinit1 >> idbmup1 >> idbmup2 >> ebmup1 >> ebmup2 >> pdfgup1 >> pdfgup2 >> pdfsup1 >> pdfsup2 >> idwtup >> nprup;
  
  getline(ifs,line);
  stringstream ssinit2(line);
  double xsecup, xerrup, xmaxup;
  int lprup;
  ssinit2 >> xsecup >> xerrup >> xmaxup >> lprup;
    
  getline(ifs,line);
  //  std::cout << line << std::endl; </init>
  //  getline(ifs,line);
  //  std::cout << line << std::endl; <event>
  //  getline(ifs,line); // one more step to initiate the if loop

  while(getline(ifs,line)) {    
    if(line.compare("<event>")==0) {//fCount++;
    
      getline(ifs,line); // lhefile << line << endl; 
      stringstream sshead(line);
      int nup, idprup;
      double xwgtup, scalup, aqedup, aqcdup;
      sshead >> nup >> idprup >> xwgtup >> scalup >> aqedup >> aqcdup;
      data.scalePdf = scalup;
      data.weight   = xwgtup;
      data.aqcd     = aqcdup;
      data.aqed     = aqedup;

      //      std::cout << "scale " << line << std::endl;

      int idup, istup, mothup1, mothup2, icolup1, icolup2; 
      double  pup1, pup2, pup3, pup4, pup5, vtimup, spinup;
      TLorentzVector pbos, pjet;
      std::vector<TLorentzVector> tl;
      

      // parton 1:
      getline(ifs,line); // lhefile << line << endl; 
      stringstream ssp1(line);
      ssp1 >> idup >> istup >> mothup1 >> mothup2 >> icolup1 >> icolup2 >> pup1 >> pup2 >> pup3 >> pup4 >> pup5 >> vtimup >> spinup;
      data.x_1  = fabs(pup3/ebmup1); // pz/beam1E
      data.id_1 = idup; // parton1 pdgid
      //std::cout << "PDF1 " << line << std::endl;

      // parton 2:
      getline(ifs,line); // lhefile << line << endl; 
      stringstream ssp2(line);
      ssp2 >> idup >> istup >> mothup1 >> mothup2 >> icolup1 >> icolup2 >> pup1 >> pup2 >> pup3 >> pup4 >> pup5 >> vtimup >> spinup;
      data.x_2  = fabs(pup3/ebmup2); // pz/beam2E
      data.id_2 = idup;
      //std::cout << "PDF2 " << line << std::endl;

      data.njet   = 0;
      //data.jetpt  = 0;
      
      getline(ifs,line); //lhefile << line << endl; 

      while(line.compare("</event>") != 0) {
        
	    stringstream ssfinal(line);
	    ssfinal >> idup >> istup >> mothup1 >> mothup2 >> icolup1 >> icolup2 >> pup1 >> pup2 >> pup3 >> pup4 >> pup5 >> vtimup >> spinup;
        
	    if(idup==21 || (fabs(idup)>0 && fabs(idup)<6)) { // jets!
	      pjet.SetPxPyPzE(pup1,pup2,pup3,pup4);
	      //if(data.jetpt < pjet.Pt()) {
          //  data.jetid  = idup;
          //  data.jetpt  = pjet.Pt();
          //  data.jeteta = pjet.Eta();
          //  data.jetphi = pjet.Phi();
          //}
          tl.push_back(pjet);
          data.njet++;
        }else if(idup==25 || idup==35){ // Higgs 
          pbos.SetPxPyPzE(pup1,pup2,pup3,pup4);
          data.vmass = pbos.M();
          data.vpt   = pbos.Pt();
          data.vy    = pbos.Rapidity();
          data.vpx   = pbos.Px();
          data.vpy   = pbos.Py();
          data.vpz   = pbos.Pz();
          data.vphi  = pbos.Phi();
        }
        
	    getline(ifs,line); //lhefile << line << endl; 
      }

    if(tl.size()==2){
      TLorentzVector alljet = tl[0] + tl[1];
      //std::cout << "M = " << alljet.M() << " dphi = " << tl[0].Phi() - tl[1].Phi() << std::endl;
      data.mjj = Float_t(alljet.M());
      data.dphi = deltaPhi(tl[0].Phi(), tl[1].Phi());
      data.deta = TMath::Abs(tl[0].Eta() - tl[1].Eta());
      data.dR = deltaR(data.deta, data.dphi);
    
      data.jetpt_1 = tl[0].Pt();
      data.jeteta_1 = tl[0].Eta();
      data.jetphi_1 = tl[0].Phi();
      data.jetpt_2 = tl[1].Pt();
      data.jeteta_2 = tl[1].Eta();
      data.jetphi_2 = tl[1].Phi();

      //std::cout << data.dphi << " " << deltaPhi(tl[0].Phi(), tl[1].Phi()) << " "
      //		  << data.deta << " " << TMath::Abs(tl[0].Eta() - tl[1].Eta()) << " " 
      //		  << data.dR << std::endl;

      }
      
      tree->Fill();
    }
    //if(entries>0 && tree->GetEntries()>entries) break;
  }
  
  ifs.close();
  tree->Print();
  outfile->Write();
  outfile->Close();
  gBenchmark->Show("readlhe");
  
}
