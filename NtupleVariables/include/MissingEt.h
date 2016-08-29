
// THIS FILE HAS BEEN GENERATED AUTOMATICALLY. DO NOT EDIT DIRECTLY, CHANGES WILL BE LOST UPON NEXT CODE GENERATION.
// Code produced by Id: CodeIt.py 494 2010-07-30 13:41:32Z svn 

#ifndef __UZHTOP_MissingEt_H__
#define __UZHTOP_MissingEt_H__

#include <cmath>
#include "Particle.h"
#include <vector>
#include "MissingEtNtupleObject.h"



namespace Ntuple {
  class MissingEtNtupleObject;
}

namespace UZH {
  
  /**
   *  @short Class that maps MissingEtNtupleObjects to MissingEt Particle class
   *
   *         This class can be used to map the offline MissingEt information from
   *         MissingEtNtupleObjects to UZH::MissingEt class. All particles inherit 
   *         from UZH::Particle.
   *
   * @author Code produced by Id: CodeIt.py 494 2010-07-30 13:41:32Z svn 
   *
   */

  class MissingEt : public Basic 

  {
  public:

    /// default c'tor
    MissingEt();
    /// default d'tor
    ~MissingEt();
    
    /// c'tor with index
    MissingEt( const Ntuple::MissingEtNtupleObject* ana, const Int_t idx );


    
    // variable definitions



    floatingnumber* m_corrPx;
    floatingnumber* m_corrPy;
    floatingnumber* m_significance;
    floatingnumber* m_cov00;
    floatingnumber* m_cov10;
    floatingnumber* m_cov11;
    floatingnumber* m_et;
    floatingnumber* m_phi;
    floatingnumber* m_sumEt;







    // check level given here must be consistent with ...NtupleObject.cxx, otherwise you'll get a segfault
    floatingnumber corrPx() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::kcorrPx)) std::cout<<"corrPx not connected!"<<std::endl;*/ return *(m_corrPx); } 
    floatingnumber corrPy() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::kcorrPy)) std::cout<<"corrPy not connected!"<<std::endl;*/ return *(m_corrPy); } 
    floatingnumber significance() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::ksignificance)) std::cout<<"significance not connected!"<<std::endl;*/ return *(m_significance); } 
    floatingnumber cov00() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::kcov00)) std::cout<<"cov00 not connected!"<<std::endl;*/ return *(m_cov00); } 
    floatingnumber cov10() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::kcov10)) std::cout<<"cov10 not connected!"<<std::endl;*/ return *(m_cov10); } 
    floatingnumber cov11() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::kcov11)) std::cout<<"cov11 not connected!"<<std::endl;*/ return *(m_cov11); } 
    floatingnumber et() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::ket)) std::cout<<"et not connected!"<<std::endl;*/ return *(m_et); } 
    floatingnumber phi() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::kphi)) std::cout<<"phi not connected!"<<std::endl;*/ return *(m_phi); } 
    floatingnumber sumEt() const { /*if(!m_ana->getConnectSucceeded(Ntuple::MissingEtNtupleObject::ksumEt)) std::cout<<"sumEt not connected!"<<std::endl;*/ return *(m_sumEt); } 
    
    void corrPx( const floatingnumber& val){ *(m_corrPx)=val; } 
    void corrPy( const floatingnumber& val){ *(m_corrPy)=val; } 
    void significance( const floatingnumber& val){ *(m_significance)=val; } 
    void cov00( const floatingnumber& val){ *(m_cov00)=val; } 
    void cov10( const floatingnumber& val){ *(m_cov10)=val; } 
    void cov11( const floatingnumber& val){ *(m_cov11)=val; } 
    void et( const floatingnumber& val){ *(m_et)=val; } 
    void phi( const floatingnumber& val){ *(m_phi)=val; } 
    void sumEt( const floatingnumber& val){ *(m_sumEt)=val; } 
    

  private:
    const Ntuple::MissingEtNtupleObject* m_ana;
  }; // class MissingEt

  typedef std::vector< MissingEt > MissingEtVec;
  typedef std::vector< MissingEt >::iterator MissingEtVecIt;
  typedef std::vector< MissingEt >::const_iterator MissingEtVecConstIt;





} // end of namespace UZH

/// output stream operator overloaded for MissingEt objects
std::ostream& operator<<( std::ostream& out,
                          const UZH::MissingEt& rhs );


#endif //__UZH_MissingEt_H__
