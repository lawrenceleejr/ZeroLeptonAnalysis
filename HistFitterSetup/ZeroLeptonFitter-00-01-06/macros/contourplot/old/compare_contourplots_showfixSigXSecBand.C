#include <vector>
#include "contourmacros/compare_SUSY_m0_vs_m12_all_withBand_cls_showfixSigXSecBand.C"

void compare_contourplots_showfixSigXSecBand(const TString& combo = "all") 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool showtevatron(false);
  bool showcms(false);
  bool doOneSigmaBand(false);
  bool showfixSigXSecBand(true);
  int applyfix(0);
  vector<TString> infilelist;

  TString regions[5] = {"SRA", "SRB", "SRC", "SRD", "SRE"};
  for(int i=0; i<5; i++){
     infilelist.push_back("ZL2011_"+regions[i]+"tight_hypotest__1_harvest_list.root");
     cout<< infilelist[i];
  }
  
  // simple channel contour plot
  (void) compare_SUSY_m0_vs_m12_all_withBand_cls_showfixSigXSecBand(
     infilelist.at(0), infilelist.at(1),
     infilelist.at(2), infilelist.at(3), infilelist.at(4),
     "Simple channel example", 5,
     showsignal, discexcl=1,
     showtevatron, showcms, doOneSigmaBand, showfixSigXSecBand, channel=2 );
}

