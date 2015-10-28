#include "CombinationGlob.C"
#include "TColor.h"
#include <TFile.h>
#include <TTree.h>
#include <Riostream.h>
//#include "zleptonoffciallcontours.C"
#include <algorithm>
#include "summary_harvest_tree_description.h"
#include "contourmacros/GetSRName.C"

TH2F* Draw1fbLimit();

void PlotFunc3Par(double p0, double p1,double p2,double p3,double xmin,double xmax);
void PlotFunc4Par(double p0, double p1,double p2,double p3,double p4,double xmin,double xmax);

void SUSY_gtt_all_witobs_merged( TString fname1 = "m0m12_nofloat_exp.root",
        TString fname2 = "m0m12_nofloat_exp.root", 
        TString fname3 = "m0m12_nofloat_exp.root", 
        const char* prefix="",
        float& lumi = 20.3,
        bool showsig = true,
        int discexcl = 1,
        TString ullistfile = "Merged_Output_hypotest_SM_SS_twostepCN_sleptons_SR4_combined_ul__1_harvest_list",
        int showtevatron = 0,
        TString plottitle = "0-lepton combined",
        bool showSR = true,
        bool useShape = false,
        TString hname0 = "sigp1clsf", //"sigCLs",
        TString hname0_exp = "sigp1expclsf",//"sigCLsexp",
        TString hname0_1su = "sigclsu1s",//"sigCLsexp1su",
        TString hname0_1sd = "sigclsd1s",//"sigCLsexp1sd",
        TString hname1 = "sigp0",
        TString hname1_exp = "sigp0",
        TString fnameMass= "mSugraGridtanbeta10_gluinoSquarkMasses.root"
        )
{

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

    //TFile *f10 = TFile::Open("Outputs/truth.Gluino_Stop_charm.dM10_combined_fixSigXSecNominal__1_harvest_list.root"); 
    //TFile *f11 = TFile::Open("Outputs/truth.Gluino_Stop_charm.dM50_combined_fixSigXSecNominal__1_harvest_list.root");

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

    //TH2F *hist10 = (TH2F*) f10->Get(hname0_exp);
    //TH2F *hist11 = (TH2F*) f11->Get(hname0_exp);
    //hist10->SetDirectory(0);
    //hist11->SetDirectory(0);

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

    //f10->Close();
    //f11->Close();

    TH2F* contour          = FixAndSetBorders( *hist0,         "contour",             "contour",          0 );
    TH2F* contour_obs_unc  = FixAndSetBorders( *hist1_unc,     "contour_obs_unc",     "contour_obs_unc",  0 );
    TH2F* contour_exp_all  = FixAndSetBorders( *hist0_all,     "contour_exp_unc",     "contour_exp_unc",  0 );
    //   TH2F* contour_isr_up  = FixAndSetBorders( *hist_isrup,     "contour_isr_up",     "contour_isr_up",  0 );
    //   TH2F* contour_isr_down  = FixAndSetBorders( *hist_isrdown,     "contour_isr_down",     "contour_isr_down",  0 );
    TH2F* contour_obs      = FixAndSetBorders( *hist1,         "contour_obs",         "contour_obs",      0 );
    
    //TH2F* contour10          = FixAndSetBorders( *hist10,         "contour10",             "contour10",          0 );
    //TH2F* contour11          = FixAndSetBorders( *hist11,         "contour11",             "contour11",          0 );

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

    double xmin=475;
    gr = (TGraph*) ContourGraph( hist0_1su ,xmin,1400);
    if(gr) gr_contour_1su   = (TGraph*) gr->Clone();

    gr = (TGraph*) ContourGraph( hist0_1sd ,xmin,1400);
    if(gr) gr_contour_1sd   = (TGraph*) gr->Clone();

    gr = (TGraph*) ContourGraph( hist1_unc ,xmin,1400);
    if(gr) gr_contour_obs_unc   = (TGraph*) gr->Clone();

    gr = (TGraph*) ContourGraph( hist0 ,xmin,1400);
    if(gr) gr_contour   = (TGraph*) gr->Clone();

    gr = (TGraph*) ContourGraph( hist0_all ,xmin,1400);
    if(gr) gr_contour_exp_all   = (TGraph*) gr->Clone();

    gr = (TGraph*) ContourGraph( hist1 ,xmin,1400);
    if(gr) gr_contour_obs   = (TGraph*) gr->Clone();
    //   TGraph* gr_contour_isr_up       = ContourGraph( hist_isrup )->Clone();
    //   TGraph* gr_contour_isr_down       = ContourGraph( hist_isrdown )->Clone();

    //cout << gr_contour_1su->GetName() << " : "<< gr_contour_1su->GetN() <<  " : " << gr_contour_1sd->GetName() << " : " << gr_contour_1sd->GetN() << endl;
    
    //TGraph* gr_contour10;
    //TGraph* gr_contour11;
    
    //gr = (TGraph*) ContourGraph( hist10 ,xmin,1400);
    //if(gr) gr_contour10   = (TGraph*) gr->Clone();
    
    //gr = (TGraph*) ContourGraph( hist11 ,xmin,1400);
    //if(gr) gr_contour11   = (TGraph*) gr->Clone();

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
    frame = new TH2F("frame", "m_{0} vs m_{12} - ATLAS", 19, 325, 1420, 24, 120, 1000/*1200.*/ );
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

    frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
    frame->SetYTitle( "m_{#tilde{t}} [GeV]" );

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

    const int nsig(3);
    //TH2F *chist[3];
    // draw contours
    //!instead of printing sigma in 68% 95% 98% levels now printing +1 sigma deviations 
    //for (Int_t nsigma=1; nsigma<=nsig; nsigma++)
    //  DrawContourSameColor( contour, nsigma, "blue", kFALSE, (nsigma==1?inverse:0) ) ;

    double  legy=0.66;

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

    std::cout << "xmin=" << xmin << std::endl;


    double xminLine =  xmin;
    double xmaxLine = xmax; // ymax + 2*175;
    double yminLine = xmin - 175;
    double ymaxLine = xmax - 175; //ymax; 

    if(ymaxLine > ymax){
        ymaxLine = ymax;
        xmaxLine = ymaxLine + 175;
    }

    //TLine lineExcl = TLine(475,125,975,625);

    TLine lineExcl = TLine(xminLine,yminLine,xmaxLine,ymaxLine);
    lineExcl.SetLineStyle(3);
    lineExcl.SetLineWidth(1);
    lineExcl.SetLineColor(14);
    if (!fname1.Contains("gridX"))
        lineExcl.Draw("same");

    TLatex gtt = TLatex(510,350,"#tilde{g}#rightarrow #tilde{t}t forbidden");
    gtt.SetTextSize(0.025);
    gtt.SetTextColor(14);
    gtt.SetTextAngle(90- atan2(ymax-ymin, xmax-xmin) * 180/TMath::Pi() ); 
    gtt.SetTextFont(42);
    gtt.Draw("same");

    Int_t c_myYellow   = TColor::GetColor("#ffe938"); // TColor::GetColor( "#fee000" )
    Int_t c_myRed      = TColor::GetColor("#aa000");
    Int_t c_myExp      = TColor::GetColor("#28373c");

    if(gr_contour_1su && gr_contour_1sd)
        TGraph* grshadeExp = DrawExpectedBand( gr_contour_1su,      gr_contour_1sd,   c_myYellow , 1001   , 400)->Clone();

    // --->
    if (contour!=0 && discexcl==1)
    {

        //DrawContourLine95( leg, contour_obs,     "Observed limit (#pm1 #sigma^{SUSY}_{theory})", c_myRed, 1, 4 );   // 95% CL_{S}
        //DrawContourLine95( leg, contour_exp_all, "", c_myRed, 3, 2 );    // Observed limit #pm 1 #sigma^{SUSY}_{theory}

        DrawContourLine95( leg, contour,         "", c_myExp, 6, 2 ); 
        //DrawContourLine95( leg, contour_obs_unc, "", c_myRed, 3, 2 );      
        DummyLegendExpected(leg, "Expected limit (#pm1 #sigma_{exp})", c_myYellow, 1001, c_myExp, 6, 2);
    }

    //DrawContourLine95( leg, contour10,         "#DeltaM = 10 GeV", c_myRed, 3, 2 ); 
    //DrawContourLine95( leg, contour11,         "#DeltaM = 50 GeV", 4, 2, 2 ); 
    
    // no reference for this LEP limit... --GJ, 24/4/2013
    //TBox *LEPbox = new TBox(325, 0, 1420, 100);
    //LEPbox->SetLineWidth(0);
    //LEPbox->SetFillColor(kBlue-9);
    //LEPbox->SetFillStyle(1001);
    //LEPbox->Draw();

    //TLine *LEPlimit = new TLine(325, 100, 1420, 100);
    ////LEPlimit->SetLineColor(kBlue-10);
    //LEPlimit->SetLineColor(kBlue-4);
    //LEPlimit->SetLineWidth(3);
    //LEPlimit->Draw();
  
    //leg->AddEntry(LEPlimit,"LEP exclusion","l"); 

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
    TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025, "#tilde{g}-#tilde{g} production, #tilde{g}#rightarrow #tilde{t}t #rightarrow ct#tilde{#chi}^{0}_{1}" );
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
    Leg1->DrawLatex(0.19, 0.79, "#int L dt = 20.3 fb^{-1}, #sqrt{s}=8 TeV");	
    Leg1->DrawLatex(0.19, 0.74, plottitle);
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

    TLatex clslimits = TLatex(/*755,503,au fost 533,475*/1120,940,"All limits at 95% CL_{S}");
    clslimits.SetTextSize(0.025);
    clslimits.SetTextFont(42);
    clslimits.Draw("same");

    TLatex* atlasLabel = new TLatex();
    atlasLabel->SetNDC();
    atlasLabel->SetTextFont(72);
    atlasLabel->SetTextColor(ROOT::kBlack);
    atlasLabel->SetTextSize( 0.05 );

    atlasLabel->DrawLatex(0.19, 0.85,"ATLAS");
    atlasLabel->AppendPad();

    TLatex* progressLabel = new TLatex();
    progressLabel->SetNDC();
    progressLabel->SetTextFont(42);
    progressLabel->SetTextColor(ROOT::kBlack);
    progressLabel->SetTextSize( 0.05 );
    progressLabel->DrawLatex(0.35, 0.85,"Internal");
    //progressLabel->DrawLatex(0.35, 0.85,"Preliminary");
    progressLabel->AppendPad();
    
    leg->Draw("same");

    ////// observed limit -> arrange the lines in a stupid way
    ////[>565 in loc de 578 si 591 -> 604<]
    //TLine obsPOneSigma = TLine(396,753,473,753); //used to be 633/655; width should be 51, height diff with low 22
    //obsPOneSigma.SetLineStyle(3);
    //obsPOneSigma.SetLineWidth(2);
    //obsPOneSigma.SetLineColor(c_myRed);
    //obsPOneSigma.Draw("same");

    //TLine obsMOneSigma = TLine(396,725,473,725);
    //obsMOneSigma.SetLineStyle(3);
    //obsMOneSigma.SetLineWidth(2);
    //obsMOneSigma.SetLineColor(c_myRed);
    //obsMOneSigma.Draw("same");

    //draw upper limit x-sections
    TCanvas *c2= (TCanvas *)c->Clone("upperlimit");
    Show_UL(fname1, c2, xmin, xmax, ymin, ymax, false);

    if(showSR){
        std::cout << "--- printing best SRs" << std::endl;
        Show_SR(fname1, c, xmin, xmax, ymin, ymax, useShape);
    } 

    // update the canvas
    c->Update();

    // create plots
    // store histograms to output file
    TObjArray* arr = fname1.Tokenize("/");
    TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
    TString outfile = objstring->GetString().ReplaceAll(".root","");
    delete arr;

    TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%dinvpb_",lumi);
    if(c2) {
        cout << outfile.Data() << endl;
        cout << c2 << endl;
        CombinationGlob::imgconv( c2, Form("plots/UpperLimit_%s",outfile.Data()) );
    }
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
    gr = (TGraph*)gr0->Clone(TString::Format("gr_%s", h->GetName()));

    cout << "==> Will dumb histogram: " << h->GetName() << " into a graph" <<endl;

    h->SetContour( 1 );
    //h->GetXaxis()->SetRangeUser(250,1200);
    h->GetXaxis()->SetRangeUser(xmin, xmax);
    //h->GetYaxis()->SetRangeUser(2,50);

    double pval = CombinationGlob::cl_percent[1];
    std::cout << pval << std::endl; 
    double signif = TMath::NormQuantile(1-pval);
    h->SetContourLevel( 0, signif );
    h->Draw("CONT LIST");
    h->SetDirectory(0);
    gPad->Update();


    TObjArray *contours = gROOT->GetListOfSpecials()->FindObject("contours");
    Int_t ncontours     = contours->GetSize();
    cout << "Found " << ncontours << " contours " << endl;

    TList *list = (TList*)contours->At(0);
    contours->Print("v");
    if(!list) return NULL;

    gr = (TGraph*)list->First();
    if(!gr) return NULL;

    gr->SetName(TString::Format("gr_%s", hist->GetName()));
    //gr->SetName(hist->GetName());
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

void Show_SR(TString oredList,  TCanvas *can, float xlow, float xhigh, float ylow, float yhigh, bool useShape)
{
    can->cd();

    TLatex lat;
    //lat.SetTextAlign( 11 );
    lat.SetTextSize( 0.0265 );
    lat.SetTextColor( 12 );
    lat.SetTextFont( 42 );

    cout << "Draw signal region labels." << endl;
    gROOT->ProcessLine(".L summary_harvest_tree_description.h+");
    gSystem->Load("libSusyFitter.so");

    TString txtfile=oredList;
    txtfile.ReplaceAll(".root","");

    TTree* tree = harvesttree( txtfile!=0 ? txtfile : 0 );
    if (tree==0) { 
        cout << "Cannot open list file. Exit." << endl;
        return;
    }

    Float_t fID;
    Float_t m0; 
    Float_t m12; 

    TBranch *b_m0;
    TBranch *b_m12;
    TBranch *b_fID;

    tree->SetBranchAddress("m0", &m0, &b_m0);
    tree->SetBranchAddress("m12", &m12, &b_m12);
    tree->SetBranchAddress("fID",  &fID,  &b_fID);

    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
        tree->GetEntry( i );
        cout << "i=" << i << "\t" << m0 << " " << m12 << " " << fID << endl;

        //if (fID > 0)
        //x= (m2-m3)/(m1-m3);
        //cout << "  At m(squark/gluino) = " << m1<< ", x = " << x<< ", fID = " <<  fID<< endl;
        // be 10% outside the edges
        if( (m0 > (xhigh-xlow)/30.0 + xlow) &&
                (m0 < xhigh - (xhigh-xlow)/30.0) &&
                (m12 > (yhigh-ylow)/30.0 + ylow) &&
                (m12 < yhigh - (yhigh-ylow)/30.0)) {

            TString mySR = GetSRName(fID, useShape);
            lat.DrawLatex(m0, m12, mySR.Data());
        }
    }
    
}

void Show_UL(TString oredList, TCanvas *can,float xlow,float
        xhigh,float ylow,float yhigh, bool acceff) {

    Int_t c_myRed      = TColor::GetColor("#aa000");
    can->cd();
    
    ///////
    TLatex lat;
    //lat.SetTextAlign( 11 );
    lat.SetTextSize( 0.0225 );
    lat.SetTextColor( 12 );
    lat.SetTextFont( 42 );

    cout << "Draw signal region labels." << endl;
    gROOT->ProcessLine(".L summary_harvest_tree_description.h+");
    gSystem->Load("libSusyFitter.so");

    TString txtfile=oredList;
    txtfile.ReplaceAll(".root","");

    TTree* tree = harvesttree( txtfile!=0 ? txtfile : 0 );
    if (tree==0) { 
        cout << "Cannot open list file. Exit." << endl;
        return;
    }

    Float_t fID;
    Float_t m0; 
    Float_t m12; 
    Float_t UL;
    Float_t xsec; // x-section

    TBranch *b_m0;
    TBranch *b_m12;
    TBranch *b_fID;
    TBranch *b_UL; // upper limit
    TBranch *b_xsec; // x-section

    tree->SetBranchAddress("m0", &m0, &b_m0);
    tree->SetBranchAddress("m12", &m12, &b_m12);
    tree->SetBranchAddress("fID",  &fID,  &b_fID);
    tree->SetBranchAddress("expectedUpperLimit",  &UL,  &b_UL);
    tree->SetBranchAddress("xsec", &xsec, &b_xsec);Float_t x;
    TString ULstring;
    char buffer[20];

    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
        tree->GetEntry( i );
        cout << m0 << " " << m12 << " " << fID << endl;
        
        if(acceff) sprintf(buffer,"%.1f",UL*xsec);
        else {
            if(UL*xsec<100.) sprintf(buffer,"%.1f",UL*xsec);
            else sprintf(buffer,"%.0f",UL*xsec);
        }
        ULstring=buffer;
        cout << "  At x = " << m0 << ", y = " << m12 << ", UL = " <<  UL << ", ULstring= " << ULstring << endl;

        // be 10% outside the edges
        if( (m0 > (xhigh-xlow)/30.0 + xlow) &&
                (m0 < xhigh - (xhigh-xlow)/30.0) &&
                (m12 > (yhigh-ylow)/30.0 + ylow) &&
                (m12 < yhigh - (yhigh-ylow)/30.0)) {
            
            lat.DrawLatex(m0, m12, ULstring.Data());
        }

    }

    if(acceff) LegendTitle="Numbers give 95% CL_{s} excluded   #sigma*Acc*eff [fb]" ;
    else LegendTitle="Numbers give 95% CL_{s} excluded cross section x BR [fb]" ;
    TLatex *Leg0 = new TLatex( xhigh+44, ylow+0.00*(yhigh-ylow), LegendTitle);
    Leg0->SetTextAngle(90);;
    Leg0->SetTextFont( 42 );
    Leg0->SetTextSize( 0.98*CombinationGlob::DescriptionTextSize);
    Leg0->SetTextColor( 1 );
    Leg0->AppendPad();

}

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

    return;

} 

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
