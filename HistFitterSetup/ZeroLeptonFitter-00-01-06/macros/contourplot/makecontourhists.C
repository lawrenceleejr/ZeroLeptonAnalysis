#include "contourmacros/SM_GG_onestep_mgluino_vs_x_nofloat.C"
#include "contourmacros/SM_GG_onestep_mgluino_vs_mlsp_nofloat.C"
////#include "contourmacros/MUED_OneOverR_vs_LambdaR_nofloat.C"
#include "contourmacros/m0_vs_m12_nofloat.C"
//#include "contourmacros/pMSSM_qL_to_h_nofloat.C"
//#include "contourmacros/m12_vs_m0_nofloat.C"
//#include "contourmacros/mgl_vs_mlsp_nofloat.C"
//#include "contourmacros/mgl_vs_msq_nofloat.C"

///ls ZL2012*final*_*list*  | awk   '{printf(const char"const char* ehistfile = m0_vs_m12_nofloat(\"%s\");  \n"),$1}'

void makecontourhists(const TString& combo = "all", const TString& gridName = "msugra")  {
  //    gSystem->AddIncludePath("-I$ZEROLEPTONFITTER/macros/contourplot/contourmacros");

    //gROOT->ProcessLine(".L contourmacros/SM_GG_onestep_mgluino_vs_x_nofloat.C");
    //gSystem->Load("contourmacros/SM_GG_onestep_mgluino_vs_mlsp_nofloat.C");
    //gSystem->Load("contourmacros/MUED_OneOverR_vs_LambdaR_nofloat.C");
    //gSystem->Load("contourmacros/m0_vs_m12_nofloat.C");
    //gSystem->Load("contourmacros/mgl_vs_msq_nofloat.C");

    // if(gridName=="SM_GG_onestep_LSP60") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_x_nofloat(combo);
    // else if(gridName=="SM_SS_onestep_LSP60") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_x_nofloat(combo);
    if(gridName=="SM_GG_onestep_X05") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_mlsp_nofloat(combo);
    else if(gridName=="SM_SS_onestep_X05") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_mlsp_nofloat(combo);
    else if(gridName=="SM_GG_twostep_WWZZ") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_mlsp_nofloat(combo);
    else if(gridName=="SM_SS_twostep_WWZZ") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_mlsp_nofloat(combo);
    // else if(gridName=="pMSSM_qL_to_h_M160") const char* ehistfile3 = pMSSM_qL_to_h_nofloat(combo);
    // else if(gridName=="pMSSM_qL_to_h_M1M2") const char* ehistfile3 = pMSSM_qL_to_h_nofloat(combo);
    //    else if(gridName=="MUED") const char* ehistfile3 = MUED_OneOverR_vs_LambdaR_nofloat(combo);
    //    else if(gridName=="mssm") const char* ehistfile3 = mgl_vs_msq_nofloat(combo);
    else if(gridName=="GG_onestepCC") const char* ehistfile3 = SM_GG_onestep_mgluino_vs_mlsp_nofloat(combo);
    else const char* ehistfile3 = m0_vs_m12_nofloat(combo);


    return;

}

