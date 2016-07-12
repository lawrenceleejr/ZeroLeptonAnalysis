#include "contourmacros/SUSY_mgl_vs_x_all_withBand_cls_blind_onestep.C"
	 
void makecontourplots_onestep_LSP60(const TString& combo = "all", bool useShape=false) 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool doOneSigmaBand(true);
  bool show7TeVlimits(true);
  bool showfixSigXSecBand(true);
  int applyfix(0);
  bool showSR(true);
  bool blind(false);

 TString combo_XSdown= combo;
 combo_XSdown.ReplaceAll("Nominal","Down");
 TString combo_XSup= combo;
 combo_XSup.ReplaceAll("Nominal","Up");

 SUSY_mgl_vs_x_all_withBand_cls_blind_onestep(combo,
   combo_XSup,
   combo_XSdown,
   "",
	 "0-lepton, 2-6 jets", 20.3, showsignal, show7TeVlimits, discexcl=1, doOneSigmaBand, showfixSigXSecBand, channel=2, blind, showSR, useShape );

 
  return;

}



