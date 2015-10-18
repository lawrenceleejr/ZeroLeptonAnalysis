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

  TString SRset="ABC"; 
  TString stopBR="100";
  TString mix="";

  TString meffcuts[3]={"combined_fixSigXSecNominal", "combined_fixSigXSecNominal","combined_fixSigXSecNominal"};
  TString dirname="";
  
  for(int i=0; i<3; i++){
     infilelist.push_back("Outputs/"+ dirname+"/GG_direct_"+meffcuts[i]+"_discovery_1_harvest_list.root");
     cout<< infilelist[i]<<" ";
  }

  // hypo-result file for each SR
  inlist.push_back("Outputs/GG_direct_SR4j-MetoMeff0.2-Meff2400-sljetpt200-34jetpt150-dphi0.4-ap0.02_fixSigXSecNominal_discovery_1_harvest_list.root");
  inlist.push_back("Outputs/GG_direct_SR4j-MetoMeff0.2-Meff2400-sljetpt200-34jetpt60-dphi0.4-ap0.02_fixSigXSecNominal_discovery_1_harvest_list.root");
  inlist.push_back("Outputs/GG_direct_SR4j-MetoMeff0.2-Meff1600-sljetpt200-34jetpt150-dphi0.4-ap0.02_fixSigXSecNominal_discovery_1_harvest_list.root");

  (void) SUSY_contourplots_p0(
     infilelist.at(0), infilelist.at(1), infilelist.at(2),
     "in 0-lepton analysis", 
     2, // lumi
     inlist.at(0), inlist.at(1), inlist.at(2),
     discexcl=1);
}

