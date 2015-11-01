#include "contourmacros/SUSY_mH1sq_vs_m12_all_withBand_cls_blind_forNUHMG.C"
//#include "contourmacros/SUSY_mgl_vs_msq_all_withBand_cls_blind_forNUHMG.C"

void makecontourplots_NUHMG(const TString& combo = "all",  bool useShape=false) 
{

  bool showsignal(false);
  int  discexcl(1); // 0=discovery, 1=exclusion
  bool doOneSigmaBand(true);
  bool show7TeVlimits(false);
  bool showfixSigXSecBand(false);
  int applyfix(0);
  bool showSR(true);
  bool blind(false);
  //bool blind(true);

  SUSY_mH1sq_vs_m12_all_withBand_cls_blind_forNUHMG("Outputs/NUHMG_combined_fixSigXSecNominal__1_harvest_list.root",
													"Outputs/NUHMG_combined_fixSigXSecUp__1_harvest_list.root",
													"Outputs/NUHMG_combined_fixSigXSecDown__1_harvest_list.root",
													//"",
													//"",
													"",
													"0-lepton combined", 20.3, showsignal,show7TeVlimits, discexcl=1, 
													doOneSigmaBand, showfixSigXSecBand, channel=2, blind, showSR, useShape );

  return;
}



