// Dear emacs, this is -*- c++ -*-
// $Id: D3PDVariables_LinkDef.h 36487 2011-08-08 13:12:51Z luzgomez $
#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ nestedclass;

// Add the declarations of your cycles, and any other classes for which you
// want to generate a dictionary, here. The usual format is:
//
// #pragma link C++ class MySuperClass+;
#pragma link C++ class vector<vector<float> >;
#pragma link C++ class vector<vector<unsigned int> >;
#pragma link C++ class vector<vector<int> >;

#endif // __CINT__
