#include "contourmacros/CombinationGlob.C"
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TGraph.h"
#include "TLegend.h"

// MACRO FOR DRAWING NEUTRALINO LINE FOR NUHMG
// Instructions for use:
// 1. Create a new TCanvas before calling this function.
// 2. Call old_limits(...), specifying the intended x- and y-axis maximum values (this assumes origin at 0,0), and the x- and y-axis labels.
// 3. Draw any other plots over the top.
//
// These limits are mostly relevant with the upper RH corner between (500,500) and (2000,2000).

TGraph* nuhmg_neutralino(){

	// Draw other LSP regions
	// Neutralino LSP
	TFile *fneut1 = new TFile("/afs/cern.ch/user/m/mamuzic/public/TWiki_NUHMG/nuhmg_neutralino.root");
	TTree *tneut1 = fneut1->Get("neutralino");
	double mH1sq, m12;
	tneut1->SetBranchAddress("mH1sq",&mH1sq);
	tneut1->SetBranchAddress("m12",&m12);

	Long64_t nneut1 = tneut1->GetEntries();
	TGraph* gneut1 = new TGraph(nneut1);
	for(Long64_t i = 0; i < nneut1; ++i) {
		tneut1->GetEntry(i);
		gneut1->SetPoint(i,mH1sq, m12);
	}

  gneut1->SetFillColor(CombinationGlob::c_MLightGray);  
  gneut1->SetLineColor(CombinationGlob::c_LightGray);  
  //gneut1->SetLineStyle(1); // kDotted; 

  gneut1->Draw("F");
  gneut1->Draw("L");
  
  gPad->RedrawAxis();

  return gneut1;
}

TGraph* nuhmg_stautachion(){

	// Draw other LSP regions
	// Stau tachion LSP
	TFile *fstau = new TFile("/afs/cern.ch/user/m/mamuzic/public/TWiki_NUHMG/nuhmg_stautachion.root");
	TTree *tstau = fstau->Get("stautachion");
	double mH1sq, m12;
	tstau->SetBranchAddress("mH1sq",&mH1sq);
	tstau->SetBranchAddress("m12",&m12);

	Long64_t nstau = tstau->GetEntries();
	TGraph* gstau = new TGraph(nstau);
	for(Long64_t i = 0; i < nstau; ++i) {
		tstau->GetEntry(i);
		gstau->SetPoint(i,mH1sq, m12);
	}

  gstau->SetFillColor(CombinationGlob::c_LightGray);  
  gstau->SetLineColor(CombinationGlob::c_Gray);  
  //gstau->SetLineStyle(1); // kDotted; 

  gstau->Draw("F");
  gstau->Draw("L");
  
  gPad->RedrawAxis();

  return gstau;
}
