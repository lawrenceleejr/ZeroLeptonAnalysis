#include "contourmacros/CombinationGlob.C"
#include "TStyle.h"
#include "TColor.h"
#include "TGraph.h"
#include "TTree.h"
#include <algorithm>
#include <string>
#include <sstream>
#include <iostream>
#include "TROOT.h"
#include "TSystem.h"
#include "TApplication.h"

#include "0lep_Moriond_mglmsqexcl-4.C"
#include "contourmacros/nuhmg_otherLSP.C"
#include "ContourUtils.C" //JM

//double scale = 0.000001;
double scale = 1;

void Show_SR(bool useShape) {
    TLatex lat;
    lat.SetTextSize( 0.025 );
    lat.SetTextColor( 12 );
    lat.SetTextFont( 42 );

    cout << "Draw signal region labels." << endl;
    gROOT->ProcessLine(".L summary_harvest_tree_description.h+");
    gSystem->Load("libSusyFitter.so");


	ifstream ifs("Outputs/NUHMG_combined_fixSigXSecNominal__1_harvest_list");
	std::string line;
	while(getline(ifs,line)){ //JM// make sure you read the mH1sq and m12 correctly
		double buf;
		double mH1sq;
		double m12;
		double fID;
		double fCLsexp;
		std::string sr;
		std::istringstream is(line);
		vector<double> val;
		for(int i=0; i<38; i++) { // vector 0-24, index 0-24
			is >> buf;
			val.push_back(buf);
		}
		cout << "JM: ID " << val.at(7) << " mH1sq " << val.at(35) << " m12 " << val.at(36) << " CLsexp " << val.at(6) << " nofit " << val.at(32) << endl;
		//p0:p1:CLs:mode:nexp:seed:CLsexp:fID:sigma0:sigma1:clsu1s:clsd1s:clsu2s:clsd2s:upperLimit:
		//upperLimitEstimatedError:expectedUpperLimit:expectedUpperLimitPlus1Sig:expectedUpperLimitPlus2Sig:
		//expectedUpperLimitMinus1Sig:expectedUpperLimitMinus2Sig:xsec:excludedXsec:
		//failedcov:failedfit:failedp0:fitstatus:m0:m12:nofit

		//p0:p1:CLs:mode:nexp:seed:CLsexp:fID:sigma0:sigma1:clsu1s:clsd1s:clsu2s:clsd2s:upperLimit:
		//upperLimitEstimatedError:expectedUpperLimit:expectedUpperLimitPlus1Sig:expectedUpperLimitPlus2Sig:
		//expectedUpperLimitMinus1Sig:expectedUpperLimitMinus2Sig:xsec:excludedXsec:
		//covqual:dodgycov:failedcov:failedfit:failedp0:failedstatus:fitstatus:m0:m12:nofit

		fID = val.at(7);
		if(scale != 1)
			mH1sq = val.at(35) * scale;
		else mH1sq = val.at(35);
		m12 = val.at(36);
		fCLsexp = val.at(6);

		int opti = 1; // 1 - CONF note, 2 - Optimization1, 3 - Optimization2
		TString mySR;
		if (opti == 1) {
			if (!useShape) {
				switch(fID) {
  				case 1: mySR = "2jm"; break;
  				case 2: mySR = "2jt"; break;
  				case 3: mySR = "2jW"; break;
 				case 4: mySR = "2jl"; break;
 				case 5: mySR = "3jW"; break;
 				case 6: mySR = "3j"; break;
 				case 7: mySR = "4jl"; break;
 				case 8: mySR = "4jm"; break;
 				case 9: mySR = "4jt"; break;
 				case 10: mySR = "4jl-"; break;
  				case 11: mySR = "5j"; break;
  				case 12: mySR = "6jm"; break;
  				case 13: mySR = "6jt"; break;
  				case 14: mySR = "6jt+"; break;
  				case 15: mySR = "6jl"; break;
				default: mySR = ; break;
				}
			} else if (useShape) {
				switch(fID) {
				case 1: mySR = "Al"; break;
				case 2: mySR = "Am"; break;
				case 3: mySR = "At"; break;
				case 4: mySR = "Bm"; break;
				case 5: mySR = "Bt"; break;
				case 6: mySR = "Cm"; break;
				case 7: mySR = "Ct"; break;
				case 8: mySR = "Dm"; break;
				case 9: mySR = "Dt"; break;
				case 10: mySR = "El"; break;
				case 11: mySR = "Em"; break;
				case 12: mySR = "Et"; break;
				default: mySR = ; break;
				}
			}	
		}
		else if (opti == 2) {
			stringstream sfID;
			sfID << fID;
			mySR = "E" + sfID.str();
		}
		else if (opti == 3) {
			stringstream sfID;
			sfID << fID;
			mySR = "D" + sfID.str();
		}

		int label = 1; // 0 - no label, 1 - SR, 2 - CLsexp, 3 - PAPER SR + CLs for new SR
		if (label == 0) {
			cout << "No label!" << endl;
		} else if (label == 1) {
			lat.DrawLatex(mH1sq,m12,mySR.Data());
			//cout << mH1sq << " " << m12 << " " << mySR.Data() << endl;
		} else if (label == 2) {
			stringstream sCLsexp;
			sCLsexp.precision(1);
			sCLsexp << std::scientific << fCLsexp;
			lat.DrawLatex(mH1sq,m12,(sCLsexp.str()).c_str());
		} else if (label == 3) {
			if (mySR != "6jt-") {
				lat.DrawLatex(mH1sq,m12,mySR.Data());
			} else {
				stringstream sCLsexp;
				sCLsexp.precision(1);
				sCLsexp << std::scientific << fCLsexp;
				lat.DrawLatex(mH1sq,m12,(sCLsexp.str()).c_str());
			}
		}

	}
}

void SUSY_mH1sq_vs_m12_all_withBand_cls_blind_forNUHMG( TString fname0 = "Outputs/NUHMG_combined_fixSigXSecNominal__1_harvest_list.root",// nominal
														TString fname1 = "Outputs/NUHMG_combined_fixSigXSecUp__1_harvest_list.root",// Up
														TString fname2 = "Outputs/NUHMG_combined_fixSigXSecDown__1_harvest_list.root",// Down
														TString fname3 = "", // external expection
														const char* prefix="test",
														const float& lumi = 20.3,
														bool showsig = true,
														bool show7TeVlimits = true,
														int discexcl = 1,
														int showOneSigmaExpBand = 0,
														int showfixSigXSecBand = 0,
														int channel = -1,
														bool blind = true,
														bool showSR = true,
														bool useShape = false,
														TString hname0 = "sigp1clsf",
														TString hname1 = "sigp1expclsf",
														TString hname3 = "sigclsu1s",
														TString hname5 = "sigclsd1s",
														TString hname6 = "sigp1ref") {
	
   CombinationGlob::Initialize(); // set style and remove existing canvas
   
   cout << "--- Plotting mH1sq versus m12 " << endl;
   
   // --- prepare
   // open reference files, and retrieve histogram
   cout << "--- Reading root base file: " << fname0 << endl;
   TFile* f0 = TFile::Open( fname0, "READ" );
   if (!f0) {
      cout << "*** Error: could not retrieve histogram: " << hname0 << " in file: " << f0->GetName() 
           << " ==> abort macro execution" << endl;
      return;
   }

   TH2F* histecls = (TH2F*)f0->Get( "sigp1expclsf" ); 
   TH2F* histocls = (TH2F*)f0->Get( "sigp1clsf" ); //nominal
   TH2F* histUL = (TH2F*)f0->Get( "upperLimit" );

   if (histecls!=0) histecls->SetDirectory(0);
   if (histocls!=0) histocls->SetDirectory(0);
   if (histUL!=0) histUL->SetDirectory(0);

   // in case we use external expectation!
   TFile* f3 = TFile::Open( fname3, "READ" );
   TH2F* histe(0);
   if (f3) { histe = (TH2F*)f3->Get( hname0 ); }
   TH2F* histe_u1s(0);
   if (f3) { histe_u1s = (TH2F*)f3->Get( hname3 ); }
   TH2F* histe_d1s(0);
   if (f3) { histe_d1s = (TH2F*)f3->Get( hname5 ); }
   
   if (f3) {
      if (histecls!=0) { delete histecls; histecls=0; }
      histecls = (TH2F*)f3->Get( "sigp1expcls" );
      if (histecls!=0) histecls->SetDirectory(0);
      else {
        histecls = (TH2F*)f3->Get( "sigp1expclsf" );
        if (histecls!=0) histecls->SetDirectory(0);
      }
   }

   TFile* f6;
   TString fname6="/afs/cern.ch/work/m/mamuzic/Analysis8TeV2012/SignalUncertaintyFiles/SignalUncertainties-NUHMG.root";
   cout << "--- Reading root base file: " << fname6 << endl;
   f6 = TFile::Open( fname6, "READ" );

   TTree *SignalUncertainties = (TTree*)f6->Get("SignalUncertainties");
   SignalUncertainties->ls();
   Int_t nmass =SignalUncertainties->GetEntries();
   SignalUncertainties->Show(10);
   Float_t mass1, mass2;
   Float_t mH1sq, m12;
   Int_t finalState;
   SignalUncertainties->SetBranchAddress("mass1",&mass1);
   SignalUncertainties->SetBranchAddress("mass2",&mass2);
   SignalUncertainties->SetBranchAddress("mH1sq",&mH1sq);
   SignalUncertainties->SetBranchAddress("m12",&m12);
   SignalUncertainties->SetBranchAddress("finalState",&finalState);

   bool extExpectation = (f3!=0) ;
   
   TH2F* hist0 = (TH2F*)f0->Get( hname0 );
   TH2F* hist1 = (TH2F*)f0->Get( hname1 );
   TH2F* hist3 = (TH2F*)f0->Get( hname3 );
   TH2F* hist5 = (TH2F*)f0->Get( hname5 );
   TH2F* hist6 = (TH2F*)f0->Get( hname6 );
   
   if (hist0!=0) hist0->SetDirectory(0);
   if (hist1!=0) hist1->SetDirectory(0);
   if (hist3!=0) hist3->SetDirectory(0);
   if (hist5!=0) hist5->SetDirectory(0);
   if (hist6!=0) hist6->SetDirectory(0);
   f0->Close();

   
   TFile* f1 = TFile::Open( fname1, "READ" );
   if (!f1) {
	   cout << "*** Error: could not retrieve histogram: " << hname0 << " in file: " << f1->GetName() 
			<< " ==> abort macro execution" << endl;
	   return;
   }
   TFile* f2 = TFile::Open( fname2, "READ" );
   if (!f2) {
	   cout << "*** Error: could not retrieve histogram: " << hname0 << " in file: " << f2->GetName() 
			<< " ==> abort macro execution" << endl;
	   return;
   }
   
   TH2F* hist7 = (TH2F*)f1->Get( hname0 );
   TH2F* hist8 = (TH2F*)f2->Get( hname0 );
   

   TH2F* contour_obs     = ( hist0!=0 ? FixAndSetBorders( *hist0, "contour_obs", "contour_obs") : 0 );
   
   TH2F* contour_ep1s    = ( hist3!=0 ? FixAndSetBorders( *hist3, "contour", "contour", 0 ) : 0 ); //good
   TH2F* contour_em1s    = ( hist5!=0 ? FixAndSetBorders( *hist5, "contour", "contour", 0 ) : 0 ); //good

   TH2F* contour_op1s    = ( hist3!=0 ? FixAndSetBorders( *hist7, "contour", "contour", 0 ) : 0 ); //good
   TH2F* contour_om1s    = ( hist5!=0 ? FixAndSetBorders( *hist8, "contour", "contour", 0 ) : 0 ); //good

   TH2F* contour_expcls(0);
   if (histecls!=0)     { contour_expcls     = FixAndSetBorders( *histecls, "contour_expcls", "contour_expcls", 0 ); }
   TH2F* contour_obscls(0);
   if (histocls!=0)     { contour_obscls     = FixAndSetBorders( *histocls, "contour_obscls", "contour_obscls", 0 ); }
   

  // For Band, only expected JM PUT BACK
   TGraph* gr_contour_ep1s = ContourGraph( contour_ep1s )->Clone(); 
   TGraph* gr_contour_em1s = ContourGraph( contour_em1s )->Clone();
  
   if (contour_obs==0) { 
      cout << "contour is zero" << endl;
      return;
   }


   
   // set text style
   gStyle->SetPaintTextFormat(".2g");
   if (hist1!=0) hist1->SetMarkerStyle(21);
   if (hist1!=0) hist1->SetMarkerSize(1.5);
   Float_t nsigmax(0)
      if (hist1!=0) nsigmax = hist1->GetMaximum();
   
   // --- draw
   
   // create canvas
   TCanvas* c = new TCanvas( "c", "A scan of m_{H_{1}}^{2} versus m_{12}", 0, 0, 
                             CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[1] );  

  // create and draw the frame
   if (scale != 1)TH2F *frame = new TH2F("frame", "m_{#tilde{g}} vs m_{#tilde{q}} - ATLAS work in progress", 100, 1000.*scale, 1410.*scale ,100, 900., 1260.);
   else TH2F *frame = new TH2F("frame", "m_{#tilde{g}} vs m_{#tilde{q}} - ATLAS work in progress", 100,1000., 1410.,100, 900., 1260.);

   bool plotMoriond=true;
   if (plotMoriond ) frame = new TH2F("frame", "m_{#tilde{g}} vs m_{#tilde{q}} - ATLAS for approval", 100, 1000.*scale, 1410.*scale ,100, 900., 1260.);
   
  // set common frame style
  CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
  
  if (scale == 1) frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
  else if (scale == 0.000001)frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
  else frame->SetXTitle( "m_{H_{#tilde{g}}" );
  frame->SetYTitle( "m_{#tilde{q}} [GeV]" );
  frame->GetYaxis()->SetTitleOffset(1.35);

  frame->GetXaxis()->SetTitleFont( 42 );
  frame->GetYaxis()->SetTitleFont( 42 );
  frame->GetXaxis()->SetLabelFont( 42 );
  frame->GetYaxis()->SetLabelFont( 42 );

  frame->GetXaxis()->SetTitleSize( 0.04 );
  frame->GetYaxis()->SetTitleSize( 0.04 );
  frame->GetXaxis()->SetLabelSize( 0.04 );
  frame->GetYaxis()->SetLabelSize( 0.04 );
  c->SetRightMargin(0.07);

  frame->Draw(); // FRAME IS DRAWN!!
    
  const int nsig(3);

  TString basecolor="yellow";
  Int_t nsigma=2;

  TLegend *leg = new TLegend (0.15,0.70,0.40,0.45);

  leg->SetTextSize( CombinationGlob::DescriptionTextSize );
  leg->SetTextSize( 0.032 );
  leg->SetTextFont( 42 );
  leg->SetFillColor( 0 );
  leg->SetFillStyle(0);

  TGraph* Moriond_obs(0);
  TGraph* Moriond_exp(0);

  if (plotMoriond ){
     Moriond_obs = zl_Moriond_mglmsqexcl_obs();
  }

  Int_t c_myYellow   = TColor::GetColor("#ffe938");
  Int_t c_myRed      = CombinationGlob::c_DarkRed;
  Int_t c_myExp      = CombinationGlob::c_DarkBlueT3;
  c->cd(1);
  
  // JM Scale all graphs
  if(scale != 1){
	  ScaleTGraph(gr_contour_em1s, scale);
	  ScaleTGraph(gr_contour_ep1s, scale);
	  if(contour_expcls)ScaleTH2F(contour_expcls,scale); 
	  if(contour_obs)ScaleTH2F(contour_obs,scale); 
	  if(contour_ep1s)ScaleTH2F(contour_ep1s,scale);
	  if(contour_em1s)ScaleTH2F(contour_em1s,scale);
	  if(contour_au1s)ScaleTH2F(contour_au1s,scale);
	  if(contour_ad1s)ScaleTH2F(contour_ad1s,scale);
	  if(contour_exp)ScaleTH2F(contour_exp);
  }	

  TGraph* grshadeExp = DrawExpectedBand_new( gr_contour_em1s, gr_contour_ep1s, c_myYellow , 1001,
                                          1000, 1410, 900, 1260,
                                          0, 0)->Clone();
  

  
  if (discexcl==1) {
	  if (contour_obs!=0 && !blind) {
		  DrawContourLine95( NULL, contour_op1s, "#pm1 #sigma_{obs}^{th}", c_myRed, 3, 1.5 );
		  DrawContourLine95( leg, contour_obscls, "Observed limit 95% CL (#pm1 #sigma_{obs}^{th})", c_myRed, 1, 2 );
		  DrawContourLine95( NULL, contour_om1s, "Obs. th. -1 sigma", c_myRed, 3, 1.5  );
	  }
     if (!extExpectation) { // expectation from toys
		 if (contour_expcls!=0) DrawContourLine95( NULL, contour_expcls, "exp. limit 95% CL", CombinationGlob::c_DarkBlueT3, 6 ); 
        
        if (showOneSigmaExpBand) {

			DummyLegendExpected(leg, "Expected limit 95% CL (#pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 2);
        } else {
           if (contour_ep1s!=0) DrawContourLine95( leg, contour_ep1s, "exp. +1 sigma", CombinationGlob::c_DarkBlueT3, 2 );
           if (contour_em1s!=0) DrawContourLine95( leg, contour_em1s, "exp. -1 sigma", CombinationGlob::c_DarkBlueT3, 3 );
        }
        
     } else { // expectation from asimov
        if (contour_exp!=0) DrawContourLine95( leg, contour_exp, "Median expected limit", CombinationGlob::c_DarkBlueT3, 6);
        if (showOneSigmaExpBand) {
           if (contour_au1s!=0) DrawContourLine95( leg, contour_au1s, "Expected limit #pm1#sigma", CombinationGlob::c_DarkBlueT3, 3 );
           if (contour_ad1s!=0) DrawContourLine95( leg, contour_ad1s, "", CombinationGlob::c_DarkBlueT3, 3 );
        }
     }
  }
  
  // JM: Add neutralino LSP and stau tachion excluded regions
  c->cd();
  TGraph* gneut1(0);
  gneut1 = nuhmg_neutralino();
  TGraph* gstau(0);
  gstau = nuhmg_stautachion();

  if (scale != 1) { // scale mH1sq
	  ScaleTGraph(gneut1,scale);
	  ScaleTGraph(gstau,scale);
  }

  leg->AddEntry(gneut1, "#tilde{#chi}_{1}^{0} LSP","F");
  leg->AddEntry(gstau, "#tilde{#tau}_{1} tachion","F");

  // Show best SR for all points
  Show_SR(useShape);

  // legend
  Float_t textSizeOffset = +0.000;
  Double_t xmax = frame->GetXaxis()->GetXmax();
  Double_t xmin = frame->GetXaxis()->GetXmin();
  Double_t ymax = frame->GetYaxis()->GetXmax();
  Double_t ymin = frame->GetYaxis()->GetXmin();
  Double_t dx   = xmax - xmin;
  Double_t dy   = ymax - ymin;
 
  //TString t1a = "99%, 95%, 68% CL fit contour (excluded)" ;
  // TString t1a = "-1#sigma, central, +1#sigma  fit contour (excluded)" ;
  TString t1b = "tan#beta = 3, A_{0}= 0, #mu < 0" ;
  Float_t nbkg(0);
  if( hist5!=0) nbkg = hist5->GetMaximum();
  TString t1c = Form("MC: n_{bkg}= %.1f", nbkg) ;
  
  // TLatex* text1a = new TLatex( 70, 260, t1a );
  TLatex* text1b = new TLatex( 150, ymax + dy*0.025, t1b );
  TLatex* text1c = new TLatex( 70, 280, t1c );
  
  text1b->SetTextColor( 1 ); //CombinationGlob::c_VDarkGreen );
  text1c->SetTextColor( 1 );
  
  text1b->SetTextFont( 42 ); //CombinationGlob::c_VDarkGreen );

  text1b->SetTextAlign( 11 );
  text1c->SetTextAlign( 11 );
  
  text1b->SetTextSize( CombinationGlob::DescriptionTextSize  );
  text1c->SetTextSize( CombinationGlob::DescriptionTextSize  );
  
  TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025, "NUHM model with gaugino mediation and #tilde{#nu}_{#tau} NLSP" );
  Leg0->SetTextAlign( 11 );
  Leg0->SetTextFont( 42 );
  Leg0->SetTextSize( CombinationGlob::DescriptionTextSize);
  Leg0->SetTextColor( 1 );
  Leg0->AppendPad();
  
  TLatex *Leg1 = new TLatex();
  Leg1->SetNDC();
  Leg1->SetTextAlign( 11 );
  Leg1->SetTextFont( 42 );
  Leg1->SetTextSize( CombinationGlob::DescriptionTextSize );
  Leg1->SetTextColor( 1 );
  if (plotMoriond ){
	  Leg1->DrawLatex(0.15,0.80, Form("#int L dt = 20.3 fb^{-1},  #sqrt{s}=8 TeV",lumi));  // 0.32,0.87
  }else{
	  Leg1->DrawLatex(0.15,0.80, Form("#int L dt = 20.3 fb^{-1},  #sqrt{s}=8 TeV"));  // 0.32,0.87
  }
  Leg1->AppendPad();
  
  TLatex *Leg2 = new TLatex();
  Leg2->SetNDC();
  Leg2->SetTextAlign( 11 );
  Leg2->SetTextSize( CombinationGlob::DescriptionTextSize );
  Leg2->SetTextColor( 1 );
  Leg2->SetTextFont(42);
  if (prefix!=0) {
     if (plotMoriond ){
		 Leg2->DrawLatex(0.15,0.70,prefix); // 0.15,0.81
     }else{
		 Leg2->DrawLatex(0.15,0.70,prefix); // 0.15,0.81
     }
    Leg2->AppendPad(); 
  }

  TLatex *atlasLabel = new TLatex();
  atlasLabel->SetNDC();
  atlasLabel->SetTextFont( 72 );
  atlasLabel->SetTextColor( 1 );
  atlasLabel->SetTextSize( 0.05 );
  atlasLabel->DrawLatex(0.15,0.87, "ATLAS"); // 0.15,0.87
  atlasLabel->AppendPad();

  TLatex *prel = new TLatex();
  prel->SetNDC();
  prel->SetTextFont( 42 );
  prel->SetTextColor( 1 );
  prel->SetTextSize( 0.04 );
  prel->DrawLatex(0.27, 0.87, "Internal");   // 0.27,0.87
  //prel->DrawLatex(0.27, 0.87, "Preliminary");   // 0.27,0.87
  prel->AppendPad();

  //// draw number of signal events
  if (nsigmax>0 && showsig) {  hist1->Draw("textsame"); }

  //reddraw cahnnel label
  if (prefix!=0) { Leg2->AppendPad(); }

  // redraw axes
  frame->Draw( "sameaxis" );

  leg->Draw("same");
  // Here read out leg coordinates and add dashed red lines on observed line
  TLine* line1 = new TLine(1020, 1130, 1040, 1130);
  line1->SetLineWidth(2);
  line1->SetLineColor(CombinationGlob::c_DarkRed);
  line1->SetLineStyle(3);
  line1->Draw("SAME") ; 
  TLine* line2 = new TLine(1020, 1150, 1040, 1150);
  line2->SetLineWidth(2);
  line2->SetLineColor(CombinationGlob::c_DarkRed);
  line2->SetLineStyle(3);
  line2->Draw("SAME") ; 

  c->Update();

  ////////////////////////////////////////////////////////////////////////////////////////////
  
  //gROOT->GetListOfSpecials()->Print();
  
   TObjArray *contours = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   if (contours!=0) {
     //contours->Print("v");
     
     TList *lcontour1 = (TList*)contours->At(0);
     if (lcontour1!=0) {
       TGraph *gc1 = (TGraph*)lcontour1->First();
     }
   }

  ////////////////////////////////////////////////////////////////////////////////////////////

  // create plots
  // store histograms to output file
  TObjArray* arr = fname0.Tokenize("/");
  TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
  TString outfile = objstring->GetString().ReplaceAll(".root","").ReplaceAll("__1_harvest_list","").ReplaceAll("merged_list_","");
                                                                                                               
  delete arr;

  TString prefixsave = TString(prefix).ReplaceAll(" ","_")+ Form("wband%d_",showOneSigmaExpBand);
  CombinationGlob::imgconv( c, Form("plots/atlascls_mH1sqvsm12_%s",outfile.Data()) );   

   c->Print("plots/NUHMG_ATLAS.ps");
   c->Print("plots/NUHMG_ATLAS.png");
   c->Print("plots/NUHMG_ATLAS.eps");
   c->Print("plots/NUHMG_ATLAS.pdf");
}

// Rescale TH2F*
TH2F* ScaleTH2F(TH2F* before, double scale) {
	Int_t nx = before->GetXaxis()->GetNbins();
	Double_t xmin = before->GetXaxis()->GetXmin();
	Double_t xmax = before->GetXaxis()->GetXmax();
	Int_t ny = before->GetYaxis()->GetNbins();
	Double_t ymin = before->GetYaxis()->GetXmin();
	Double_t ymax = before->GetYaxis()->GetXmax();
	TH2F *after = new TH2F("after",before->GetTitle(),nx,xmin*scale,xmax*scale,ny,ymin*scale,ymax*scale);
	for (int i=0;i<nx;i++) {
		for (Int_t j=1;j<=ny;j++) {
			after->SetBinContent(i,j,before->GetBinContent(i,j));
		}	
	}	
	return after;
}

TGraph* ScaleTGraph(TGraph* graph, double scale) {
	for (int i=0;i<graph->GetN();i++) 
		graph->GetX()[i] *= scale;
	return graph;
}

void MirrorBorders( TH2& hist )
{
  int numx = hist.GetNbinsX();
  int numy = hist.GetNbinsY();
  
  Float_t val;
  // corner points
  hist.SetBinContent(0,0,hist.GetBinContent(1,1));
  hist.SetBinContent(numx+1,numy+1,hist.GetBinContent(numx,numy));
  hist.SetBinContent(numx+1,0,hist.GetBinContent(numx,1));
  hist.SetBinContent(0,numy+1,hist.GetBinContent(1,numy));
  
  for(int i=1; i<=numx; i++){
    hist.SetBinContent(i,0,	   hist.GetBinContent(i,1));
    hist.SetBinContent(i,numy+1, hist.GetBinContent(i,numy));
  }
  for(int i=1; i<=numy; i++) {
    hist.SetBinContent(0,i,      hist.GetBinContent(1,i));
    hist.SetBinContent(numx+1,i, hist.GetBinContent(numx,i));
  }
}

void DrawContourMassLine(TH2F* hist, Double_t mass, int color=14 ) {

  // contour plot
  TH2F* h = new TH2F( *hist );

  //  Double_t contours[5] = {500, 1000, 1500, 2000, 2500}
  h->SetContour( 1 );
  //h->SetContour( 5, contours )
  //  h->SetContourLevel( 0, contours );
  h->SetContourLevel( 0, mass );

  h->SetLineColor( color );
  h->SetLineStyle( 7 );
  h->SetLineWidth( 1 );
  h->Draw( "samecont3" );

}

void DrawContourLine99( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[2];
  double signif = TMath::NormQuantile(1-pval);

  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( 2 );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}


void DrawContourLine68( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[0];
  double signif = TMath::NormQuantile(1-pval);

  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( 2 );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}


TGraph* ContourGraph( TH2F* hist)
{
   TGraph* gr0 = new TGraph();
   TH2F* h = (TH2F*)hist->Clone();
   h->GetYaxis()->SetRangeUser(800,2800);
   h->GetXaxis()->SetRangeUser(800,2400);
   gr = (TGraph*)gr0->Clone(h->GetName());
   //  cout << "==> Will dumb histogram: " << h->GetName() << " into a graph" <<endl;
   h->SetContour( 1 );
   double pval = CombinationGlob::cl_percent[1];
   double signif = TMath::NormQuantile(1-pval);
   h->SetContourLevel( 0, signif );
   h->Draw("CONT LIST");
   h->SetDirectory(0);
   gPad->Update();
   TObjArray *contours = gROOT->GetListOfSpecials()->FindObject("contours");
   Int_t ncontours     = contours->GetSize();
   TList *list = (TList*)contours->At(0);
   Int_t number_of_lists = list->GetSize();
   gr = (TGraph*)list->At(0);
   TGraph* grTmp = new TGraph();
   for (int k = 0 ; k<number_of_lists ; k++){
      grTmp = (TGraph*)list->At(k);
      Int_t N = gr->GetN();
      Int_t N_tmp = grTmp->GetN();
      if(N < N_tmp) gr = grTmp;
      //    mg->Add((TGraph*)list->At(k));
   }

   gr->SetName(hist->GetName());
   int N = gr->GetN();
   double x0, y0;

   return gr;
}




// This produces the shaded band for the expected limit systematics
TGraph* DrawExpectedBand_new(TGraph* gr1,  TGraph* gr2, Int_t fillColor, Int_t fillStyle,
                             double xlow, double xhigh, double ylow, double yhigh,
                             int cutx = 0, int cuty = 0) {

   int number_of_bins = max(gr1->GetN(),gr2->GetN());
   
   const Int_t gr1N = gr1->GetN();
   const Int_t gr2N = gr2->GetN();
   
   const Int_t N = number_of_bins;
   Double_t x1[N], y1[N], x2[N], y2[N];
   
   // Get the points in the first graph
   Double_t xx0, yy0;
   for(int j=0; j<gr1N; j++) {
    gr1->GetPoint(j,xx0,yy0);
    x1[j] = xx0;
    y1[j] = yy0;
  }
   if (gr1N < N) {
    for(int i=gr1N; i<N; i++) {
       x1[i] = x1[gr1N-1];
       y1[i] = y1[gr1N-1];
    }
  }
   
   // Get the points in the second graph
   Double_t xx1, yy1;
   for(int j=0; j<gr2N; j++) {
      gr2->GetPoint(j,xx1,yy1);
      x2[j] = xx1;
      y2[j] = yy1;
   }
   if (gr2N < N) {
      for(int i=gr2N; i<N; i++) {
         x2[i] = x2[gr2N-1];
         y2[i] = y2[gr2N-1];
      }      
   }
   
   // Prepare and fill the 2D region enclosed by the error band
   TGraph *grshade = new TGraph(2*N+10);
   
   int point = 0;
   double lastx = 0; // This is the last point in the first graph
   double lasty = 0;
   double firstx = -875; // This is the first point drawn in the first graph
   double firsty = -875; // Set an arbitrary initial value so we can check if it's filled!
   for (int i=0;i<N;i++) {
    if (x1[i] > cutx && y1[i] > cuty) { // Allow to exclude some points from being plotted
       grshade->SetPoint(point,x1[i],y1[i]);
       lastx = x1[i]; 
       lasty = y1[i]; 
       if(firstx == -875) {
          firstx = x1[i];
          firsty = y1[i];
      }
       point++;
    }
   }
   
   // Find the first point to be drawn in the second graph
   double nextx = 0;
   double nexty = 0;
   for (int i=0;i<N;i++) {
      if (x2[N-i-1] > cutx && y2[N-i-1] > cuty) {
         nextx = x2[N-i-1];
         nexty = y2[N-i-1];
         i = N;
      }
   }
   
   // Make expected band reach axes where needed
   // Find the closest frame edge to the end of the first contour
   int nearestedge1 = 0; // left
   double dist = fabs(lastx-1-xlow);
   if(fabs(lasty-yhigh) < dist) { // top
      dist = fabs(lasty-yhigh);
      nearestedge1 = 1;
   }
   if(fabs(lastx-1-xhigh) < dist) { // right
      dist = fabs(lastx-1-xhigh);
      nearestedge1 = 2;
   }
   if(fabs(lasty-ylow) < dist) { // bottom
      dist = fabs(lasty-ylow);
      nearestedge1 = 3;
   }
   
   // Find the closest frame edge to the end of the second contour
   int nearestedge2 = 0; // left
   double dist = fabs(nextx-1-xlow);
   if(fabs(nexty-yhigh) < dist) { // top
      dist = fabs(nexty-yhigh);
      nearestedge2 = 1;
   }
   if(fabs(nextx-1-xhigh) < dist) { // right
      dist = fabs(nextx-1-xhigh);
    nearestedge2 = 2;
   }
   if(fabs(nexty-ylow) < dist) { // bottom
      dist = fabs(nexty-ylow);
      nearestedge2 = 3;
   }
   
   if(nearestedge2 == nearestedge1) {
      // when graphs will be connected on the same frame edge
      // add two points just outside the boundary
      switch(nearestedge1) {
         case 0:
            grshade->SetPoint(point,xlow-100,lasty);
            point++;
            grshade->SetPoint(point,xlow-100,nexty);
            point++;
            break;
         case 1:
            grshade->SetPoint(point,lastx,yhigh+100);
      point++;
      grshade->SetPoint(point,nextx,yhigh+100);
      point++;
      break;
         case 2:
            grshade->SetPoint(point,xhigh+100,lasty);
            point++;
            grshade->SetPoint(point,xhigh+100,nexty);
            point++;
            break;
         case 3:
            grshade->SetPoint(point,lastx,ylow-100);
            point++;
            grshade->SetPoint(point,nextx,ylow-100);
      point++;
      break;
      }
   } else if(nearestedge2 == (nearestedge1-1 >= 0 ? nearestedge1-1 : nearestedge1+3)) {
      // when graphs will be connected across a corner, usually a triangle will be left in
      // to fix, add three points, two outside the boundary, and one outside the corner.
      switch(nearestedge2) {
         case 0:
            grshade->SetPoint(point,lastx,yhigh+100);
            point++;
            grshade->SetPoint(point,xlow-100,yhigh+100);
            point++;
            grshade->SetPoint(point,xlow-100,nexty);
            point++;
            break;      
    case 1:
       grshade->SetPoint(point,xhigh+100,lasty);
       point++;
       grshade->SetPoint(point,xhigh+100,yhigh+100);
      point++;
      grshade->SetPoint(point,nextx,yhigh+100);
      point++;
      break;      
    case 2:
      grshade->SetPoint(point,lastx,ylow-100);
      point++;
      grshade->SetPoint(point,xhigh+100,ylow-100);
      point++;
      grshade->SetPoint(point,xhigh+100,nexty);
      point++;
      break;      
    case 3:
      grshade->SetPoint(point,xlow-100,lasty);
      point++;
      grshade->SetPoint(point,xlow-100,ylow-100);
      point++;
      grshade->SetPoint(point,nextx,ylow-100);
      point++;
      break;      
      }
   }
   
   // this is the last point drawn in the second graph
   double finalx = 0;
   double finaly = 0;
   for (int i=0;i<N;i++) {
      if (x2[N-i-1] > cutx && y2[N-i-1] > cuty) {
         grshade->SetPoint(point,x2[N-i-1],y2[N-i-1]);
         finalx = x2[N-i-1];
         finaly = y2[N-i-1];
         point++;
      }
   }
   
  // repeat for the other end of the band
  int nearestedge3 = 0;
  double dist = fabs(finalx-1-xlow);
  if(fabs(finaly-yhigh) < dist) {
    dist = fabs(finaly-yhigh);
    nearestedge3 = 1;
  }
  if(fabs(finalx-1-xhigh) < dist) {
    dist = fabs(finalx-1-xhigh);
    nearestedge3 = 2;
  }
  if(fabs(finaly-ylow) < dist) {
    dist = fabs(finaly-ylow);
    nearestedge3 = 3;
  }

  int nearestedge4 = 0;
  double dist = fabs(firstx-1-xlow);
  if(fabs(firsty-yhigh) < dist) {
    dist = fabs(firsty-yhigh);
    nearestedge4 = 1;
  }
  if(fabs(firstx-1-xhigh) < dist) {
    dist = fabs(firstx-1-xhigh);
    nearestedge4 = 2;
  }
  if(fabs(firsty-ylow) < dist) {
     dist = fabs(firstx-ylow);
     nearestedge4 = 3;
  }
  
  if(nearestedge4 == nearestedge3) {
     switch(nearestedge3) {
        case 0:
           grshade->SetPoint(point,xlow-100,finaly);
           point++;
           grshade->SetPoint(point,xlow-100,firsty);
           point++;
           break;
        case 1:
           grshade->SetPoint(point,finalx,yhigh+100);
           point++;
           grshade->SetPoint(point,firstx,yhigh+100);
           point++;
           break;
        case 2:
           grshade->SetPoint(point,xhigh+100,finaly);
           point++;
           grshade->SetPoint(point,xhigh+100,firsty);
           point++;
           break;
        case 3:
           grshade->SetPoint(point,finalx,ylow-100);
           point++;
           grshade->SetPoint(point,firstx,ylow-100);
           point++;
           break;
     }
  } else if(nearestedge4 == (nearestedge3-1 >= 0 ? nearestedge3-1 : nearestedge3+3)) {
     switch(nearestedge4) {
        case 0:
           grshade->SetPoint(point,finalx,yhigh+100);
           point++;
           grshade->SetPoint(point,xlow-100,yhigh+100);
           point++;
           grshade->SetPoint(point,xlow-100,firsty);
           point++;
      break;      
        case 1:
           grshade->SetPoint(point,xhigh+100,finaly);
           point++;
           grshade->SetPoint(point,xhigh+100,yhigh+100);
           point++;
           grshade->SetPoint(point,firstx,yhigh+100);
           point++;
           break;      
        case 2:
           grshade->SetPoint(point,finalx,ylow-100);
           point++;
           grshade->SetPoint(point,xhigh+100,ylow-100);
           point++;
           grshade->SetPoint(point,xhigh+100,firsty);
           point++;
           break;      
        case 3:
           grshade->SetPoint(point,xlow-100,finaly);
g           point++;
           grshade->SetPoint(point,xlow-100,ylow-100);
           point++;
           grshade->SetPoint(point,firstx,ylow-100);
           point++;
           break;      
     }
  }
  grshade->Set(point);
  
  // Now draw the plot...
  grshade->SetFillStyle(fillStyle);
  grshade->SetFillColor(fillColor);
  //  grshade->SetMarkerStyle(21);
  grshade->Draw("F");
  
  return grshade;
}

void DummyLegendExpected(TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth)
{

   TGraph* gr = new TGraph();
   gr->SetFillColor(fillColor);
   gr->SetFillStyle(fillStyle);
   gr->SetLineColor(lineColor);
   gr->SetLineStyle(lineStyle);
   gr->SetLineWidth(lineWidth);
   leg->AddEntry(gr,what,"LF");
}

