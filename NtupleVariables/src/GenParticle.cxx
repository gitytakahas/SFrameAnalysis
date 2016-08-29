
// THIS FILE HAS BEEN GENERATED AUTOMATICALLY. DO NOT EDIT DIRECTLY, CHANGES WILL BE LOST UPON NEXT CODE GENERATION.
// Code produced by Id: CodeIt.py 494 2010-07-30 13:41:32Z svn 

#include "../include/GenParticle.h"

using namespace std;
using namespace UZH;

GenParticle::GenParticle() {
  
}


GenParticle::GenParticle( const Ntuple::GenParticleNtupleObject* ana, const Int_t idx ) 
: Basic( idx )
 , Particle() 


{
  m_ana=ana;
  // copy variables defined in Particle.h
    m_e = &((*ana->e)[idx]); 
    m_pt = &((*ana->pt)[idx]); 
    m_eta = &((*ana->eta)[idx]); 
    m_phi = &((*ana->phi)[idx]); 
    m_m = &((*ana->m)[idx]); 

  m_lvl    = ana->detailLevel;


  // copy rest of variables
  /*${ {AllNoBools:    printf("acc#name#\n"); if (ana->m_connectsucceeded[#index#]) 
         {printf("?\n"); m_#name# = &((*ana->#name#)[idx]);}
    else {printf("fak\n"); m_#name# = new #type#(); *m_#name# = #default#; } }}
  */
if(  ((ana->detailLevel & Ntuple::GenParticleBasic) == Ntuple::GenParticleBasic)  ) {
     if (ana->m_connectsucceeded[1]) m_pdgId = &((*ana->pdgId)[idx]); else m_pdgId = 0; 
    if (ana->m_connectsucceeded[2]) m_status = &((*ana->status)[idx]); else m_status = 0; 
    if (ana->m_connectsucceeded[3]) m_mother = &((*ana->mother)[idx]); else m_mother = 0; 
    if (ana->m_connectsucceeded[4]) m_nMoth = &((*ana->nMoth)[idx]); else m_nMoth = 0; 
    if (ana->m_connectsucceeded[5]) m_nDau = &((*ana->nDau)[idx]); else m_nDau = 0; 
    if (ana->m_connectsucceeded[6]) m_dau = &((*ana->dau)[idx]); else m_dau = 0; 
}







}


GenParticle::~GenParticle() {

}

ostream& operator<<( ostream& out,
                     const GenParticle& rhs ) {
  
   out << "GenParticle -" << ( Basic) rhs; 
   out << "GenParticle -" << ( Particle ) rhs; 


  ;
if(  ((rhs.getLvl() & Ntuple::GenParticleBasic) == Ntuple::GenParticleBasic)  ) {
   out << " pdgId " << rhs.pdgId();
  out << " status " << rhs.status();
  try{  out << " mother " << rhs.mother().at(0);} catch(...){std::cout<<"except: no element"<<std::endl;};
  out << " nMoth " << rhs.nMoth();
  out << " nDau " << rhs.nDau();
  try{  out << " dau " << rhs.dau().at(0);} catch(...){std::cout<<"except: no element"<<std::endl;};
;
}


  return out;
}








TLorentzVector* GenParticle::getTLV() const {

  TLorentzVector* tlv = new TLorentzVector();
  tlv->SetPtEtaPhiM(*(m_pt), *(m_eta), *(m_phi), *(m_m));
  return tlv;

}

TLorentzVector GenParticle::tlv() const {
  TLorentzVector tlv;
  tlv.SetPtEtaPhiM(*(m_pt), *(m_eta), *(m_phi), *(m_m));
  return tlv;
}







  floatingnumber GenParticle::DeltaR(const GenParticle& p) const {
    return this->tlv().DeltaR(p.tlv());
  }

