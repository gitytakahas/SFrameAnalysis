// Generator level info data object
struct TGenData
{
  UInt_t  njet;                       // number of photons
  Float_t scalePdf;                   // pdf scale sqrt(Q^2)  
  Float_t weight;                     // event weight
  Float_t vmass, vpt, vy, vphi;       // boson kinematics
  Float_t vpx, vpy, vpz;              // boson kinematics
  Float_t x_1, x_2;                   // parton momentum fraction
  Int_t   id_1, id_2;                 // parton PDG ID
  Float_t aqcd, aqed;                 // QCD, QED coupling constants
  Float_t jetpt_1, jeteta_1, jetphi_1;      // "jet" kinematics
  //  Int_t   jetid_1;                      // "jet" PDG ID
  Float_t jetpt_2, jeteta_2, jetphi_2;      // "jet" kinematics
  //  Int_t   jetid_2;                      // "jet" PDG ID
  Float_t mjj, dphi, deta, dR;        // dijet mass, dijet dphi
};
