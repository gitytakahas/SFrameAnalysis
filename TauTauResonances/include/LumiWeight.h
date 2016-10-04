#ifndef LumiWeight_H
#define LumiWeight_H

#include <string>
#include <vector>

#include "TString.h"

class LumiWeight{

public:
   LumiWeight( void );
   ~LumiWeight( void );
   
   double getLumiWeight( TString sample );

private:

   double genEvents_ ;
   double xSec_      ;
    
};

#endif //LumiWeight_H
