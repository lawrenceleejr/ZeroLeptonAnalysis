#include "contourmacros/SUSY_mgl_vs_mlsp_all_withBand_cls_blind_onestep_Compare.C"
	 
void makecontourplots_Compare_onestep_X05(const TString& combo1 = "all", const TString& combo2 = "all", bool useShape=false) 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool doOneSigmaBand(true);
  bool show7TeVlimits(true);
  bool showfixSigXSecBand(false);
  int applyfix(0);
  bool showSR(true);
  bool blind(true);

 TString combo_XSdown= combo1;
 combo_XSdown.ReplaceAll("Nominal","Down");
 TString combo_XSup= combo1;
 combo_XSup.ReplaceAll("Nominal","Up");
 
 cout << "processing SUSY_mgl_vs_x_all_withBand_cls_blind_onestep_Compare" << endl;

 SUSY_mgl_vs_mlsp_all_withBand_cls_blind_onestep_Compare(combo1, combo2,
   combo_XSup,
   combo_XSdown,
   "","0-lepton combined", 20.3, showsignal, show7TeVlimits, discexcl=1, doOneSigmaBand, showfixSigXSecBand, channel=2, blind, showSR, useShape );

 
  return;

}



