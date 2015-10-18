#include "CombinationGlob.C"
#include "TColor.h"
#include <TStyle.h>
#include "TPave.h"

#include <TFile.h>
#include <TTree.h>
#include <Riostream.h>
#include "contourmacros/GG_direct_8TeVobs.C"
#include "TROOT.h"
#include <algorithm>
#include <iostream>
#include <sstream>

void initialize() {
   gSystem->Load("libSusyFitter.so");
}

void SUSY_contourplots_p0(
   TString fname0="", TString fname1="", TString fname2="", 
   const char* prefix="",
   const float& lumi = 5,
   TString fnamesr1="", TString fnamesr2="", TString fnamesr3="",
   int discexcl = 1)
{

   initialize();
   
  //set style and remove existing canvas'
   CombinationGlob::Initialize();
  
  cout << "--- Plotting mGluino versus mLSP " << endl;

  // Open files and retrieve histogram
  TFile* f0;
  TFile* f1;
  TFile* f2;
  
  cout << "--- Reading root base file0: " << fname0 << endl;
  f0 = TFile::Open( fname0, "READ" );
  cout << "--- Reading root base file1: " << fname1 << endl;
  f1 = TFile::Open( fname1, "READ" );
  cout << "--- Reading root base file2: " << fname2 << endl;
  f2 = TFile::Open( fname2, "READ" );

  if(!f0 || !f1 || !f2) cout << "Cannot open!"<< endl;

  // Which variable to plot?
  TString disc_p0exp = "p0exp";

  // hist for best SR contour
  TH2F* histecls0 = (TH2F*)f0->Get(disc_p0exp);
  // place holder for xsec +/-1 lines
  TH2F* histecls1 = (TH2F*)f1->Get(disc_p0exp);  
  TH2F* histecls2 = (TH2F*)f2->Get(disc_p0exp);

  TH2F* contourobs_comb(0);
  if (histecls0!=0) { contourobs_comb     = FixAndSetBorders( *histecls0, "contourobs_comb", "contourobs_comb", 0 ); }
  
  TFile* f0_sr1;
  TFile* f0_sr2;
  TFile* f0_sr3;

  f0_sr1 = TFile::Open( fnamesr1, "READ" );
  cout << "--- Reading root base file sr1: " << fnamesr1 << endl;  
  f0_sr2 = TFile::Open( fnamesr2, "READ" );
  cout << "--- Reading root base file sr2: " << fnamesr2 << endl;
  f0_sr3 = TFile::Open( fnamesr3, "READ" );
  cout << "--- Reading root base file sr3: " << fnamesr3 << endl;
  
  if( !f0_sr1 || !f0_sr2 | !f0_sr3 ) cout << "Cannot open input files!"<< endl;
  
  TH2F* histobs0zz_sr1 = (TH2F*)f0_sr1->Get(disc_p0exp); 
  TH2F* histobs0zz_sr2 = (TH2F*)f0_sr2->Get(disc_p0exp);
  TH2F* histobs0zz_sr3 = (TH2F*)f0_sr3->Get(disc_p0exp);  

  TH2F* contourobs_sr1 = (histobs0zz_sr1!=0 ? FixAndSetBorders( *histobs0zz_sr1, "contourobs_sr1", "contourobs_sr1", 0 ): 0);
  TH2F* contourobs_sr2 = (histobs0zz_sr2!=0 ? FixAndSetBorders( *histobs0zz_sr2, "contourobs_sr2", "contourobs_sr2", 0 ): 0);
  TH2F* contourobs_sr3 = (histobs0zz_sr3!=0 ? FixAndSetBorders( *histobs0zz_sr3, "contourobs_sr3", "contourobs_sr3", 0 ): 0);
  
  gStyle->SetPaintTextFormat(".2g");
      
  // --- draw
  // Create canvas
  TCanvas* c = new TCanvas( "c", "A scan of m_#tilda{g} versus m_{#tilda{#chi}_{1}^{0}}", 0, 0, 
                            CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[1] );

  // Create and draw the frame
  TH2F *frame = new TH2F("frame", "m_#tilda{g} vs m_{#tilda{#chi}_{1}^{0}} - ATLAS",
                         180, 200., 2000., 200, 0., 1400. );
     
  // Set common frame style
  gPad->SetTopMargin( 0.07  );
  gPad->SetBottomMargin( 0.120  );
  gPad->SetRightMargin( 0.12 );
  gPad->SetLeftMargin( 0.1  );

  //Palette
  frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
  frame->SetYTitle( "m_{#tilde{#chi}_{1}^{0}} [GeV]" );
  frame->SetZTitle( "X-Section" );
  frame->GetXaxis()->SetTitleOffset(1.15);
  frame->GetYaxis()->SetTitleOffset(1.15);
  frame->GetZaxis()->SetTitleOffset(1);

  frame->GetXaxis()->SetTitleFont( 42 );
  frame->GetYaxis()->SetTitleFont( 42 );
  frame->GetXaxis()->SetLabelFont( 42 );
  frame->GetYaxis()->SetLabelFont( 42 );

  frame->GetXaxis()->SetTitleSize( 0.04 );
  frame->GetYaxis()->SetTitleSize( 0.04 );
  frame->GetXaxis()->SetLabelSize( 0.035 );
  frame->GetYaxis()->SetLabelSize( 0.035 );
  frame->GetZaxis()->SetLabelSize( 0.015 );
  
  frame->Draw("axis");

  // creat legend
  TLegend *leg = new TLegend(0.45,0.68,0.8,0.9);
  leg->SetTextSize( CombinationGlob::DescriptionTextSize );
  leg->SetFillStyle(0000); 
  leg->SetTextSize( 0.03 );
  leg->SetTextFont( 42 );

  Int_t c_myYellow   = TColor::GetColor("#ffe938"); 
  Int_t c_myRed      = TColor::GetColor("#aa000");
  Int_t c_myExp      =  kBlue+2; //TColor::GetColor("#28373c");

  // color code for colz
  const Int_t ncontours=99;
  const Int_t NRGBs=4;
  Double_t stops[NRGBs] = {0.00, 0.33, 0.66, 1.00};
  Double_t red[NRGBs]   = {1.00, 238./255., 139./255., 0.00};
  Double_t green[NRGBs] = {1.00, 201./255., 90./255., 0.00};
  Double_t blue[NRGBs]  = {1.00, 0.00, 0.00, 0.00};
  
  TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, ncontours);
  gStyle->SetNumberContours(ncontours);

  // plot p0 map in 2D 
  contourobs_comb->Draw("colz same");
  latexz=TLatex();
  latexz.SetTextSize(0.035);
  latexz.SetTextFont( 42 );
  latexz.SetTextAngle(90.);
  latexz.DrawText(2200, 20,"p0 significance on best SR");

  // plot 3-sigma contours
  if (contourobs_comb!=0) DrawContourLine3sigma( leg, contourobs_comb, "Best SR", CombinationGlob::c_DarkRed, 1, 6);
  if (contourobs_sr1!=0) DrawContourLine3sigma( leg, contourobs_sr1, "SR4j Meff2400-1,2jetpt200-3,4jetpt150", CombinationGlob::c_DarkOrange, 1, 2);
  if (contourobs_sr2!=0) DrawContourLine3sigma( leg, contourobs_sr2, "SR4j Meff2400-1,2jetpt200-3,4jetpt60", CombinationGlob::c_DarkGreen, 1, 2);
  if (contourobs_sr3!=0) DrawContourLine3sigma( leg, contourobs_sr3, "SR4j Meff1600-1,2jetpt200-3,4jetpt150", CombinationGlob::c_DarkBlue, 1, 2);
  
  gPad->RedrawAxis();     
  TLine lineExcl = ( TLine(200,200,800,800));
  lineExcl.SetLineStyle(9);
  lineExcl.SetLineWidth(1);
  lineExcl.SetLineColor(14);
  lineExcl.Draw("same") ;                
  
  // mass forbidden line
  TLatex massforbidden = TLatex(300,380,"m_{#tilde{g}} < m_{#tilde{#chi}^{0}_{1}}");
  massforbidden.SetTextSize(0.032);
  massforbidden.SetTextColor(14);
  massforbidden.SetTextAngle(45.);
  massforbidden.SetTextFont(42);
  massforbidden.Draw("same"); 

  // plot 8 TeV exclusion:
  TGraphAsymmErrors *g=GG_direct_8TeVobs();
  g->SetLineColor(c_myRed);
  g->SetLineWidth(2);
  g->SetLineStyle(6);
  g->Draw("same");
  leg->AddEntry(g,"Observed limit at 95% CL (#sqrt{s} = 8 TeV)","l"); 
    
  // Cosmetics for plotting 
  Float_t textSizeOffset = +0.000;
  Double_t xmax = frame->GetXaxis()->GetXmax();
  Double_t xmin = frame->GetXaxis()->GetXmin();
  Double_t ymax = frame->GetYaxis()->GetXmax();
  Double_t ymin = frame->GetYaxis()->GetXmin();
  Double_t dx   = xmax - xmin;
  Double_t dy   = ymax - ymin;
   
  TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025, "" );
  Leg0->SetTextAlign( 11 );
  Leg0->SetTextFont( 42 );
  Leg0->SetTextSize( CombinationGlob::DescriptionTextSize);
  Leg0->SetTextColor( 1 );
  Leg0->AppendPad();

  TLatex* decayLabel = new TLatex();
  decayLabel->SetNDC();
  decayLabel->SetTextFont(42);
  decayLabel->SetTextColor(ROOT::kBlack);
  decayLabel->SetTextSize( 0.0335 );
  decayLabel->DrawLatex(0.14, 0.962,"#tilde{g}#tilde{g} production, #it{B}(#tilde{g} #rightarrow qq #tilde{#chi}_{1}^{0})=100%");

  TLatex* atlasLabel = new TLatex();
  atlasLabel->SetNDC();
  atlasLabel->SetTextFont(42);
  atlasLabel->SetTextColor(ROOT::kBlack);
  atlasLabel->SetTextSize( 0.04 );
  atlasLabel->DrawLatex(0.13, 0.87,"#bf{#it{ATLAS}}");
  atlasLabel->AppendPad();

  TLatex* progressLabel = new TLatex();
  progressLabel->SetNDC();
  progressLabel->SetTextFont(42);
  progressLabel->SetTextColor(ROOT::kBlack);
  progressLabel->SetTextSize( 0.04 );
  progressLabel->DrawLatex(0.23, 0.87,"Simulation Internal");
  progressLabel->AppendPad();
  
  TLatex *Leg1 = new TLatex();
  Leg1->SetNDC();
  Leg1->SetTextFont( 42 );
  Leg1->SetTextSize( 0.04 );
  Leg1->SetTextColor( ROOT::kBlack );
  Leg1->DrawLatex(0.13, 0.79, "#int Ldt = 2 fb^{-1}, #sqrt{s} = 13 TeV");
  Leg1->AppendPad();

  TLatex *Leg2 = new TLatex();
  Leg2->SetNDC();
  Leg2->SetTextSize(0.04);
  Leg2->SetTextColor( 1 );
  Leg2->SetTextFont( 42 );
  Leg2->DrawLatex(0.13, 0.65, prefix);
  if (prefix!=0) { Leg2->AppendPad(); }
    
  TLatex *Leg2 = new TLatex();
  Leg2->SetNDC();
  Leg2->SetTextFont( 42 );
  Leg2->SetTextSize( 0.04 );
  Leg2->SetTextColor( ROOT::kBlack );
  Leg2->DrawLatex(0.13, 0.7, "3#sigma evidence");
  Leg2->AppendPad();

  TLatex *Leg3 = new TLatex();
  Leg3->SetNDC();
  Leg3->SetTextFont( 42 );
  Leg3->SetTextSize( 0.04 );
  Leg3->SetTextColor( ROOT::kBlack );
  Leg3->DrawLatex(0.13, 0.6, "(Fit to SR,CRT,CRW)");
  Leg3->AppendPad();

  if (prefix!=0) { Leg2->AppendPad(); }

  leg->Draw("same");

  c->Update();
  gPad->Update();
  
  frame->Draw("same"); 
  
  // create plots
  // store histograms to output file
  TObjArray* arr = fname0.Tokenize("/");
  TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-2 );
  TString outfile = fname0.ReplaceAll("/","").ReplaceAll(".root","").ReplaceAll("_merged_hypotest__1_harvest_list","").ReplaceAll("_fixSigXSecNominal__1_harvest_list","");
  delete arr;
  
  CombinationGlob::imgconv( c, Form("plots/atlascls_SM_GG_direct_%s",outfile.Data()));
}


void
DummyLegendExpected(TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth)
{
  TGraph* gr = new TGraph();
  gr->SetFillColor(fillColor);
  gr->SetFillStyle(fillStyle);
  gr->SetLineColor(lineColor);
  gr->SetLineStyle(lineStyle);
  gr->SetLineWidth(lineWidth);
  leg->AddEntry(gr,what,"LF");
}

void
DummyLegendBestSR(TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth)
{
  TGraph* gr = new TGraph();
  gr->SetFillColor(fillColor);
  gr->SetFillStyle(fillStyle);
  gr->SetLineColor(lineColor);
  gr->SetLineStyle(lineStyle);
  gr->SetLineWidth(lineWidth);
  leg->AddEntry(gr,what,"LF");
}

void
DummyLegendLine(TLegend* leg, TString what, Int_t lineColor, Int_t lineStyle, Int_t lineWidth)
{
  TGraph* gr = new TGraph();
  gr->SetFillColor(0);
  gr->SetFillStyle(0);
  gr->SetLineColor(lineColor);
  gr->SetLineStyle(lineStyle);
  gr->SetLineWidth(lineWidth);
  leg->AddEntry(gr,what,"L");
}

TGraph*
ContourGraph( TH2F* hist)
{

   TGraph* gr0 = new TGraph();
   TH2F* h = (TH2F*)hist->Clone();
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
      //
      //    mg->Add((TGraph*)list->At(k));
   }
   
   gr->SetName(hist->GetName());
   int N = gr->GetN();
   double x0, y0;



   //  for(int j=0; j<N; j++) {
   //    gr->GetPoint(j,x0,y0);
   //    cout << j << " : " << x0 << " : "<<y0 << endl;
   //  }
   //  //  gr->SetMarkerSize(2.0);
   //  gr->SetMarkerSize(2.0);
   //  gr->SetMarkerStyle(21);

   //  gr->Draw("LP");


   //  cout << "Generated graph " << gr << " with name " << gr->GetName() << endl;
   return gr;
   
}


TGraph*
DrawExpectedBand( TGraph* gr1,  TGraph* gr2, Int_t fillColor, Int_t fillStyle, Int_t cut = 0)
{
  //  TGraph* gr1 = new TGraph( *graph1 );
  //  TGraph* gr2 = new TGraph( *graph2 );

  int number_of_bins = max(gr1->GetN(),gr2->GetN());
  
  const Int_t gr1N = gr1->GetN();
  const Int_t gr2N = gr2->GetN();

  const Int_t N = number_of_bins;
  Double_t x1[N], y1[N], x2[N], y2[N];

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

  Double_t xx1, yy1;

  for(int j=0; j<gr2N; j++) {
    gr2->GetPoint(j,xx1,yy1);
      x2[j] = xx1;
      y2[j] = yy1;
  }
  if (gr2N < N) {
    for(int i=gr2N; i<N; i++) {
      x2[i] = x2[gr1N-1];
      y2[i] = y2[gr1N-1];
    }      
  }

  
  TGraph *grshade = new TGraphAsymmErrors(2*N);

  for (int i=0;i<N;i++) {
    if (x1[i] > cut)
      grshade->SetPoint(i,x1[i],y1[i]);
    if (x2[N-i-1] > cut)
      grshade->SetPoint(N+i,x2[N-i-1],y2[N-i-1]);
  }

  // Apply the cut in the shade plot if there is something that doesn't look good...
  int Nshade = grshade->GetN();
  double x0, y0;
  double x00, y00;

  for(int j=0; j<Nshade; j++) {
    grshade->GetPoint(j,x0,y0);
    if ((x0 != 0) && (y0 != 0)) {
      x00 = x0;
      y00 = y0;
      break;
    }
  }

  for(int j=0; j<Nshade; j++) {
    grshade->GetPoint(j,x0,y0);
    if ((x0 == 0) && (y0 == 0)) 
      grshade->SetPoint(j,x00,y00);
  }


  // Now draw the plot... 
  grshade->SetFillStyle(fillStyle);
  grshade->SetFillColor(fillColor);
  grshade->SetLineColor(fillColor);
  grshade->SetMarkerStyle(21);
  grshade->GetXaxis()->SetRangeUser(200.,800.);
  grshade->GetXaxis()->SetLimits(200.,800.);
  grshade->SetMinimum(0.);
  grshade->SetMaximum(500.);
  grshade->Draw("FLA same");
  
  return grshade;
}


void
MirrorBorders( TH2& hist )
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


TH2F*
AddBorders( const TH2& hist, const char* name=0, const char* title=0)
{
  int nbinsx = hist.GetNbinsX();
  int nbinsy = hist.GetNbinsY();
  
  double xbinwidth = ( hist.GetXaxis()->GetBinCenter(nbinsx) - hist.GetXaxis()->GetBinCenter(1) ) / double(nbinsx-1);
  double ybinwidth = ( hist.GetYaxis()->GetBinCenter(nbinsy) - hist.GetYaxis()->GetBinCenter(1) ) / double(nbinsy-1);
  
  double xmin = hist.GetXaxis()->GetBinCenter(0) - xbinwidth/2. ;
  double xmax = hist.GetXaxis()->GetBinCenter(nbinsx+1) + xbinwidth/2. ;
  double ymin = hist.GetYaxis()->GetBinCenter(0) - ybinwidth/2. ;
  double ymax = hist.GetYaxis()->GetBinCenter(nbinsy+1) + ybinwidth/2. ;
  
  TH2F* hist2 = new TH2F(name, title, nbinsx+2, xmin, xmax, nbinsy+2, ymin, ymax);
  
  for (Int_t ibin1=0; ibin1 <= hist.GetNbinsX()+1; ibin1++) {
    for (Int_t ibin2=0; ibin2 <= hist.GetNbinsY()+1; ibin2++)
      hist2->SetBinContent( ibin1+1, ibin2+1, hist.GetBinContent(ibin1,ibin2) );
  }
  
  return hist2;
}


void SetBorders( TH2 &hist, Double_t val=0 )
{
  int numx = hist.GetNbinsX();
  int numy = hist.GetNbinsY();
  
  for(int i=0; i <= numx+1 ; i++){
    hist.SetBinContent(i,0,val);
    hist.SetBinContent(i,numy+1,val);
  }
  for(int i=0; i <= numy+1 ; i++) {
    hist.SetBinContent(0,i,val);
    hist.SetBinContent(numx+1,i,val);
  }
}


TH2F* 
FixAndSetBorders( const TH2& hist, const char* name=0, const char* title=0, Double_t val=0 )
{
  TH2F* hist0 = hist.Clone(); // histogram we can modify
  
  MirrorBorders( *hist0 );    // mirror values of border bins into overflow bins
  
  TH2F* hist1 = AddBorders( *hist0, "hist1", "hist1" );   
  // add new border of bins around original histogram,
  // ... so 'overflow' bins become normal bins
  SetBorders( *hist1, val );                              
  // set overflow bins to value 1
  
  TH2F* histX = AddBorders( *hist1, "histX", "histX" );   
  // add new border of bins around original histogram,
  // ... so 'overflow' bins become normal bins
  
  TH2F* hist3 = histX->Clone();
  hist3->SetName( name!=0 ? name : "hist3" );
  hist3->SetTitle( title!=0 ? title : "hist3" );
  
  delete hist0; delete hist1; delete histX;
  return hist3; // this can be used for filled contour histograms
}


void 
DrawContourSameColor( TLegend *leg, TH2F* hist, Int_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE, Bool_t isnobs=kFALSE )
{
  if (nsigma < 1 || nsigma > 3) {
    cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
	 << "==> abort" << endl;
    exit(1);
  }
  nsigma--; // used as array index
  
  Int_t lcol_sigma;
  Int_t fcol_sigma[3];
  
  if( color == "pink" ){
    lcol_sigma    = CombinationGlob::c_VDarkPink;
    fcol_sigma[0] = CombinationGlob::c_LightPink;
    fcol_sigma[1] = CombinationGlob::c_LightPink;
    fcol_sigma[2] = CombinationGlob::c_LightPink;
  }
  else if( color == "green" ){ // HF
    lcol_sigma    = CombinationGlob::c_VDarkGreen;
    fcol_sigma[0] = CombinationGlob::c_DarkGreen;
    fcol_sigma[1] = CombinationGlob::c_LightGreen;
    fcol_sigma[2] = CombinationGlob::c_VLightGreen;
  } 
  else if( color == "yellow" ){
    lcol_sigma    = CombinationGlob::c_VDarkYellow;
    fcol_sigma[0] = CombinationGlob::c_DarkYellow;
    fcol_sigma[1] = CombinationGlob::c_DarkYellow;
    fcol_sigma[2] = CombinationGlob::c_White; //c_DarkYellow;
  }
  else if( color == "orange" ){
    lcol_sigma    = CombinationGlob::c_VDarkOrange;
    fcol_sigma[0] = CombinationGlob::c_DarkOrange;
    fcol_sigma[1] = CombinationGlob::c_LightOrange; // c_DarkOrange
    fcol_sigma[2] = CombinationGlob::c_VLightOrange;
  }
  else if( color == "gray" ){
    lcol_sigma    = CombinationGlob::c_VDarkGray;
    fcol_sigma[0] = CombinationGlob::c_LightGray;
    fcol_sigma[1] = CombinationGlob::c_LightGray;
    fcol_sigma[2] = CombinationGlob::c_LightGray;
  }
  else if( color == "blue" ){
    lcol_sigma    = CombinationGlob::c_DarkBlueT1;
    fcol_sigma[0] = CombinationGlob::c_BlueT5;
    fcol_sigma[1] = CombinationGlob::c_BlueT3;
    fcol_sigma[2] = CombinationGlob::c_White;  //CombinationGlob::c_BlueT2;
  }
  
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[1];
  double signif = TMath::NormQuantile(1-pval);
  double dnsigma = double(nsigma)-1.;
  double dsignif = signif + dnsigma;
  h->SetContourLevel( 0, dsignif );

  if( !second ){
    h->SetFillColor( fcol_sigma[nsigma] );
    
    if (!linesOnly) h->Draw( "samecont0" );
  }

  /*  
  // inverse contours plot, needed in case of contours within contours
  if (inverse!=0) {
    TH2F* g = new TH2F( *inverse );
    g->SetContour( 1 );
    g->SetContourLevel( 0, CombinationGlob::cl_percent[nsigma] );
    if( !second ){
      g->SetFillColor( 0 );
      if (!linesOnly) g->Draw( "samecont0" );
    }
  }
  */

  h->SetLineColor( nsigma==1? 4 : lcol_sigma );
   if (isnobs)h->SetLineColor( nsigma==1? 1 : lcol_sigma );
  //h->SetLineStyle( 4 );
  h->SetLineWidth( 2 );
  h->Draw( "samecont3" );
  
  if (linesOnly&&!isnobs)
    if(nsigma==1){ leg->AddEntry(h,"expected 95% C.L. exclusion ","l");}
  if (isnobs)
    if(nsigma==1){ leg->AddEntry(h,"observed 95% C.L. exclusion","l");}  
  if (!linesOnly) {
  if(nsigma==0){ leg->AddEntry(h,"expected 68% C.L. exclusion","l"); }
  if(nsigma==2){ leg->AddEntry(h,"expected 99% C.L. exclusion","l");}
  }

  
}


void 
DrawContourSameColorDisc( TLegend *leg, TH2F* hist, Double_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE )
{
  if (nsigma < 0.5 || nsigma > 10.5 ) {
    cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
	 << "==> abort" << endl;
    exit(1);
  }
  
  Int_t lcol_sigma;
  Int_t fcol_sigma[3];

  if( color == "pink" ){
    lcol_sigma    = CombinationGlob::c_DarkPink;
    fcol_sigma[0] = CombinationGlob::c_VLightPink;
    fcol_sigma[1] = CombinationGlob::c_VLightPink;
    fcol_sigma[2] = CombinationGlob::c_VLightPink;
  }
  else if( color == "green" ){ // HF
    lcol_sigma    = CombinationGlob::c_VDarkGreen;
    fcol_sigma[0] = CombinationGlob::c_DarkGreen;
    fcol_sigma[1] = CombinationGlob::c_LightGreen;
    fcol_sigma[2] = CombinationGlob::c_VLightGreen;
  } 
  else if( color == "yellow" ){
    lcol_sigma    = CombinationGlob::c_VDarkYellow;
    fcol_sigma[0] = CombinationGlob::c_DarkYellow;
    fcol_sigma[1] = CombinationGlob::c_DarkYellow;
    fcol_sigma[2] = CombinationGlob::c_White; //c_DarkYellow;
  }
  else if( color == "orange" ){
    lcol_sigma    = CombinationGlob::c_VDarkOrange;
    fcol_sigma[0] = CombinationGlob::c_DarkOrange;
    fcol_sigma[1] = CombinationGlob::c_LightOrange; // c_DarkOrange
    fcol_sigma[2] = CombinationGlob::c_VLightOrange;
  }
  else if( color == "gray" ){
    lcol_sigma    = CombinationGlob::c_VDarkGray;
    fcol_sigma[0] = CombinationGlob::c_LightGray;
    fcol_sigma[1] = CombinationGlob::c_LightGray;
    fcol_sigma[2] = CombinationGlob::c_LightGray;
  }
  else if( color == "blue" ){
    lcol_sigma    = CombinationGlob::c_DarkBlueT1;
    fcol_sigma[0] = CombinationGlob::c_LightBlue;
    fcol_sigma[1] = CombinationGlob::c_LightBlue;
    fcol_sigma[2] = CombinationGlob::c_LightBlue;
  }

  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double dsignif = double (nsigma);
  h->SetContourLevel( 0, dsignif );

  Int_t mycolor = (nsigma==3   ? 0 : 2);
  Int_t mycolor = (nsigma==2 ? 1 : 2);

  h->SetFillStyle(3003);

  if( !second ){
    h->SetFillColor( fcol_sigma[mycolor] );
    if (!linesOnly) h->Draw( "samecont0" );
  }

  h->SetLineColor( (nsigma==3) ? lcol_sigma : lcol_sigma );

  h->SetLineStyle( nsigma==3 || nsigma==2 ? 1 : 2 );
  h->SetLineWidth( nsigma==3 || nsigma==2 ? 2 : 1 );

  
  h->Draw( "samecont3" );

  if(nsigma==3)   { leg->AddEntry(h,"3 #sigma evidence","l"); }
  if(nsigma==6)   { leg->AddEntry(h,"N (int) #sigma","l"); }
  if(nsigma==2)   { leg->AddEntry(h,"2 #sigma evidence","l"); }
}




void
DrawContourMassLine(TH2F* hist, Double_t mass, int color=14 )
{

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


void 
DrawContourLine95( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2, Int_t linewidth=2 )
{
   
   // contour plot
   TH2F* h = new TH2F( *hist );
   h->SetContour( 1 );
   double pval = CombinationGlob::cl_percent[1];
   double signif = TMath::NormQuantile(1-pval);
   //cout << "signif: " <<signif << endl;
   h->SetContourLevel( 0, signif );
   
   h->SetLineColor( linecolor );
   h->SetLineWidth( linewidth );
   h->SetLineStyle( linestyle );
   h->Draw( "samecont3" );
   
   if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}


void
DrawContourLine3sigma( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2, Int_t linewidth=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = (1.-0.9973)*0.5; // one-sided
  double signif = TMath::NormQuantile(1-pval);
  cout <<"DrawContourLine3sigma: pval="<<pval<<", "<<signif<<"sigma for "<<text<<endl;
  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( linewidth );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}

void
DrawContourLine99( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2, Int_t linewidth=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[2];
  double signif = TMath::NormQuantile(1-pval);
    
  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( linewidth );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}


void
DrawContourLine68( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2 )
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

TH2F* linearsmooth(const TH2& hist, const char* name, const char* title) {
   int nbinsx = hist.GetNbinsX();
   int nbinsy = hist.GetNbinsY();

   double xbinwidth = ( hist.GetXaxis()->GetBinCenter(nbinsx) - hist.GetXaxis()->GetBinCenter(1) ) / double(nbinsx-1);
   double ybinwidth = ( hist.GetYaxis()->GetBinCenter(nbinsy) - hist.GetYaxis()->GetBinCenter(1) ) / double(nbinsy-1);

   int nbinsxsm = 2*nbinsx - 1 ;
   int nbinsysm = 2*nbinsy - 1 ;

   double xmin = hist.GetXaxis()->GetBinCenter(1) - xbinwidth/4. ;
   double xmax = hist.GetXaxis()->GetBinCenter(nbinsx) + xbinwidth/4. ;
   double ymin = hist.GetYaxis()->GetBinCenter(1) - ybinwidth/4. ;
   double ymax = hist.GetYaxis()->GetBinCenter(nbinsy) + ybinwidth/4. ;

   TH2F* hist2 = new TH2F(name, title, nbinsxsm, xmin, xmax, nbinsysm, ymin, ymax);

   for (Int_t ibin1=1; ibin1 < hist.GetNbinsX(); ibin1++) {
      for (Int_t ibin2=1; ibin2 < hist.GetNbinsY(); ibin2++) {
         float f00 = hist.GetBinContent(ibin1,ibin2);
         float f10 = hist.GetBinContent(ibin1+1,ibin2);
         float f01 = hist.GetBinContent(ibin1,ibin2+1);
         float f11 = hist.GetBinContent(ibin1+1,ibin2+1);
         
         for (Int_t i=0; i<=2; ++i)
            for (Int_t j=0; j<=2; ++j) {
               float x = i*0.5; float y = j*0.5;
               float val = (1-x)*(1-y)*f00 + x*(1-y)*f10 + (1-x)*y*f01 + x*y*f11 ;
               Int_t jbin1 = 2*ibin1 - 1 + i;
               Int_t jbin2 = 2*ibin2 - 1 + j;
               hist2->SetBinContent(jbin1,jbin2,val);
            }
      }
   }
   
   return hist2; // caller owns histogram
}


void GetSRName(int fID, TString SRset, TString& text=""){
   cout<<" "<< SRset<<" "<<fID<<endl;
   
   TString SRSets[15]={"A1+C1","A1+C2","A1+C3", "A2+C1","A2+C2","A2+C3", "no+C1","no+C2","no+C3", "A3+C1","A3+C2","A3+C3", "A4+C1","A4+C2","A4+C3"};
//   TString SRSets[15]={"A1+C1","A2+C1","no+C1","A3+C1","A4+C1", "A1+C2","A2+C2","no+C2","A3+C2","A4+C2","A1+C3","A2+C3","no+C3","A3+C3","A4+C3"};
   TString SRAs[5]= {"A1","A2","no","A3","A4"};
   TString SRABs[5]= {"A1+B","A2+B","no+B","A3+B","A4+B"};
   TString SRABCSets[20]={"A1+B","A2+B","no+B","A3+B","A4+B", "A1+C1","A1+C2","A1+C3", "A2+C1","A2+C2","A2+C3", "no+C1","no+C2","no+C3", "A3+C1","A3+C2","A3+C3", "A4+C1","A4+C2","A4+C3"};
   TString SRAABCSets[25]={"A1","A2","no","A3","A4", "A1+B","A2+B","no+B","A3+B","A4+B", "A1+C1","A1+C2","A1+C3", "A2+C1","A2+C2","A2+C3", "no+C1","no+C2","no+C3", "A3+C1","A3+C2","A3+C3", "A4+C1","A4+C2","A4+C3"};
   
   cout<< fID<<endl;
   if (SRset=="ABC"){
      text= SRABCSets[fID-1];
   }else if (SRset=="AC"){
      text= SRSets[fID-1];
   }else if (SRset=="A"){
      text= SRAs[fID-1];
   }else if (SRset=="AABC"){
      text= SRAABCSets[fID-1];
   }else{
      text= SRABs[fID-1];
   }
}


                           
