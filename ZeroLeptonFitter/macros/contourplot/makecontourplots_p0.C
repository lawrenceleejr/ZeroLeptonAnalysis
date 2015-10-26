#include <vector>
#include "contourmacros/SUSY_contourplots_p0.C"

void makecontourplots_p0(const TString& combo = "all") 
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

  TString Grid="GG_direct"; // "GG_onestepCC"; 

  // combined contours (later for SigXSecNominal/Up/Down)
  TString meffcuts[3]={"combined_fixSigXSecNominal", "combined_fixSigXSecNominal","combined_fixSigXSecNominal"};
  TString dirname="4ifb"; 

  for(int i=0; i<3; i++){
     infilelist.push_back("Outputs/"+dirname+"/"+Grid+"_"+meffcuts[i]+"_discovery_1_harvest_list.root");
  }

  // List three SRs whose contours are shown in the plots:
  // GG_direct
  TString  GG_direct_mainsrs[3]={
     "SR4jbase-MetoMeff0.2-Meff2200-sljetpt100-34jetpt100-dphi0.4-ap0.04", //SR4jt
     "SR5jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.04", //SR5j          
     "SR2jbase-MeSig20-Meff1800-sljetpt60-dphi0.4-ap0.00" //SR2jm
  };
  
  // SS_direct
  TString  SS_direct_mainsrs[3]={
     "SR2jbase-MeSig20-Meff2200-sljetpt200-dphi0.8-ap0.00", //SR2jt
     "SR2jbase-MeSig15-Meff1200-sljetpt200-dphi0.8-ap0.00", //SR2jl
     "SR2jbase-MeSig20-Meff1800-sljetpt60-dphi0.4-ap0.00" //SR2jm
  };
  
  // GG_onestepCC
  TString  GG_onestepCC_mainsrs[3]={
     "SR6jbase-MetoMeff0.2-Meff1800-sljetpt100-34jetpt100-dphi0.4-ap0.04", //SR6jt               
     "SR6jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.04", //SR6jm
     "SR2jbase-MeSig20-Meff1800-sljetpt60-dphi0.4-ap0.00" //SR2jm
  };

  // hypo-result file for each SR
  TString mainsrs[3]={"","",""};
  for(int i=0; i<3; i++){
     if(Grid=="SS_direct"){
        mainsrs[i]=SS_direct_mainsrs[i];
     }else if(Grid=="GG_direct"){
        mainsrs[i]=GG_direct_mainsrs[i];
     }else if(Grid=="GG_onestepCC"){
        mainsrs[i]=GG_onestepCC_mainsrs[i];
     }
     inlist.push_back("Outputs/"+dirname+"/"+Grid+"_"+mainsrs[i]+"_fixSigXSecNominal_discovery_1_harvest_list.root");
  }
     
  (void) SUSY_contourplots_p0(
     infilelist.at(0), infilelist.at(1), infilelist.at(2),
     "in 0-lepton analysis", 
     dirname.ReplaceAll("ifb",""), // lumi
     inlist.at(0), inlist.at(1), inlist.at(2),
     Grid,
     showSR,
     discexcl=1);
}

