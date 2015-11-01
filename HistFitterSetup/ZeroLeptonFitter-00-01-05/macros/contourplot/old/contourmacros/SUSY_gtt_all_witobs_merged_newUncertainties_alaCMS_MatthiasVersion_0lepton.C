#include "CombinationGlob.C"
#include "TColor.h"
#include <TFile.h>
#include <TTree.h>
#include <Riostream.h>
//#include "zleptonoffciallcontours.C"
#include <algorithm>
#include "summary_harvest_tree_description.h"

TH2F* Draw1fbLimit();

void PlotFunc3Par(double p0, double p1,double p2,double p3,double xmin,double xmax);
void PlotFunc4Par(double p0, double p1,double p2,double p3,double p4,double xmin,double xmax);

void SUSY_gtt_all_witobs_merged( TString fname1 = "m0m12_nofloat_exp.root",
				 TString fname2 = "m0m12_nofloat_exp.root", 
				 TString fname3 = "m0m12_nofloat_exp.root", 
                                 const char* prefix="",
                                 const float& lumi = 20,
                                 bool showsig = true,
                                 int discexcl = 1,
				 TString ullistfile = "Merged_Output_hypotest_SM_SS_twostepCN_sleptons_SR4_combined_ul__1_harvest_list",
                                 int showtevatron = 0,
                                 TString hname0 = "sigp1clsf", //"sigCLs",
                                 TString hname0_exp = "sigp1expclsf",//"sigCLsexp",
                                 TString hname0_1su = "sigclsu1s",//"sigCLsexp1su",
                                 TString hname0_1sd = "sigclsd1s",//"sigCLsexp1sd",
                                 TString hname1 = "sigp0",
                                 TString hname1_exp = "sigp0",
                                 TString fnameMass= "mSugraGridtanbeta10_gluinoSquarkMasses.root"
                                 )
{

  //bool taulimits=true;
  bool taulimits=false;

  bool gluinomasses=false;
  //  TString xSection = "7j55GtGrid_xSection.root";
  //TFile* histFile = TFile::Open(xSection,"READ");
  //TH2F* histoxSec = (TH2F*)histFile->Get("excludedXsec"); 

  // set style and remove existing canvas'
  CombinationGlob::Initialize();
  
  cout << "--- Plotting m0 versus m12 " << endl;
  
  // --- prepare
  
  // open reference files, and retrieve histogram
  cout << "--- Reading root base file: " << fname1 << endl;
  TFile* f0 = TFile::Open( fname1, "READ" );
  TFile* f1 = TFile::Open( fname2, "READ" ); // this is the expected BAND!
  TFile* f2 = TFile::Open( fname3, "READ" ); // this is the observed!
  //TFile* f3 = TFile::Open( fname4, "READ" ); // this is the ISR up
  //TFile* f4 = TFile::Open( fname5, "READ" ); // this is the ISR down
  if (!f0) {
    cout << "*** Error: could not retrieve histogram: " << hname0_exp << " in file: " << f0->GetName() 
	 << " ==> abort macro execution" << endl;
    return;
  }
  if (!f1) {
    cout << "*** Error: could not retrieve histogram: " << hname0 << " in file: " << f1->GetName() 
	 << " ==> abort macro execution" << endl;
    return;
  }
  
  TH2F* hist0; 
  TH2F* hist0_1su; 
  TH2F* hist0_1sd; 
  TH2F* hist1;
  TH2F* hist1_unc;
  TH2F* hist0_all;
  TH2F* hist_isrup;
  TH2F* hist_isrdown;


  if (discexcl==1)
    { 
      hist0     = (TH2F*)f0->Get( hname0_exp );
      hist1     = (TH2F*)f0->Get( hname0 );
      hist1_unc = (TH2F*)f2->Get( hname0 );
      hist0_all = (TH2F*)f1->Get( hname0 );
//       hist_isrup = (TH2F*)f3->Get( hname0 );
//       hist_isrdown = (TH2F*)f4->Get( hname0 );
      hist0_1su = (TH2F*)f0->Get( hname0_1su );
      hist0_1sd = (TH2F*)f0->Get( hname0_1sd );
      cout << hist0 << endl;
      cout << hist1 << endl;
      cout << hist1_unc << endl;
      cout << hist0_all << endl;
      cout << hist0_1su << endl;
      cout << hist0_1sd << endl;

    }

  if (discexcl==0) 
    {
      hist0 = (TH2F*)f0->Get( hname1_exp );
      hist1 = (TH2F*)f0->Get( hname1 );
    }

  hist0->SetDirectory(0);
  hist1->SetDirectory(0);
  hist1_unc->SetDirectory(0);
  hist0_all->SetDirectory(0);
//   hist_isrup->SetDirectory(0);
//   hist_isrdown->SetDirectory(0);

  if (discexcl == 1) {
    hist0_1su->SetDirectory(0);
    hist0_1sd->SetDirectory(0);
  }

  f0->Close();
  f1->Close();
  f2->Close();
//   f3->Close();
//   f4->Close();
  
  TH2F* contour          = FixAndSetBorders( *hist0,         "contour",             "contour",          0 );
  TH2F* contour_obs_unc  = FixAndSetBorders( *hist1_unc,     "contour_obs_unc",     "contour_obs_unc",  0 );
  TH2F* contour_exp_all  = FixAndSetBorders( *hist0_all,     "contour_exp_unc",     "contour_exp_unc",  0 );
//   TH2F* contour_isr_up  = FixAndSetBorders( *hist_isrup,     "contour_isr_up",     "contour_isr_up",  0 );
//   TH2F* contour_isr_down  = FixAndSetBorders( *hist_isrdown,     "contour_isr_down",     "contour_isr_down",  0 );
  TH2F* contour_obs      = FixAndSetBorders( *hist1,         "contour_obs",         "contour_obs",      0 );
      
  if (discexcl==1) 
    {
      TH2F* contour_1su  = FixAndSetBorders( *hist0_1su, "contour_1su",     "contour_1su",     0 );
      TH2F* contour_1sd  = FixAndSetBorders( *hist0_1sd, "contour_1sd",     "contour_1sd",     0 );

      TH2F* inverse = FixAndSetBorders( *hist0, "inverse", "inverse contour", 10000 ); // inverse contour
    }


  TGraph* gr_contour_1su;
  TGraph* gr_contour_1sd;
  TGraph* gr_contour_obs_unc;
  TGraph* gr_contour;
  TGraph* gr_contour_exp_all;
  TGraph* gr_contour_obs;

  
  if (fname1.Contains("GMSB"))
    {
      gr_contour_1su   = (TGraph*) ContourGraph( hist0_1su )->Clone();
      gr_contour_1sd   = (TGraph*) ContourGraph( hist0_1sd )->Clone();
      gr_contour_obs_unc   = (TGraph*) ContourGraph( hist1_unc )->Clone();
      gr_contour           = (TGraph*) ContourGraph( hist0 )->Clone();
      gr_contour_exp_all   = (TGraph*) ContourGraph( hist0_all )->Clone();
      gr_contour_obs       = (TGraph*) ContourGraph( hist1 )->Clone();
    }
  else if (fname1.Contains("gridX"))
    {
      double xmin=550;
      gr_contour_1su   = (TGraph*) ContourGraph( hist0_1su ,xmin,1200)->Clone();
      gr_contour_1sd   = (TGraph*) ContourGraph( hist0_1sd ,xmin,1200)->Clone();
      gr_contour_obs_unc   = (TGraph*) ContourGraph( hist1_unc ,xmin,1200)->Clone();
      gr_contour           = (TGraph*) ContourGraph( hist0 ,xmin,1200)->Clone();
      gr_contour_exp_all   = (TGraph*) ContourGraph( hist0_all ,xmin,1200)->Clone();
      gr_contour_obs       = (TGraph*) ContourGraph( hist1 ,xmin,1200)->Clone();
    }
  else if (fname1.Contains("x12"))
    {
      double xmin=300;
      gr_contour_1su   = (TGraph*) ContourGraph( hist0_1su ,xmin,1200)->Clone();
      gr_contour_1sd   = (TGraph*) ContourGraph( hist0_1sd ,xmin,1200)->Clone();
      gr_contour_obs_unc   = (TGraph*) ContourGraph( hist1_unc ,xmin,1200)->Clone();
      gr_contour           = (TGraph*) ContourGraph( hist0 ,xmin,1200)->Clone();
      gr_contour_exp_all   = (TGraph*) ContourGraph( hist0_all ,xmin,1200)->Clone();
      gr_contour_obs       = (TGraph*) ContourGraph( hist1 ,xmin,1200)->Clone();
    }
  else 
    {
      double xmin=300;
      gr_contour_1su   = (TGraph*) ContourGraph( hist0_1su ,xmin,1200)->Clone();
      gr_contour_1sd   = (TGraph*) ContourGraph( hist0_1sd ,xmin,1200)->Clone();
      gr_contour_obs_unc   = (TGraph*) ContourGraph( hist1_unc ,xmin,1200)->Clone();
      gr_contour           = (TGraph*) ContourGraph( hist0 ,xmin,1200)->Clone();
      gr_contour_exp_all   = (TGraph*) ContourGraph( hist0_all ,xmin,1200)->Clone();
      gr_contour_obs       = (TGraph*) ContourGraph( hist1 ,xmin,1200)->Clone();
    }
//   TGraph* gr_contour_isr_up       = ContourGraph( hist_isrup )->Clone();
//   TGraph* gr_contour_isr_down       = ContourGraph( hist_isrdown )->Clone();

  cout << gr_contour_1su->GetName() << " : "<< gr_contour_1su->GetN() <<  " : " << gr_contour_1sd->GetName() << " : " << gr_contour_1sd->GetN() << endl;
  
  if (contour==0) { 



    cout << "contour is zero" << endl;
    return;
  }
 
  gStyle->SetPaintTextFormat(".2g");
  Float_t nsigmax = hist0->GetMaximum();
  
  // --- draw
  
  // create canvas
  TCanvas* c = new TCanvas( "c", "A scan of m_{0} versus m_{12}", 0, 0, 650,640);
  // create and draw the frame
  TH2F *frame ;
  frame = new TH2F("frame", "m_{0} vs m_{12} - ATLAS", 19, 480,1220, 24, 0., 600/*1200.*/ );
  // set common frame style
  CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
  
  CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
  gPad->SetTopMargin( 0.07  );
  gPad->SetBottomMargin( 0.120  );
  gPad->SetRightMargin( 0.05 );
  gPad->SetLeftMargin( 0.14  );
  gPad->SetLogz();

  //Palette
  
  const Int_t NRGBs = 2;
  const Int_t NCont = 20;
  
  Double_t stops[NRGBs] = { 0.00, 1.0 };
  
  Double_t red   [NRGBs] = { 1.0, 0.10 };
  Double_t green [NRGBs] = { 1.00, 0.10 };
  Double_t blue  [NRGBs] = { 1.00, 0.10 };
  
  TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);


//  const Int_t Number = 3;
//  
//  Double_t Red[Number]    = { 0.50, 1.00, 0.00};
//  Double_t Green[Number]  = { 0.00, 1.00, 0.80};
//  Double_t Blue[Number]   = { 0.00, 0.00, 1.00};
//  Double_t Length[Number] = { 0.00, 0.50, 1.00 };
//  Int_t nb=50;
//  TColor::CreateGradientColorTable(Number,Length,Red,Green,Blue,nb);
  //*************
  if (fname1.Contains("GMSB"))
    {
      frame->SetXTitle("\\Lambda [TeV]");
      frame->SetYTitle("tan\\beta");
    }
  else if (fname1.Contains("gridX"))
    {
      frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
      frame->SetYTitle( "X = ( m_{#tilde{#chi}^{#pm}_{1}} - m_{#tilde{#chi}^{0}_{1}} ) / ( m_{#tilde{g}} - m_{#tilde{#chi}^{0}_{1}} ) " );
    }
  else if (fname1.Contains("SS"))
    {
      frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
      frame->SetYTitle( "m_{#tilde{#chi}^{0}_{1}} [GeV]" );
    }
  else
        {
      frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
      frame->SetYTitle( "m_{#tilde{#chi}^{0}_{1}} [GeV]" );
    }


  frame->SetZTitle( "X-Section" );
  frame->GetXaxis()->SetTitleOffset(1.15);
  frame->GetYaxis()->SetTitleOffset(1.7);
  frame->GetZaxis()->SetTitleOffset(2.5);

  frame->GetXaxis()->SetTitleFont( 42 );
  frame->GetYaxis()->SetTitleFont( 42 );
  frame->GetXaxis()->SetLabelFont( 42 );
  frame->GetYaxis()->SetLabelFont( 42 );

  frame->GetXaxis()->SetTitleSize( 0.04 );
  frame->GetYaxis()->SetTitleSize( 0.04 );
  frame->GetXaxis()->SetLabelSize( 0.035 );
  frame->GetYaxis()->SetLabelSize( 0.035 );
  frame->GetZaxis()->SetLabelSize( 0.015 );

  frame->Draw();

  TPolyLine *pline1;
  TPolyLine *pline2;
  TPolyLine *pline3;
  if (fname1.Contains("GMSB"))
    {

  double lambda[50] = {25.,26.,27.,28.,29.,30.,31,32.,33.,34,35.,36.,37,38.,39.,40,41,42.,43.,44.,45.,46.,47,48,49,50,51,52,53,54.,10.,10.};
  double tanbeta[50] = {7.69772,10.0959,12.4008,14.6153,16.7424,18.7849,20.7459,22.6282,24.4347,26.1683,27.832,29.4286,30.9611,32.4324,33.8455,35.2031,36.5083,37.7639,38.9729,40.1381,41.2626,42.3491,43.4007,44.4202,45.4106,46.3747,47.3155,48.2359,49.1388,50.0,50,7.69772};

  // Selectron limit
  double lambda1[13] = {30.,30.,30.,30.,29.8,27.98,25.45,24,30.};
  double tanbeta1[13] = {2.,3.,4.,5.,10.18,9.78,9.19,2,2};

  // Theory Excluded
  double lambda2[50] = {10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,41.,42,43,44,10,10.};
  double tanbeta2[50] = {20.9672,21.5845, 22.1717,22.7429,23.3104,23.8849,24.4754,25.0893,25.7325,26.4096,27.124,27.8778,28.6719,29.5064,30.3803,31.292,32.2388,33.2178,34.2252,35.2568,36.3081,37.3744,38.4505,39.5314,40.6119,41.6871,42.7519,43.8019,44.8327,45.8404,46.8219,47.7744,48.6959,49.5854,50.,50.,20.4672};

  // GMSB limit
  double lambda3[4] = {10.,26.,26.,10.};
  double tanbeta3[4] = {2.,2.,40.,40.};

  // shadowed region
  double lambda8[50] = {10,11,12,13,14,15,16,17,18,19,20,21,22,23,23.71,22,20.52,10,10};
  double tanbeta8[50] = {21.3907,20.9318,20.2113,19.2912,18.2233,17.0496,15.8021,14.5028,13.1636,11.7866,10.364,8.87766,7.29981,5.59256,4.17,3.21,2,2,21.3907};

  TPolyLine *pline = new TPolyLine(32,lambda,tanbeta);
  pline1 = new TPolyLine(9,lambda1,tanbeta1);
  pline2 = new TPolyLine(36,lambda2,tanbeta2);
  pline3 = new TPolyLine(4,lambda3,tanbeta3);
  TPolyLine *pline8 = new TPolyLine(19,lambda8,tanbeta8);
  TPolyLine *pline9 = new TPolyLine(19,lambda8,tanbeta8);

  pline1->SetFillColor(kCyan-7);
  pline1->SetLineColor(kCyan-7);
  pline1->SetFillStyle(1001);
  pline1->SetLineWidth(2);
  pline1->Draw("f");

  pline->SetLineColor(26);
  pline->SetFillColor(26);
  pline->SetLineWidth(2);
  pline->SetFillStyle(1001);
  pline->Draw("F");

  pline3->SetFillColor(kOrange-3);
  pline3->SetLineColor(kOrange-3);
  pline3->SetLineWidth(2);
  pline3->SetFillStyle(1001);
  pline3->Draw("f");

  pline2->SetFillColor(12);
  pline2->SetLineColor(12);
  pline2->SetLineWidth(2);
  pline2->SetFillStyle(1001);
  pline2->Draw("f");

  pline8->SetFillColor(17);
  //pline8->SetFillStyle(3001);
  //pline8->SetLineColor(11);
  pline8->SetLineWidth(2);

  //  pline8->Draw("F");

  pline9->SetFillStyle(3004);
  pline9->SetFillColor(19);
  //  pline9->Draw("F");

  // Dm10 lines
  //PlotFunc4Par(2.26016,0.309971,-0.00147257,-3.45103e-07,0,21.2,70);
  PlotFunc4Par(2.26016,0.309971,-0.00147257,-3.45103e-07,0,21.2,90);

  //Transition regions
  //PlotFunc4Par(-2.26016,0.309971,-0.00147257,-3.45103e-07,0,23.4,70);
  PlotFunc4Par(-2.26016,0.309971,-0.00147257,-3.45103e-07,0,23.4,90);
  PlotFunc4Par(-30.4,1.65088,0.049198,-0.00350292,4.61376e-05,20,23.8);
  PlotFunc4Par(-9.15791,8.52723,-0.80006,0.0294394,-0.000415712,10.7,23.75);
    }

	const int nsig(3);
  //TH2F *chist[3];
  // draw contours
  //!instead of printing sigma in 68% 95% 98% levels now printing +1 sigma deviations 
  //for (Int_t nsigma=1; nsigma<=nsig; nsigma++)
  //  DrawContourSameColor( contour, nsigma, "blue", kFALSE, (nsigma==1?inverse:0) ) ;

  double  legy=0.66;
  if (taulimits) legy=0.63;

  TString basecolor="yellow";
  Int_t nsigma=2;
  //TLegend *leg = new TLegend(0.58,0.80,0.90,0.92);
  TLegend *leg = new TLegend(0.18,legy+0.06,0.50,0.60); 
  leg->SetTextSize( CombinationGlob::DescriptionTextSize ); 
  leg->SetTextSize( 0.03 );
  leg->SetTextFont( 42 );
  
   if (discexcl==0) {  
    DrawContourSameColorDisc( leg, contour, 2, "pink", kFALSE, 0, kFALSE ) ;
    for (Double_t dnsigma=1.0; dnsigma<=10.0; dnsigma+=1.0) {
      if (dnsigma!=2.0){
	bool lineonly = ( dnsigma==3 ? false : true );
        DrawContourSameColorDisc( leg, contour, dnsigma, "blue", lineonly, 0, lineonly ) ;
      }
    }

  }
 
  Double_t xmax = frame->GetXaxis()->GetXmax();
  Double_t xmin = frame->GetXaxis()->GetXmin();
  Double_t ymax = frame->GetYaxis()->GetXmax();
  Double_t ymin = frame->GetYaxis()->GetXmin();
  Double_t dx   = xmax - xmin;
  Double_t dy   = ymax - ymin;
  

 double xminLine =  xmin;
 double xmaxLine = xmax; // ymax + 2*175;
 double yminLine = xmin - 2*175;
 double ymaxLine = xmax - 2*175; //ymax; 
 
  
 
  //TLine lineExcl = TLine(475,125,975,625);
  TLine lineExcl = TLine(xminLine,yminLine,xmaxLine,ymaxLine);
  lineExcl.SetLineStyle(3);
  lineExcl.SetLineWidth(1);
  lineExcl.SetLineColor(14);
  if (!fname1.Contains("gridX"))
  lineExcl.Draw("same");

  TLatex gtt = TLatex(565,230,"#tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1} forbidden");
  gtt.SetTextSize(0.025);
  gtt.SetTextColor(14);
  gtt.SetTextAngle(51.5);
  gtt.SetTextFont(42);
  //l.SetTextFont(42)
  if (!fname1.Contains("GMSB") && !fname1.Contains("gridX") )
  gtt.Draw("same");
 
  Int_t c_myYellow   = TColor::GetColor("#ffe938"); // TColor::GetColor( "#fee000" )
  Int_t c_myRed      = TColor::GetColor("#aa000");
  Int_t c_myExp      = TColor::GetColor("#28373c");

  //  TGraph* grshadeExp = DrawExpectedBand( gr_contour_1su,      gr_contour_1sd,   TColor::GetColor("#868686") ,   3244, 400)->Clone(); // 3354
  if (fname1.Contains("GMSB"))
    TGraph* grshadeExp = DrawExpectedBand2( gr_contour_1su,      gr_contour_1sd,   c_myYellow , 1001   , 0)->Clone();
   else  if (fname1.Contains("gridX"))
     //     cout << endl;
     TGraph* grshadeExp = DrawExpectedBand( gr_contour_1su,      gr_contour_1sd,   c_myYellow , 1001   , 0)->Clone();
  else
    TGraph* grshadeExp = DrawExpectedBand( gr_contour_1su,      gr_contour_1sd,   c_myYellow , 1001   , 400)->Clone();

// --->
  if (contour!=0 && discexcl==1)
    {

      DrawContourLine95( leg, contour_obs,     "Observed limit (#pm1 #sigma^{SUSY}_{theory})", c_myRed, 1, 4 );   // 95% CL_{S}
      DrawContourLine95( leg, contour_exp_all, "", c_myRed, 3, 2 );    // Observed limit #pm 1 #sigma^{SUSY}_{theory}
      DrawContourLine95( leg, contour,         "", c_myExp, 6, 2 ); 
      DrawContourLine95( leg, contour_obs_unc, "", c_myRed, 3, 2 );      
      DummyLegendExpected(leg, "Expected limit (#pm1 #sigma_{exp})", c_myYellow, 1001, c_myExp, 6, 2);
    }


  //  SSDileptonGtt(leg);
  //  LeptonBjet(leg);
//// <------

  if (discexcl==1) {
    //DrawContourSameColor( leg, contour, 1, "yellow", kFALSE, (nsigma==2?inverse:0) ) ;
    //DrawContourSameColor( leg, contour, 2, "yellow", kFALSE, (nsigma==2?inverse:0), kTRUE ) ;
    //DrawContourSameColor( leg, contour, 3, "yellow", kFALSE, (nsigma==2?inverse:0) ) ;
  }
  
 
  // legend
  Float_t textSizeOffset = +0.000;  
  TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025, "#tilde{g}-#tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}" );
  Leg0->SetTextAlign( 11 );
  Leg0->SetTextFont( 42 );
  Leg0->SetTextSize( CombinationGlob::DescriptionTextSize);
  Leg0->SetTextColor( 1 );
  Leg0->AppendPad();


  

  prefix="Test SR";
  

  TLatex *Leg1 = new TLatex();
  Leg1->SetNDC();
  Leg1->SetTextFont( 42 );
  Leg1->SetTextSize( 0.032 );//025 );
  Leg1->SetTextColor( ROOT::kBlack );
  if (fname1.Contains("GMSB"))
    {
      if (taulimits)
	Leg1->DrawLatex(0.61, 0.55, "#int L dt = 4.7 fb^{-1}, #sqrt{s}=7 TeV");
      else
	Leg1->DrawLatex(0.61, 0.60, "#int L dt = 5.8 fb^{-1}, #sqrt{s}=8 TeV");
    }
  else
    Leg1->DrawLatex(0.19, 0.79, "#int L dt = 5.8 fb^{-1}, #sqrt{s}=8 TeV");
	
  if (fname1.Contains("GMSB"))
    {
      if (taulimits)
	Leg1->DrawLatex(0.61, 0.50, "#geq 2 leptons + jets + E^{miss}_{T}");

	Leg1->DrawLatex(0.61, 0.55, "#geq 2 leptons + jets + E^{miss}_{T}");
    }
  else if (fname1.Contains("gridX"))
    Leg1->DrawLatex(0.19, 0.74, "1 lepton Combination");
  else 
    Leg1->DrawLatex(0.19, 0.74, "0-lepton SRE, 5 meff bins");
  Leg1->AppendPad();

  if (gluinomasses)
    {

 TLine *line = new TLine(63.5, 2,63.5, 25.0);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(63.5, 38,63.5, 50);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(53.8, 2,53.8, 25);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(53.8, 40,53.8, 50);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(44.0, 2,44.0, 50);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(34.4, 2, 34.4, 41);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(25.0, 2, 25.0, 31.5);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();
 line = new TLine(15.9, 2, 15.9, 24);
 line->SetLineColor(kGray+2);
 line->SetLineStyle(7);
 line->Draw();

 // DrawCaptions(73.9,45,"#tilde{g} (1600 GeV)");
 DrawCaptions(64.5,38,"#tilde{g} (1400 GeV)");
 DrawCaptions(54.8,38,"#tilde{g} (1200 GeV)");
 DrawCaptions(45.3,38,"#tilde{g} (1000 GeV)");
 DrawCaptions(35.4,38,"#tilde{g} (800 GeV)");
 DrawCaptions(26.3,27,"#tilde{g} (600 GeV)");
 DrawCaptions(16.9,20,"#tilde{g} (400 GeV)");
    }


  //// draw number of signal events
  //if (nsigmax>0 && showsig) {  hist1->Draw("textsame"); }
  if (nsigmax>0 && showsig) {  

    TTree* ultree = harvesttree(ullistfile);
    
    if (!ultree)
      {
	cerr << "INPUT UPPERLIMIT LIST FILE BROKEN" << endl;
	exit(1);
      }

    int nentries = ultree->GetEntries();
    cout << "Have found ul harvest tree with " << nentries << " entries " << endl;

    Float_t excludedXsec=0;
    Float_t m0=0;
    Float_t m12=0;
    TBranch *b_excludedXsec;
    TBranch *b_m0;
    TBranch *b_m12;
    ultree->SetBranchAddress("excludedXsec",&excludedXsec,&b_excludedXsec);
    ultree->SetBranchAddress("m0",&m0,&b_m0);
    ultree->SetBranchAddress("m12",&m12,&b_m12);
    
    for (int i=0; i<nentries; i++)
      {
	
	ultree->GetEntry(i);
	//cout << "point " << i << " with m0 " << m0 << " and m12 " << m12 << " has excludedXsec " << excludedXsec << endl;
	TLatex point;
	point.SetTextSize(0.02);
	point.SetTextFont(42);
	point.SetTextColor(14);
	char excludedXsec_text[10];
	if(excludedXsec>=0.1) sprintf(excludedXsec_text,"%1.0f", excludedXsec*1000); // %1.0f"
	else if(excludedXsec>=0.01) sprintf(excludedXsec_text,"%1.1f", excludedXsec*1000); // %1.0f"
	else sprintf(excludedXsec_text,"%1.2f", excludedXsec*1000); // %1.0f"
	//sprintf(excludedXsec_text,"%1.2f", excludedXsec); 
	if (m0 > frame->GetXaxis()->GetXmin() && m12 > frame->GetYaxis()->GetXmin() && m0 < frame->GetXaxis()->GetXmax() && m12<frame->GetYaxis()->GetXmax())
	  point.DrawLatex(m0,m12,excludedXsec_text);
      }

    
//  histoxSec->SetMinimum(0.05);
//  histoxSec->SetMaximum(1.0);
//
//  histoxSec->Draw("textcolzsame");
//
//     histoxSec->GetZaxis()->SetLabelFont( 42 );
//   histoxSec->GetZaxis()->SetLabelSize( 0.025 );
//   histoxSec->GetZaxis()->SetTitleFont( 42 );
//   histoxSec->GetZaxis()->SetTitleSize( 0.035 );
//   histoxSec->GetZaxis()->SetTitle("Cross section excluded at 95% C.L. [pb]");
//   histoxSec->SetMarkerColor(14);
    gStyle->SetPaintTextFormat("1.2f");
//     if (fname1.Contains("GMSB"))
//       {
//     histoxSec->Rebin2D(4,5);
//     histoxSec->Scale(1./(4*5));

//     for (int i=0; i<histoxSec->GetNbinsX()+1; i++)
//       for (int j=0; j<histoxSec->GetNbinsY()+1; j++)
// 	{
// 	  if (histoxSec->GetBinContent(i,j)>0)
// 	    //if (histoxSec->GetXaxis()->GetBinLowEdge(i)<histoxSec->GetYaxis()->GetBinUpEdge(j))
// 	    if (histoxSec->GetXaxis()->GetBinCenter(i)<histoxSec->GetYaxis()->GetBinCenter(j)+0.2*histoxSec->GetYaxis()->GetBinWidth(j))
// 	      {
// 		cout << "Bin "<<i<<","<<j<<" with xlowedge "<< histoxSec->GetXaxis()->GetBinCenter(i) << " and yhighedge "<< histoxSec->GetYaxis()->GetBinCenter(j)<<  " has content " << histoxSec->GetBinContent(i,j) << endl;
// 		histoxSec->SetBinContent(i+1,j,(histoxSec->GetBinContent(i,j)+histoxSec->GetBinContent(i+1,j))/2);
// 		histoxSec->SetBinContent(i,j,0);
// 	      }
// 	}
//       }
//     else
//       {
// 	histoxSec->Rebin2D(4,5);
// 	histoxSec->Scale(1./(4*5));
//       }
//     histoxSec->SetMarkerSize(1.5);
//     histoxSec->GetXaxis()->SetRangeUser(frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
//     histoxSec->GetYaxis()->SetRangeUser(frame->GetYaxis()->GetXmin(),frame->GetYaxis()->GetXmax());
//     histoxSec->Draw("textsame"); 

    //    char axistitlecontent[300];

	
	/*
    TLatex axistitle;
    //    sprintf(axistitlecontent,"Numbers give 95% CL_{s} excluded model cross sections [pb]");
    axistitle.SetTextSize(0.03);
    axistitle.SetTextAngle(90);
    axistitle.SetTextFont(42);
    axistitle.SetNDC();
    axistitle.DrawLatex(0.99,0.18,"Numbers give 95% CL_{s} excluded model cross sections [fb]");
*/

	
}
  //else {
  //  // draw grid for clarity
  //  c->SetGrid();
  //}
  //reddraw cahnnel label
  //if (prefix!=0) { Leg2->AppendPad(); }

  // redraw axes
  
if(showsig){
	TLatex axistitle;
    //    sprintf(axistitlecontent,"Numbers give 95% CL_{s} excluded model cross sections [pb]");
    axistitle.SetTextSize(0.03);
    axistitle.SetTextAngle(90);
    axistitle.SetTextFont(42);
    axistitle.SetNDC();
    axistitle.DrawLatex(0.99,0.18,"Numbers give 95% CL_{s} excluded model cross sections [fb]");
}	
  frame->Draw( "sameaxis" );
 
  

  //pave1->Draw("same");
  leg->Draw("same");

  if (fname1.Contains("GMSB"))
  {


  char neu0[30];
  char stau[30];
  char slep[30];
  char theory[30];
  char nl[30];
  sprintf(neu0, "\\tilde\\chi^{0}_{1}");
  sprintf(stau, "\\tilde\\tau_{1}");
  sprintf(slep, "\\tilde l_{R}");
  sprintf(theory, "Theory excl.");

  sprintf(nl, "CoNLSP");


  TLatex texNeu0;
  texNeu0.SetNDC();
  texNeu0.SetTextFont(42);
  texNeu0.SetTextSize(0.04);
  texNeu0.SetTextColor(14);

  TLatex texstau;
  texstau.SetNDC();
  texstau.SetTextFont(42);
  texstau.SetTextSize(0.04);
  texstau.SetTextColor(14);

  TLatex texslep;
  texslep.SetNDC();
  texslep.SetTextFont(42);
  texslep.SetTextSize(0.04);
  texslep.SetTextColor(14);

  TLatex texnl;
  texnl.SetNDC();
  texnl.SetTextFont(42);
  texnl.SetTextSize(0.04);
  texnl.SetTextColor(14);

  TLatex textheor;
  textheor.SetNDC();
  textheor.SetTextFont(42);
  textheor.SetTextSize(0.05);
  textheor.SetTextColor(kWhite);  

  texNeu0.DrawLatex(0.13,0.30,neu0);
  texstau.DrawLatex(0.7,0.45,stau);
  texslep.DrawLatex(0.7,0.17,slep);

  texnl.DrawLatex(0.7,0.32,nl);

  leg->AddEntry(pline,"LEP (\\tilde\\tau_{1})","F");
  leg->AddEntry(pline1,"LEP (\\tildee_{R})","F");
  leg->AddEntry(pline3,"OPAL","F");


  TH2F* oldlimit = Draw1fbLimit();
  TCanvas* c2 = new TCanvas( "c2", "A scan of m_{0} versus m_{12}", 0, 0, 
			    CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[1] );  
  c2->cd();
  oldlimit->Draw("cont list");

  gPad->Update();
  TObjArray *contours = gROOT->GetListOfSpecials()->FindObject("contours");
  TList *list         = (TList*)contours->At(0);
  TGraph *gr2 = (TGraph*)list->First();
  oldlimit->SetLineColor(kGreen+2);
  oldlimit->SetFillColor(kGreen+2);
  gr2->SetFillColor(oldlimit->GetFillColor());
  gr2->SetLineColor(oldlimit->GetLineColor());
  gr2->SetFillStyle(3744);
  c2->Close();
  c->cd();

  oldlimit->Draw("same cont3");
  TH2F* onetaulimit = Draw1TauLimit();
  onetaulimit->SetLineColor(4);
  onetaulimit->SetLineWidth(gr2->GetLineWidth());

  TGraph* twotaulimit = Draw2TauLimit();
  twotaulimit->SetLineWidth(gr2->GetLineWidth());
  twotaulimit->SetFillStyle(0);
  twotaulimit->SetLineColor(2);
  if (taulimits)
    {
      onetaulimit->Draw("same cont3");
      twotaulimit->Draw("sameL");
    }
  else
    gr2->Draw("SAMEF");

  pline2->Draw("f");

  //leg->AddEntry(gr2,"ATLAS 2 leptons (1fb^{-1})","F");
  leg->AddEntry(gr2,"ATLAS 2 leptons (1fb^{-1})","L");
  if (taulimits)
    {
      leg->AddEntry(onetaulimit,"ATLAS #geq 1 tau (2fb^{-1})","L");
      leg->AddEntry(twotaulimit,"ATLAS #geq 2 taus (2fb^{-1})","L");
    }
  //leg->Draw("same");
  // update the canvas
  textheor.DrawLatex(0.14,0.78,theory);
  c->Update();
}

  
  	
  TLatex clslimits = TLatex(/*755,503,au fost 533,475*/1000,560,"All limits at 95% CL_{S}");
  clslimits.SetTextSize(0.025);
  gtt.SetTextColor( TColor::GetColor("#8f9497") );
  clslimits.SetTextFont(42);
  clslimits.Draw("same");
  
  // observed limit -> arrange the lines in a stupid way
/*565 in loc de 578 si 591 -> 604*/
  TLine obsPOneSigma = TLine(528,430,579,430); //used to be 633/655
  obsPOneSigma.SetLineStyle(3);
  obsPOneSigma.SetLineWidth(2);
  obsPOneSigma.SetLineColor(c_myRed);
  obsPOneSigma.Draw("same");

  TLine obsMOneSigma = TLine(528,415,579,415);
  obsMOneSigma.SetLineStyle(3);
  obsMOneSigma.SetLineWidth(2);
  obsMOneSigma.SetLineColor(c_myRed);
  obsMOneSigma.Draw("same");

  

  TLatex* atlasLabel = new TLatex();
  atlasLabel->SetNDC();
  atlasLabel->SetTextFont(72);
  atlasLabel->SetTextColor(ROOT::kBlack);
  atlasLabel->SetTextSize( 0.05 );
  if (fname1.Contains("GMSB"))
    {
      atlasLabel->SetTextColor(kWhite);
    }

  atlasLabel->DrawLatex(0.19, 0.85,"ATLAS");
  atlasLabel->AppendPad();

  TLatex* progressLabel = new TLatex();
  progressLabel->SetNDC();
  progressLabel->SetTextFont(42);
  progressLabel->SetTextColor(ROOT::kBlack);
  progressLabel->SetTextSize( 0.05 );
  if (fname1.Contains("GMSB"))
    {
      progressLabel->SetTextColor(kWhite);
    }
  progressLabel->DrawLatex(0.35, 0.85,"Internal");
  progressLabel->AppendPad();

  
  // update the canvas
  c->Update();



  // create plots
  // store histograms to output file
  TObjArray* arr = fname1.Tokenize("/");
  TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
  TString outfile = objstring->GetString().ReplaceAll(".root","");
  delete arr;

  TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%dinvpb_",lumi);
  CombinationGlob::imgconv( c, Form("plots/m0m12_alaCMS%s",outfile.Data()) );   


  //  delete leg;
  //  delete contour;
  //delete hist4;
  //  delete inverse;
  //  delete frame;
}


void
DummyLegendExpectedDummyLegendExpected(TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth)
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


TGraph*
ContourGraph( TH2F* hist,double xmin=16, double xmax=90)
{

  TGraph* gr0 = new TGraph();
  TH2F* h = (TH2F*)hist->Clone();
  gr = (TGraph*)gr0->Clone(h->GetName());
  cout << "==> Will dumb histogram: " << h->GetName() << " into a graph" <<endl;
  h->SetContour( 1 );
  //h->GetXaxis()->SetRangeUser(250,1200);
  h->GetXaxis()->SetRangeUser(xmin,xmax);
  //h->GetYaxis()->SetRangeUser(2,50);
  double pval = CombinationGlob::cl_percent[1];
  double signif = TMath::NormQuantile(1-pval);
  h->SetContourLevel( 0, signif );
  h->Draw("CONT LIST");
  h->SetDirectory(0);
  gPad->Update();
  TObjArray *contours = gROOT->GetListOfSpecials()->FindObject("contours");
  Int_t ncontours     = contours->GetSize();
  //cout << "Found " << ncontours << " contours " << endl;
  TList *list = (TList*)contours->At(0);
  gr = (TGraph*)list->First();
  gr->SetName(hist->GetName());
  int N = gr->GetN();
  double x0, y0;
  for(int j=0; j<N; j++) {
    gr->GetPoint(j,x0,y0);
    cout << j << " : " << x0 << " : "<<y0 << endl;
  }
//  //  gr->SetMarkerSize(2.0);    
  //gr->Draw("ALP");
 

  cout << "Generated graph " << gr << " with name " << gr->GetName() << endl;
  return gr;
}


TGraph*
DrawExpectedBand( TGraph* gr1,  TGraph* gr2, Int_t fillColor, Int_t fillStyle, Int_t cut = 0)
{
  //  TGraph* gr1 = new TGraph( *graph1 );
  //  TGraph* gr2 = new TGraph( *graph2 );

  int number_of_bins = max(gr1->GetN(),gr2->GetN());
  cout << "Drawing expected band for bins: " << number_of_bins << endl;
  
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
      {
	//cout << "Using x1: " << x1[i] << "," << y1[i] << endl;
	grshade->SetPoint(i,x1[i],y1[i]);
      }
    if (x2[N-i-1] > cut)
      {
	//cout << "Using x2: " << x2[N-i-1] << "," << y2[N-i-1] << endl;
	grshade->SetPoint(N+i,x2[N-i-1],y2[N-i-1]);
      }
  }

  // Apply the cut in the shade plot if there is something that doesn't look good...
  int Nshade = grshade->GetN();
  cout << "Drawing shaded with points " << Nshade << endl;
  double x0, y0;
  double x00, y00;

  for(int j=0; j<Nshade; j++) {
    grshade->GetPoint(j,x0,y0);
    cout << "Punkt " << j << ": " << x0 << "," << y0 << endl;
    if ((x0 != 0) && (y0 != 0)) {
      x00 = x0;
      y00 = y0;
      break;
    }
  }

  // for(int j=0; j<Nshade; j++) {
    // grshade->GetPoint(j,x0,y0);
    // if ((x0 == 0) && (y0 == 0)) 
      // {    
	  // grshade->SetPoint(j,x00,y00);

      // }
    
  //}
  
    for(int j=0; j<Nshade; j++) {
    grshade->GetPoint(j,x0,y0);
    if ((x0 >700) && (y0 <15)) 
     {    
	 grshade->SetPoint(j,x0,0);

     }
    
    }
  
  //grshade->GetPoint(0,x0,y0);
 // grshade->SetPoint(0,x0,0);
  //grshade->GetPoint(Nshade-1,x0,y0);
 // grshade->SetPoint(Nshade-1,x0,0);
  for(int j=0; j<Nshade; j++) {
    grshade->GetPoint(j,x0,y0);
    cout << "Punkt " << j << ": " << x0 << "," << y0 << endl;
  }

  // Now draw the plot... 
  grshade->SetFillStyle(fillStyle);
  grshade->SetFillColor(fillColor);
  //  grshade->SetMarkerStyle(21);
  grshade->Draw("SAME F");


  return grshade;
}


TGraph*
DrawExpectedBand2( TGraph* gr1,  TGraph* gr2, Int_t fillColor, Int_t fillStyle, Int_t cut = 0)
{
  //  TGraph* gr1 = new TGraph( *graph1 );
  //  TGraph* gr2 = new TGraph( *graph2 );

  int number_of_bins = max(gr1->GetN(),gr2->GetN());
  cout << "Drawing expected band for bins: " << number_of_bins << endl;
  
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
    cout << "graph2 point " << j << ": " << xx1 << ","<< yy1 << endl;
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
      {
	//cout << "Using x1: " << x1[i] << "," << y1[i] << endl;
	grshade->SetPoint(i,x1[i],y1[i]);
      }
    if (x2[N-i-1] > cut)
      {
	//cout << "Using x2: " << x2[N-i-1] << "," << y2[N-i-1] << endl;
	grshade->SetPoint(N+i,x2[N-i-1],y2[N-i-1]);
      }
  }

  // Apply the cut in the shade plot if there is something that doesn't look good...
  int Nshade = grshade->GetN();
  cout << "Drawing shaded with points " << Nshade << endl;
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
      {    
	if (true)
	  //grshade->SetPoint(j,x00,y00);
	  grshade->SetPoint(j, 58.4949 ,-20000.);
      }
    
  }
  //  grshade->SetPoint(0,16.125 , 44.);


  grshade->SetPoint(148,56.8203,50.2);
  grshade->SetPoint(149,47.5 ,50.);
  grshade->SetPoint(150,42 ,44.);
  grshade->SetPoint(151,40 ,44.3);
  grshade->SetPoint(0,16.125 ,30.);

  for(int j=0; j<Nshade; j++) {
    grshade->GetPoint(j,x0,y0);
    cout << "Punkt " << j << ": " << x0 << "," << y0 << endl;
  }
  // Now draw the plot... 
  grshade->SetFillStyle(fillStyle);
  grshade->SetFillColor(fillColor);
  //  grshade->SetMarkerStyle(21);
  grshade->Draw("SAME F");
  gr2->Draw("SAMEF");
  gr2->SetFillStyle(fillStyle);
  gr2->SetFillColor(fillColor);


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
DrawContourLine99( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2 )
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


void DrawContourMassLineLegends(){
Double_t labelsize=0.025;

  // Gluino masses

// TLatex *gl400 = new TLatex( 1000, 140, "#tilde{g} (400)" );
//   gl400->SetTextAlign( 11 );
//   gl400->SetTextSize(labelsize);
//   gl400->SetTextColor( 12 );
//   gl400->AppendPad();

TLatex *gl600 = new TLatex( 1900, 190, "#tilde{g} (600)" );
  gl600->SetTextAlign( 11 );
  gl600->SetTextSize(labelsize);
  gl600->SetTextColor( 12 );
  gl600->AppendPad();

TLatex *gl800 = new TLatex( 1850, 275, "#tilde{g} (800)" );
  gl800->SetTextAlign( 11 );
  gl800->SetTextSize(labelsize);
  gl800->SetTextColor( 12 );
  gl800->AppendPad();

TLatex *gl1000 = new TLatex( 1180, 378, "#tilde{g} (1000)" );
  gl1000->SetTextAlign( 11 );
  gl1000->SetTextSize(labelsize);
  gl1000->SetTextColor( 12 );
  gl1000->AppendPad();

// TLatex *gl1200 = new TLatex( 1000, 315, "#tilde{g} (1200)" );
//   gl1200->SetTextAlign( 11 );
//   gl1200->SetTextSize(labelsize);
//   gl1200->SetTextColor( 12 );
//   gl1200->AppendPad();

  // Squark masses

// TLatex *sq400 = new TLatex( 240, 142, "#tilde{q} (400)" );
//   sq400->SetTextAngle(-40);
//   sq400->SetTextAlign( 11 );
//   sq400->SetTextSize(labelsize);
//   sq400->SetTextColor( 12 );
//   sq400->AppendPad();

TLatex *sq600 = new TLatex( 180, 270, "#tilde{q} (600)" );
  sq600->SetTextAngle(-45);
  sq600->SetTextAlign( 11 );
  sq600->SetTextSize(labelsize);
  sq600->SetTextColor( 12 );
  sq600->AppendPad();

// TLatex *sq800 = new TLatex( 450, 310, "#tilde{q} (800)" );
//   sq800->SetTextAngle(-40);
//   sq800->SetTextAlign( 11 );
//   sq800->SetTextSize(labelsize);
//   sq800->SetTextColor( 12 );
//   sq800->AppendPad();

TLatex *sq1000 = new TLatex( 570, 400, "#tilde{q} (1000)" );
  sq1000->SetTextAngle(-60);
  sq1000->SetTextAlign( 11 );
  sq1000->SetTextSize(labelsize);
  sq1000->SetTextColor( 12 );
  sq1000->AppendPad();

// TLatex *sq1200 = new TLatex( 450, 310, "#tilde{q} (1200)" );
//   sq1200->SetTextAngle(-40);
//   sq1200->SetTextAlign( 11 );
//   sq1200->SetTextSize(labelsize);
//   sq1200->SetTextColor( 12 );
//   sq1200->AppendPad();

  TLatex *sq1400 = new TLatex( 1050, 480, "#tilde{q} (1400)" );
  sq1400->SetTextAngle(-70);
  sq1400->SetTextAlign( 11 );
  sq1400->SetTextSize(labelsize);
  sq1400->SetTextColor( 12 );
  sq1400->AppendPad();

return;} 
void PlotFunc3Par(double p0, double p1,double p2,double p3,double xmin,double xmax){
  char function1[200];
  sprintf(function1,"%f+%f*x+%f*x*x+%f*x*x*x",p0,p1,p2,p3);
  TF1 *fdmst2 = new TF1("", function1,xmin,xmax);
  fdmst2->SetLineWidth(0.3);
  fdmst2->SetLineStyle(5);
  fdmst2->SetLineColor(17);
  fdmst2->Draw("SAME");
  //delete fdmst2;
}

void PlotFunc4Par(double p0, double p1,double p2,double p3,double p4,double xmin,double xmax){
  char function1[200];
  sprintf(function1,"%f+%f*x+%f*x*x+%f*x*x*x+%f*x*x*x*x",p0,p1,p2,p3,p4);
  TF1 *fdmst2 = new TF1("", function1,xmin,xmax);
  fdmst2->SetLineWidth(0.5);
  //                fdmst2->SetLineStyle(2);
  fdmst2->SetLineColor(14);
  fdmst2->Draw("SAME");
  //delete fdmst2;
}


TH2F* Draw1fbLimit()
{
   TH2F *sigp1cls = new TH2F("sigp1cls","significalce p1 cls",40,10,80,40,2,50);
   sigp1cls->SetBinContent(43,-5.372311);
   sigp1cls->SetBinContent(44,-3.245461);
   sigp1cls->SetBinContent(45,-1.118612);
   sigp1cls->SetBinContent(46,1.008237);
   sigp1cls->SetBinContent(47,3.135087);
   sigp1cls->SetBinContent(48,4.232357);
   sigp1cls->SetBinContent(49,4.612531);
   sigp1cls->SetBinContent(50,4.63679);
   sigp1cls->SetBinContent(51,4.559969);
   sigp1cls->SetBinContent(52,4.483149);
   sigp1cls->SetBinContent(53,4.406329);
   sigp1cls->SetBinContent(54,4.312113);
   sigp1cls->SetBinContent(55,3.942241);
   sigp1cls->SetBinContent(56,3.522852);
   sigp1cls->SetBinContent(57,3.082921);
   sigp1cls->SetBinContent(58,2.567669);
   sigp1cls->SetBinContent(59,2.052418);
   sigp1cls->SetBinContent(60,1.530633);
   sigp1cls->SetBinContent(61,1.023921);
   sigp1cls->SetBinContent(62,0.5162491);
   sigp1cls->SetBinContent(63,0.1129298);
   sigp1cls->SetBinContent(64,-0.186037);
   sigp1cls->SetBinContent(65,-0.4910024);
   sigp1cls->SetBinContent(66,-0.7147657);
   sigp1cls->SetBinContent(67,-0.8811972);
   sigp1cls->SetBinContent(68,-1.047629);
   sigp1cls->SetBinContent(69,-1.21406);
   sigp1cls->SetBinContent(70,-1.381394);
   sigp1cls->SetBinContent(71,-1.560469);
   sigp1cls->SetBinContent(72,-1.663374);
   sigp1cls->SetBinContent(73,-1.76525);
   sigp1cls->SetBinContent(74,-1.868442);
   sigp1cls->SetBinContent(75,-1.971634);
   sigp1cls->SetBinContent(76,-2.074827);
   sigp1cls->SetBinContent(77,-2.165492);
   sigp1cls->SetBinContent(78,-2.211689);
   sigp1cls->SetBinContent(79,-2.276947);
   sigp1cls->SetBinContent(80,-2.342205);
   sigp1cls->SetBinContent(81,-2.407463);
   sigp1cls->SetBinContent(82,-2.472721);
   sigp1cls->SetBinContent(85,-3.443781);
   sigp1cls->SetBinContent(86,-1.316932);
   sigp1cls->SetBinContent(87,0.5723224);
   sigp1cls->SetBinContent(88,1.590395);
   sigp1cls->SetBinContent(89,2.608467);
   sigp1cls->SetBinContent(90,3.626539);
   sigp1cls->SetBinContent(91,4.006713);
   sigp1cls->SetBinContent(92,4.212914);
   sigp1cls->SetBinContent(93,4.419116);
   sigp1cls->SetBinContent(94,4.524238);
   sigp1cls->SetBinContent(95,4.447418);
   sigp1cls->SetBinContent(96,4.353202);
   sigp1cls->SetBinContent(97,4.032847);
   sigp1cls->SetBinContent(98,3.677122);
   sigp1cls->SetBinContent(99,3.237191);
   sigp1cls->SetBinContent(100,2.720585);
   sigp1cls->SetBinContent(101,2.186365);
   sigp1cls->SetBinContent(102,1.663226);
   sigp1cls->SetBinContent(103,1.160032);
   sigp1cls->SetBinContent(104,0.6539593);
   sigp1cls->SetBinContent(105,0.25064);
   sigp1cls->SetBinContent(106,-0.05832466);
   sigp1cls->SetBinContent(107,-0.3852855);
   sigp1cls->SetBinContent(108,-0.6090488);
   sigp1cls->SetBinContent(109,-0.7754802);
   sigp1cls->SetBinContent(110,-0.9464269);
   sigp1cls->SetBinContent(111,-1.125501);
   sigp1cls->SetBinContent(112,-1.304575);
   sigp1cls->SetBinContent(113,-1.483649);
   sigp1cls->SetBinContent(114,-1.586555);
   sigp1cls->SetBinContent(115,-1.683602);
   sigp1cls->SetBinContent(116,-1.780648);
   sigp1cls->SetBinContent(117,-1.880768);
   sigp1cls->SetBinContent(118,-1.98396);
   sigp1cls->SetBinContent(119,-2.074625);
   sigp1cls->SetBinContent(120,-2.119357);
   sigp1cls->SetBinContent(121,-2.164088);
   sigp1cls->SetBinContent(122,-2.208819);
   sigp1cls->SetBinContent(123,-2.269679);
   sigp1cls->SetBinContent(124,-2.334937);
   sigp1cls->SetBinContent(127,-2.06964);
   sigp1cls->SetBinContent(128,-1.051568);
   sigp1cls->SetBinContent(129,-0.03349524);
   sigp1cls->SetBinContent(130,0.9845771);
   sigp1cls->SetBinContent(131,2.002649);
   sigp1cls->SetBinContent(132,3.020722);
   sigp1cls->SetBinContent(133,3.400895);
   sigp1cls->SetBinContent(134,3.607097);
   sigp1cls->SetBinContent(135,3.813298);
   sigp1cls->SetBinContent(136,4.019499);
   sigp1cls->SetBinContent(137,4.225701);
   sigp1cls->SetBinContent(138,4.394291);
   sigp1cls->SetBinContent(139,4.073936);
   sigp1cls->SetBinContent(140,3.753581);
   sigp1cls->SetBinContent(141,3.387397);
   sigp1cls->SetBinContent(142,2.853177);
   sigp1cls->SetBinContent(143,2.318957);
   sigp1cls->SetBinContent(144,1.795818);
   sigp1cls->SetBinContent(145,1.292624);
   sigp1cls->SetBinContent(146,0.7894304);
   sigp1cls->SetBinContent(147,0.3743531);
   sigp1cls->SetBinContent(148,0.04739227);
   sigp1cls->SetBinContent(149,-0.2795686);
   sigp1cls->SetBinContent(150,-0.5114594);
   sigp1cls->SetBinContent(151,-0.6905336);
   sigp1cls->SetBinContent(152,-0.8696077);
   sigp1cls->SetBinContent(153,-1.048682);
   sigp1cls->SetBinContent(154,-1.227756);
   sigp1cls->SetBinContent(155,-1.40683);
   sigp1cls->SetBinContent(156,-1.509736);
   sigp1cls->SetBinContent(157,-1.606783);
   sigp1cls->SetBinContent(158,-1.703829);
   sigp1cls->SetBinContent(159,-1.800876);
   sigp1cls->SetBinContent(160,-1.897923);
   sigp1cls->SetBinContent(161,-1.983759);
   sigp1cls->SetBinContent(162,-2.02849);
   sigp1cls->SetBinContent(163,-2.073221);
   sigp1cls->SetBinContent(164,-2.117953);
   sigp1cls->SetBinContent(165,-2.162684);
   sigp1cls->SetBinContent(166,-2.207416);
   sigp1cls->SetBinContent(169,-1.838297);
   sigp1cls->SetBinContent(170,-0.7300462);
   sigp1cls->SetBinContent(171,0.2880262);
   sigp1cls->SetBinContent(172,1.306098);
   sigp1cls->SetBinContent(173,2.324171);
   sigp1cls->SetBinContent(174,3.133879);
   sigp1cls->SetBinContent(175,3.419343);
   sigp1cls->SetBinContent(176,3.625544);
   sigp1cls->SetBinContent(177,3.831745);
   sigp1cls->SetBinContent(178,4.037946);
   sigp1cls->SetBinContent(179,4.238191);
   sigp1cls->SetBinContent(180,4.394291);
   sigp1cls->SetBinContent(181,4.073936);
   sigp1cls->SetBinContent(182,3.753581);
   sigp1cls->SetBinContent(183,3.321042);
   sigp1cls->SetBinContent(184,2.786822);
   sigp1cls->SetBinContent(185,2.252338);
   sigp1cls->SetBinContent(186,1.75556);
   sigp1cls->SetBinContent(187,1.280258);
   sigp1cls->SetBinContent(188,0.777064);
   sigp1cls->SetBinContent(189,0.3756546);
   sigp1cls->SetBinContent(190,0.05377046);
   sigp1cls->SetBinContent(191,-0.2731904);
   sigp1cls->SetBinContent(192,-0.5050812);
   sigp1cls->SetBinContent(193,-0.6841554);
   sigp1cls->SetBinContent(194,-0.8632296);
   sigp1cls->SetBinContent(195,-1.042304);
   sigp1cls->SetBinContent(196,-1.222879);
   sigp1cls->SetBinContent(197,-1.406955);
   sigp1cls->SetBinContent(198,-1.494491);
   sigp1cls->SetBinContent(199,-1.584037);
   sigp1cls->SetBinContent(200,-1.681084);
   sigp1cls->SetBinContent(201,-1.77813);
   sigp1cls->SetBinContent(202,-1.875177);
   sigp1cls->SetBinContent(203,-1.961013);
   sigp1cls->SetBinContent(204,-2.005744);
   sigp1cls->SetBinContent(205,-2.050476);
   sigp1cls->SetBinContent(206,-2.095207);
   sigp1cls->SetBinContent(207,-2.139939);
   sigp1cls->SetBinContent(208,-2.197422);
   sigp1cls->SetBinContent(211,-1.849745);
   sigp1cls->SetBinContent(212,-0.4085248);
   sigp1cls->SetBinContent(213,0.6095476);
   sigp1cls->SetBinContent(214,1.62762);
   sigp1cls->SetBinContent(215,2.576238);
   sigp1cls->SetBinContent(216,3.152326);
   sigp1cls->SetBinContent(217,3.437789);
   sigp1cls->SetBinContent(218,3.643991);
   sigp1cls->SetBinContent(219,3.850192);
   sigp1cls->SetBinContent(220,4.045441);
   sigp1cls->SetBinContent(221,4.238191);
   sigp1cls->SetBinContent(222,4.394291);
   sigp1cls->SetBinContent(223,4.073936);
   sigp1cls->SetBinContent(224,3.696902);
   sigp1cls->SetBinContent(225,3.254687);
   sigp1cls->SetBinContent(226,2.720467);
   sigp1cls->SetBinContent(227,2.181763);
   sigp1cls->SetBinContent(228,1.684985);
   sigp1cls->SetBinContent(229,1.266679);
   sigp1cls->SetBinContent(230,0.7646974);
   sigp1cls->SetBinContent(231,0.3632881);
   sigp1cls->SetBinContent(232,0.06014866);
   sigp1cls->SetBinContent(233,-0.2668122);
   sigp1cls->SetBinContent(234,-0.498703);
   sigp1cls->SetBinContent(235,-0.6777772);
   sigp1cls->SetBinContent(236,-0.8568513);
   sigp1cls->SetBinContent(237,-1.039284);
   sigp1cls->SetBinContent(238,-1.22336);
   sigp1cls->SetBinContent(239,-1.407437);
   sigp1cls->SetBinContent(240,-1.494973);
   sigp1cls->SetBinContent(241,-1.575083);
   sigp1cls->SetBinContent(242,-1.658338);
   sigp1cls->SetBinContent(243,-1.755384);
   sigp1cls->SetBinContent(244,-1.852431);
   sigp1cls->SetBinContent(245,-1.938267);
   sigp1cls->SetBinContent(246,-1.982999);
   sigp1cls->SetBinContent(247,-2.02773);
   sigp1cls->SetBinContent(248,-2.076015);
   sigp1cls->SetBinContent(249,-2.13538);
   sigp1cls->SetBinContent(250,-2.194745);
   sigp1cls->SetBinContent(253,-1.861192);
   sigp1cls->SetBinContent(254,-0.3575403);
   sigp1cls->SetBinContent(255,0.9310689);
   sigp1cls->SetBinContent(256,1.949141);
   sigp1cls->SetBinContent(257,2.594685);
   sigp1cls->SetBinContent(258,3.170774);
   sigp1cls->SetBinContent(259,3.456236);
   sigp1cls->SetBinContent(260,3.65994);
   sigp1cls->SetBinContent(261,3.85269);
   sigp1cls->SetBinContent(262,4.045441);
   sigp1cls->SetBinContent(263,4.238191);
   sigp1cls->SetBinContent(264,4.394291);
   sigp1cls->SetBinContent(265,4.04767);
   sigp1cls->SetBinContent(266,3.630547);
   sigp1cls->SetBinContent(267,3.188331);
   sigp1cls->SetBinContent(268,2.651562);
   sigp1cls->SetBinContent(269,2.111189);
   sigp1cls->SetBinContent(270,1.61441);
   sigp1cls->SetBinContent(271,1.196104);
   sigp1cls->SetBinContent(272,0.7523309);
   sigp1cls->SetBinContent(273,0.3509215);
   sigp1cls->SetBinContent(274,0.05129677);
   sigp1cls->SetBinContent(275,-0.260434);
   sigp1cls->SetBinContent(276,-0.4923248);
   sigp1cls->SetBinContent(277,-0.6716133);
   sigp1cls->SetBinContent(278,-0.8556896);
   sigp1cls->SetBinContent(279,-1.039766);
   sigp1cls->SetBinContent(280,-1.223842);
   sigp1cls->SetBinContent(281,-1.407919);
   sigp1cls->SetBinContent(282,-1.495455);
   sigp1cls->SetBinContent(283,-1.575564);
   sigp1cls->SetBinContent(284,-1.655674);
   sigp1cls->SetBinContent(285,-1.735784);
   sigp1cls->SetBinContent(286,-1.829685);
   sigp1cls->SetBinContent(287,-1.915522);
   sigp1cls->SetBinContent(288,-1.960253);
   sigp1cls->SetBinContent(289,-2.013973);
   sigp1cls->SetBinContent(290,-2.073339);
   sigp1cls->SetBinContent(291,-2.132704);
   sigp1cls->SetBinContent(292,-2.192069);
   sigp1cls->SetBinContent(295,-1.872639);
   sigp1cls->SetBinContent(296,-0.3689874);
   sigp1cls->SetBinContent(297,1.134664);
   sigp1cls->SetBinContent(298,2.037043);
   sigp1cls->SetBinContent(299,2.613132);
   sigp1cls->SetBinContent(300,3.18922);
   sigp1cls->SetBinContent(301,3.467189);
   sigp1cls->SetBinContent(302,3.65994);
   sigp1cls->SetBinContent(303,3.85269);
   sigp1cls->SetBinContent(304,4.045441);
   sigp1cls->SetBinContent(305,4.238191);
   sigp1cls->SetBinContent(306,4.394291);
   sigp1cls->SetBinContent(307,3.981315);
   sigp1cls->SetBinContent(308,3.564192);
   sigp1cls->SetBinContent(309,3.121361);
   sigp1cls->SetBinContent(310,2.580987);
   sigp1cls->SetBinContent(311,2.040614);
   sigp1cls->SetBinContent(312,1.543836);
   sigp1cls->SetBinContent(313,1.125529);
   sigp1cls->SetBinContent(314,0.7072222);
   sigp1cls->SetBinContent(315,0.338555);
   sigp1cls->SetBinContent(316,0.03893024);
   sigp1cls->SetBinContent(317,-0.2606945);
   sigp1cls->SetBinContent(318,-0.4880189);
   sigp1cls->SetBinContent(319,-0.6720952);
   sigp1cls->SetBinContent(320,-0.8561715);
   sigp1cls->SetBinContent(321,-1.040248);
   sigp1cls->SetBinContent(322,-1.224324);
   sigp1cls->SetBinContent(323,-1.4084);
   sigp1cls->SetBinContent(324,-1.495936);
   sigp1cls->SetBinContent(325,-1.576046);
   sigp1cls->SetBinContent(326,-1.656156);
   sigp1cls->SetBinContent(327,-1.736266);
   sigp1cls->SetBinContent(328,-1.816376);
   sigp1cls->SetBinContent(329,-1.892776);
   sigp1cls->SetBinContent(330,-1.951932);
   sigp1cls->SetBinContent(331,-2.011297);
   sigp1cls->SetBinContent(332,-2.070662);
   sigp1cls->SetBinContent(333,-2.130027);
   sigp1cls->SetBinContent(334,-2.189392);
   sigp1cls->SetBinContent(337,-2.037436);
   sigp1cls->SetBinContent(338,-0.5337849);
   sigp1cls->SetBinContent(339,0.8765826);
   sigp1cls->SetBinContent(340,1.909749);
   sigp1cls->SetBinContent(341,2.485838);
   sigp1cls->SetBinContent(342,3.061927);
   sigp1cls->SetBinContent(343,3.336821);
   sigp1cls->SetBinContent(344,3.529572);
   sigp1cls->SetBinContent(345,3.722322);
   sigp1cls->SetBinContent(346,3.915072);
   sigp1cls->SetBinContent(347,4.087058);
   sigp1cls->SetBinContent(348,4.146263);
   sigp1cls->SetBinContent(349,3.72914);
   sigp1cls->SetBinContent(350,3.312017);
   sigp1cls->SetBinContent(351,2.83916);
   sigp1cls->SetBinContent(352,2.385098);
   sigp1cls->SetBinContent(353,1.844724);
   sigp1cls->SetBinContent(354,1.452455);
   sigp1cls->SetBinContent(355,1.096853);
   sigp1cls->SetBinContent(356,0.6785462);
   sigp1cls->SetBinContent(357,0.3517261);
   sigp1cls->SetBinContent(358,0.05669356);
   sigp1cls->SetBinContent(359,-0.2429312);
   sigp1cls->SetBinContent(360,-0.4682748);
   sigp1cls->SetBinContent(361,-0.6523511);
   sigp1cls->SetBinContent(362,-0.8364275);
   sigp1cls->SetBinContent(363,-1.020504);
   sigp1cls->SetBinContent(364,-1.205247);
   sigp1cls->SetBinContent(365,-1.398661);
   sigp1cls->SetBinContent(366,-1.486864);
   sigp1cls->SetBinContent(367,-1.566973);
   sigp1cls->SetBinContent(368,-1.647083);
   sigp1cls->SetBinContent(369,-1.727193);
   sigp1cls->SetBinContent(370,-1.808596);
   sigp1cls->SetBinContent(371,-1.88456);
   sigp1cls->SetBinContent(372,-1.932901);
   sigp1cls->SetBinContent(373,-1.992266);
   sigp1cls->SetBinContent(374,-2.051631);
   sigp1cls->SetBinContent(375,-2.110996);
   sigp1cls->SetBinContent(376,-2.170361);
   sigp1cls->SetBinContent(379,-2.232904);
   sigp1cls->SetBinContent(380,-0.7292525);
   sigp1cls->SetBinContent(381,0.3826065);
   sigp1cls->SetBinContent(382,1.450933);
   sigp1cls->SetBinContent(383,2.329396);
   sigp1cls->SetBinContent(384,2.905485);
   sigp1cls->SetBinContent(385,3.18038);
   sigp1cls->SetBinContent(386,3.37313);
   sigp1cls->SetBinContent(387,3.56588);
   sigp1cls->SetBinContent(388,3.701873);
   sigp1cls->SetBinContent(389,3.797719);
   sigp1cls->SetBinContent(390,3.856925);
   sigp1cls->SetBinContent(391,3.439801);
   sigp1cls->SetBinContent(392,2.955762);
   sigp1cls->SetBinContent(393,2.452489);
   sigp1cls->SetBinContent(394,2.153789);
   sigp1cls->SetBinContent(395,1.623772);
   sigp1cls->SetBinContent(396,1.231502);
   sigp1cls->SetBinContent(397,1.076557);
   sigp1cls->SetBinContent(398,0.6582501);
   sigp1cls->SetBinContent(399,0.33143);
   sigp1cls->SetBinContent(400,0.08048284);
   sigp1cls->SetBinContent(401,-0.2191419);
   sigp1cls->SetBinContent(402,-0.4444855);
   sigp1cls->SetBinContent(403,-0.6285619);
   sigp1cls->SetBinContent(404,-0.8126382);
   sigp1cls->SetBinContent(405,-1.00085);
   sigp1cls->SetBinContent(406,-1.194263);
   sigp1cls->SetBinContent(407,-1.387677);
   sigp1cls->SetBinContent(408,-1.47588);
   sigp1cls->SetBinContent(409,-1.55599);
   sigp1cls->SetBinContent(410,-1.636099);
   sigp1cls->SetBinContent(411,-1.718846);
   sigp1cls->SetBinContent(412,-1.802575);
   sigp1cls->SetBinContent(413,-1.87854);
   sigp1cls->SetBinContent(414,-1.926033);
   sigp1cls->SetBinContent(415,-1.973525);
   sigp1cls->SetBinContent(416,-2.029329);
   sigp1cls->SetBinContent(417,-2.088694);
   sigp1cls->SetBinContent(418,-2.148059);
   sigp1cls->SetBinContent(421,-2.428371);
   sigp1cls->SetBinContent(422,-1.179696);
   sigp1cls->SetBinContent(423,-0.1113695);
   sigp1cls->SetBinContent(424,0.9569569);
   sigp1cls->SetBinContent(425,2.025283);
   sigp1cls->SetBinContent(426,2.749043);
   sigp1cls->SetBinContent(427,3.023938);
   sigp1cls->SetBinContent(428,3.216688);
   sigp1cls->SetBinContent(429,3.316688);
   sigp1cls->SetBinContent(430,3.412534);
   sigp1cls->SetBinContent(431,3.50838);
   sigp1cls->SetBinContent(432,3.567586);
   sigp1cls->SetBinContent(433,3.128158);
   sigp1cls->SetBinContent(434,2.569092);
   sigp1cls->SetBinContent(435,2.065818);
   sigp1cls->SetBinContent(436,1.767118);
   sigp1cls->SetBinContent(437,1.40282);
   sigp1cls->SetBinContent(438,1.01055);
   sigp1cls->SetBinContent(439,0.884867);
   sigp1cls->SetBinContent(440,0.637954);
   sigp1cls->SetBinContent(441,0.3111339);
   sigp1cls->SetBinContent(442,0.07580031);
   sigp1cls->SetBinContent(443,-0.1953527);
   sigp1cls->SetBinContent(444,-0.4206963);
   sigp1cls->SetBinContent(445,-0.6047726);
   sigp1cls->SetBinContent(446,-0.7964521);
   sigp1cls->SetBinContent(447,-0.9898657);
   sigp1cls->SetBinContent(448,-1.183279);
   sigp1cls->SetBinContent(449,-1.376693);
   sigp1cls->SetBinContent(450,-1.464896);
   sigp1cls->SetBinContent(451,-1.545368);
   sigp1cls->SetBinContent(452,-1.629097);
   sigp1cls->SetBinContent(453,-1.712826);
   sigp1cls->SetBinContent(454,-1.796555);
   sigp1cls->SetBinContent(455,-1.87252);
   sigp1cls->SetBinContent(456,-1.920012);
   sigp1cls->SetBinContent(457,-1.967505);
   sigp1cls->SetBinContent(458,-2.014998);
   sigp1cls->SetBinContent(459,-2.066392);
   sigp1cls->SetBinContent(460,-2.125757);
   sigp1cls->SetBinContent(463,-2.741998);
   sigp1cls->SetBinContent(464,-1.673672);
   sigp1cls->SetBinContent(465,-0.6053456);
   sigp1cls->SetBinContent(466,0.4629809);
   sigp1cls->SetBinContent(467,1.531307);
   sigp1cls->SetBinContent(468,2.592602);
   sigp1cls->SetBinContent(469,2.835656);
   sigp1cls->SetBinContent(470,2.931503);
   sigp1cls->SetBinContent(471,3.027349);
   sigp1cls->SetBinContent(472,3.123195);
   sigp1cls->SetBinContent(473,3.219042);
   sigp1cls->SetBinContent(474,3.278247);
   sigp1cls->SetBinContent(475,2.741487);
   sigp1cls->SetBinContent(476,2.182421);
   sigp1cls->SetBinContent(477,1.679148);
   sigp1cls->SetBinContent(478,1.380447);
   sigp1cls->SetBinContent(479,1.081746);
   sigp1cls->SetBinContent(480,0.7895982);
   sigp1cls->SetBinContent(481,0.6639149);
   sigp1cls->SetBinContent(482,0.5382316);
   sigp1cls->SetBinContent(483,0.2908378);
   sigp1cls->SetBinContent(484,0.05550419);
   sigp1cls->SetBinContent(485,-0.1798294);
   sigp1cls->SetBinContent(486,-0.398641);
   sigp1cls->SetBinContent(487,-0.5920547);
   sigp1cls->SetBinContent(488,-0.7854683);
   sigp1cls->SetBinContent(489,-0.9788819);
   sigp1cls->SetBinContent(490,-1.172296);
   sigp1cls->SetBinContent(491,-1.365709);
   sigp1cls->SetBinContent(492,-1.455618);
   sigp1cls->SetBinContent(493,-1.539348);
   sigp1cls->SetBinContent(494,-1.623077);
   sigp1cls->SetBinContent(495,-1.706806);
   sigp1cls->SetBinContent(496,-1.790535);
   sigp1cls->SetBinContent(497,-1.8665);
   sigp1cls->SetBinContent(498,-1.913992);
   sigp1cls->SetBinContent(499,-1.961485);
   sigp1cls->SetBinContent(500,-2.008978);
   sigp1cls->SetBinContent(501,-2.056471);
   sigp1cls->SetBinContent(502,-2.103964);
   sigp1cls->SetBinContent(505,-2.531106);
   sigp1cls->SetBinContent(506,-1.46278);
   sigp1cls->SetBinContent(507,-0.3944535);
   sigp1cls->SetBinContent(508,0.673873);
   sigp1cls->SetBinContent(509,1.7422);
   sigp1cls->SetBinContent(510,2.65921);
   sigp1cls->SetBinContent(511,2.82993);
   sigp1cls->SetBinContent(512,2.925776);
   sigp1cls->SetBinContent(513,3.021623);
   sigp1cls->SetBinContent(514,3.117469);
   sigp1cls->SetBinContent(515,3.213315);
   sigp1cls->SetBinContent(516,3.202084);
   sigp1cls->SetBinContent(517,2.676792);
   sigp1cls->SetBinContent(518,2.117726);
   sigp1cls->SetBinContent(519,1.614452);
   sigp1cls->SetBinContent(520,1.315752);
   sigp1cls->SetBinContent(521,1.017051);
   sigp1cls->SetBinContent(522,0.6514468);
   sigp1cls->SetBinContent(523,0.5257635);
   sigp1cls->SetBinContent(524,0.4000801);
   sigp1cls->SetBinContent(525,0.1767806);
   sigp1cls->SetBinContent(526,-0.05855301);
   sigp1cls->SetBinContent(527,-0.2938866);
   sigp1cls->SetBinContent(528,-0.4609349);
   sigp1cls->SetBinContent(529,-0.6368953);
   sigp1cls->SetBinContent(530,-0.8303089);
   sigp1cls->SetBinContent(531,-1.023723);
   sigp1cls->SetBinContent(532,-1.217136);
   sigp1cls->SetBinContent(533,-1.41055);
   sigp1cls->SetBinContent(534,-1.467323);
   sigp1cls->SetBinContent(535,-1.551053);
   sigp1cls->SetBinContent(536,-1.634782);
   sigp1cls->SetBinContent(537,-1.718511);
   sigp1cls->SetBinContent(538,-1.80224);
   sigp1cls->SetBinContent(539,-1.875558);
   sigp1cls->SetBinContent(540,-1.914405);
   sigp1cls->SetBinContent(541,-1.961898);
   sigp1cls->SetBinContent(542,-2.009391);
   sigp1cls->SetBinContent(543,-2.056884);
   sigp1cls->SetBinContent(544,-2.104377);
   sigp1cls->SetBinContent(547,-2.350672);
   sigp1cls->SetBinContent(548,-0.8994537);
   sigp1cls->SetBinContent(549,0.1688728);
   sigp1cls->SetBinContent(550,1.237199);
   sigp1cls->SetBinContent(551,2.305526);
   sigp1cls->SetBinContent(552,2.79529);
   sigp1cls->SetBinContent(553,2.96601);
   sigp1cls->SetBinContent(554,3.061857);
   sigp1cls->SetBinContent(555,3.157703);
   sigp1cls->SetBinContent(556,3.227552);
   sigp1cls->SetBinContent(557,3.250607);
   sigp1cls->SetBinContent(558,3.238336);
   sigp1cls->SetBinContent(559,2.76683);
   sigp1cls->SetBinContent(560,2.214018);
   sigp1cls->SetBinContent(561,1.710745);
   sigp1cls->SetBinContent(562,1.412044);
   sigp1cls->SetBinContent(563,0.9725828);
   sigp1cls->SetBinContent(564,0.5546958);
   sigp1cls->SetBinContent(565,0.4290124);
   sigp1cls->SetBinContent(566,0.1598707);
   sigp1cls->SetBinContent(567,-0.06744055);
   sigp1cls->SetBinContent(568,-0.2194908);
   sigp1cls->SetBinContent(569,-0.4548243);
   sigp1cls->SetBinContent(570,-0.6218727);
   sigp1cls->SetBinContent(571,-0.7509848);
   sigp1cls->SetBinContent(572,-0.9030617);
   sigp1cls->SetBinContent(573,-1.096475);
   sigp1cls->SetBinContent(574,-1.289889);
   sigp1cls->SetBinContent(575,-1.483303);
   sigp1cls->SetBinContent(576,-1.539533);
   sigp1cls->SetBinContent(577,-1.58521);
   sigp1cls->SetBinContent(578,-1.655349);
   sigp1cls->SetBinContent(579,-1.739078);
   sigp1cls->SetBinContent(580,-1.822808);
   sigp1cls->SetBinContent(581,-1.896125);
   sigp1cls->SetBinContent(582,-1.931268);
   sigp1cls->SetBinContent(583,-1.96641);
   sigp1cls->SetBinContent(584,-2.013021);
   sigp1cls->SetBinContent(585,-2.060514);
   sigp1cls->SetBinContent(586,-2.108006);
   sigp1cls->SetBinContent(589,-2.195764);
   sigp1cls->SetBinContent(590,-0.5318277);
   sigp1cls->SetBinContent(591,0.732199);
   sigp1cls->SetBinContent(592,1.800526);
   sigp1cls->SetBinContent(593,2.486111);
   sigp1cls->SetBinContent(594,2.93137);
   sigp1cls->SetBinContent(595,3.10209);
   sigp1cls->SetBinContent(596,3.197937);
   sigp1cls->SetBinContent(597,3.240749);
   sigp1cls->SetBinContent(598,3.263804);
   sigp1cls->SetBinContent(599,3.286858);
   sigp1cls->SetBinContent(600,3.274587);
   sigp1cls->SetBinContent(601,2.803081);
   sigp1cls->SetBinContent(602,2.310311);
   sigp1cls->SetBinContent(603,1.807038);
   sigp1cls->SetBinContent(604,1.456054);
   sigp1cls->SetBinContent(605,0.8758318);
   sigp1cls->SetBinContent(606,0.4579448);
   sigp1cls->SetBinContent(607,0.2589382);
   sigp1cls->SetBinContent(608,-0.08990263);
   sigp1cls->SetBinContent(609,-0.3172139);
   sigp1cls->SetBinContent(610,-0.4229956);
   sigp1cls->SetBinContent(611,-0.6157621);
   sigp1cls->SetBinContent(612,-0.7828104);
   sigp1cls->SetBinContent(613,-0.9119226);
   sigp1cls->SetBinContent(614,-1.041035);
   sigp1cls->SetBinContent(615,-1.170147);
   sigp1cls->SetBinContent(616,-1.362642);
   sigp1cls->SetBinContent(617,-1.556055);
   sigp1cls->SetBinContent(618,-1.612285);
   sigp1cls->SetBinContent(619,-1.657963);
   sigp1cls->SetBinContent(620,-1.70364);
   sigp1cls->SetBinContent(621,-1.759646);
   sigp1cls->SetBinContent(622,-1.843375);
   sigp1cls->SetBinContent(623,-1.916693);
   sigp1cls->SetBinContent(624,-1.951835);
   sigp1cls->SetBinContent(625,-1.986978);
   sigp1cls->SetBinContent(626,-2.02212);
   sigp1cls->SetBinContent(627,-2.064143);
   sigp1cls->SetBinContent(628,-2.111636);
   sigp1cls->SetBinContent(631,-2.040855);
   sigp1cls->SetBinContent(632,-0.3769193);
   sigp1cls->SetBinContent(633,1.287017);
   sigp1cls->SetBinContent(634,2.176932);
   sigp1cls->SetBinContent(635,2.622191);
   sigp1cls->SetBinContent(636,3.06745);
   sigp1cls->SetBinContent(637,3.230891);
   sigp1cls->SetBinContent(638,3.253946);
   sigp1cls->SetBinContent(639,3.277);
   sigp1cls->SetBinContent(640,3.300055);
   sigp1cls->SetBinContent(641,3.32311);
   sigp1cls->SetBinContent(642,3.310839);
   sigp1cls->SetBinContent(643,2.839333);
   sigp1cls->SetBinContent(644,2.367827);
   sigp1cls->SetBinContent(645,1.90333);
   sigp1cls->SetBinContent(646,1.359303);
   sigp1cls->SetBinContent(647,0.7790808);
   sigp1cls->SetBinContent(648,0.3580058);
   sigp1cls->SetBinContent(649,0.009164894);
   sigp1cls->SetBinContent(650,-0.339676);
   sigp1cls->SetBinContent(651,-0.5669872);
   sigp1cls->SetBinContent(652,-0.6727689);
   sigp1cls->SetBinContent(653,-0.7785506);
   sigp1cls->SetBinContent(654,-0.9437482);
   sigp1cls->SetBinContent(655,-1.07286);
   sigp1cls->SetBinContent(656,-1.201972);
   sigp1cls->SetBinContent(657,-1.331085);
   sigp1cls->SetBinContent(658,-1.460197);
   sigp1cls->SetBinContent(659,-1.628808);
   sigp1cls->SetBinContent(660,-1.685038);
   sigp1cls->SetBinContent(661,-1.730716);
   sigp1cls->SetBinContent(662,-1.776393);
   sigp1cls->SetBinContent(663,-1.82207);
   sigp1cls->SetBinContent(664,-1.867748);
   sigp1cls->SetBinContent(665,-1.93726);
   sigp1cls->SetBinContent(666,-1.972403);
   sigp1cls->SetBinContent(667,-2.007545);
   sigp1cls->SetBinContent(668,-2.042688);
   sigp1cls->SetBinContent(669,-2.07783);
   sigp1cls->SetBinContent(670,-2.115266);
   sigp1cls->SetBinContent(673,-1.534596);
   sigp1cls->SetBinContent(674,0.2994978);
   sigp1cls->SetBinContent(675,1.452528);
   sigp1cls->SetBinContent(676,2.173373);
   sigp1cls->SetBinContent(677,2.618632);
   sigp1cls->SetBinContent(678,3.063891);
   sigp1cls->SetBinContent(679,3.177418);
   sigp1cls->SetBinContent(680,3.200473);
   sigp1cls->SetBinContent(681,3.223527);
   sigp1cls->SetBinContent(682,3.246582);
   sigp1cls->SetBinContent(683,3.269637);
   sigp1cls->SetBinContent(684,3.227702);
   sigp1cls->SetBinContent(685,2.859003);
   sigp1cls->SetBinContent(686,2.387497);
   sigp1cls->SetBinContent(687,1.913634);
   sigp1cls->SetBinContent(688,1.345975);
   sigp1cls->SetBinContent(689,0.7657521);
   sigp1cls->SetBinContent(690,0.2784779);
   sigp1cls->SetBinContent(691,-0.07036295);
   sigp1cls->SetBinContent(692,-0.4192038);
   sigp1cls->SetBinContent(693,-0.6465151);
   sigp1cls->SetBinContent(694,-0.7522967);
   sigp1cls->SetBinContent(695,-0.8580784);
   sigp1cls->SetBinContent(696,-1.022039);
   sigp1cls->SetBinContent(697,-1.151152);
   sigp1cls->SetBinContent(698,-1.280264);
   sigp1cls->SetBinContent(699,-1.409376);
   sigp1cls->SetBinContent(700,-1.538488);
   sigp1cls->SetBinContent(701,-1.6676);
   sigp1cls->SetBinContent(702,-1.719237);
   sigp1cls->SetBinContent(703,-1.764914);
   sigp1cls->SetBinContent(704,-1.810592);
   sigp1cls->SetBinContent(705,-1.856269);
   sigp1cls->SetBinContent(706,-1.901946);
   sigp1cls->SetBinContent(707,-1.967111);
   sigp1cls->SetBinContent(708,-2.00117);
   sigp1cls->SetBinContent(709,-2.036312);
   sigp1cls->SetBinContent(710,-2.071455);
   sigp1cls->SetBinContent(711,-2.106597);
   sigp1cls->SetBinContent(712,-2.14174);
   sigp1cls->SetBinContent(716,-0.2411705);
   sigp1cls->SetBinContent(717,1.085124);
   sigp1cls->SetBinContent(718,1.988136);
   sigp1cls->SetBinContent(719,2.475434);
   sigp1cls->SetBinContent(720,2.920693);
   sigp1cls->SetBinContent(721,3.03422);
   sigp1cls->SetBinContent(722,3.057275);
   sigp1cls->SetBinContent(723,3.08033);
   sigp1cls->SetBinContent(724,3.103384);
   sigp1cls->SetBinContent(725,3.063813);
   sigp1cls->SetBinContent(726,2.971069);
   sigp1cls->SetBinContent(727,2.862092);
   sigp1cls->SetBinContent(728,2.390586);
   sigp1cls->SetBinContent(729,1.916723);
   sigp1cls->SetBinContent(730,1.416068);
   sigp1cls->SetBinContent(731,0.8358457);
   sigp1cls->SetBinContent(732,0.3490012);
   sigp1cls->SetBinContent(733,0.0203547);
   sigp1cls->SetBinContent(734,-0.3284862);
   sigp1cls->SetBinContent(735,-0.5557974);
   sigp1cls->SetBinContent(736,-0.6615791);
   sigp1cls->SetBinContent(737,-0.8525844);
   sigp1cls->SetBinContent(738,-1.018063);
   sigp1cls->SetBinContent(739,-1.146796);
   sigp1cls->SetBinContent(740,-1.275908);
   sigp1cls->SetBinContent(741,-1.40502);
   sigp1cls->SetBinContent(742,-1.534132);
   sigp1cls->SetBinContent(743,-1.663245);
   sigp1cls->SetBinContent(744,-1.714882);
   sigp1cls->SetBinContent(745,-1.760559);
   sigp1cls->SetBinContent(746,-1.806236);
   sigp1cls->SetBinContent(747,-1.851914);
   sigp1cls->SetBinContent(748,-1.914273);
   sigp1cls->SetBinContent(749,-2.009859);
   sigp1cls->SetBinContent(750,-2.038136);
   sigp1cls->SetBinContent(751,-2.073279);
   sigp1cls->SetBinContent(752,-2.108421);
   sigp1cls->SetBinContent(753,-2.143564);
   sigp1cls->SetBinContent(754,-2.178706);
   sigp1cls->SetBinContent(758,-2.390254);
   sigp1cls->SetBinContent(759,0.4381946);
   sigp1cls->SetBinContent(760,1.620733);
   sigp1cls->SetBinContent(761,2.332236);
   sigp1cls->SetBinContent(762,2.777495);
   sigp1cls->SetBinContent(763,2.891022);
   sigp1cls->SetBinContent(764,2.914077);
   sigp1cls->SetBinContent(765,2.937132);
   sigp1cls->SetBinContent(766,2.899924);
   sigp1cls->SetBinContent(767,2.80718);
   sigp1cls->SetBinContent(768,2.714436);
   sigp1cls->SetBinContent(769,2.621692);
   sigp1cls->SetBinContent(770,2.393676);
   sigp1cls->SetBinContent(771,1.919812);
   sigp1cls->SetBinContent(772,1.437304);
   sigp1cls->SetBinContent(773,0.9059394);
   sigp1cls->SetBinContent(774,0.4190949);
   sigp1cls->SetBinContent(775,0.1003307);
   sigp1cls->SetBinContent(776,-0.2377685);
   sigp1cls->SetBinContent(777,-0.4650798);
   sigp1cls->SetBinContent(778,-0.6161932);
   sigp1cls->SetBinContent(779,-0.8489037);
   sigp1cls->SetBinContent(780,-1.014383);
   sigp1cls->SetBinContent(781,-1.142511);
   sigp1cls->SetBinContent(782,-1.271553);
   sigp1cls->SetBinContent(783,-1.400665);
   sigp1cls->SetBinContent(784,-1.529777);
   sigp1cls->SetBinContent(785,-1.658889);
   sigp1cls->SetBinContent(786,-1.710526);
   sigp1cls->SetBinContent(787,-1.756204);
   sigp1cls->SetBinContent(788,-1.801881);
   sigp1cls->SetBinContent(789,-1.847558);
   sigp1cls->SetBinContent(790,-1.957021);
   sigp1cls->SetBinContent(791,-2.052606);
   sigp1cls->SetBinContent(792,-2.079318);
   sigp1cls->SetBinContent(793,-2.110245);
   sigp1cls->SetBinContent(794,-2.145388);
   sigp1cls->SetBinContent(795,-2.18053);
   sigp1cls->SetBinContent(796,-2.215673);
   sigp1cls->SetBinContent(801,-1.83729);
   sigp1cls->SetBinContent(802,1.11756);
   sigp1cls->SetBinContent(803,2.156342);
   sigp1cls->SetBinContent(804,2.634298);
   sigp1cls->SetBinContent(805,2.747825);
   sigp1cls->SetBinContent(806,2.770879);
   sigp1cls->SetBinContent(807,2.736035);
   sigp1cls->SetBinContent(808,2.643291);
   sigp1cls->SetBinContent(809,2.550547);
   sigp1cls->SetBinContent(810,2.457803);
   sigp1cls->SetBinContent(811,2.365058);
   sigp1cls->SetBinContent(812,2.272315);
   sigp1cls->SetBinContent(813,1.922901);
   sigp1cls->SetBinContent(814,1.440394);
   sigp1cls->SetBinContent(815,0.957886);
   sigp1cls->SetBinContent(816,0.4891885);
   sigp1cls->SetBinContent(817,0.1704243);
   sigp1cls->SetBinContent(818,-0.1483399);
   sigp1cls->SetBinContent(819,-0.3798019);
   sigp1cls->SetBinContent(820,-0.6125124);
   sigp1cls->SetBinContent(821,-0.8452229);
   sigp1cls->SetBinContent(822,-1.010702);
   sigp1cls->SetBinContent(823,-1.13883);
   sigp1cls->SetBinContent(824,-1.267197);
   sigp1cls->SetBinContent(825,-1.39631);
   sigp1cls->SetBinContent(826,-1.525422);
   sigp1cls->SetBinContent(827,-1.654534);
   sigp1cls->SetBinContent(828,-1.706171);
   sigp1cls->SetBinContent(829,-1.751848);
   sigp1cls->SetBinContent(830,-1.797526);
   sigp1cls->SetBinContent(831,-1.885399);
   sigp1cls->SetBinContent(832,-1.999768);
   sigp1cls->SetBinContent(833,-2.095354);
   sigp1cls->SetBinContent(834,-2.122066);
   sigp1cls->SetBinContent(835,-2.148777);
   sigp1cls->SetBinContent(836,-2.182354);
   sigp1cls->SetBinContent(837,-2.217497);
   sigp1cls->SetBinContent(838,-2.252639);
   sigp1cls->SetBinContent(844,-1.255668);
   sigp1cls->SetBinContent(845,1.788939);
   sigp1cls->SetBinContent(846,2.4911);
   sigp1cls->SetBinContent(847,2.604627);
   sigp1cls->SetBinContent(848,2.572145);
   sigp1cls->SetBinContent(849,2.479401);
   sigp1cls->SetBinContent(850,2.386657);
   sigp1cls->SetBinContent(851,2.293913);
   sigp1cls->SetBinContent(852,2.201169);
   sigp1cls->SetBinContent(853,2.108425);
   sigp1cls->SetBinContent(854,2.092044);
   sigp1cls->SetBinContent(855,1.923037);
   sigp1cls->SetBinContent(856,1.442651);
   sigp1cls->SetBinContent(857,0.9601432);
   sigp1cls->SetBinContent(858,0.5361154);
   sigp1cls->SetBinContent(859,0.2173512);
   sigp1cls->SetBinContent(860,-0.101413);
   sigp1cls->SetBinContent(861,-0.3761212);
   sigp1cls->SetBinContent(862,-0.6088316);
   sigp1cls->SetBinContent(863,-0.8415421);
   sigp1cls->SetBinContent(864,-1.007021);
   sigp1cls->SetBinContent(865,-1.135149);
   sigp1cls->SetBinContent(866,-1.263278);
   sigp1cls->SetBinContent(867,-1.391954);
   sigp1cls->SetBinContent(868,-1.521066);
   sigp1cls->SetBinContent(869,-1.650178);
   sigp1cls->SetBinContent(870,-1.701815);
   sigp1cls->SetBinContent(871,-1.747493);
   sigp1cls->SetBinContent(872,-1.813778);
   sigp1cls->SetBinContent(873,-1.928147);
   sigp1cls->SetBinContent(874,-2.042516);
   sigp1cls->SetBinContent(875,-2.138101);
   sigp1cls->SetBinContent(876,-2.164813);
   sigp1cls->SetBinContent(877,-2.191525);
   sigp1cls->SetBinContent(878,-2.219321);
   sigp1cls->SetBinContent(879,-2.254463);
   sigp1cls->SetBinContent(880,-2.289606);
   sigp1cls->SetBinContent(887,-0.674045);
   sigp1cls->SetBinContent(888,2.324547);
   sigp1cls->SetBinContent(889,2.408256);
   sigp1cls->SetBinContent(890,2.321386);
   sigp1cls->SetBinContent(891,2.310879);
   sigp1cls->SetBinContent(892,2.300373);
   sigp1cls->SetBinContent(893,2.289866);
   sigp1cls->SetBinContent(894,2.279359);
   sigp1cls->SetBinContent(895,2.268852);
   sigp1cls->SetBinContent(896,2.208179);
   sigp1cls->SetBinContent(897,1.821783);
   sigp1cls->SetBinContent(898,1.443244);
   sigp1cls->SetBinContent(899,0.9607366);
   sigp1cls->SetBinContent(900,0.5367088);
   sigp1cls->SetBinContent(901,0.2179446);
   sigp1cls->SetBinContent(902,-0.1018968);
   sigp1cls->SetBinContent(903,-0.375383);
   sigp1cls->SetBinContent(904,-0.6051509);
   sigp1cls->SetBinContent(905,-0.8378614);
   sigp1cls->SetBinContent(906,-1.00334);
   sigp1cls->SetBinContent(907,-1.131469);
   sigp1cls->SetBinContent(908,-1.259597);
   sigp1cls->SetBinContent(909,-1.387725);
   sigp1cls->SetBinContent(910,-1.516711);
   sigp1cls->SetBinContent(911,-1.645823);
   sigp1cls->SetBinContent(912,-1.69746);
   sigp1cls->SetBinContent(913,-1.743137);
   sigp1cls->SetBinContent(914,-1.856525);
   sigp1cls->SetBinContent(915,-1.970894);
   sigp1cls->SetBinContent(916,-2.085263);
   sigp1cls->SetBinContent(917,-2.180849);
   sigp1cls->SetBinContent(918,-2.207561);
   sigp1cls->SetBinContent(919,-2.234273);
   sigp1cls->SetBinContent(920,-2.260984);
   sigp1cls->SetBinContent(921,-2.29143);
   sigp1cls->SetBinContent(922,-2.326572);
   sigp1cls->SetBinContent(930,-0.09242225);
   sigp1cls->SetBinContent(931,2.326772);
   sigp1cls->SetBinContent(932,2.487687);
   sigp1cls->SetBinContent(933,2.47718);
   sigp1cls->SetBinContent(934,2.466674);
   sigp1cls->SetBinContent(935,2.456167);
   sigp1cls->SetBinContent(936,2.44566);
   sigp1cls->SetBinContent(937,2.435153);
   sigp1cls->SetBinContent(938,2.106925);
   sigp1cls->SetBinContent(939,1.720529);
   sigp1cls->SetBinContent(940,1.386549);
   sigp1cls->SetBinContent(941,0.96133);
   sigp1cls->SetBinContent(942,0.5373021);
   sigp1cls->SetBinContent(943,0.218278);
   sigp1cls->SetBinContent(944,-0.1030865);
   sigp1cls->SetBinContent(945,-0.3765726);
   sigp1cls->SetBinContent(946,-0.6021804);
   sigp1cls->SetBinContent(947,-0.8341807);
   sigp1cls->SetBinContent(948,-0.9996597);
   sigp1cls->SetBinContent(949,-1.127788);
   sigp1cls->SetBinContent(950,-1.255916);
   sigp1cls->SetBinContent(951,-1.384045);
   sigp1cls->SetBinContent(952,-1.512356);
   sigp1cls->SetBinContent(953,-1.641468);
   sigp1cls->SetBinContent(954,-1.693105);
   sigp1cls->SetBinContent(955,-1.784904);
   sigp1cls->SetBinContent(956,-1.899273);
   sigp1cls->SetBinContent(957,-2.013642);
   sigp1cls->SetBinContent(958,-2.128011);
   sigp1cls->SetBinContent(959,-2.223596);
   sigp1cls->SetBinContent(960,-2.250308);
   sigp1cls->SetBinContent(961,-2.27702);
   sigp1cls->SetBinContent(962,-2.303732);
   sigp1cls->SetBinContent(963,-2.330444);
   sigp1cls->SetBinContent(964,-2.363539);
   sigp1cls->SetBinContent(972,-2.058687);
   sigp1cls->SetBinContent(973,0.4892004);
   sigp1cls->SetBinContent(974,2.18396);
   sigp1cls->SetBinContent(975,2.405703);
   sigp1cls->SetBinContent(976,2.627445);
   sigp1cls->SetBinContent(977,2.622468);
   sigp1cls->SetBinContent(978,2.611961);
   sigp1cls->SetBinContent(979,2.406362);
   sigp1cls->SetBinContent(980,2.005671);
   sigp1cls->SetBinContent(981,1.619275);
   sigp1cls->SetBinContent(982,1.285295);
   sigp1cls->SetBinContent(983,0.9513143);
   sigp1cls->SetBinContent(984,0.5378956);
   sigp1cls->SetBinContent(985,0.2170883);
   sigp1cls->SetBinContent(986,-0.1042761);
   sigp1cls->SetBinContent(987,-0.3777622);
   sigp1cls->SetBinContent(988,-0.6033701);
   sigp1cls->SetBinContent(989,-0.8304999);
   sigp1cls->SetBinContent(990,-0.995979);
   sigp1cls->SetBinContent(991,-1.124107);
   sigp1cls->SetBinContent(992,-1.252236);
   sigp1cls->SetBinContent(993,-1.380364);
   sigp1cls->SetBinContent(994,-1.508492);
   sigp1cls->SetBinContent(995,-1.637112);
   sigp1cls->SetBinContent(996,-1.713282);
   sigp1cls->SetBinContent(997,-1.827651);
   sigp1cls->SetBinContent(998,-1.94202);
   sigp1cls->SetBinContent(999,-2.056389);
   sigp1cls->SetBinContent(1000,-2.170758);
   sigp1cls->SetBinContent(1001,-2.266344);
   sigp1cls->SetBinContent(1002,-2.293056);
   sigp1cls->SetBinContent(1003,-2.319768);
   sigp1cls->SetBinContent(1004,-2.34648);
   sigp1cls->SetBinContent(1005,-2.373191);
   sigp1cls->SetBinContent(1006,-2.400506);
   sigp1cls->SetBinContent(1015,-1.580238);
   sigp1cls->SetBinContent(1016,1.070823);
   sigp1cls->SetBinContent(1017,2.041148);
   sigp1cls->SetBinContent(1018,2.262891);
   sigp1cls->SetBinContent(1019,2.484633);
   sigp1cls->SetBinContent(1020,2.705168);
   sigp1cls->SetBinContent(1021,2.330428);
   sigp1cls->SetBinContent(1022,1.929736);
   sigp1cls->SetBinContent(1023,1.54334);
   sigp1cls->SetBinContent(1024,1.20936);
   sigp1cls->SetBinContent(1025,0.8753797);
   sigp1cls->SetBinContent(1026,0.5260539);
   sigp1cls->SetBinContent(1027,0.2046895);
   sigp1cls->SetBinContent(1028,-0.116675);
   sigp1cls->SetBinContent(1029,-0.3901611);
   sigp1cls->SetBinContent(1030,-0.6157689);
   sigp1cls->SetBinContent(1031,-0.8413767);
   sigp1cls->SetBinContent(1032,-0.9917998);
   sigp1cls->SetBinContent(1033,-1.119928);
   sigp1cls->SetBinContent(1034,-1.248056);
   sigp1cls->SetBinContent(1035,-1.376185);
   sigp1cls->SetBinContent(1036,-1.504313);
   sigp1cls->SetBinContent(1037,-1.632892);
   sigp1cls->SetBinContent(1038,-1.745407);
   sigp1cls->SetBinContent(1039,-1.859776);
   sigp1cls->SetBinContent(1040,-1.974145);
   sigp1cls->SetBinContent(1041,-2.088515);
   sigp1cls->SetBinContent(1042,-2.202884);
   sigp1cls->SetBinContent(1043,-2.298469);
   sigp1cls->SetBinContent(1044,-2.325181);
   sigp1cls->SetBinContent(1045,-2.351893);
   sigp1cls->SetBinContent(1046,-2.378605);
   sigp1cls->SetBinContent(1047,-2.405317);
   sigp1cls->SetBinContent(1048,-2.432029);
   sigp1cls->SetBinContent(1058,-1.101788);
   sigp1cls->SetBinContent(1059,1.652446);
   sigp1cls->SetBinContent(1060,1.898336);
   sigp1cls->SetBinContent(1061,2.120079);
   sigp1cls->SetBinContent(1062,2.340613);
   sigp1cls->SetBinContent(1063,2.38109);
   sigp1cls->SetBinContent(1064,1.980399);
   sigp1cls->SetBinContent(1065,1.594003);
   sigp1cls->SetBinContent(1066,1.260022);
   sigp1cls->SetBinContent(1067,0.9146997);
   sigp1cls->SetBinContent(1068,0.5025682);
   sigp1cls->SetBinContent(1069,0.1362446);
   sigp1cls->SetBinContent(1070,-0.1851198);
   sigp1cls->SetBinContent(1071,-0.4586059);
   sigp1cls->SetBinContent(1072,-0.6842138);
   sigp1cls->SetBinContent(1073,-0.8613093);
   sigp1cls->SetBinContent(1074,-0.9851288);
   sigp1cls->SetBinContent(1075,-1.113257);
   sigp1cls->SetBinContent(1076,-1.241385);
   sigp1cls->SetBinContent(1077,-1.369514);
   sigp1cls->SetBinContent(1078,-1.497642);
   sigp1cls->SetBinContent(1079,-1.633425);
   sigp1cls->SetBinContent(1080,-1.724421);
   sigp1cls->SetBinContent(1081,-1.83879);
   sigp1cls->SetBinContent(1082,-1.953159);
   sigp1cls->SetBinContent(1083,-2.067528);
   sigp1cls->SetBinContent(1084,-2.181897);
   sigp1cls->SetBinContent(1085,-2.277483);
   sigp1cls->SetBinContent(1086,-2.304194);
   sigp1cls->SetBinContent(1087,-2.330906);
   sigp1cls->SetBinContent(1088,-2.357618);
   sigp1cls->SetBinContent(1089,-2.38433);
   sigp1cls->SetBinContent(1090,-2.426852);
   sigp1cls->SetBinContent(1101,-0.6233387);
   sigp1cls->SetBinContent(1102,1.533782);
   sigp1cls->SetBinContent(1103,1.755524);
   sigp1cls->SetBinContent(1104,1.976059);
   sigp1cls->SetBinContent(1105,2.180892);
   sigp1cls->SetBinContent(1106,2.031061);
   sigp1cls->SetBinContent(1107,1.644665);
   sigp1cls->SetBinContent(1108,1.310684);
   sigp1cls->SetBinContent(1109,0.9158691);
   sigp1cls->SetBinContent(1110,0.5037376);
   sigp1cls->SetBinContent(1111,0.08085239);
   sigp1cls->SetBinContent(1112,-0.2535647);
   sigp1cls->SetBinContent(1113,-0.5270509);
   sigp1cls->SetBinContent(1114,-0.7385744);
   sigp1cls->SetBinContent(1115,-0.8546382);
   sigp1cls->SetBinContent(1116,-0.9784577);
   sigp1cls->SetBinContent(1117,-1.106586);
   sigp1cls->SetBinContent(1118,-1.234714);
   sigp1cls->SetBinContent(1119,-1.362843);
   sigp1cls->SetBinContent(1120,-1.495323);
   sigp1cls->SetBinContent(1121,-1.633957);
   sigp1cls->SetBinContent(1122,-1.720919);
   sigp1cls->SetBinContent(1123,-1.817803);
   sigp1cls->SetBinContent(1124,-1.932172);
   sigp1cls->SetBinContent(1125,-2.046541);
   sigp1cls->SetBinContent(1126,-2.16091);
   sigp1cls->SetBinContent(1127,-2.256496);
   sigp1cls->SetBinContent(1128,-2.283208);
   sigp1cls->SetBinContent(1129,-2.30992);
   sigp1cls->SetBinContent(1130,-2.336631);
   sigp1cls->SetBinContent(1131,-2.363343);
   sigp1cls->SetBinContent(1132,-2.442003);
   sigp1cls->SetBinContent(1144,-0.1448892);
   sigp1cls->SetBinContent(1145,1.39097);
   sigp1cls->SetBinContent(1146,1.611504);
   sigp1cls->SetBinContent(1147,1.816337);
   sigp1cls->SetBinContent(1148,2.02117);
   sigp1cls->SetBinContent(1149,1.695327);
   sigp1cls->SetBinContent(1150,1.323196);
   sigp1cls->SetBinContent(1151,0.9170384);
   sigp1cls->SetBinContent(1152,0.5049069);
   sigp1cls->SetBinContent(1153,0.08202174);
   sigp1cls->SetBinContent(1154,-0.3220096);
   sigp1cls->SetBinContent(1155,-0.5954957);
   sigp1cls->SetBinContent(1156,-0.7319034);
   sigp1cls->SetBinContent(1157,-0.8479672);
   sigp1cls->SetBinContent(1158,-0.9717867);
   sigp1cls->SetBinContent(1159,-1.099915);
   sigp1cls->SetBinContent(1160,-1.228043);
   sigp1cls->SetBinContent(1161,-1.357222);
   sigp1cls->SetBinContent(1162,-1.495856);
   sigp1cls->SetBinContent(1163,-1.63449);
   sigp1cls->SetBinContent(1164,-1.721452);
   sigp1cls->SetBinContent(1165,-1.804438);
   sigp1cls->SetBinContent(1166,-1.911185);
   sigp1cls->SetBinContent(1167,-2.025554);
   sigp1cls->SetBinContent(1168,-2.139924);
   sigp1cls->SetBinContent(1169,-2.235509);
   sigp1cls->SetBinContent(1170,-2.262221);
   sigp1cls->SetBinContent(1171,-2.288933);
   sigp1cls->SetBinContent(1172,-2.315645);
   sigp1cls->SetBinContent(1173,-2.377741);
   sigp1cls->SetBinContent(1174,-2.457153);
   sigp1cls->SetBinContent(1187,0.3335603);
   sigp1cls->SetBinContent(1188,1.24695);
   sigp1cls->SetBinContent(1189,1.451783);
   sigp1cls->SetBinContent(1190,1.656616);
   sigp1cls->SetBinContent(1191,1.730522);
   sigp1cls->SetBinContent(1192,1.324365);
   sigp1cls->SetBinContent(1193,0.9182078);
   sigp1cls->SetBinContent(1194,0.5060763);
   sigp1cls->SetBinContent(1195,0.08319108);
   sigp1cls->SetBinContent(1196,-0.3396941);
   sigp1cls->SetBinContent(1197,-0.6091686);
   sigp1cls->SetBinContent(1198,-0.7252324);
   sigp1cls->SetBinContent(1199,-0.8412961);
   sigp1cls->SetBinContent(1200,-0.9651157);
   sigp1cls->SetBinContent(1201,-1.093244);
   sigp1cls->SetBinContent(1202,-1.221372);
   sigp1cls->SetBinContent(1203,-1.357755);
   sigp1cls->SetBinContent(1204,-1.496389);
   sigp1cls->SetBinContent(1205,-1.635023);
   sigp1cls->SetBinContent(1206,-1.721985);
   sigp1cls->SetBinContent(1207,-1.804971);
   sigp1cls->SetBinContent(1208,-1.890199);
   sigp1cls->SetBinContent(1209,-2.004568);
   sigp1cls->SetBinContent(1210,-2.118937);
   sigp1cls->SetBinContent(1211,-2.214522);
   sigp1cls->SetBinContent(1212,-2.241234);
   sigp1cls->SetBinContent(1213,-2.267946);
   sigp1cls->SetBinContent(1214,-2.313479);
   sigp1cls->SetBinContent(1215,-2.392892);
   sigp1cls->SetBinContent(1216,-2.472304);
   sigp1cls->SetBinContent(1229,-1.248671);
   sigp1cls->SetBinContent(1230,0.8120099);
   sigp1cls->SetBinContent(1231,1.151237);
   sigp1cls->SetBinContent(1232,1.395032);
   sigp1cls->SetBinContent(1233,1.514061);
   sigp1cls->SetBinContent(1234,1.175611);
   sigp1cls->SetBinContent(1235,0.8371609);
   sigp1cls->SetBinContent(1236,0.5190073);
   sigp1cls->SetBinContent(1237,0.1087886);
   sigp1cls->SetBinContent(1238,-0.3014302);
   sigp1cls->SetBinContent(1239,-0.5922258);
   sigp1cls->SetBinContent(1240,-0.7185613);
   sigp1cls->SetBinContent(1241,-0.8346251);
   sigp1cls->SetBinContent(1242,-0.9584447);
   sigp1cls->SetBinContent(1243,-1.086573);
   sigp1cls->SetBinContent(1244,-1.219654);
   sigp1cls->SetBinContent(1245,-1.358288);
   sigp1cls->SetBinContent(1246,-1.496922);
   sigp1cls->SetBinContent(1247,-1.635556);
   sigp1cls->SetBinContent(1248,-1.722517);
   sigp1cls->SetBinContent(1249,-1.805504);
   sigp1cls->SetBinContent(1250,-1.88849);
   sigp1cls->SetBinContent(1251,-1.983581);
   sigp1cls->SetBinContent(1252,-2.09795);
   sigp1cls->SetBinContent(1253,-2.193536);
   sigp1cls->SetBinContent(1254,-2.220248);
   sigp1cls->SetBinContent(1255,-2.249218);
   sigp1cls->SetBinContent(1256,-2.32863);
   sigp1cls->SetBinContent(1257,-2.408042);
   sigp1cls->SetBinContent(1258,-2.487455);
   sigp1cls->SetBinContent(1272,-0.7702218);
   sigp1cls->SetBinContent(1273,0.920267);
   sigp1cls->SetBinContent(1274,1.164062);
   sigp1cls->SetBinContent(1275,1.28309);
   sigp1cls->SetBinContent(1276,0.9446403);
   sigp1cls->SetBinContent(1277,0.641274);
   sigp1cls->SetBinContent(1278,0.4200792);
   sigp1cls->SetBinContent(1279,0.1533857);
   sigp1cls->SetBinContent(1280,-0.256833);
   sigp1cls->SetBinContent(1281,-0.5476288);
   sigp1cls->SetBinContent(1282,-0.7118903);
   sigp1cls->SetBinContent(1283,-0.8279541);
   sigp1cls->SetBinContent(1284,-0.9517736);
   sigp1cls->SetBinContent(1285,-1.081553);
   sigp1cls->SetBinContent(1286,-1.220187);
   sigp1cls->SetBinContent(1287,-1.358821);
   sigp1cls->SetBinContent(1288,-1.497455);
   sigp1cls->SetBinContent(1289,-1.636089);
   sigp1cls->SetBinContent(1290,-1.72305);
   sigp1cls->SetBinContent(1291,-1.806037);
   sigp1cls->SetBinContent(1292,-1.889023);
   sigp1cls->SetBinContent(1293,-1.972009);
   sigp1cls->SetBinContent(1294,-2.076964);
   sigp1cls->SetBinContent(1295,-2.172549);
   sigp1cls->SetBinContent(1296,-2.199261);
   sigp1cls->SetBinContent(1297,-2.264369);
   sigp1cls->SetBinContent(1298,-2.343781);
   sigp1cls->SetBinContent(1299,-2.423193);
   sigp1cls->SetBinContent(1300,-2.502605);
   sigp1cls->SetBinContent(1315,-0.2917722);
   sigp1cls->SetBinContent(1316,0.9330915);
   sigp1cls->SetBinContent(1317,1.05212);
   sigp1cls->SetBinContent(1318,0.73472);
   sigp1cls->SetBinContent(1319,0.4945042);
   sigp1cls->SetBinContent(1320,0.2733093);
   sigp1cls->SetBinContent(1321,0.08635207);
   sigp1cls->SetBinContent(1322,-0.2122359);
   sigp1cls->SetBinContent(1323,-0.5030316);
   sigp1cls->SetBinContent(1324,-0.6744043);
   sigp1cls->SetBinContent(1325,-0.821283);
   sigp1cls->SetBinContent(1326,-0.9451026);
   sigp1cls->SetBinContent(1327,-1.082086);
   sigp1cls->SetBinContent(1328,-1.22072);
   sigp1cls->SetBinContent(1329,-1.359354);
   sigp1cls->SetBinContent(1330,-1.497988);
   sigp1cls->SetBinContent(1331,-1.636622);
   sigp1cls->SetBinContent(1332,-1.723583);
   sigp1cls->SetBinContent(1333,-1.80657);
   sigp1cls->SetBinContent(1334,-1.889556);
   sigp1cls->SetBinContent(1335,-1.972542);
   sigp1cls->SetBinContent(1336,-2.055977);
   sigp1cls->SetBinContent(1337,-2.151562);
   sigp1cls->SetBinContent(1338,-2.200107);
   sigp1cls->SetBinContent(1339,-2.279519);
   sigp1cls->SetBinContent(1340,-2.358932);
   sigp1cls->SetBinContent(1341,-2.438344);
   sigp1cls->SetBinContent(1342,-2.517756);
   sigp1cls->SetBinContent(1358,-0.00222009);
   sigp1cls->SetBinContent(1359,0.8281659);
   sigp1cls->SetBinContent(1360,0.5879501);
   sigp1cls->SetBinContent(1361,0.3477343);
   sigp1cls->SetBinContent(1362,0.1265394);
   sigp1cls->SetBinContent(1363,-0.0604178);
   sigp1cls->SetBinContent(1364,-0.247375);
   sigp1cls->SetBinContent(1365,-0.4584345);
   sigp1cls->SetBinContent(1366,-0.6298072);
   sigp1cls->SetBinContent(1367,-0.8011798);
   sigp1cls->SetBinContent(1368,-0.9439846);
   sigp1cls->SetBinContent(1369,-1.082619);
   sigp1cls->SetBinContent(1370,-1.221253);
   sigp1cls->SetBinContent(1371,-1.359887);
   sigp1cls->SetBinContent(1372,-1.498521);
   sigp1cls->SetBinContent(1373,-1.637155);
   sigp1cls->SetBinContent(1374,-1.724116);
   sigp1cls->SetBinContent(1375,-1.807103);
   sigp1cls->SetBinContent(1376,-1.890089);
   sigp1cls->SetBinContent(1377,-1.973075);
   sigp1cls->SetBinContent(1378,-2.056062);
   sigp1cls->SetBinContent(1379,-2.135846);
   sigp1cls->SetBinContent(1380,-2.215258);
   sigp1cls->SetBinContent(1381,-2.29467);
   sigp1cls->SetBinContent(1382,-2.374082);
   sigp1cls->SetBinContent(1383,-2.453494);
   sigp1cls->SetBinContent(1384,-2.532907);
   sigp1cls->SetBinContent(1401,-0.1713723);
   sigp1cls->SetBinContent(1402,-0.4115881);
   sigp1cls->SetBinContent(1403,-0.2803748);
   sigp1cls->SetBinContent(1404,-0.1976731);
   sigp1cls->SetBinContent(1405,-0.3846304);
   sigp1cls->SetBinContent(1406,-0.5715876);
   sigp1cls->SetBinContent(1407,-0.7433313);
   sigp1cls->SetBinContent(1408,-0.914704);
   sigp1cls->SetBinContent(1409,-0.9183563);
   sigp1cls->SetBinContent(1410,-0.9452944);
   sigp1cls->SetBinContent(1411,-1.083929);
   sigp1cls->SetBinContent(1412,-1.222563);
   sigp1cls->SetBinContent(1413,-1.361197);
   sigp1cls->SetBinContent(1414,-1.499831);
   sigp1cls->SetBinContent(1415,-1.638465);
   sigp1cls->SetBinContent(1416,-1.725426);
   sigp1cls->SetBinContent(1417,-1.808412);
   sigp1cls->SetBinContent(1418,-1.891399);
   sigp1cls->SetBinContent(1419,-1.974385);
   sigp1cls->SetBinContent(1420,-2.057371);
   sigp1cls->SetBinContent(1421,-2.13981);
   sigp1cls->SetBinContent(1422,-2.19168);
   sigp1cls->SetBinContent(1423,-2.271092);
   sigp1cls->SetBinContent(1424,-2.350504);
   sigp1cls->SetBinContent(1425,-2.429916);
   sigp1cls->SetBinContent(1426,-2.509328);
   sigp1cls->SetBinContent(1443,-1.1051);
   sigp1cls->SetBinContent(1444,-0.872588);
   sigp1cls->SetBinContent(1445,-0.6400759);
   sigp1cls->SetBinContent(1446,-0.5573742);
   sigp1cls->SetBinContent(1447,-0.7443314);
   sigp1cls->SetBinContent(1448,-0.9227543);
   sigp1cls->SetBinContent(1449,-1.094127);
   sigp1cls->SetBinContent(1450,-1.057526);
   sigp1cls->SetBinContent(1451,-0.9471289);
   sigp1cls->SetBinContent(1452,-0.9712225);
   sigp1cls->SetBinContent(1453,-1.085394);
   sigp1cls->SetBinContent(1454,-1.224028);
   sigp1cls->SetBinContent(1455,-1.362662);
   sigp1cls->SetBinContent(1456,-1.501296);
   sigp1cls->SetBinContent(1457,-1.63993);
   sigp1cls->SetBinContent(1458,-1.726891);
   sigp1cls->SetBinContent(1459,-1.809878);
   sigp1cls->SetBinContent(1460,-1.892864);
   sigp1cls->SetBinContent(1461,-1.97585);
   sigp1cls->SetBinContent(1462,-2.072649);
   sigp1cls->SetBinContent(1463,-2.161366);
   sigp1cls->SetBinContent(1464,-2.163661);
   sigp1cls->SetBinContent(1465,-2.239768);
   sigp1cls->SetBinContent(1466,-2.31918);
   sigp1cls->SetBinContent(1467,-2.398592);
   sigp1cls->SetBinContent(1468,-2.478004);
   sigp1cls->SetBinContent(1486,-1.232289);
   sigp1cls->SetBinContent(1487,-0.999777);
   sigp1cls->SetBinContent(1488,-0.9170753);
   sigp1cls->SetBinContent(1489,-1.102177);
   sigp1cls->SetBinContent(1490,-1.27355);
   sigp1cls->SetBinContent(1491,-1.196696);
   sigp1cls->SetBinContent(1492,-1.086299);
   sigp1cls->SetBinContent(1493,-0.9759015);
   sigp1cls->SetBinContent(1494,-0.9999951);
   sigp1cls->SetBinContent(1495,-1.098806);
   sigp1cls->SetBinContent(1496,-1.225493);
   sigp1cls->SetBinContent(1497,-1.364127);
   sigp1cls->SetBinContent(1498,-1.502761);
   sigp1cls->SetBinContent(1499,-1.641395);
   sigp1cls->SetBinContent(1500,-1.728356);
   sigp1cls->SetBinContent(1501,-1.811343);
   sigp1cls->SetBinContent(1502,-1.894329);
   sigp1cls->SetBinContent(1503,-1.98192);
   sigp1cls->SetBinContent(1504,-2.094206);
   sigp1cls->SetBinContent(1505,-2.182923);
   sigp1cls->SetBinContent(1506,-2.185218);
   sigp1cls->SetBinContent(1507,-2.208444);
   sigp1cls->SetBinContent(1508,-2.287856);
   sigp1cls->SetBinContent(1509,-2.367268);
   sigp1cls->SetBinContent(1510,-2.446681);
   sigp1cls->SetBinContent(1529,-1.359478);
   sigp1cls->SetBinContent(1530,-1.276776);
   sigp1cls->SetBinContent(1531,-1.446264);
   sigp1cls->SetBinContent(1532,-1.335867);
   sigp1cls->SetBinContent(1533,-1.225469);
   sigp1cls->SetBinContent(1534,-1.115072);
   sigp1cls->SetBinContent(1535,-1.004674);
   sigp1cls->SetBinContent(1536,-1.028768);
   sigp1cls->SetBinContent(1537,-1.127578);
   sigp1cls->SetBinContent(1538,-1.226958);
   sigp1cls->SetBinContent(1539,-1.365592);
   sigp1cls->SetBinContent(1540,-1.504226);
   sigp1cls->SetBinContent(1541,-1.642861);
   sigp1cls->SetBinContent(1542,-1.729822);
   sigp1cls->SetBinContent(1543,-1.812808);
   sigp1cls->SetBinContent(1544,-1.895794);
   sigp1cls->SetBinContent(1545,-2.003477);
   sigp1cls->SetBinContent(1546,-2.115763);
   sigp1cls->SetBinContent(1547,-2.20448);
   sigp1cls->SetBinContent(1548,-2.206774);
   sigp1cls->SetBinContent(1549,-2.209069);
   sigp1cls->SetBinContent(1550,-2.256532);
   sigp1cls->SetBinContent(1551,-2.335944);
   sigp1cls->SetBinContent(1552,-2.415357);
   sigp1cls->SetBinContent(1572,-1.585434);
   sigp1cls->SetBinContent(1573,-1.475037);
   sigp1cls->SetBinContent(1574,-1.364639);
   sigp1cls->SetBinContent(1575,-1.254242);
   sigp1cls->SetBinContent(1576,-1.143844);
   sigp1cls->SetBinContent(1577,-1.033447);
   sigp1cls->SetBinContent(1578,-1.05754);
   sigp1cls->SetBinContent(1579,-1.156351);
   sigp1cls->SetBinContent(1580,-1.255162);
   sigp1cls->SetBinContent(1581,-1.367058);
   sigp1cls->SetBinContent(1582,-1.505692);
   sigp1cls->SetBinContent(1583,-1.644326);
   sigp1cls->SetBinContent(1584,-1.731287);
   sigp1cls->SetBinContent(1585,-1.814273);
   sigp1cls->SetBinContent(1586,-1.912747);
   sigp1cls->SetBinContent(1587,-2.025033);
   sigp1cls->SetBinContent(1588,-2.13732);
   sigp1cls->SetBinContent(1589,-2.226037);
   sigp1cls->SetBinContent(1590,-2.228331);
   sigp1cls->SetBinContent(1591,-2.230626);
   sigp1cls->SetBinContent(1592,-2.23292);
   sigp1cls->SetBinContent(1593,-2.304621);
   sigp1cls->SetBinContent(1594,-2.384033);
   sigp1cls->SetBinContent(1615,-1.506561);
   sigp1cls->SetBinContent(1616,-1.393412);
   sigp1cls->SetBinContent(1617,-1.283014);
   sigp1cls->SetBinContent(1618,-1.172617);
   sigp1cls->SetBinContent(1619,-1.062219);
   sigp1cls->SetBinContent(1620,-1.086313);
   sigp1cls->SetBinContent(1621,-1.185124);
   sigp1cls->SetBinContent(1622,-1.283934);
   sigp1cls->SetBinContent(1623,-1.382745);
   sigp1cls->SetBinContent(1624,-1.507157);
   sigp1cls->SetBinContent(1625,-1.645791);
   sigp1cls->SetBinContent(1626,-1.732752);
   sigp1cls->SetBinContent(1627,-1.822017);
   sigp1cls->SetBinContent(1628,-1.934304);
   sigp1cls->SetBinContent(1629,-2.04659);
   sigp1cls->SetBinContent(1630,-2.158877);
   sigp1cls->SetBinContent(1631,-2.247593);
   sigp1cls->SetBinContent(1632,-2.249888);
   sigp1cls->SetBinContent(1633,-2.252182);
   sigp1cls->SetBinContent(1634,-2.254477);
   sigp1cls->SetBinContent(1635,-2.273297);
   sigp1cls->SetBinContent(1636,-2.352709);
   sigp1cls->SetBinContent(1658,-1.452455);
   sigp1cls->SetBinContent(1659,-1.311787);
   sigp1cls->SetBinContent(1660,-1.201389);
   sigp1cls->SetBinContent(1661,-1.090992);
   sigp1cls->SetBinContent(1662,-1.115085);
   sigp1cls->SetBinContent(1663,-1.213896);
   sigp1cls->SetBinContent(1664,-1.312707);
   sigp1cls->SetBinContent(1665,-1.411518);
   sigp1cls->SetBinContent(1666,-1.510329);
   sigp1cls->SetBinContent(1667,-1.647256);
   sigp1cls->SetBinContent(1668,-1.734217);
   sigp1cls->SetBinContent(1669,-1.843574);
   sigp1cls->SetBinContent(1670,-1.95586);
   sigp1cls->SetBinContent(1671,-2.068147);
   sigp1cls->SetBinContent(1672,-2.180434);
   sigp1cls->SetBinContent(1673,-2.26915);
   sigp1cls->SetBinContent(1674,-2.271445);
   sigp1cls->SetBinContent(1675,-2.273739);
   sigp1cls->SetBinContent(1676,-2.276034);
   sigp1cls->SetBinContent(1677,-2.278328);
   sigp1cls->SetBinContent(1678,-2.321385);
   sigp1cls->SetBinContent(1701,-1.398348);
   sigp1cls->SetBinContent(1702,-1.249425);
   sigp1cls->SetBinContent(1703,-1.119764);
   sigp1cls->SetBinContent(1704,-1.143858);
   sigp1cls->SetBinContent(1705,-1.242669);
   sigp1cls->SetBinContent(1706,-1.34148);
   sigp1cls->SetBinContent(1707,-1.440291);
   sigp1cls->SetBinContent(1708,-1.539101);
   sigp1cls->SetBinContent(1709,-1.648721);
   sigp1cls->SetBinContent(1710,-1.752844);
   sigp1cls->SetBinContent(1711,-1.865131);
   sigp1cls->SetBinContent(1712,-1.977417);
   sigp1cls->SetBinContent(1713,-2.089704);
   sigp1cls->SetBinContent(1714,-2.20199);
   sigp1cls->SetBinContent(1715,-2.290707);
   sigp1cls->SetBinContent(1716,-2.293001);
   sigp1cls->SetBinContent(1717,-2.295296);
   sigp1cls->SetBinContent(1718,-2.29759);
   sigp1cls->SetBinContent(1719,-2.299885);
   sigp1cls->SetBinContent(1720,-2.30218);
   sigp1cls->SetEntries(1600);
   sigp1cls->SetStats(0);
   sigp1cls->SetContour(1);
   sigp1cls->SetContourLevel(0,1.644854);

   //ci = TColor::GetColor("#00ff00");
   
   //sigp1cls->SetLineColor(kGreen+1);
   //sigp1cls->SetFillColor(kGreen+1);
   sigp1cls->SetLineColor(kBlue);
   sigp1cls->SetFillColor(kBlue);
   sigp1cls->SetFillStyle(3244);
   //sigp1cls->SetFillStyle(3002);
   sigp1cls->SetLineWidth(3);
   sigp1cls->SetMarkerStyle(21);
   sigp1cls->SetMarkerSize(0.3);

   
   return sigp1cls;
}

TH2F* Draw1TauLimit()
{
   TH2F *contour_obs = new TH2F("contour_obs1tau","contour_obs1tau",44,8,52,44,-0.4,52.4);
   contour_obs->SetBinContent(94,-6.432424);
   contour_obs->SetBinContent(95,-6.432424);
   contour_obs->SetBinContent(96,-4.647453);
   contour_obs->SetBinContent(97,-3.012663);
   contour_obs->SetBinContent(98,-1.377873);
   contour_obs->SetBinContent(99,0.2569167);
   contour_obs->SetBinContent(100,1.322334);
   contour_obs->SetBinContent(101,1.818377);
   contour_obs->SetBinContent(102,2.314421);
   contour_obs->SetBinContent(103,2.810465);
   contour_obs->SetBinContent(104,2.871982);
   contour_obs->SetBinContent(105,3.02776);
   contour_obs->SetBinContent(106,3.27859);
   contour_obs->SetBinContent(107,3.095683);
   contour_obs->SetBinContent(108,2.912776);
   contour_obs->SetBinContent(109,2.729869);
   contour_obs->SetBinContent(110,2.590707);
   contour_obs->SetBinContent(111,2.495291);
   contour_obs->SetBinContent(112,2.399875);
   contour_obs->SetBinContent(113,2.304458);
   contour_obs->SetBinContent(114,2.107912);
   contour_obs->SetBinContent(115,1.800362);
   contour_obs->SetBinContent(116,1.482837);
   contour_obs->SetBinContent(117,1.165213);
   contour_obs->SetBinContent(118,0.8475888);
   contour_obs->SetBinContent(119,0.5299645);
   contour_obs->SetBinContent(120,0.201166);
   contour_obs->SetBinContent(121,-0.1388069);
   contour_obs->SetBinContent(122,-0.4787797);
   contour_obs->SetBinContent(123,-0.8187525);
   contour_obs->SetBinContent(124,-1.159074);
   contour_obs->SetBinContent(140,-6.432424);
   contour_obs->SetBinContent(141,-6.432424);
   contour_obs->SetBinContent(142,-4.647453);
   contour_obs->SetBinContent(143,-3.012663);
   contour_obs->SetBinContent(144,-1.377873);
   contour_obs->SetBinContent(145,0.2569167);
   contour_obs->SetBinContent(146,1.322334);
   contour_obs->SetBinContent(147,1.818377);
   contour_obs->SetBinContent(148,2.314421);
   contour_obs->SetBinContent(149,2.810465);
   contour_obs->SetBinContent(150,2.871982);
   contour_obs->SetBinContent(151,3.02776);
   contour_obs->SetBinContent(152,3.27859);
   contour_obs->SetBinContent(153,3.095683);
   contour_obs->SetBinContent(154,2.912776);
   contour_obs->SetBinContent(155,2.729869);
   contour_obs->SetBinContent(156,2.590707);
   contour_obs->SetBinContent(157,2.495291);
   contour_obs->SetBinContent(158,2.399875);
   contour_obs->SetBinContent(159,2.304458);
   contour_obs->SetBinContent(160,2.107912);
   contour_obs->SetBinContent(161,1.800362);
   contour_obs->SetBinContent(162,1.482837);
   contour_obs->SetBinContent(163,1.165213);
   contour_obs->SetBinContent(164,0.8475888);
   contour_obs->SetBinContent(165,0.5299645);
   contour_obs->SetBinContent(166,0.201166);
   contour_obs->SetBinContent(167,-0.1388069);
   contour_obs->SetBinContent(168,-0.4787797);
   contour_obs->SetBinContent(169,-0.8187525);
   contour_obs->SetBinContent(170,-1.159074);
   contour_obs->SetBinContent(186,-6.432424);
   contour_obs->SetBinContent(187,-6.432424);
   contour_obs->SetBinContent(188,-4.497272);
   contour_obs->SetBinContent(189,-2.56212);
   contour_obs->SetBinContent(190,-0.7771497);
   contour_obs->SetBinContent(191,0.8576403);
   contour_obs->SetBinContent(192,1.923057);
   contour_obs->SetBinContent(193,2.419101);
   contour_obs->SetBinContent(194,2.480618);
   contour_obs->SetBinContent(195,2.107608);
   contour_obs->SetBinContent(196,1.734598);
   contour_obs->SetBinContent(197,1.890377);
   contour_obs->SetBinContent(198,2.574944);
   contour_obs->SetBinContent(199,3.259511);
   contour_obs->SetBinContent(200,3.510341);
   contour_obs->SetBinContent(201,3.327434);
   contour_obs->SetBinContent(202,3.188272);
   contour_obs->SetBinContent(203,3.092856);
   contour_obs->SetBinContent(204,2.89631);
   contour_obs->SetBinContent(205,2.598634);
   contour_obs->SetBinContent(206,2.300958);
   contour_obs->SetBinContent(207,1.993407);
   contour_obs->SetBinContent(208,1.675983);
   contour_obs->SetBinContent(209,1.358558);
   contour_obs->SetBinContent(210,1.041034);
   contour_obs->SetBinContent(211,0.7234092);
   contour_obs->SetBinContent(212,0.3946106);
   contour_obs->SetBinContent(213,0.05463783);
   contour_obs->SetBinContent(214,-0.2856838);
   contour_obs->SetBinContent(215,-0.6263543);
   contour_obs->SetBinContent(216,-0.9670248);
   contour_obs->SetBinContent(217,-1.22839);
   contour_obs->SetBinContent(232,-6.432424);
   contour_obs->SetBinContent(233,-6.432424);
   contour_obs->SetBinContent(234,-4.497272);
   contour_obs->SetBinContent(235,-2.56212);
   contour_obs->SetBinContent(236,-0.6269687);
   contour_obs->SetBinContent(237,1.308183);
   contour_obs->SetBinContent(238,2.089254);
   contour_obs->SetBinContent(239,1.716244);
   contour_obs->SetBinContent(240,1.343234);
   contour_obs->SetBinContent(241,0.9702241);
   contour_obs->SetBinContent(242,0.5972142);
   contour_obs->SetBinContent(243,0.7529928);
   contour_obs->SetBinContent(244,1.43756);
   contour_obs->SetBinContent(245,2.122127);
   contour_obs->SetBinContent(246,2.806694);
   contour_obs->SetBinContent(247,3.491261);
   contour_obs->SetBinContent(248,3.684707);
   contour_obs->SetBinContent(249,3.387031);
   contour_obs->SetBinContent(250,3.089355);
   contour_obs->SetBinContent(251,2.791679);
   contour_obs->SetBinContent(252,2.494003);
   contour_obs->SetBinContent(253,2.186453);
   contour_obs->SetBinContent(254,1.869028);
   contour_obs->SetBinContent(255,1.551604);
   contour_obs->SetBinContent(256,1.234179);
   contour_obs->SetBinContent(257,0.9167541);
   contour_obs->SetBinContent(258,0.5877065);
   contour_obs->SetBinContent(259,0.247036);
   contour_obs->SetBinContent(260,-0.09363444);
   contour_obs->SetBinContent(261,-0.4343049);
   contour_obs->SetBinContent(262,-0.7749754);
   contour_obs->SetBinContent(263,-1.036341);
   contour_obs->SetBinContent(264,-1.2184);
   contour_obs->SetBinContent(278,-6.432424);
   contour_obs->SetBinContent(279,-6.432424);
   contour_obs->SetBinContent(280,-4.497272);
   contour_obs->SetBinContent(281,-2.56212);
   contour_obs->SetBinContent(282,-0.6269687);
   contour_obs->SetBinContent(283,1.145976);
   contour_obs->SetBinContent(284,2.274244);
   contour_obs->SetBinContent(285,2.549516);
   contour_obs->SetBinContent(286,2.176506);
   contour_obs->SetBinContent(287,1.803496);
   contour_obs->SetBinContent(288,1.430486);
   contour_obs->SetBinContent(289,1.619576);
   contour_obs->SetBinContent(290,2.350778);
   contour_obs->SetBinContent(291,3.035345);
   contour_obs->SetBinContent(292,3.719912);
   contour_obs->SetBinContent(293,4.40448);
   contour_obs->SetBinContent(294,4.597925);
   contour_obs->SetBinContent(295,4.300249);
   contour_obs->SetBinContent(296,4.002573);
   contour_obs->SetBinContent(297,3.704897);
   contour_obs->SetBinContent(298,3.044424);
   contour_obs->SetBinContent(299,2.477733);
   contour_obs->SetBinContent(300,2.160308);
   contour_obs->SetBinContent(301,1.842883);
   contour_obs->SetBinContent(302,1.525459);
   contour_obs->SetBinContent(303,1.149637);
   contour_obs->SetBinContent(304,0.8045688);
   contour_obs->SetBinContent(305,0.4998671);
   contour_obs->SetBinContent(306,0.1591966);
   contour_obs->SetBinContent(307,-0.1814739);
   contour_obs->SetBinContent(308,-0.5221444);
   contour_obs->SetBinContent(309,-0.8088352);
   contour_obs->SetBinContent(310,-1.026351);
   contour_obs->SetBinContent(311,-1.208411);
   contour_obs->SetBinContent(324,-6.432424);
   contour_obs->SetBinContent(325,-6.432424);
   contour_obs->SetBinContent(326,-4.497272);
   contour_obs->SetBinContent(327,-2.56212);
   contour_obs->SetBinContent(328,-0.8355201);
   contour_obs->SetBinContent(329,0.8679078);
   contour_obs->SetBinContent(330,1.996175);
   contour_obs->SetBinContent(331,2.549282);
   contour_obs->SetBinContent(332,3.009778);
   contour_obs->SetBinContent(333,2.636768);
   contour_obs->SetBinContent(334,2.263758);
   contour_obs->SetBinContent(335,2.452847);
   contour_obs->SetBinContent(336,3.204036);
   contour_obs->SetBinContent(337,3.948563);
   contour_obs->SetBinContent(338,4.633131);
   contour_obs->SetBinContent(339,5.317698);
   contour_obs->SetBinContent(340,5.511143);
   contour_obs->SetBinContent(341,5.213468);
   contour_obs->SetBinContent(342,4.915792);
   contour_obs->SetBinContent(343,4.151662);
   contour_obs->SetBinContent(344,3.335704);
   contour_obs->SetBinContent(345,2.769013);
   contour_obs->SetBinContent(346,2.451588);
   contour_obs->SetBinContent(347,2.134163);
   contour_obs->SetBinContent(348,1.741656);
   contour_obs->SetBinContent(349,1.340807);
   contour_obs->SetBinContent(350,0.9957392);
   contour_obs->SetBinContent(351,0.7064525);
   contour_obs->SetBinContent(352,0.4120276);
   contour_obs->SetBinContent(353,0.07135712);
   contour_obs->SetBinContent(354,-0.2693134);
   contour_obs->SetBinContent(355,-0.5560042);
   contour_obs->SetBinContent(356,-0.7887153);
   contour_obs->SetBinContent(357,-1.016361);
   contour_obs->SetBinContent(358,-1.200578);
   contour_obs->SetBinContent(370,-6.432424);
   contour_obs->SetBinContent(371,-6.432424);
   contour_obs->SetBinContent(372,-4.520445);
   contour_obs->SetBinContent(373,-2.817017);
   contour_obs->SetBinContent(374,-1.113589);
   contour_obs->SetBinContent(375,0.5898393);
   contour_obs->SetBinContent(376,1.718107);
   contour_obs->SetBinContent(377,2.271214);
   contour_obs->SetBinContent(378,2.824321);
   contour_obs->SetBinContent(379,3.377428);
   contour_obs->SetBinContent(380,3.09703);
   contour_obs->SetBinContent(381,3.286119);
   contour_obs->SetBinContent(382,4.037308);
   contour_obs->SetBinContent(383,4.788497);
   contour_obs->SetBinContent(384,5.539687);
   contour_obs->SetBinContent(385,6.230916);
   contour_obs->SetBinContent(386,6.424362);
   contour_obs->SetBinContent(387,6.074857);
   contour_obs->SetBinContent(388,5.2589);
   contour_obs->SetBinContent(389,4.442942);
   contour_obs->SetBinContent(390,3.626984);
   contour_obs->SetBinContent(391,3.060292);
   contour_obs->SetBinContent(392,2.734525);
   contour_obs->SetBinContent(393,2.333676);
   contour_obs->SetBinContent(394,1.932827);
   contour_obs->SetBinContent(395,1.531977);
   contour_obs->SetBinContent(396,1.186909);
   contour_obs->SetBinContent(397,0.8976229);
   contour_obs->SetBinContent(398,0.6083363);
   contour_obs->SetBinContent(399,0.3190497);
   contour_obs->SetBinContent(400,-0.01648234);
   contour_obs->SetBinContent(401,-0.3031732);
   contour_obs->SetBinContent(402,-0.5358843);
   contour_obs->SetBinContent(403,-0.7685955);
   contour_obs->SetBinContent(404,-1.001307);
   contour_obs->SetBinContent(405,-1.194903);
   contour_obs->SetBinContent(416,-6.501941);
   contour_obs->SetBinContent(417,-6.501941);
   contour_obs->SetBinContent(418,-4.798513);
   contour_obs->SetBinContent(419,-3.095085);
   contour_obs->SetBinContent(420,-1.391657);
   contour_obs->SetBinContent(421,0.3117707);
   contour_obs->SetBinContent(422,1.440038);
   contour_obs->SetBinContent(423,1.993145);
   contour_obs->SetBinContent(424,2.546252);
   contour_obs->SetBinContent(425,3.099359);
   contour_obs->SetBinContent(426,3.652467);
   contour_obs->SetBinContent(427,4.119391);
   contour_obs->SetBinContent(428,4.87058);
   contour_obs->SetBinContent(429,5.621769);
   contour_obs->SetBinContent(430,6.372958);
   contour_obs->SetBinContent(431,7.124147);
   contour_obs->SetBinContent(432,7.182095);
   contour_obs->SetBinContent(433,6.366137);
   contour_obs->SetBinContent(434,5.550179);
   contour_obs->SetBinContent(435,4.734221);
   contour_obs->SetBinContent(436,3.918263);
   contour_obs->SetBinContent(437,3.326545);
   contour_obs->SetBinContent(438,2.925696);
   contour_obs->SetBinContent(439,2.524846);
   contour_obs->SetBinContent(440,2.123997);
   contour_obs->SetBinContent(441,1.723148);
   contour_obs->SetBinContent(442,1.37808);
   contour_obs->SetBinContent(443,1.088793);
   contour_obs->SetBinContent(444,0.7995067);
   contour_obs->SetBinContent(445,0.5102201);
   contour_obs->SetBinContent(446,0.2209335);
   contour_obs->SetBinContent(447,-0.05034213);
   contour_obs->SetBinContent(448,-0.2830533);
   contour_obs->SetBinContent(449,-0.5157644);
   contour_obs->SetBinContent(450,-0.7484756);
   contour_obs->SetBinContent(451,-0.9811867);
   contour_obs->SetBinContent(452,-1.189227);
   contour_obs->SetBinContent(462,-6.535715);
   contour_obs->SetBinContent(463,-6.535715);
   contour_obs->SetBinContent(464,-4.819715);
   contour_obs->SetBinContent(465,-3.116287);
   contour_obs->SetBinContent(466,-1.412859);
   contour_obs->SetBinContent(467,0.290569);
   contour_obs->SetBinContent(468,1.792804);
   contour_obs->SetBinContent(469,2.719879);
   contour_obs->SetBinContent(470,3.272986);
   contour_obs->SetBinContent(471,3.826093);
   contour_obs->SetBinContent(472,4.3792);
   contour_obs->SetBinContent(473,5.031348);
   contour_obs->SetBinContent(474,5.782537);
   contour_obs->SetBinContent(475,6.533726);
   contour_obs->SetBinContent(476,7.284915);
   contour_obs->SetBinContent(477,7.502059);
   contour_obs->SetBinContent(478,7.185157);
   contour_obs->SetBinContent(479,6.618728);
   contour_obs->SetBinContent(480,5.80277);
   contour_obs->SetBinContent(481,4.986812);
   contour_obs->SetBinContent(482,4.170854);
   contour_obs->SetBinContent(483,3.614895);
   contour_obs->SetBinContent(484,3.26649);
   contour_obs->SetBinContent(485,2.865641);
   contour_obs->SetBinContent(486,2.464791);
   contour_obs->SetBinContent(487,2.063942);
   contour_obs->SetBinContent(488,1.718874);
   contour_obs->SetBinContent(489,1.429588);
   contour_obs->SetBinContent(490,1.140301);
   contour_obs->SetBinContent(491,0.8510144);
   contour_obs->SetBinContent(492,0.5238864);
   contour_obs->SetBinContent(493,0.2250461);
   contour_obs->SetBinContent(494,-0.007665039);
   contour_obs->SetBinContent(495,-0.2403762);
   contour_obs->SetBinContent(496,-0.4730873);
   contour_obs->SetBinContent(497,-0.7542362);
   contour_obs->SetBinContent(498,-1.001462);
   contour_obs->SetBinContent(499,-1.183552);
   contour_obs->SetBinContent(508,-6.535715);
   contour_obs->SetBinContent(509,-6.535715);
   contour_obs->SetBinContent(510,-4.807144);
   contour_obs->SetBinContent(511,-3.086115);
   contour_obs->SetBinContent(512,-1.382687);
   contour_obs->SetBinContent(513,0.3207406);
   contour_obs->SetBinContent(514,1.822976);
   contour_obs->SetBinContent(515,3.124018);
   contour_obs->SetBinContent(516,4.20068);
   contour_obs->SetBinContent(517,4.753787);
   contour_obs->SetBinContent(518,5.306894);
   contour_obs->SetBinContent(519,5.959042);
   contour_obs->SetBinContent(520,6.710231);
   contour_obs->SetBinContent(521,7.46142);
   contour_obs->SetBinContent(522,7.464946);
   contour_obs->SetBinContent(523,7.148044);
   contour_obs->SetBinContent(524,6.831142);
   contour_obs->SetBinContent(525,6.514241);
   contour_obs->SetBinContent(526,6.047622);
   contour_obs->SetBinContent(527,5.231664);
   contour_obs->SetBinContent(528,4.415707);
   contour_obs->SetBinContent(529,3.859747);
   contour_obs->SetBinContent(530,3.563787);
   contour_obs->SetBinContent(531,3.23636);
   contour_obs->SetBinContent(532,2.83551);
   contour_obs->SetBinContent(533,2.434661);
   contour_obs->SetBinContent(534,2.089593);
   contour_obs->SetBinContent(535,1.800307);
   contour_obs->SetBinContent(536,1.51102);
   contour_obs->SetBinContent(537,1.168756);
   contour_obs->SetBinContent(538,0.8037861);
   contour_obs->SetBinContent(539,0.5049458);
   contour_obs->SetBinContent(540,0.2722346);
   contour_obs->SetBinContent(541,0.0395235);
   contour_obs->SetBinContent(542,-0.2610005);
   contour_obs->SetBinContent(543,-0.5905872);
   contour_obs->SetBinContent(544,-0.8378125);
   contour_obs->SetBinContent(545,-1.002677);
   contour_obs->SetBinContent(546,-1.177876);
   contour_obs->SetBinContent(554,-6.535715);
   contour_obs->SetBinContent(555,-6.535715);
   contour_obs->SetBinContent(556,-4.807144);
   contour_obs->SetBinContent(557,-3.078573);
   contour_obs->SetBinContent(558,-1.352516);
   contour_obs->SetBinContent(559,0.3509122);
   contour_obs->SetBinContent(560,1.853147);
   contour_obs->SetBinContent(561,3.15419);
   contour_obs->SetBinContent(562,4.455232);
   contour_obs->SetBinContent(563,5.681481);
   contour_obs->SetBinContent(564,6.234588);
   contour_obs->SetBinContent(565,6.886736);
   contour_obs->SetBinContent(566,7.637925);
   contour_obs->SetBinContent(567,7.427832);
   contour_obs->SetBinContent(568,7.11093);
   contour_obs->SetBinContent(569,6.794029);
   contour_obs->SetBinContent(570,6.477128);
   contour_obs->SetBinContent(571,6.160226);
   contour_obs->SetBinContent(572,5.843324);
   contour_obs->SetBinContent(573,5.476517);
   contour_obs->SetBinContent(574,4.660559);
   contour_obs->SetBinContent(575,4.1046);
   contour_obs->SetBinContent(576,3.808639);
   contour_obs->SetBinContent(577,3.512679);
   contour_obs->SetBinContent(578,3.206229);
   contour_obs->SetBinContent(579,2.80538);
   contour_obs->SetBinContent(580,2.460312);
   contour_obs->SetBinContent(581,2.171026);
   contour_obs->SetBinContent(582,1.813625);
   contour_obs->SetBinContent(583,1.448655);
   contour_obs->SetBinContent(584,1.083686);
   contour_obs->SetBinContent(585,0.7848455);
   contour_obs->SetBinContent(586,0.5521343);
   contour_obs->SetBinContent(587,0.2322352);
   contour_obs->SetBinContent(588,-0.0973515);
   contour_obs->SetBinContent(589,-0.4269382);
   contour_obs->SetBinContent(590,-0.6741635);
   contour_obs->SetBinContent(591,-0.8390275);
   contour_obs->SetBinContent(592,-1.003892);
   contour_obs->SetBinContent(593,-1.172201);
   contour_obs->SetBinContent(600,-6.535715);
   contour_obs->SetBinContent(601,-6.535715);
   contour_obs->SetBinContent(602,-4.807144);
   contour_obs->SetBinContent(603,-3.078573);
   contour_obs->SetBinContent(604,-1.350001);
   contour_obs->SetBinContent(605,0.3785696);
   contour_obs->SetBinContent(606,1.883319);
   contour_obs->SetBinContent(607,3.184361);
   contour_obs->SetBinContent(608,4.485404);
   contour_obs->SetBinContent(609,5.786446);
   contour_obs->SetBinContent(610,7.087488);
   contour_obs->SetBinContent(611,7.707621);
   contour_obs->SetBinContent(612,7.390719);
   contour_obs->SetBinContent(613,7.073817);
   contour_obs->SetBinContent(614,6.756916);
   contour_obs->SetBinContent(615,6.440014);
   contour_obs->SetBinContent(616,6.123112);
   contour_obs->SetBinContent(617,5.806211);
   contour_obs->SetBinContent(618,5.489309);
   contour_obs->SetBinContent(619,5.172408);
   contour_obs->SetBinContent(620,4.855506);
   contour_obs->SetBinContent(621,4.349452);
   contour_obs->SetBinContent(622,4.053492);
   contour_obs->SetBinContent(623,3.757531);
   contour_obs->SetBinContent(624,3.461571);
   contour_obs->SetBinContent(625,3.165611);
   contour_obs->SetBinContent(626,2.823463);
   contour_obs->SetBinContent(627,2.458494);
   contour_obs->SetBinContent(628,2.093524);
   contour_obs->SetBinContent(629,1.728555);
   contour_obs->SetBinContent(630,1.363585);
   contour_obs->SetBinContent(631,1.055058);
   contour_obs->SetBinContent(632,0.7254709);
   contour_obs->SetBinContent(633,0.3958842);
   contour_obs->SetBinContent(634,0.06629753);
   contour_obs->SetBinContent(635,-0.2632892);
   contour_obs->SetBinContent(636,-0.5105145);
   contour_obs->SetBinContent(637,-0.6753785);
   contour_obs->SetBinContent(638,-0.8402425);
   contour_obs->SetBinContent(639,-1.005106);
   contour_obs->SetBinContent(640,-1.169971);
   contour_obs->SetBinContent(641,-1.169971);
   contour_obs->SetBinContent(646,-5.911989);
   contour_obs->SetBinContent(647,-5.911989);
   contour_obs->SetBinContent(648,-4.183418);
   contour_obs->SetBinContent(649,-2.454847);
   contour_obs->SetBinContent(650,-0.7262758);
   contour_obs->SetBinContent(651,1.002295);
   contour_obs->SetBinContent(652,2.272336);
   contour_obs->SetBinContent(653,3.573378);
   contour_obs->SetBinContent(654,4.87442);
   contour_obs->SetBinContent(655,6.175462);
   contour_obs->SetBinContent(656,7.334352);
   contour_obs->SetBinContent(657,7.735408);
   contour_obs->SetBinContent(658,7.71032);
   contour_obs->SetBinContent(659,7.422599);
   contour_obs->SetBinContent(660,7.105698);
   contour_obs->SetBinContent(661,6.788796);
   contour_obs->SetBinContent(662,6.471895);
   contour_obs->SetBinContent(663,6.154993);
   contour_obs->SetBinContent(664,5.838091);
   contour_obs->SetBinContent(665,5.52119);
   contour_obs->SetBinContent(666,5.204288);
   contour_obs->SetBinContent(667,4.897857);
   contour_obs->SetBinContent(668,4.601896);
   contour_obs->SetBinContent(669,4.305936);
   contour_obs->SetBinContent(670,4.009975);
   contour_obs->SetBinContent(671,3.548473);
   contour_obs->SetBinContent(672,2.979815);
   contour_obs->SetBinContent(673,2.637472);
   contour_obs->SetBinContent(674,2.272503);
   contour_obs->SetBinContent(675,1.907533);
   contour_obs->SetBinContent(676,1.542564);
   contour_obs->SetBinContent(677,1.211544);
   contour_obs->SetBinContent(678,0.8917126);
   contour_obs->SetBinContent(679,0.5621259);
   contour_obs->SetBinContent(680,0.2325393);
   contour_obs->SetBinContent(681,-0.09704744);
   contour_obs->SetBinContent(682,-0.3442728);
   contour_obs->SetBinContent(683,-0.5091368);
   contour_obs->SetBinContent(684,-0.6740008);
   contour_obs->SetBinContent(685,-0.8388648);
   contour_obs->SetBinContent(686,-1.02161);
   contour_obs->SetBinContent(687,-1.02161);
   contour_obs->SetBinContent(692,-5.366229);
   contour_obs->SetBinContent(693,-5.366229);
   contour_obs->SetBinContent(694,-3.247829);
   contour_obs->SetBinContent(695,-1.519258);
   contour_obs->SetBinContent(696,0.2093126);
   contour_obs->SetBinContent(697,1.631926);
   contour_obs->SetBinContent(698,2.840774);
   contour_obs->SetBinContent(699,4.141817);
   contour_obs->SetBinContent(700,5.442859);
   contour_obs->SetBinContent(701,6.50698);
   contour_obs->SetBinContent(702,7.334181);
   contour_obs->SetBinContent(703,7.735237);
   contour_obs->SetBinContent(704,7.710149);
   contour_obs->SetBinContent(705,7.685061);
   contour_obs->SetBinContent(706,7.659972);
   contour_obs->SetBinContent(707,7.488977);
   contour_obs->SetBinContent(708,7.172075);
   contour_obs->SetBinContent(709,6.855174);
   contour_obs->SetBinContent(710,6.538272);
   contour_obs->SetBinContent(711,6.22137);
   contour_obs->SetBinContent(712,5.904469);
   contour_obs->SetBinContent(713,5.598038);
   contour_obs->SetBinContent(714,5.302077);
   contour_obs->SetBinContent(715,5.006117);
   contour_obs->SetBinContent(716,4.434253);
   contour_obs->SetBinContent(717,3.586486);
   contour_obs->SetBinContent(718,3.017829);
   contour_obs->SetBinContent(719,2.72828);
   contour_obs->SetBinContent(720,2.401021);
   contour_obs->SetBinContent(721,2.036052);
   contour_obs->SetBinContent(722,1.671082);
   contour_obs->SetBinContent(723,1.340062);
   contour_obs->SetBinContent(724,1.042992);
   contour_obs->SetBinContent(725,0.729664);
   contour_obs->SetBinContent(726,0.4000773);
   contour_obs->SetBinContent(727,0.07049063);
   contour_obs->SetBinContent(728,-0.1767347);
   contour_obs->SetBinContent(729,-0.3415987);
   contour_obs->SetBinContent(730,-0.5064627);
   contour_obs->SetBinContent(731,-0.701129);
   contour_obs->SetBinContent(732,-0.9255974);
   contour_obs->SetBinContent(733,-0.9255974);
   contour_obs->SetBinContent(738,-5.366229);
   contour_obs->SetBinContent(739,-5.366229);
   contour_obs->SetBinContent(740,-2.312241);
   contour_obs->SetBinContent(741,-0.58367);
   contour_obs->SetBinContent(742,1.083709);
   contour_obs->SetBinContent(743,2.200364);
   contour_obs->SetBinContent(744,3.409213);
   contour_obs->SetBinContent(745,4.710255);
   contour_obs->SetBinContent(746,5.679608);
   contour_obs->SetBinContent(747,6.506809);
   contour_obs->SetBinContent(748,7.33401);
   contour_obs->SetBinContent(749,7.735066);
   contour_obs->SetBinContent(750,7.709978);
   contour_obs->SetBinContent(751,7.684889);
   contour_obs->SetBinContent(752,7.659801);
   contour_obs->SetBinContent(753,7.634713);
   contour_obs->SetBinContent(754,7.609624);
   contour_obs->SetBinContent(755,7.555355);
   contour_obs->SetBinContent(756,7.238453);
   contour_obs->SetBinContent(757,6.921551);
   contour_obs->SetBinContent(758,6.60465);
   contour_obs->SetBinContent(759,6.298219);
   contour_obs->SetBinContent(760,6.002258);
   contour_obs->SetBinContent(761,5.320033);
   contour_obs->SetBinContent(762,4.472266);
   contour_obs->SetBinContent(763,3.624499);
   contour_obs->SetBinContent(764,3.055842);
   contour_obs->SetBinContent(765,2.766293);
   contour_obs->SetBinContent(766,2.476744);
   contour_obs->SetBinContent(767,2.164569);
   contour_obs->SetBinContent(768,1.7996);
   contour_obs->SetBinContent(769,1.46858);
   contour_obs->SetBinContent(770,1.17151);
   contour_obs->SetBinContent(771,0.8744404);
   contour_obs->SetBinContent(772,0.5676154);
   contour_obs->SetBinContent(773,0.2380287);
   contour_obs->SetBinContent(774,-0.009196648);
   contour_obs->SetBinContent(775,-0.1740606);
   contour_obs->SetBinContent(776,-0.3806478);
   contour_obs->SetBinContent(777,-0.6051162);
   contour_obs->SetBinContent(778,-0.8295847);
   contour_obs->SetBinContent(779,-0.8295847);
   contour_obs->SetBinContent(784,-5.366229);
   contour_obs->SetBinContent(785,-5.366229);
   contour_obs->SetBinContent(786,-1.376652);
   contour_obs->SetBinContent(787,0.3519185);
   contour_obs->SetBinContent(788,1.652148);
   contour_obs->SetBinContent(789,2.768803);
   contour_obs->SetBinContent(790,3.977652);
   contour_obs->SetBinContent(791,4.852237);
   contour_obs->SetBinContent(792,5.679438);
   contour_obs->SetBinContent(793,6.506638);
   contour_obs->SetBinContent(794,7.333839);
   contour_obs->SetBinContent(795,7.734895);
   contour_obs->SetBinContent(796,7.709806);
   contour_obs->SetBinContent(797,7.684718);
   contour_obs->SetBinContent(798,7.65963);
   contour_obs->SetBinContent(799,7.634542);
   contour_obs->SetBinContent(800,7.609453);
   contour_obs->SetBinContent(801,7.584365);
   contour_obs->SetBinContent(802,7.559277);
   contour_obs->SetBinContent(803,7.534188);
   contour_obs->SetBinContent(804,7.304831);
   contour_obs->SetBinContent(805,6.998399);
   contour_obs->SetBinContent(806,6.205813);
   contour_obs->SetBinContent(807,5.358046);
   contour_obs->SetBinContent(808,4.510279);
   contour_obs->SetBinContent(809,3.662513);
   contour_obs->SetBinContent(810,3.093855);
   contour_obs->SetBinContent(811,2.804306);
   contour_obs->SetBinContent(812,2.514757);
   contour_obs->SetBinContent(813,2.225209);
   contour_obs->SetBinContent(814,1.928118);
   contour_obs->SetBinContent(815,1.597098);
   contour_obs->SetBinContent(816,1.300028);
   contour_obs->SetBinContent(817,1.002958);
   contour_obs->SetBinContent(818,0.7058884);
   contour_obs->SetBinContent(819,0.4055668);
   contour_obs->SetBinContent(820,0.1583414);
   contour_obs->SetBinContent(821,-0.06016661);
   contour_obs->SetBinContent(822,-0.2846351);
   contour_obs->SetBinContent(823,-0.5091035);
   contour_obs->SetBinContent(824,-0.7335721);
   contour_obs->SetBinContent(825,-0.7335721);
   contour_obs->SetBinContent(830,-5.366229);
   contour_obs->SetBinContent(831,-5.366229);
   contour_obs->SetBinContent(832,-1.298687);
   contour_obs->SetBinContent(833,1.103932);
   contour_obs->SetBinContent(834,2.311108);
   contour_obs->SetBinContent(835,3.729498);
   contour_obs->SetBinContent(836,4.852294);
   contour_obs->SetBinContent(837,5.679494);
   contour_obs->SetBinContent(838,6.506695);
   contour_obs->SetBinContent(839,7.333896);
   contour_obs->SetBinContent(840,7.747456);
   contour_obs->SetBinContent(841,7.73487);
   contour_obs->SetBinContent(842,7.709782);
   contour_obs->SetBinContent(843,7.684694);
   contour_obs->SetBinContent(844,7.659606);
   contour_obs->SetBinContent(845,7.634517);
   contour_obs->SetBinContent(846,7.609429);
   contour_obs->SetBinContent(847,7.58434);
   contour_obs->SetBinContent(848,7.559252);
   contour_obs->SetBinContent(849,7.534163);
   contour_obs->SetBinContent(850,7.511754);
   contour_obs->SetBinContent(851,7.102997);
   contour_obs->SetBinContent(852,6.260015);
   contour_obs->SetBinContent(853,5.412248);
   contour_obs->SetBinContent(854,4.564481);
   contour_obs->SetBinContent(855,3.716714);
   contour_obs->SetBinContent(856,3.148056);
   contour_obs->SetBinContent(857,2.858508);
   contour_obs->SetBinContent(858,2.568959);
   contour_obs->SetBinContent(859,2.27941);
   contour_obs->SetBinContent(860,1.976076);
   contour_obs->SetBinContent(861,1.672529);
   contour_obs->SetBinContent(862,1.387197);
   contour_obs->SetBinContent(863,1.090127);
   contour_obs->SetBinContent(864,0.7930573);
   contour_obs->SetBinContent(865,0.4959873);
   contour_obs->SetBinContent(866,0.2352181);
   contour_obs->SetBinContent(867,0.01074961);
   contour_obs->SetBinContent(868,-0.2137189);
   contour_obs->SetBinContent(869,-0.4381874);
   contour_obs->SetBinContent(870,-0.6636959);
   contour_obs->SetBinContent(871,-0.6636959);
   contour_obs->SetBinContent(878,-4.370387);
   contour_obs->SetBinContent(879,0.6929976);
   contour_obs->SetBinContent(880,3.965794);
   contour_obs->SetBinContent(881,5.384185);
   contour_obs->SetBinContent(882,6.50698);
   contour_obs->SetBinContent(883,7.334181);
   contour_obs->SetBinContent(884,7.747741);
   contour_obs->SetBinContent(885,7.747659);
   contour_obs->SetBinContent(886,7.747578);
   contour_obs->SetBinContent(887,7.734993);
   contour_obs->SetBinContent(888,7.709904);
   contour_obs->SetBinContent(889,7.684816);
   contour_obs->SetBinContent(890,7.659728);
   contour_obs->SetBinContent(891,7.634639);
   contour_obs->SetBinContent(892,7.609551);
   contour_obs->SetBinContent(893,7.584463);
   contour_obs->SetBinContent(894,7.55991);
   contour_obs->SetBinContent(895,7.542321);
   contour_obs->SetBinContent(896,7.524733);
   contour_obs->SetBinContent(897,7.115976);
   contour_obs->SetBinContent(898,6.316052);
   contour_obs->SetBinContent(899,5.482637);
   contour_obs->SetBinContent(900,4.634871);
   contour_obs->SetBinContent(901,3.787104);
   contour_obs->SetBinContent(902,3.218446);
   contour_obs->SetBinContent(903,2.928897);
   contour_obs->SetBinContent(904,2.639349);
   contour_obs->SetBinContent(905,2.308443);
   contour_obs->SetBinContent(906,1.881036);
   contour_obs->SetBinContent(907,1.577489);
   contour_obs->SetBinContent(908,1.397802);
   contour_obs->SetBinContent(909,1.135947);
   contour_obs->SetBinContent(910,0.838877);
   contour_obs->SetBinContent(911,0.5418071);
   contour_obs->SetBinContent(912,0.2810378);
   contour_obs->SetBinContent(913,0.05656934);
   contour_obs->SetBinContent(914,-0.1678991);
   contour_obs->SetBinContent(915,-0.395488);
   contour_obs->SetBinContent(916,-0.6303577);
   contour_obs->SetBinContent(917,-0.6303577);
   contour_obs->SetBinContent(925,-6.294257);
   contour_obs->SetBinContent(926,-1.340773);
   contour_obs->SetBinContent(927,4.718453);
   contour_obs->SetBinContent(928,7.748026);
   contour_obs->SetBinContent(929,7.747944);
   contour_obs->SetBinContent(930,7.747863);
   contour_obs->SetBinContent(931,7.747781);
   contour_obs->SetBinContent(932,7.7477);
   contour_obs->SetBinContent(933,7.735115);
   contour_obs->SetBinContent(934,7.710027);
   contour_obs->SetBinContent(935,7.684938);
   contour_obs->SetBinContent(936,7.65985);
   contour_obs->SetBinContent(937,7.634761);
   contour_obs->SetBinContent(938,7.609673);
   contour_obs->SetBinContent(939,7.590477);
   contour_obs->SetBinContent(940,7.572889);
   contour_obs->SetBinContent(941,7.5553);
   contour_obs->SetBinContent(942,7.537712);
   contour_obs->SetBinContent(943,7.128955);
   contour_obs->SetBinContent(944,6.329031);
   contour_obs->SetBinContent(945,5.529106);
   contour_obs->SetBinContent(946,4.705261);
   contour_obs->SetBinContent(947,3.857494);
   contour_obs->SetBinContent(948,3.288836);
   contour_obs->SetBinContent(949,2.999287);
   contour_obs->SetBinContent(950,2.64081);
   contour_obs->SetBinContent(951,2.213403);
   contour_obs->SetBinContent(952,1.785997);
   contour_obs->SetBinContent(953,1.48245);
   contour_obs->SetBinContent(954,1.302763);
   contour_obs->SetBinContent(955,1.123075);
   contour_obs->SetBinContent(956,0.8846967);
   contour_obs->SetBinContent(957,0.5876268);
   contour_obs->SetBinContent(958,0.3268576);
   contour_obs->SetBinContent(959,0.1023891);
   contour_obs->SetBinContent(960,-0.12728);
   contour_obs->SetBinContent(961,-0.3621497);
   contour_obs->SetBinContent(962,-0.5970195);
   contour_obs->SetBinContent(963,-0.5970195);
   contour_obs->SetBinContent(973,-3.865892);
   contour_obs->SetBinContent(974,1.68884);
   contour_obs->SetBinContent(975,7.748066);
   contour_obs->SetBinContent(976,7.747985);
   contour_obs->SetBinContent(977,7.747903);
   contour_obs->SetBinContent(978,7.747822);
   contour_obs->SetBinContent(979,7.735237);
   contour_obs->SetBinContent(980,7.710149);
   contour_obs->SetBinContent(981,7.685061);
   contour_obs->SetBinContent(982,7.659972);
   contour_obs->SetBinContent(983,7.638634);
   contour_obs->SetBinContent(984,7.621045);
   contour_obs->SetBinContent(985,7.603456);
   contour_obs->SetBinContent(986,7.585868);
   contour_obs->SetBinContent(987,7.568279);
   contour_obs->SetBinContent(988,7.550691);
   contour_obs->SetBinContent(989,7.141934);
   contour_obs->SetBinContent(990,6.34201);
   contour_obs->SetBinContent(991,5.542085);
   contour_obs->SetBinContent(992,4.742161);
   contour_obs->SetBinContent(993,3.927884);
   contour_obs->SetBinContent(994,3.359226);
   contour_obs->SetBinContent(995,2.973177);
   contour_obs->SetBinContent(996,2.54577);
   contour_obs->SetBinContent(997,2.118364);
   contour_obs->SetBinContent(998,1.690958);
   contour_obs->SetBinContent(999,1.387411);
   contour_obs->SetBinContent(1000,1.207723);
   contour_obs->SetBinContent(1001,1.028036);
   contour_obs->SetBinContent(1002,0.8483487);
   contour_obs->SetBinContent(1003,0.6334465);
   contour_obs->SetBinContent(1004,0.3726773);
   contour_obs->SetBinContent(1005,0.1409279);
   contour_obs->SetBinContent(1006,-0.0939418);
   contour_obs->SetBinContent(1007,-0.3288115);
   contour_obs->SetBinContent(1008,-0.5636812);
   contour_obs->SetBinContent(1009,-0.5636812);
   contour_obs->SetBinContent(1020,-4.967365);
   contour_obs->SetBinContent(1021,-0.8362792);
   contour_obs->SetBinContent(1022,4.718453);
   contour_obs->SetBinContent(1023,7.748026);
   contour_obs->SetBinContent(1024,7.747944);
   contour_obs->SetBinContent(1025,7.735359);
   contour_obs->SetBinContent(1026,7.710271);
   contour_obs->SetBinContent(1027,7.68679);
   contour_obs->SetBinContent(1028,7.669201);
   contour_obs->SetBinContent(1029,7.651613);
   contour_obs->SetBinContent(1030,7.634024);
   contour_obs->SetBinContent(1031,7.616436);
   contour_obs->SetBinContent(1032,7.598847);
   contour_obs->SetBinContent(1033,7.581259);
   contour_obs->SetBinContent(1034,7.56367);
   contour_obs->SetBinContent(1035,7.154913);
   contour_obs->SetBinContent(1036,6.354989);
   contour_obs->SetBinContent(1037,5.555065);
   contour_obs->SetBinContent(1038,4.75514);
   contour_obs->SetBinContent(1039,3.955215);
   contour_obs->SetBinContent(1040,3.399206);
   contour_obs->SetBinContent(1041,2.9718);
   contour_obs->SetBinContent(1042,2.544394);
   contour_obs->SetBinContent(1043,2.116987);
   contour_obs->SetBinContent(1044,1.689581);
   contour_obs->SetBinContent(1045,1.386034);
   contour_obs->SetBinContent(1046,1.206347);
   contour_obs->SetBinContent(1047,1.026659);
   contour_obs->SetBinContent(1048,0.8469718);
   contour_obs->SetBinContent(1049,0.6672844);
   contour_obs->SetBinContent(1050,0.4091359);
   contour_obs->SetBinContent(1051,0.1742662);
   contour_obs->SetBinContent(1052,-0.06060357);
   contour_obs->SetBinContent(1053,-0.2954733);
   contour_obs->SetBinContent(1054,-0.5303431);
   contour_obs->SetBinContent(1055,-0.5303431);
   contour_obs->SetBinContent(1068,-3.260499);
   contour_obs->SetBinContent(1069,2.193334);
   contour_obs->SetBinContent(1070,7.748066);
   contour_obs->SetBinContent(1071,7.735482);
   contour_obs->SetBinContent(1072,7.717357);
   contour_obs->SetBinContent(1073,7.699769);
   contour_obs->SetBinContent(1074,7.68218);
   contour_obs->SetBinContent(1075,7.664592);
   contour_obs->SetBinContent(1076,7.647003);
   contour_obs->SetBinContent(1077,7.629415);
   contour_obs->SetBinContent(1078,7.611826);
   contour_obs->SetBinContent(1079,7.594238);
   contour_obs->SetBinContent(1080,7.576649);
   contour_obs->SetBinContent(1081,7.167892);
   contour_obs->SetBinContent(1082,6.367968);
   contour_obs->SetBinContent(1083,5.568044);
   contour_obs->SetBinContent(1084,4.769551);
   contour_obs->SetBinContent(1085,3.983948);
   contour_obs->SetBinContent(1086,3.442353);
   contour_obs->SetBinContent(1087,3.144766);
   contour_obs->SetBinContent(1088,2.730341);
   contour_obs->SetBinContent(1089,2.302935);
   contour_obs->SetBinContent(1090,1.875529);
   contour_obs->SetBinContent(1091,1.571982);
   contour_obs->SetBinContent(1092,1.392295);
   contour_obs->SetBinContent(1093,1.212607);
   contour_obs->SetBinContent(1094,1.023316);
   contour_obs->SetBinContent(1095,0.7475921);
   contour_obs->SetBinContent(1096,0.4767261);
   contour_obs->SetBinContent(1097,0.2107182);
   contour_obs->SetBinContent(1098,-0.02726534);
   contour_obs->SetBinContent(1099,-0.2621351);
   contour_obs->SetBinContent(1100,-0.4970048);
   contour_obs->SetBinContent(1101,-0.4970048);
   contour_obs->SetBinContent(1115,-3.640473);
   contour_obs->SetBinContent(1116,-0.2308861);
   contour_obs->SetBinContent(1117,5.222948);
   contour_obs->SetBinContent(1118,7.469672);
   contour_obs->SetBinContent(1119,7.67551);
   contour_obs->SetBinContent(1120,7.695159);
   contour_obs->SetBinContent(1121,7.677571);
   contour_obs->SetBinContent(1122,7.659982);
   contour_obs->SetBinContent(1123,7.642394);
   contour_obs->SetBinContent(1124,7.624805);
   contour_obs->SetBinContent(1125,7.607217);
   contour_obs->SetBinContent(1126,7.589628);
   contour_obs->SetBinContent(1127,7.180872);
   contour_obs->SetBinContent(1128,6.380947);
   contour_obs->SetBinContent(1129,5.585319);
   contour_obs->SetBinContent(1130,4.799716);
   contour_obs->SetBinContent(1131,4.014113);
   contour_obs->SetBinContent(1132,3.472518);
   contour_obs->SetBinContent(1133,3.174931);
   contour_obs->SetBinContent(1134,2.877344);
   contour_obs->SetBinContent(1135,2.488883);
   contour_obs->SetBinContent(1136,2.061477);
   contour_obs->SetBinContent(1137,1.75793);
   contour_obs->SetBinContent(1138,1.578242);
   contour_obs->SetBinContent(1139,1.369744);
   contour_obs->SetBinContent(1140,1.09402);
   contour_obs->SetBinContent(1141,0.8182961);
   contour_obs->SetBinContent(1142,0.5474302);
   contour_obs->SetBinContent(1143,0.2814223);
   contour_obs->SetBinContent(1144,0.01541435);
   contour_obs->SetBinContent(1145,-0.2287968);
   contour_obs->SetBinContent(1146,-0.4636666);
   contour_obs->SetBinContent(1147,-0.4636666);
   contour_obs->SetBinContent(1163,-2.053857);
   contour_obs->SetBinContent(1164,2.798727);
   contour_obs->SetBinContent(1165,6.794784);
   contour_obs->SetBinContent(1166,7.000622);
   contour_obs->SetBinContent(1167,7.20646);
   contour_obs->SetBinContent(1168,7.412297);
   contour_obs->SetBinContent(1169,7.618135);
   contour_obs->SetBinContent(1170,7.637784);
   contour_obs->SetBinContent(1171,7.620196);
   contour_obs->SetBinContent(1172,7.602607);
   contour_obs->SetBinContent(1173,7.193851);
   contour_obs->SetBinContent(1174,6.401087);
   contour_obs->SetBinContent(1175,5.615484);
   contour_obs->SetBinContent(1176,4.829881);
   contour_obs->SetBinContent(1177,4.044278);
   contour_obs->SetBinContent(1178,3.502683);
   contour_obs->SetBinContent(1179,3.205096);
   contour_obs->SetBinContent(1180,2.907509);
   contour_obs->SetBinContent(1181,2.609921);
   contour_obs->SetBinContent(1182,2.247425);
   contour_obs->SetBinContent(1183,1.943878);
   contour_obs->SetBinContent(1184,1.716172);
   contour_obs->SetBinContent(1185,1.440448);
   contour_obs->SetBinContent(1186,1.164724);
   contour_obs->SetBinContent(1187,0.8890002);
   contour_obs->SetBinContent(1188,0.6181343);
   contour_obs->SetBinContent(1189,0.3521264);
   contour_obs->SetBinContent(1190,0.08611842);
   contour_obs->SetBinContent(1191,-0.1798895);
   contour_obs->SetBinContent(1192,-0.4303283);
   contour_obs->SetBinContent(1193,-0.4303283);
   contour_obs->SetBinContent(1210,-2.313581);
   contour_obs->SetBinContent(1211,0.374507);
   contour_obs->SetBinContent(1212,5.828341);
   contour_obs->SetBinContent(1213,6.325734);
   contour_obs->SetBinContent(1214,6.531571);
   contour_obs->SetBinContent(1215,6.737409);
   contour_obs->SetBinContent(1216,6.943247);
   contour_obs->SetBinContent(1217,7.149085);
   contour_obs->SetBinContent(1218,7.354922);
   contour_obs->SetBinContent(1219,7.234111);
   contour_obs->SetBinContent(1220,6.448508);
   contour_obs->SetBinContent(1221,5.662905);
   contour_obs->SetBinContent(1222,4.877302);
   contour_obs->SetBinContent(1223,4.091699);
   contour_obs->SetBinContent(1224,3.550104);
   contour_obs->SetBinContent(1225,3.252517);
   contour_obs->SetBinContent(1226,2.95493);
   contour_obs->SetBinContent(1227,2.657343);
   contour_obs->SetBinContent(1228,2.359755);
   contour_obs->SetBinContent(1229,2.055943);
   contour_obs->SetBinContent(1230,1.780219);
   contour_obs->SetBinContent(1231,1.504495);
   contour_obs->SetBinContent(1232,1.228771);
   contour_obs->SetBinContent(1233,0.9530467);
   contour_obs->SetBinContent(1234,0.6821808);
   contour_obs->SetBinContent(1235,0.4161729);
   contour_obs->SetBinContent(1236,0.1501649);
   contour_obs->SetBinContent(1237,-0.115843);
   contour_obs->SetBinContent(1238,-0.3818509);
   contour_obs->SetBinContent(1239,-0.3818509);
   contour_obs->SetBinContent(1257,-2.573305);
   contour_obs->SetBinContent(1258,-0.7269655);
   contour_obs->SetBinContent(1259,3.40412);
   contour_obs->SetBinContent(1260,5.650846);
   contour_obs->SetBinContent(1261,5.856683);
   contour_obs->SetBinContent(1262,6.062521);
   contour_obs->SetBinContent(1263,6.268359);
   contour_obs->SetBinContent(1264,6.474196);
   contour_obs->SetBinContent(1265,6.606992);
   contour_obs->SetBinContent(1266,6.582211);
   contour_obs->SetBinContent(1267,5.796607);
   contour_obs->SetBinContent(1268,5.011005);
   contour_obs->SetBinContent(1269,4.225402);
   contour_obs->SetBinContent(1270,3.683807);
   contour_obs->SetBinContent(1271,3.38622);
   contour_obs->SetBinContent(1272,3.088632);
   contour_obs->SetBinContent(1273,2.791045);
   contour_obs->SetBinContent(1274,2.446249);
   contour_obs->SetBinContent(1275,2.1167);
   contour_obs->SetBinContent(1276,1.810977);
   contour_obs->SetBinContent(1277,1.535253);
   contour_obs->SetBinContent(1278,1.259529);
   contour_obs->SetBinContent(1279,0.9838054);
   contour_obs->SetBinContent(1280,0.7129394);
   contour_obs->SetBinContent(1281,0.4469315);
   contour_obs->SetBinContent(1282,0.1809236);
   contour_obs->SetBinContent(1283,-0.08508433);
   contour_obs->SetBinContent(1284,-0.320843);
   contour_obs->SetBinContent(1285,-0.320843);
   contour_obs->SetBinContent(1305,-0.9866894);
   contour_obs->SetBinContent(1306,0.9799001);
   contour_obs->SetBinContent(1307,4.975957);
   contour_obs->SetBinContent(1308,5.181795);
   contour_obs->SetBinContent(1309,5.387632);
   contour_obs->SetBinContent(1310,5.59347);
   contour_obs->SetBinContent(1311,5.726266);
   contour_obs->SetBinContent(1312,5.78602);
   contour_obs->SetBinContent(1313,5.845775);
   contour_obs->SetBinContent(1314,5.144707);
   contour_obs->SetBinContent(1315,4.359104);
   contour_obs->SetBinContent(1316,3.817509);
   contour_obs->SetBinContent(1317,3.519922);
   contour_obs->SetBinContent(1318,3.217089);
   contour_obs->SetBinContent(1319,2.867047);
   contour_obs->SetBinContent(1320,2.517005);
   contour_obs->SetBinContent(1321,2.187457);
   contour_obs->SetBinContent(1322,1.878401);
   contour_obs->SetBinContent(1323,1.569345);
   contour_obs->SetBinContent(1324,1.290288);
   contour_obs->SetBinContent(1325,1.014564);
   contour_obs->SetBinContent(1326,0.7436981);
   contour_obs->SetBinContent(1327,0.4776902);
   contour_obs->SetBinContent(1328,0.2150433);
   contour_obs->SetBinContent(1329,-0.01735435);
   contour_obs->SetBinContent(1330,-0.249752);
   contour_obs->SetBinContent(1331,-0.249752);
   contour_obs->SetBinContent(1352,-1.246413);
   contour_obs->SetBinContent(1353,0.5999264);
   contour_obs->SetBinContent(1354,4.009513);
   contour_obs->SetBinContent(1355,4.506907);
   contour_obs->SetBinContent(1356,4.712744);
   contour_obs->SetBinContent(1357,4.84554);
   contour_obs->SetBinContent(1358,4.905294);
   contour_obs->SetBinContent(1359,4.965048);
   contour_obs->SetBinContent(1360,5.024803);
   contour_obs->SetBinContent(1361,4.492806);
   contour_obs->SetBinContent(1362,3.951212);
   contour_obs->SetBinContent(1363,3.637888);
   contour_obs->SetBinContent(1364,3.287846);
   contour_obs->SetBinContent(1365,2.937804);
   contour_obs->SetBinContent(1366,2.587762);
   contour_obs->SetBinContent(1367,2.258213);
   contour_obs->SetBinContent(1368,1.949158);
   contour_obs->SetBinContent(1369,1.640102);
   contour_obs->SetBinContent(1370,1.331046);
   contour_obs->SetBinContent(1371,1.045323);
   contour_obs->SetBinContent(1372,0.7744568);
   contour_obs->SetBinContent(1373,0.518532);
   contour_obs->SetBinContent(1374,0.2861343);
   contour_obs->SetBinContent(1375,0.05373666);
   contour_obs->SetBinContent(1376,-0.178661);
   contour_obs->SetBinContent(1377,-0.178661);
   contour_obs->SetBinContent(1400,0.3402024);
   contour_obs->SetBinContent(1401,2.186542);
   contour_obs->SetBinContent(1402,3.832018);
   contour_obs->SetBinContent(1403,3.964814);
   contour_obs->SetBinContent(1404,4.024568);
   contour_obs->SetBinContent(1405,4.084322);
   contour_obs->SetBinContent(1406,4.144076);
   contour_obs->SetBinContent(1407,4.203831);
   contour_obs->SetBinContent(1408,4.058687);
   contour_obs->SetBinContent(1409,3.708645);
   contour_obs->SetBinContent(1410,3.358603);
   contour_obs->SetBinContent(1411,3.008561);
   contour_obs->SetBinContent(1412,2.658519);
   contour_obs->SetBinContent(1413,2.32897);
   contour_obs->SetBinContent(1414,2.019914);
   contour_obs->SetBinContent(1415,1.710859);
   contour_obs->SetBinContent(1416,1.401803);
   contour_obs->SetBinContent(1417,1.092747);
   contour_obs->SetBinContent(1418,0.8220206);
   contour_obs->SetBinContent(1419,0.589623);
   contour_obs->SetBinContent(1420,0.3572253);
   contour_obs->SetBinContent(1421,0.1248277);
   contour_obs->SetBinContent(1422,-0.10757);
   contour_obs->SetBinContent(1423,-0.10757);
   contour_obs->SetBinContent(1447,0.08047837);
   contour_obs->SetBinContent(1448,1.926818);
   contour_obs->SetBinContent(1449,3.235357);
   contour_obs->SetBinContent(1450,3.395956);
   contour_obs->SetBinContent(1451,3.556556);
   contour_obs->SetBinContent(1452,3.717156);
   contour_obs->SetBinContent(1453,3.877755);
   contour_obs->SetBinContent(1454,3.811902);
   contour_obs->SetBinContent(1455,3.519595);
   contour_obs->SetBinContent(1456,3.227288);
   contour_obs->SetBinContent(1457,2.93498);
   contour_obs->SetBinContent(1458,2.642673);
   contour_obs->SetBinContent(1459,2.388013);
   contour_obs->SetBinContent(1460,2.071148);
   contour_obs->SetBinContent(1461,1.754283);
   contour_obs->SetBinContent(1462,1.437418);
   contour_obs->SetBinContent(1463,1.120553);
   contour_obs->SetBinContent(1464,0.865584);
   contour_obs->SetBinContent(1465,0.660714);
   contour_obs->SetBinContent(1466,0.4283163);
   contour_obs->SetBinContent(1467,0.1959187);
   contour_obs->SetBinContent(1468,-0.03647896);
   contour_obs->SetBinContent(1469,-0.03647896);
   contour_obs->SetBinContent(1495,1.667094);
   contour_obs->SetBinContent(1496,3.047968);
   contour_obs->SetBinContent(1497,3.280904);
   contour_obs->SetBinContent(1498,3.441503);
   contour_obs->SetBinContent(1499,3.602103);
   contour_obs->SetBinContent(1500,3.536249);
   contour_obs->SetBinContent(1501,3.243942);
   contour_obs->SetBinContent(1502,2.951635);
   contour_obs->SetBinContent(1503,2.705238);
   contour_obs->SetBinContent(1504,2.596572);
   contour_obs->SetBinContent(1505,2.391837);
   contour_obs->SetBinContent(1506,2.091033);
   contour_obs->SetBinContent(1507,1.778184);
   contour_obs->SetBinContent(1508,1.461319);
   contour_obs->SetBinContent(1509,1.144454);
   contour_obs->SetBinContent(1510,0.8894848);
   contour_obs->SetBinContent(1511,0.6964123);
   contour_obs->SetBinContent(1512,0.4994074);
   contour_obs->SetBinContent(1513,0.2670097);
   contour_obs->SetBinContent(1514,0.03461205);
   contour_obs->SetBinContent(1515,0.03461205);
   contour_obs->SetBinContent(1542,1.40737);
   contour_obs->SetBinContent(1543,2.788244);
   contour_obs->SetBinContent(1544,3.165851);
   contour_obs->SetBinContent(1545,3.326451);
   contour_obs->SetBinContent(1546,3.260597);
   contour_obs->SetBinContent(1547,2.96829);
   contour_obs->SetBinContent(1548,2.813713);
   contour_obs->SetBinContent(1549,2.705047);
   contour_obs->SetBinContent(1550,2.59638);
   contour_obs->SetBinContent(1551,2.391645);
   contour_obs->SetBinContent(1552,2.090842);
   contour_obs->SetBinContent(1553,1.790038);
   contour_obs->SetBinContent(1554,1.485219);
   contour_obs->SetBinContent(1555,1.168354);
   contour_obs->SetBinContent(1556,0.9133857);
   contour_obs->SetBinContent(1557,0.7203132);
   contour_obs->SetBinContent(1558,0.5272407);
   contour_obs->SetBinContent(1559,0.3341682);
   contour_obs->SetBinContent(1560,0.1057031);
   contour_obs->SetBinContent(1561,0.1057031);
   contour_obs->SetBinContent(1589,1.147646);
   contour_obs->SetBinContent(1590,2.52852);
   contour_obs->SetBinContent(1591,2.978463);
   contour_obs->SetBinContent(1592,3.030855);
   contour_obs->SetBinContent(1593,2.922189);
   contour_obs->SetBinContent(1594,2.813522);
   contour_obs->SetBinContent(1595,2.704856);
   contour_obs->SetBinContent(1596,2.596189);
   contour_obs->SetBinContent(1597,2.391454);
   contour_obs->SetBinContent(1598,2.090651);
   contour_obs->SetBinContent(1599,1.789847);
   contour_obs->SetBinContent(1600,1.489043);
   contour_obs->SetBinContent(1601,1.18824);
   contour_obs->SetBinContent(1602,0.9372865);
   contour_obs->SetBinContent(1603,0.744214);
   contour_obs->SetBinContent(1604,0.5511415);
   contour_obs->SetBinContent(1605,0.358069);
   contour_obs->SetBinContent(1606,0.1649965);
   contour_obs->SetBinContent(1607,0.1649965);
   contour_obs->SetBinContent(1637,2.268796);
   contour_obs->SetBinContent(1638,2.439434);
   contour_obs->SetBinContent(1639,2.330768);
   contour_obs->SetBinContent(1640,2.222101);
   contour_obs->SetBinContent(1641,2.295711);
   contour_obs->SetBinContent(1642,2.369321);
   contour_obs->SetBinContent(1643,2.255725);
   contour_obs->SetBinContent(1644,1.954921);
   contour_obs->SetBinContent(1645,1.654117);
   contour_obs->SetBinContent(1646,1.353314);
   contour_obs->SetBinContent(1647,1.092976);
   contour_obs->SetBinContent(1648,1.001545);
   contour_obs->SetBinContent(1649,0.8084729);
   contour_obs->SetBinContent(1650,0.6154004);
   contour_obs->SetBinContent(1651,0.4223279);
   contour_obs->SetBinContent(1652,0.2292554);
   contour_obs->SetBinContent(1653,0.2292554);
   contour_obs->SetBinContent(1684,1.912044);
   contour_obs->SetBinContent(1685,1.985654);
   contour_obs->SetBinContent(1686,2.059264);
   contour_obs->SetBinContent(1687,2.132874);
   contour_obs->SetBinContent(1688,2.206484);
   contour_obs->SetBinContent(1689,2.092888);
   contour_obs->SetBinContent(1690,1.792084);
   contour_obs->SetBinContent(1691,1.49128);
   contour_obs->SetBinContent(1692,1.230942);
   contour_obs->SetBinContent(1693,1.051534);
   contour_obs->SetBinContent(1694,0.9601041);
   contour_obs->SetBinContent(1695,0.8808033);
   contour_obs->SetBinContent(1696,0.6877308);
   contour_obs->SetBinContent(1697,0.4946583);
   contour_obs->SetBinContent(1698,0.3015858);
   contour_obs->SetBinContent(1699,0.3015858);
   contour_obs->SetBinContent(1732,1.896427);
   contour_obs->SetBinContent(1733,1.970037);
   contour_obs->SetBinContent(1734,2.043647);
   contour_obs->SetBinContent(1735,1.93005);
   contour_obs->SetBinContent(1736,1.629247);
   contour_obs->SetBinContent(1737,1.368909);
   contour_obs->SetBinContent(1738,1.189501);
   contour_obs->SetBinContent(1739,1.010093);
   contour_obs->SetBinContent(1740,0.9186628);
   contour_obs->SetBinContent(1741,0.9152098);
   contour_obs->SetBinContent(1742,0.7600612);
   contour_obs->SetBinContent(1743,0.5669887);
   contour_obs->SetBinContent(1744,0.3739162);
   contour_obs->SetBinContent(1745,0.3739162);
   contour_obs->SetBinContent(1779,1.8072);
   contour_obs->SetBinContent(1780,1.88081);
   contour_obs->SetBinContent(1781,1.767213);
   contour_obs->SetBinContent(1782,1.506875);
   contour_obs->SetBinContent(1783,1.327467);
   contour_obs->SetBinContent(1784,1.14806);
   contour_obs->SetBinContent(1785,0.968652);
   contour_obs->SetBinContent(1786,0.8772216);
   contour_obs->SetBinContent(1787,0.8737686);
   contour_obs->SetBinContent(1788,0.8323917);
   contour_obs->SetBinContent(1789,0.6393192);
   contour_obs->SetBinContent(1790,0.4462467);
   contour_obs->SetBinContent(1791,0.4462467);
   contour_obs->SetBinContent(1827,1.644841);
   contour_obs->SetBinContent(1828,1.465434);
   contour_obs->SetBinContent(1829,1.286026);
   contour_obs->SetBinContent(1830,1.106618);
   contour_obs->SetBinContent(1831,0.9272107);
   contour_obs->SetBinContent(1832,0.8357803);
   contour_obs->SetBinContent(1833,0.8323273);
   contour_obs->SetBinContent(1834,0.8288743);
   contour_obs->SetBinContent(1835,0.7116496);
   contour_obs->SetBinContent(1836,0.5185771);
   contour_obs->SetBinContent(1837,0.5185771);
   contour_obs->SetBinContent(1874,1.423993);
   contour_obs->SetBinContent(1875,1.244585);
   contour_obs->SetBinContent(1876,1.065177);
   contour_obs->SetBinContent(1877,0.8857694);
   contour_obs->SetBinContent(1878,0.7943391);
   contour_obs->SetBinContent(1879,0.790886);
   contour_obs->SetBinContent(1880,0.787433);
   contour_obs->SetBinContent(1881,0.78398);
   contour_obs->SetBinContent(1882,0.5909075);
   contour_obs->SetBinContent(1883,0.5909075);
   contour_obs->SetBinContent(1922,1.023736);
   contour_obs->SetBinContent(1923,0.8443282);
   contour_obs->SetBinContent(1924,0.7528978);
   contour_obs->SetBinContent(1925,0.7494448);
   contour_obs->SetBinContent(1926,0.7459918);
   contour_obs->SetBinContent(1927,0.7425388);
   contour_obs->SetBinContent(1928,0.663238);
   contour_obs->SetBinContent(1929,0.663238);
   contour_obs->SetBinContent(1969,0.8028869);
   contour_obs->SetBinContent(1970,0.7114565);
   contour_obs->SetBinContent(1971,0.7080035);
   contour_obs->SetBinContent(1972,0.7045505);
   contour_obs->SetBinContent(1973,0.7010975);
   contour_obs->SetBinContent(1974,0.6976445);
   contour_obs->SetBinContent(1975,0.6976445);
   contour_obs->SetBinContent(2015,0.8028869);
   contour_obs->SetBinContent(2016,0.7114565);
   contour_obs->SetBinContent(2017,0.7080035);
   contour_obs->SetBinContent(2018,0.7045505);
   contour_obs->SetBinContent(2019,0.7010975);
   contour_obs->SetBinContent(2020,0.6976445);
   contour_obs->SetBinContent(2021,0.6976445);
   contour_obs->SetEntries(1936);
   contour_obs->SetContour(1);
   contour_obs->SetContourLevel(0,1.644854);

   
   contour_obs->SetLineColor(TColor::GetColor("#ff0000"));
   contour_obs->SetLineWidth(4);

   return contour_obs;
}

TGraph* Draw2TauLimit()
{
  TFile* f_ditau=TFile::Open("exclusioncontours_tau2.root");
  TGraph* contour_obs=(TGraph*) f_ditau->Get("obsExcl");


   return contour_obs;
}




void DrawCaptions( double x, double y, TString caption){

  TLatex* l = new TLatex(x,y,caption);
  l->SetTextAlign(23);
  l->SetTextSize(0.02);
  l->SetTextAngle(90);
  //  l->SetTextColor(kGray+3);
  l->SetTextColor(14);

  l->Draw();

  return;
}
