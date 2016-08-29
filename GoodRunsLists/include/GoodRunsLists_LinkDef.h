// Dear emacs, this is -*- c++ -*-
// $Id: GoodRunsLists_LinkDef.h 45093 2010-08-20 11:58:27Z krasznaa $
#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class Root::TLumiBlockRange+;

#pragma link C++ class std::vector<Root::TLumiBlockRange>+;
#pragma link C++ class Root::TGoodRun+;

#pragma link C++ class std::pair<Int_t,Root::TGoodRun>+;
#pragma link C++ class std::map<Int_t,Root::TGoodRun>+;
#pragma link C++ class std::pair<TString,TString>+;
#pragma link C++ class std::map<TString,TString>+;
#pragma link C++ class Root::TGoodRunsList+;

#pragma link C++ class Root::TGRLCollection+;

#endif // __CINT__
