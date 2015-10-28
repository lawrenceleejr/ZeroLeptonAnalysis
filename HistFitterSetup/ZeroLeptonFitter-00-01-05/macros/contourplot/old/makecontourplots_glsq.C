#include "contourmacros/SUSY_mgl_vs_msq_all_withBand_cls_blind.C"

void makecontourplots_glsq(const TString& combo = "all") 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool showtevatron(true);
  bool showcms(false);
  bool doOneSigmaBand(true);
  bool showfixSigXSecBand(true);
  int applyfix(0);

  // simple channel contour plot


  (void) SUSY_mgl_vs_msq_all_withBand_cls("ZL2012_final_toy_msugra_combined_msugra_0_10_P_fixSigXSecNominal_merged_hypotest__1_harvest_list_glsq.root",
                                          "ZL2012_final_toy_msugra_combined_msugra_0_10_P_fixSigXSecUp_merged_hypotest__1_harvest_list_glsq.root",
                                          "ZL2012_final_toy_msugra_combined_msugra_0_10_P_fixSigXSecDown_merged_hypotest__1_harvest_list_glsq.root",
                                          "","0-lepton combined", 5.835, showsignal, discexcl=1, showtevatron, showcms, doOneSigmaBand, showfixSigXSecBand, channel=2 );

  
  return;
}



