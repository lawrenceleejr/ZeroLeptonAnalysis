#include <vector>
#include "contourmacros/SUSY_contourplots.C"

void makecontourplots_CLs(const TString& combo = "all") 
{
  bool showsignal(false);
  int  discexcl; // 0=discovery, 1=exclusion
  bool showtevatron(false);
  bool showcms(false);
  bool doOneSigmaBand(false);
  bool showfixSigXSecBand(false);
  int applyfix(0);
  bool showSR(true); 
  vector<TString> infilelist;
  vector<TString> inlist;
  
  TString Grid="GG_direct";

  // XSec Nominal Up Down
  TString combined[3]={"combined_fixSigXSecNominal", "combined_fixSigXSecNominal","combined_fixSigXSecNominal"};
  TString dirname="3.2ifb"; 

  TString listSuffix="__1_harvest_list";
  if(Grid=="GG_onestepCC"){
     listSuffix="__mlspNE60_harvest_list";
  }
  
  for(int i=0; i<3; i++){
     infilelist.push_back("Outputs/"+dirname+"/"+Grid+"_"+combined[i]+listSuffix+".root");
     cout<< infilelist[i]<<" ";
  }
  
  (void) SUSY_contourplots(
     infilelist.at(0), infilelist.at(1), infilelist.at(2),
     "0-leptons, 2-6 jets", 
     dirname.ReplaceAll("ifb","").ReplaceAll("SUSY/",""), // lumi
     Grid,
     showSR,
     discexcl=1);
}

