//#include "contourmacros/SUSY_bRPV_m0_vs_m12_all_withBand_cls_blind.C"
#include "contourmacros/SUSY_bRPV_m0_vs_m12_all_withBand_cls.C"

void makecontourplots_bRPV(const TString& combo = "all", const TString& gridName="", const bool useShape=false) {
  bool showsignal(false);
  int  discexcl=1; // 0=discovery, 1=exclusion
  bool showtevatron(false);
  bool showcms(false);
  bool doOneSigmaBand(true);
  bool showfixSigXSecBand(true);
  bool showSR(false);

  TString comboUp(combo);
  TString comboDown(combo);

  comboUp.ReplaceAll("Nominal", "Up");
  comboDown.ReplaceAll("Nominal", "Down");

  (void) SUSY_bRPV_m0_vs_m12_all_withBand_cls(combo,
                                         comboUp,
                                         comboDown,
                                         gridName,
                                        "",
                                        20.3, showsignal, discexcl, showtevatron, showcms, doOneSigmaBand, showSR, useShape);

  
  return;
}



