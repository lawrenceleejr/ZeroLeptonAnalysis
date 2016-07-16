
// cannot change the order of include
#include "summary_harvest_tree_description.h"
// #include "contourmacros/m0_vs_m12_nofloat.C"
// #include "contourmacros/SM_GG_onestep_mgluino_vs_mlsp_nofloat.C"
#include "contourmacros/mX_vs_mY_nofloat.C"

void makecontourhists(const TString& combo = "all", const TString& gridName = "msugra")  {

  std::cout<<" makecontourhists : Start! "<<std::endl;
  if(gridName=="GG_onestepCC" && 0 ){
    const char* ehistfile = mX_vs_mY_nofloat(combo, 0, "mgluinomlsp_nofloat.root", "mgluino", "mlsp", 100, 100, 0, 1600, 0, 1600);
  }else if(gridName=="SS_onestepCC" && 0 ){
    const char* ehistfile = mX_vs_mY_nofloat(combo, 0, "msquarkmlsp_nofloat.root", "msquark", "mlsp", 100, 100, 0, 1600, 0, 1600);
  }else if(gridName=="SM_GG_N2" && 0 ){
    const char* ehistfile = mX_vs_mY_nofloat(combo, 0, "mgluinomlsp2_nofloat.root", "mgluino", "mlsp2", 100, 100, 0, 1600, 0, 1600);
  }else{
    const char* ehistfile = mX_vs_mY_nofloat(combo, 0, "m0m12_nofloat.root", "m0", "m12", 1000, 1000, 0, 1600, 0, 1600);
  }

  return;
}

