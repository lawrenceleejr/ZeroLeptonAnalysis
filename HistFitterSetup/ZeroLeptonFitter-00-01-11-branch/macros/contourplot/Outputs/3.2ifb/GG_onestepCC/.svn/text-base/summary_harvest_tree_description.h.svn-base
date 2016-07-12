
#include "TTree.h"
#include "TFile.h"
#include <iostream>
using namespace std;

TTree* harvesttree(const char* textfile=0) {
  const char* filename    = "/data/data1/zp/shadachi/analysis/HistFitter/ZeroLeptonFitter/00-01-11-08_2/ZeroLeptonFitter/macros/contourplot/Outputs/3.2ifb/GG_onestepCC/GG_onestepCC_SR6jt_fixSigXSecDown__mlspNE60_harvest_list";
  const char* description = "expectedUpperLimitMinus1Sig/F:upperLimitEstimatedError/F:mgluino/F:fitstatus/F:p0d2s/F:p0u2s/F:seed/F:CLsexp/F:sigma1/F:failedfit/F:mlsp/F:expectedUpperLimitPlus2Sig/F:nofit/F:nexp/F:sigma0/F:clsd2s/F:expectedUpperLimit/F:failedstatus/F:xsec/F:covqual/F:upperLimit/F:p0d1s/F:mchargino/F:clsd1s/F:failedp0/F:failedcov/F:p0exp/F:p1/F:p0u1s/F:excludedXsec/F:p0/F:clsu1s/F:clsu2s/F:expectedUpperLimitMinus2Sig/F:expectedUpperLimitPlus1Sig/F:mode/F:fID/C:dodgycov/F:CLs/F";
  TTree* tree = new TTree("tree","data from ascii file");
  Long64_t nlines(0);
  if (textfile!=0) {
    nlines = tree->ReadFile(textfile,description);
  } else if (filename!=0) {
    nlines = tree->ReadFile(filename,description);
  } else {
    cout << "WARNING: file name is empty. No tree is read." << endl;
  }
  tree->SetMarkerStyle(8);
  tree->SetMarkerSize(0.5);
  return tree;
}

void writetree() {
  TTree* tree = (TTree *)gDirectory->Get("tree");
  if (tree==0) {
    tree = harvesttree();
    if (tree==0) return;
  }
  TFile* file = TFile::Open("/data/data1/zp/shadachi/analysis/HistFitter/ZeroLeptonFitter/00-01-11-08_2/ZeroLeptonFitter/macros/contourplot/Outputs/3.2ifb/GG_onestepCC/GG_onestepCC_SR6jt_fixSigXSecDown__mlspNE60_harvest_list.root","RECREATE");
  file->cd();
  tree->Write();
  file->Close();
}

void summary_harvest_tree_description() {
  TTree* tree = harvesttree();
  gDirectory->Add(tree);
}
