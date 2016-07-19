#include <vector>
#include "TPRegexp.h"
#include "contourmacros/SUSY_contourplots.C"

void makecontourplots_CLs(const TString Grid="GG_direct",TString dirname = "Outputs/3.2ifb/GG_direct") 
{
  int  discexcl; // 0=discovery, 1=exclusion
  bool showtevatron(false);
  bool showcms(false);
  bool doOneSigmaBand(false);
  bool showfixSigXSecBand(false);
  int applyfix(0);
  bool showSR(true); 
  vector<TString> infilelist;
  vector<TString> inlist;
  
  // XSec Nominal Up Down
  // TString combined[1]={"combined_fixSigXSecNominal"};
  TString combined[3]={"combined_fixSigXSecNominal", "combined_fixSigXSecNominal","combined_fixSigXSecNominal"}; // no xsection error

  TString listSuffix="__1_harvest_list";
  if(Grid=="GG_onestepCC"){
     listSuffix="__mlspNE60_harvest_list";
  }
  
  for(int i=0; i<3; i++){
     infilelist.push_back(dirname+"/"+Grid+"_"+combined[i]+listSuffix+".root");
     cout<< infilelist[i]<<" ";
  }
  cout<<endl;
  
  TPMERegexp tmp('/');
  int nsplit = tmp.Split(dirname);
  TString lumi="0";
  for( int i=0 ; i<nsplit ; i++ ){
    if( tmp[i].Contains("ifb") ){
      lumi = tmp[i].ReplaceAll("ifb","");
      lumi = tmp[i].ReplaceAll("_RJigsaw","");
    }
  }
  cout<<"lumi="<<lumi<<" fb-1"<<endl;

  // TFile * customContourFile = TFile::Open(  "output.root", "READ" );
  TFile * customContourFile = 0;
  // customContourFile->ls();

  (void) SUSY_contourplots(
      infilelist.at(0), infilelist.at(1), infilelist.at(2),
      "0-leptons, 2-6 jets", 
      lumi,
      Grid,
      showSR,
      discexcl=1,customContourFile);
}

