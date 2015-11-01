#include "contourmacros/MUED_R_vs_RLambda_all_withBand_cls_blind.C"
	 
void makecontourplots_MUED(const TString& combo = "all", bool useShape=false) 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool doOneSigmaBand(true);
  bool show7TeVlimits(false);
  bool showfixSigXSecBand(false);
  int applyfix(0);
  bool showSR(true);
  bool blind(false);

 MUED_R_vs_RLambda_all_withBand_cls_blind(combo,
   "",
   "",
   "",
	 "0-lepton, 2-6 jets", 20.3, showsignal, show7TeVlimits, discexcl=1, doOneSigmaBand, showfixSigXSecBand, channel=2, blind, showSR, useShape );

 
  return;

}



