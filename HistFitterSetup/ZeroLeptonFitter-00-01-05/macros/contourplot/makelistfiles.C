#include "TString.h"

void makelistfiles(const TString inputfile)
{
  gSystem->Load("libSusyFitter.so");

  // input root file with HypoTestInverterResults, 
  // as obtained from running: 
  // SusyFitter.py -f python/MySimpleChannelConfig.py
  //const char* inputfile  = "../../results/ZeroLepton_meffIncabove=800Andmetovermeff2Jetabove0.3_Output_hypotest.root";
  //const char* inputfile  = "../../results/ZeroLepton_Output_hypotest.root";
  
  // search for objects labelled
  //const char* format     = "hypo_msugra_%f_%f";
  //const char* format     = "hypo_msugra_0_10_P_%f_%f";
  //const char *format = "hypo_Gtt_%f_2500_%f";
  const char *format = "hypo_Gluino_Stop_charm_%f_%f";

  //const char* format     = "hypo_SU_%f_%f_0_10";
  // interpret %f's above respectively as (seperated by ':')
  const char* interpretation = "m0:m12";
  // cut string on m0 and m12 value, eg "m0>1200"
  const char* cutStr = "1"; // accept everything
  
  TString outputfile = CollectAndWriteHypoTestResults( inputfile, format, interpretation, cutStr ) ;

  // load the listfile in root with:
  // root -l summary_harvest_tree_description.h
  // or look directly at the outputfile in vi.
}

