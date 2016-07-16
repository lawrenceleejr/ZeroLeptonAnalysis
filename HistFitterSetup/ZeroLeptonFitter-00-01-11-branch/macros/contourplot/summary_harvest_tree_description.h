
#include "TTree.h"
#include "TFile.h"
#include <iostream>
using namespace std;

TTree* harvesttree(const char* textfile=0) {
  const char* filename    = "/imports/rcs5_data/larryl/ZeroLeptonAnalysis/HistFitterSetup/ZeroLeptonFitter-00-01-11-branch/macros/contourplot/Outputs/8.3ifb_RJigsaw/GG_direct/GG_direct_SRJigsawSRG1a_fixSigXSecNominal__1_harvest_list";
  const char* description = "expectedUpperLimitMinus1Sig/F:upperLimitEstimatedError/F:fitstatus/F:p0d2s/F:p0u2s/F:m12/F:CLsexp/F:sigma1/F:sigma0/F:expectedUpperLimitPlus2Sig/F:nofit/F:nexp/F:failedfit/F:clsd2s/F:m0/F:expectedUpperLimit/F:failedstatus/F:xsec/F:covqual/F:p0d1s/F:CLs/F:fID/F:failedp0/F:failedcov/F:p0exp/F:clsu1s/F:p0u1s/F:excludedXsec/F:p0/F:p1/F:clsu2s/F:expectedUpperLimitMinus2Sig/F:expectedUpperLimitPlus1Sig/F:seed/F:mode/F:clsd1s/F:dodgycov/F:upperLimit/F";
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
  TFile* file = TFile::Open("/imports/rcs5_data/larryl/ZeroLeptonAnalysis/HistFitterSetup/ZeroLeptonFitter-00-01-11-branch/macros/contourplot/Outputs/8.3ifb_RJigsaw/GG_direct/GG_direct_SRJigsawSRG1a_fixSigXSecNominal__1_harvest_list.root","RECREATE");
  file->cd();
  tree->Write();
  file->Close();
}

void summary_harvest_tree_description() {
  TTree* tree = harvesttree();
  gDirectory->Add(tree);
}
