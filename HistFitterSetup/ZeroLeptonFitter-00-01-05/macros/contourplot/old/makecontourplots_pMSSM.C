#include "contourmacros/SUSY_mgl_vs_msq_all_withBand_cls_blind_forpMSSM.C"

void makecontourplots_pMSSM(const TString& combo = "all") 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool showtevatron(true);
  bool showcms(false);
  bool doOneSigmaBand(true);
  bool showfixSigXSecBand(true);
  int applyfix(0);

  (void) SUSY_mgl_vs_msq_all_withBand_cls_blind_forpMSSM("ZL2012_final_toy_combined_SM_SG_pMSSM0_fixSigXSecNominal_merged_list_wfitfailed.root",
                                                         "ZL2012_final_toy_combined_SM_SG_pMSSM0_fixSigXSecUp_merged_list_wfitfailed.root",
                                                         "ZL2012_final_toy_combined_SM_SG_pMSSM0_fixSigXSecDown_merged_list_wfitfailed.root",
                                                         "","0-lepton combined", 5.835, showsignal, discexcl=1, showtevatron, showcms, doOneSigmaBand, showfixSigXSecBand, channel=2 );

  return;
  
  
}



