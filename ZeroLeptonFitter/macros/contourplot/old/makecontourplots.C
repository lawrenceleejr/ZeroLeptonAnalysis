#include "contourmacros/SUSY_m0_vs_m12_all_withBand_cls_unblind.C"


void makecontourplots(const TString& combo = "all") 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool showtevatron(true);
  bool showcms(false);
  bool doOneSigmaBand(false);
  bool showfixSigXSecBand(false);
  int applyfix(0);



  //(void) SUSY_m0_vs_m12_all_withBand_cls("ZL2012_final_toy_msugra_combined_msugra_0_10_P_fixSigXSecNominal_merged_hypotest__1_harvest_list.root",
                                         //"ZL2012_final_toy_msugra_combined_msugra_0_10_P_fixSigXSecUp_merged_hypotest__1_harvest_list.root",
                                         //"ZL2012_final_toy_msugra_combined_msugra_0_10_P_fixSigXSecDown_merged_hypotest__1_harvest_list.root",
                                         //"","0-lepton combined", 5.835, showsignal, discexcl=1, showtevatron, showcms, doOneSigmaBand, showfixSigXSecBand, channel=2 );

  (void) SUSY_m0_vs_m12_all_withBand_cls("msugra_SREtight_fixSigXSecNominal__1_harvest_list.root",
                                         "msugra_SREtight_fixSigXSecUp__1_harvest_list.root",
                                         "msugra_SREtight_fixSigXSecDown__1_harvest_list.root",
                                         "","0-lepton 5-bin SRE tight, shapefactor", 5.835, showsignal, discexcl=1, showtevatron, showcms, doOneSigmaBand, showfixSigXSecBand, channel=2 );

  return;

}



