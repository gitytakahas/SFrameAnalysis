In order to load the SVFit library when running a job configuration,
add the following line into your config.xml after <JobConfiguration ...>:
 <Library Name="libSVFit"/>

Here are two example pieces of code to run the two SVFit version in your code, assuming lepton1 as hadronic tau and lepton2 as leptonic tau:


STANDALONE (Htautau analysis):

#include "../SVFit/include/NSVfitStandaloneAlgorithm.h"

    NSVfitStandalone::Vector measuredMET(met *TMath::Cos(met_phi), met *TMath::Sin(met_phi), 0); 
    // setup measure tau lepton vectors 
    NSVfitStandalone::LorentzVector l1(lep1.Px(), lep1.Py(), lep1.Pz(), TMath::Sqrt(lep1.M()*lep1.M()+lep1.Px()*lep1.Px()+lep1.Py()*lep1.Py()+lep1.Pz()*lep1.Pz()));
    NSVfitStandalone::LorentzVector l2(lep2.Px(), lep2.Py(), lep2.Pz(), TMath::Sqrt(lep2.M()*lep2.M()+lep2.Px()*lep2.Px()+lep2.Py()*lep2.Py()+lep2.Pz()*lep2.Pz()));
    std::vector<NSVfitStandalone::MeasuredTauLepton> measuredTauLeptons;
    measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kHadDecay, l1));
    measuredTauLeptons.push_back(NSVfitStandalone::MeasuredTauLepton(NSVfitStandalone::kLepDecay, l2));
    // construct the class object from the minimal necesarry information
    NSVfitStandaloneAlgorithm algo(measuredTauLeptons, measuredMET, covMETraw, 1);
    // apply customized configurations if wanted (examples are given below)
    //algo.maxObjFunctionCalls(5000);
    algo.addLogM(false);
    //algo.metPower(0.5)
    //algo.fit();
    // integration by VEGAS (same as function algo.integrate() that has been in use when markov chain integration had not yet been implemented)
    //algo.integrateVEGAS();
    // integration by markov chain MC
    algo.integrateMarkovChain();
    if(algo.isValidSolution()){
      std::cout << "... m svfit : " << algo.getMass() << "+/-" << algo.massUncert() << std::endl;
      std::cout << "... pt svfit : " << algo.pt() << std::endl;
    }
    else{
      std::cout << "... m svfit : ---" << std::endl;
    }



NTFIT (Phil Harris):

#include "../SVFit/include/NTFit.h"

   NTFitSemileptonic = new  NTFit(1,"/shome/cgalloni/TAU/ExoDiBosonAnalysis/data/params.root",// NTFit::kHistLikelihood,NTFit::kMax//
				  NTFit::kFlat,   NTFit::kMean
				  , 5000);

  float lcov00 =  covMETraw[0][0];
  float lcov10 =  covMETraw[1][0];
  float lcov01 =  covMETraw[0][1];
  float lcov11 =  covMETraw[1][1];

  TLorentzVector   lBoson4;

    lBoson4 = NTFitSemileptonic->NeutrinoToys(nJets,nJets,
								  -1,lep1.Pt(),lep1.Phi(),lep1.Eta(),lep1.M(),
								  -1,lep2.Pt(),lep2.Phi(),lep2.Eta(),lep2.M(),
								  met,met_phi,lcov00,lcov10,lcov10,lcov11);
   std::cout << "Channel"<< Channel_<< " lep1 MAss "<< lep1.M()<<  " lep2 mass " << lep2.M() << std::endl;
   std::cout << "lBoson4.M() (njets=2)" << lBoson4.M() << std::endl; 
   std::cout << "lBoson4.Pt() (njets=2)" << lBoson4.Pt() << std::endl; 

