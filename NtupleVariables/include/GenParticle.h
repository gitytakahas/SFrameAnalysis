
// THIS FILE HAS BEEN GENERATED AUTOMATICALLY. DO NOT EDIT DIRECTLY, CHANGES WILL BE LOST UPON NEXT CODE GENERATION.
// Code produced by Id: CodeIt.py 494 2010-07-30 13:41:32Z svn 

#ifndef __UZHTOP_GenParticle_H__
#define __UZHTOP_GenParticle_H__

#include <cmath>
#include "Particle.h"
#include <vector>
#include "GenParticleNtupleObject.h"



namespace Ntuple {
  class GenParticleNtupleObject;
}

namespace UZH {
  
  /**
   *  @short Class that maps GenParticleNtupleObjects to GenParticle Particle class
   *
   *         This class can be used to map the offline GenParticle information from
   *         GenParticleNtupleObjects to UZH::GenParticle class. All particles inherit 
   *         from UZH::Particle.
   *
   * @author Code produced by Id: CodeIt.py 494 2010-07-30 13:41:32Z svn 
   *
   */

  class GenParticle : public Basic 
 , public Particle 
  {
  public:

    /// default c'tor
    GenParticle();
    /// default d'tor
    ~GenParticle();
    
    /// c'tor with index
    GenParticle( const Ntuple::GenParticleNtupleObject* ana, const Int_t idx );

    TLorentzVector* getTLV() const;
    TLorentzVector tlv() const;


    floatingnumber DeltaR(const GenParticle& p) const;

    
    // variable definitions



    int* m_pdgId;
    int* m_status;
    std::vector<int>* m_mother;
    int* m_nMoth;
    int* m_nDau;
    std::vector<int>* m_dau;







    // check level given here must be consistent with ...NtupleObject.cxx, otherwise you'll get a segfault
    int pdgId() const { /*if(!m_ana->getConnectSucceeded(Ntuple::GenParticleNtupleObject::kpdgId)) std::cout<<"pdgId not connected!"<<std::endl;*/ return *(m_pdgId); } 
    int status() const { /*if(!m_ana->getConnectSucceeded(Ntuple::GenParticleNtupleObject::kstatus)) std::cout<<"status not connected!"<<std::endl;*/ return *(m_status); } 
    std::vector<int> mother() const { /*if(!m_ana->getConnectSucceeded(Ntuple::GenParticleNtupleObject::kmother)) std::cout<<"mother not connected!"<<std::endl;*/ return *(m_mother); } 
    int nMoth() const { /*if(!m_ana->getConnectSucceeded(Ntuple::GenParticleNtupleObject::knMoth)) std::cout<<"nMoth not connected!"<<std::endl;*/ return *(m_nMoth); } 
    int nDau() const { /*if(!m_ana->getConnectSucceeded(Ntuple::GenParticleNtupleObject::knDau)) std::cout<<"nDau not connected!"<<std::endl;*/ return *(m_nDau); } 
    std::vector<int> dau() const { /*if(!m_ana->getConnectSucceeded(Ntuple::GenParticleNtupleObject::kdau)) std::cout<<"dau not connected!"<<std::endl;*/ return *(m_dau); } 
    
    void pdgId( const int& val){ *(m_pdgId)=val; } 
    void status( const int& val){ *(m_status)=val; } 
    void mother( const std::vector<int>& val){ *(m_mother)=val; } 
    void nMoth( const int& val){ *(m_nMoth)=val; } 
    void nDau( const int& val){ *(m_nDau)=val; } 
    void dau( const std::vector<int>& val){ *(m_dau)=val; } 
    

  private:
    const Ntuple::GenParticleNtupleObject* m_ana;
  }; // class GenParticle

  typedef std::vector< GenParticle > GenParticleVec;
  typedef std::vector< GenParticle >::iterator GenParticleVecIt;
  typedef std::vector< GenParticle >::const_iterator GenParticleVecConstIt;





} // end of namespace UZH

/// output stream operator overloaded for GenParticle objects
std::ostream& operator<<( std::ostream& out,
                          const UZH::GenParticle& rhs );


#endif //__UZH_GenParticle_H__
