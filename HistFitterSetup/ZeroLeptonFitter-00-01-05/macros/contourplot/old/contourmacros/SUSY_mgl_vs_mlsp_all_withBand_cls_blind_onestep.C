//vim: ts=4 sw=4

#include "contourmacros/CombinationGlob.C"
#include "TColor.h"
#include "TMarker.h"
#include <algorithm>
#include <fstream>
#include "contourmacros/SimplifiedModels_7TeV.C"
#include "contourmacros/GetSRName.C"
#include <stdio.h>

void SUSY_mgl_vs_mlsp_all_withBand_cls_blind_onestep( TString& fname0 = "mudat_list.root",// nominal
        TString fname1 = "",               // Up
        TString fname2 = "",               // Down  
        TString fname3 = "", // external expection
        const char* prefix="test",
        const float& lumi = 21,
        bool showsig = true,
        bool show7TeVlimits = true,
        int discexcl = 1,
        int showOneSigmaExpBand = 0,
        int showfixSigXSecBand = 0,
        int channel = -1,
        bool blind = true,
        bool showSR = false,
        bool useShape = false,
        TString hname0 = "sigp1clsf",
        TString hname1 = "sigp1expclsf",
        TString hname3 = "sigclsu1s",
        TString hname5 = "sigclsd1s",
        TString hname6 = "sigp1ref")
{
    // set style and remove existing canvas'
    CombinationGlob::Initialize();

    cout << "--- Plotting mgluino/msquark versus mlsp " << endl;

    // --- prepare
    // open reference files, and retrieve histogram
    cout << "--- Reading root base file: " << fname0 << endl;
    TFile* f0 = TFile::Open( fname0, "READ" );
    if (!f0) {
        cout << "*** Error: could not retrieve histogram: " << hname0 << " in file: " << f0->GetName() 
            << " ==> abort macro execution" << endl;
        return;
    }

    TFile* f1;
    TFile* f2;
    if(showfixSigXSecBand){
        cout << "--- Reading root base file: " << fname1 << endl;
        f1 = TFile::Open( fname1, "READ" );
        cout << "--- Reading root base file: " << fname2 << endl;
        f2 = TFile::Open( fname2, "READ" );

        if(!f1 || !f2){
            cout << "*** Error: could not open in files: " << f1->GetName() <<" or "<< f2->GetName() 
                << " ==> abort macro execution" << endl;
            return;
        }
    }

    TH2F* histecls = (TH2F*)f0->Get( "sigp1expclsf" ); 
    TH2F* histocls = (TH2F*)f0->Get( "sigp1clsf" ); 
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
    TString fname6="";
    if(fname0.Contains("GG_onestep")) 
        fname6="/afs/cern.ch/atlas/groups/susy/SignalCrossSectionsUncert/SimplModels/SignalUncertainties-SM_GG_onestep_merge.root";
    else if(fname0.Contains("SS_onestep")) 
        fname6="/afs/cern.ch/atlas/groups/susy/SignalCrossSectionsUncert/SimplModels/SignalUncertainties-SM_SS_onestep_mc12.root";
    cout << "--- Reading root base file: " << fname6 << endl;
    f6 = TFile::Open( fname6, "READ" );

    if(f6){
        TTree *SignalUncertainties = (TTree*)f6->Get("SignalUncertainties");
        SignalUncertainties->ls();
        Int_t nmass =SignalUncertainties->GetEntries();
        SignalUncertainties->Show(10);
        Float_t mass1, mass2;
        Float_t mgluino, mchargino, mlsp;
        Int_t finalState;
        SignalUncertainties->SetBranchAddress("mass1",&mass1);
        SignalUncertainties->SetBranchAddress("mass2",&mass2);
        if(fname0.Contains("GG_onestep")) SignalUncertainties->SetBranchAddress("mgluino",&mgluino);
        else if(fname0.Contains("SS_onestep")) SignalUncertainties->SetBranchAddress("msquark",&mgluino);
        SignalUncertainties->SetBranchAddress("mchargino",&mchargino);
        SignalUncertainties->SetBranchAddress("mlsp",&mlsp);
        SignalUncertainties->SetBranchAddress("finalState",&finalState);
        ofstream fout;
    }
    //fout.open("test.data", ios::out);
    //for(Int_t i=0; i<nmass; i++){
    //SignalUncertainties->GetEntry(i);
    //SignalUncertainties->Scan("mass1:mass2:m0:m12","finalState==1");
    //if (finalState==1)      fout<<m0<<"  "<<m12 <<"  "<<mass1 <<"  "<<mass2<<endl;
    //}
    //fout.close();

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

    //TH2F* histe_esigxsp1s = (TH2F*)f1->Get( hname0 ); 
    //TH2F* histe_esigxsm1s = (TH2F*)f2->Get( hname0 ); 
    TH2F* histe_esigxsp1s; 
    TH2F* histe_esigxsm1s; 
    if(showfixSigXSecBand){
        histe_esigxsp1s = (TH2F*)f1->Get( hname0 ); 
        histe_esigxsm1s = (TH2F*)f2->Get( hname0 ); 
    }

    if (histe_esigxsp1s!=0) histe_esigxsp1s->SetDirectory(0);
    if (histe_esigxsm1s!=0) histe_esigxsm1s->SetDirectory(0);

    TH2F* contour_esigxsp1s
        = ( histe_esigxsp1s!=0 ? FixAndSetBorders( *histe_esigxsp1s, "contour_esigxsp1s", "contour_esigxsp1s", 0 ) : 0);
    TH2F* contour_esigxsm1s
        = ( histe_esigxsm1s!=0 ? FixAndSetBorders( *histe_esigxsm1s, "contour_esigxsm1s", "contour_esigxsm1s", 0 ) : 0);

    TH2F* contour         = ( hist1!=0 ? FixAndSetBorders( *hist1, "contour", "contour", 0 ) : 0);
    TH2F* contour_obs     = ( hist0!=0 ? FixAndSetBorders( *hist0, "contour_obs", "contour_obs") : 0 );

    TH2F* contour_ep1s    = ( hist3!=0 ? FixAndSetBorders( *hist3, "contour_ep1s", "contour_ep1s", 0 ) : 0 );
    TH2F* contour_em1s    = ( hist5!=0 ? FixAndSetBorders( *hist5, "contour_em1s", "contour_em1s", 0 ) : 0 );


    TH2F* contour_exp(0);
    if (histe!=0)     { contour_exp     = FixAndSetBorders( *histe, "contour_exp", "contour_exp", 0 ); } 
    TH2F* contour_au1s(0);
    if (histe_u1s!=0) {  contour_au1s   = FixAndSetBorders( *histe_u1s, "contour_au1s", "contour_au1s", 0 ); }
    TH2F* contour_ad1s(0);
    if (histe_d1s!=0) {  contour_ad1s   = FixAndSetBorders( *histe_d1s, "contour_ad1s", "contour_ad1s", 0 ); }


    TH2F* contour_expcls(0);
    if (histecls!=0)     { contour_expcls     = FixAndSetBorders( *histecls, "contour_expcls", "contour_expcls", 0 ); }
    TH2F* contour_obscls(0);
    if (histocls!=0)     { contour_obscls     = FixAndSetBorders( *histocls, "contour_obscls", "contour_obscls", 0 ); }

    
    //Dump Countours for HEP Database ---------------------------------
    TString ContourFileName="";
    if(fname0.Contains("GG_onestep")) ContourFileName="GG_onestep_X05_Countours2.dat";
    else ContourFileName="SS_onestep_X05_Countours.dat";
    ofstream ContourFile(ContourFileName);
    TString RootFileName=ContourFileName;
    RootFileName.ReplaceAll(".dat",".root");
    TDirectory currentDir= gDirectory->pwd();
    TFile *RootFile= new TFile(RootFileName,"RECREATE");
    TString CLsType="";
    
    ContourFile << "Observed CLs contour  \n";
    CLsType="ObsClsGraph";
    DumpContours(contour_obscls,ContourFile,RootFile,CLsType);   
    
    ContourFile << "Observed CLs contour with plus 1-sigma signal cross-section uncertainty \n";
    CLsType="ObsClsp1sGraph";
    DumpContours(contour_esigxsp1s,ContourFile,RootFile,CLsType);
    
    ContourFile << "Observed CLs contour with minus 1-sigma signal cross-section uncertainty\n";
    CLsType="ObsClsm1sGraph";
    DumpContours(contour_esigxsm1s,ContourFile,RootFile,CLsType);
    
    ContourFile << "Expected CLs contour  \n";
    CLsType="ExpClsGraph";
    DumpContours(contour_expcls,ContourFile,RootFile,CLsType);   
    
    ContourFile << "Expected CLs contour with plus 1-sigma experimental uncertainty \n";
    CLsType="ExpClsp1sGraph";
    DumpContours(contour_em1s,ContourFile,RootFile,CLsType);
    
    ContourFile << "Expected CLs contour with minus 1-sigma experimental uncertainty \n";
    CLsType="ExpClsm1sGraph";
    DumpContours(contour_ep1s,ContourFile,RootFile,CLsType);
    
    RootFile.Close();
    ContourFile.close();
    currentDir->cd();
    //----------------------------------------------------
    
   
   
    // For Band
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
    //TCanvas* c = new TCanvas( "c", "A scan of m_{0} versus m_{12}", 0, 0, 
    //                        CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[1] );  
    TCanvas* c = new TCanvas( "c", "A scan of m_{gluino} versus m_{lsp}", 0, 0, 
            CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[0]-10 );  
    //c->SetGrayscale();

    // create and draw the frame
    //TH2F *frame = new TH2F("frame", "m_{0} vs m_{12} - ATLAS work in progress", 100, 1000., 2400. ,100, 1000., 2400.);
    TString title;
    if(fname0.Contains("GG_onestep")) title=  "m_{#tilde{g}} vs m_{lsp} - ATLAS for approval";
    else if(fname0.Contains("SS_onestep")) title=  "m_{#tilde{q}} vs m_{lsp} - ATLAS for approval";
    float xlow = 200;
    float xhigh = 1600;
    float ylow = 0;
    float yhigh = 1250;
    if(fname0.Contains("SS_onestep")) {
      xhigh= 1050.;
      yhigh= 1050.;
    } 
    TH2F *frame = new TH2F("frame", title, 100,xlow, xhigh ,100, ylow, yhigh);
    
    // set common frame style
    CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0

    if(fname0.Contains("GG_onestep"))   frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
    else if(fname0.Contains("SS_onestep"))   frame->SetXTitle( "m_{#tilde{q}} [GeV]" );
    //frame->SetXTitle( "gluino mass [GeV]" );
    frame->SetYTitle( "m_{#tilde{#chi}_{1}^{0}} [GeV]" );
    //frame->GetYaxis()->SetTitleOffset(1.65);
    frame->GetYaxis()->SetTitleOffset(1.75);
    
    gPad->SetLeftMargin(0.14);
    //frame->SetTextFont( 42 );
    frame->GetXaxis()->SetTitleFont( 42 );
    frame->GetYaxis()->SetTitleFont( 42 );
    frame->GetXaxis()->SetLabelFont( 42 );
    frame->GetYaxis()->SetLabelFont( 42 );

    frame->GetXaxis()->SetTitleSize( 0.04 );
    frame->GetYaxis()->SetTitleSize( 0.04 );
    frame->GetXaxis()->SetLabelSize( 0.04 );
    frame->GetYaxis()->SetLabelSize( 0.04 );

    frame->Draw();

    const int nsig(3);
    //TH2F *chist[3];
    // draw contours
    //!instead of printing sigma in 68% 95% 98% levels now printing +1 sigma deviations 
    //for (Int_t nsigma=1; nsigma<=nsig; nsigma++)
    //  DrawContourSameColor( contour, nsigma, "blue", kFALSE, (nsigma==1?inverse:0) ) ;

    TString basecolor="yellow";
    Int_t nsigma=2;
    TLegend *leg = new TLegend (0.15,0.79,0.35,0.92);

    leg->SetTextSize( CombinationGlob::DescriptionTextSize );
    //leg->SetTextSize( 0.032 );
    leg->SetTextSize( 0.029 );
    leg->SetTextFont( 42 );
    leg->SetFillColor( 0 );
    leg->SetFillStyle(0);



Int_t c_myYellow   = TColor::GetColor("#ffe938");
Int_t c_myRed      = CombinationGlob::c_DarkRed;
Int_t c_myExp      = CombinationGlob::c_DarkBlueT3;
c->cd(1);

// draw 7TeV observed exclusion limits 
TGraph *graph_7TeV(0);
if(show7TeVlimits){
    c->cd();
    if (fname0.Contains("SS")) graph_7TeV= SimplifiedModels_7TeV("SM_SS_onestep_X05") ;
    else if (fname0.Contains("GG"))graph_7TeV= SimplifiedModels_7TeV("SM_GG_onestep_X05") ; 
    leg->AddEntry(graph_7TeV,"Observed limit (4.7 fb^{-1}, 7 TeV)","f");
}


TGraph* grshadeExp;
if(gr_contour_em1s->GetN()>0 && gr_contour_ep1s->GetN()>0){
    grshadeExp = (TGraph *)DrawExpectedBand_new( gr_contour_em1s, gr_contour_ep1s, c_myYellow , 1001,
            xlow,xhigh,ylow,yhigh,//200, 1000, 0, 0,
            0, 0)->Clone();
}


// redrawdraw 7TeV observed exclusion limits without fill area 
if(show7TeVlimits){
    c->cd();
    if (fname0.Contains("SS")) SimplifiedModels_7TeV("SM_SS_onestep_X05",false) ;
    else if (fname0.Contains("GG")) SimplifiedModels_7TeV("SM_GG_onestep_X05",false) ; 
}


if (discexcl==1) {
    //if (contour_obs!=0) DrawContourLine95( leg, contour_obs, "Observed PCL 95% CL", 2, 1, 3 );
    if (!extExpectation) { // expectation from toys
        //if (contour!=0) DrawContourLine95( leg, contour, "Expected PCL", CombinationGlob::c_DarkBlueT3, 6 );

        if (showfixSigXSecBand) {
            if (contour_esigxsp1s!=0) DrawContourLine95( leg, contour_esigxsp1s, "", c_myRed, 3, 2 );
            if (contour_esigxsm1s!=0) DrawContourLine95( leg, contour_esigxsm1s, "", c_myRed, 3, 2 );
        }
        //if (contour_obscls!=0) DrawContourLine95( leg, contour_obscls, "Observed limit", CombinationGlob::c_DarkRed, 1, 4);
        if (!blind){
            if (contour_obscls!=0) {
	      DrawContourLine95( leg, contour_obscls, "Observed limit (#pm1 #sigma^{SUSY}_{theory})", c_myRed, 1, 4);
	    }  
        }

        TLine* line1;
	if(fname0.Contains("SS")) line1= new TLine( 219, 961, 256, 961);
        else line1= new TLine(232, 1144, 288, 1144);
        line1->SetLineWidth(2);
        line1->SetLineColor(CombinationGlob::c_DarkRed);
        line1->SetLineStyle(3);
        line1->Draw("SAME") ;
        TLine* line2;
	if(fname0.Contains("SS")) line2= new TLine( 219, 920, 256, 920);
	else line2= new TLine(232, 1096, 288, 1096);
        line2->SetLineWidth(2);
        line2->SetLineColor(CombinationGlob::c_DarkRed);
        line2->SetLineStyle(3);
        line2->Draw("SAME") ;                

        if (contour_expcls!=0) {
            cout << "v 95% CLS" << endl;
            //DrawContourLine95( leg, contour_expcls, "exp. limit 95% CL", c_myExp, 6 ); 
            DrawContourLine95( leg, contour_expcls, "", c_myExp, 6 ); 
        }

        if (showOneSigmaExpBand) {
            if (contour_ep1s!=0) DrawContourLine95( leg, contour_ep1s, "", CombinationGlob::c_DarkYellow, 1 );
            if (contour_em1s!=0) DrawContourLine95( leg, contour_em1s, "", CombinationGlob::c_DarkYellow, 1 );

            cout << "v 95% =- 1 sigma CLS" << endl;
            DummyLegendExpected(leg, "Expected limit (#pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 2);
        } else {
            if (contour!=0) DrawContourLine68( leg, contour, "exp. limit 68% CL", CombinationGlob::c_DarkBlueT3, 2 );
            if (contour!=0) DrawContourLine99( leg, contour, "exp. limit 99% CL", CombinationGlob::c_DarkBlueT3, 3 );
        }
	

    } else { // expectation from asimov
        if (contour_exp!=0) DrawContourLine95( leg, contour_exp, "Median expected limit", CombinationGlob::c_DarkBlueT3, 6);
        if (showOneSigmaExpBand) {
            if (contour_au1s!=0) DrawContourLine95( leg, contour_au1s, "Expected limit #pm1#sigma", CombinationGlob::c_DarkBlueT3, 3 );
            if (contour_ad1s!=0) DrawContourLine95( leg, contour_ad1s, "", CombinationGlob::c_DarkBlueT3, 3 );
        }
    }
}


// legend
Float_t textSizeOffset = +0.000;
Double_t xmax = frame->GetXaxis()->GetXmax();
Double_t xmin = frame->GetXaxis()->GetXmin();
Double_t ymax = frame->GetYaxis()->GetXmax();
Double_t ymin = frame->GetYaxis()->GetXmin();
Double_t dx   = xmax - xmin;
Double_t dy   = ymax - ymin;


TString LegendTitle="";
if(fname0.Contains("GG_onestep")) LegendTitle="Simplified model, #tilde{g}#tilde{g} #rightarrow q#bar{q}q#bar{q} #tilde{#chi}^{#pm}_{1}#tilde{#chi}^{#pm}_{1} #rightarrow q#bar{q}q#bar{q} W^{#pm}W^{#pm} #tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}"; 
else if(fname0.Contains("SS_onestep")) LegendTitle="Simplified model, #tilde{q}#tilde{q}* #rightarrow q#bar{q} #tilde{#chi}^{+}_{1}#tilde{#chi}^{-}_{1} #rightarrow q#bar{q} W^{+}W^{-} #tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}" ; 
TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025, LegendTitle);
Leg0->SetTextAlign( 11 );
Leg0->SetTextFont( 42 );
Leg0->SetTextSize( CombinationGlob::DescriptionTextSize);
Leg0->SetTextColor( 1 );
Leg0->AppendPad();
 
TLatex *Leg01 = new TLatex();
Leg01->SetNDC();
Leg01->SetTextAlign( 11 );
Leg01->SetTextFont( 72 );
Leg01->SetTextSize( 1.1*CombinationGlob::DescriptionTextSize);
Leg01->SetTextColor( 1 );
Leg01->DrawLatex(0.58,0.88,"ATLAS");
Leg01->AppendPad();

TLatex *Leg1 = new TLatex();
Leg1->SetNDC();
Leg1->SetTextAlign( 11 );
Leg1->SetTextFont( 42 );
Leg1->SetTextSize( 0.94*CombinationGlob::DescriptionTextSize );
Leg1->SetTextColor( 1 );
Leg1->DrawLatex(0.58,0.81, Form("#int L dt = %1.1f fb^{-1},  #sqrt{s}=8 TeV",lumi));  // 0.32,0.87
Leg1->AppendPad();

TLatex *Leg2 = new TLatex();
Leg2->SetNDC();
Leg2->SetTextAlign( 11 );
Leg2->SetTextSize( CombinationGlob::DescriptionTextSize );
Leg2->SetTextColor( 1 );
Leg2->SetTextFont(42);
if (prefix!=0) {
    Leg2->DrawLatex(0.7,0.88,"Internal");
    //Leg2->DrawLatex(0.72,0.88,"Preliminary");
    Leg2->DrawLatex(0.58,0.75,prefix); // 0.15,0.81
    Leg2->SetTextSize(0.9*CombinationGlob::DescriptionTextSize );
    if (fname0.Contains("SS")) Leg2->DrawLatex(0.16,0.75,"m(#tilde{#chi}^{#pm}_{1})= (m(#tilde{q}) + m(#tilde{#chi}_{1}^{0}))/2");
    else Leg2->DrawLatex(0.16,0.75,"m(#tilde{#chi}^{#pm}_{1})= (m(#tilde{g}) + m(#tilde{#chi}_{1}^{0}))/2");
    Leg2->AppendPad(); 
}

TLatex *atlasLabel = new TLatex();
atlasLabel->SetNDC();
atlasLabel->SetTextFont( 72 );
atlasLabel->SetTextColor( 1 );
atlasLabel->SetTextSize( 0.05 );
//atlasLabel->DrawLatex(0.6,0.87, "ATLAS"); // 0.15,0.87
atlasLabel->AppendPad();


//// draw number of signal events
if (nsigmax>0 && showsig) {  hist1->Draw("textsame"); }
//else {
//  // draw grid for clarity
//  c->SetGrid();
//}
//reddraw cahnnel label
if (prefix!=0) { Leg2->AppendPad(); }

// redraw axes
frame->Draw( "sameaxis" );

leg->Draw("same");
c->Update();  // update the canvas

if(yhigh > 2) {
    double framewidth = (xhigh-xlow);
    double frameheight (yhigh-ylow);
    double bottomleft = max(xlow,ylow);
    double topright = min(xhigh,yhigh);

    TLatex badLSP;
    badLSP.SetTextFont( 42 );
    badLSP.SetTextSize( 0.0265 );
    double angle = TMath::ATan2((topright-bottomleft)/(frameheight),
            (topright-bottomleft)/(framewidth)) * 180 / TMath::Pi();
    badLSP.SetTextAngle(angle);

    TString badLSPstr = "";
    if (fname0.Contains("SS")) badLSPstr = "#tilde{q} LSP";
    else if (fname0.Contains("GG")) badLSPstr = "#tilde{g} LSP";

    TPolyLine* equalmass = new TPolyLine(2);
    equalmass->SetLineWidth(2);
    equalmass->SetLineColor(kGray+1);
    equalmass->SetFillColor(kWhite);
    equalmass->SetFillStyle(1001);
    equalmass->SetPoint(0,bottomleft,bottomleft);
    equalmass->SetPoint(1,0.7*topright,0.7*topright);
    equalmass->Draw("f");
    equalmass->Draw("l");

    if (fname0.Contains("SS")) badLSP.DrawLatex(bottomleft+0.2*(xhigh-bottomleft)-20,bottomleft+0.2*(yhigh-bottomleft),badLSPstr);
    else if (fname0.Contains("GG")) badLSP.DrawLatex(bottomleft+0.2*(xhigh-bottomleft)-20,bottomleft+0.2*(yhigh-bottomleft)+80,badLSPstr);

}

else {

        TLatex badLSP;
        badLSP.SetTextFont( 42 );
        badLSP.SetTextSize( 0.0265 );

        TString badLSPstr = "";
        badLSPstr = "x=1";

        TPolyLine* equalmass = new TPolyLine(4);
        TPolyLine* gumi = new TPolyLine(4);
        equalmass->SetLineWidth(2);
        equalmass->SetLineColor(kGray+1);
        equalmass->SetFillColor(kWhite);
        equalmass->SetFillStyle(1001);
        equalmass->SetPoint(0,xlow,1.0);
        equalmass->SetPoint(1,xhigh,1.0);
        //equalmass->SetPoint(2,xlow,yhigh);
        //equalmass->SetPoint(3,bottomleft,bottomleft);
        //equalmass->Draw("f");
        //equalmass->Draw("l");

        gumi->SetLineWidth(10);
        gumi->SetLineColor(kWhite);
        gumi->SetFillColor(kWhite);
        gumi->SetPoint(0,1.2*xlow,1.015);
        gumi->SetPoint(1,0.9*xhigh,1.015);
        gumi->Draw("f");
        gumi->Draw("l");
        equalmass->Draw("f");
        equalmass->Draw("l");
     

        badLSP.DrawLatex(1.8*xlow,1.012,badLSPstr);


}


//draw benchmark points
TMarker *marker= new TMarker();
marker->SetMarkerSize(1.8);
marker->SetMarkerStyle(29);
float m1= 0,m2=0,m3=0;
c->cd();
        	
if (fname0.Contains("GG_onestep")){
  m1=1265;  m2=945;  m3=625; 
  marker->DrawMarker(m1,m3);
}
if (fname0.Contains("SS_onestep")){
  m1=665; m2=465; m3=265; 
  marker->DrawMarker(m1,m3);
  m1=465; m2=385; m3=305;
  marker->DrawMarker(m1,m3);
}

////draw upper limit x-sections
TCanvas *c2= (TCanvas *)c->Clone("upperlimit");
Show_UL(fname0, c2, !blind, xlow, xhigh, ylow, yhigh,false);


//draw best SRs
if(showSR){
    Show_SR(fname0, c, xlow, xhigh, ylow, yhigh, useShape);
}


////////////////////////////////////////////////////////////////////////////////////////////

//gROOT->GetListOfSpecials()->Print();

TObjArray *contours = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
if (contours!=0) {
    //contours->Print("v");

    TList *lcontour1 = (TList*)contours->At(0);
    //lcontour1->Print();
    if (lcontour1!=0) {
        TGraph *gc1 = (TGraph*)lcontour1->First();
        if (gc1!=0) { 
            //gc1->Print();
            //if (gc1->GetN() < 10) return;
            //gc1->SetMarkerStyle(21);
            //gc1->Draw("alp");
        }
    }
}

////////////////////////////////////////////////////////////////////////////////////////////

//c->SetGrid(); 

// create plots
// store histograms to output file
TObjArray* arr = fname0.Tokenize("/");
TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
TString outfile = objstring->GetString().ReplaceAll(".root","").ReplaceAll("_hypotest__1_harvest_list","").ReplaceAll("merged_list_","");

delete arr;

TString prefixsave = TString(prefix).ReplaceAll(" ","_")+ Form("wband%d_",showOneSigmaExpBand);
CombinationGlob::imgconv( c, Form("plots/CLs_%s",outfile.Data()) );   
if(c2) {
    //CombinationGlob::imgconv( c2, Form("plots/UpperLimit_%s",outfile.Data()) );
     TString filename="plots/UpperLimit_"+outfile;
    c2->Print(filename+".eps");
    c2->Print(filename+".pdf");    
    c2->Print(filename+".png");
}

TLatex *prel = new TLatex();
prel->SetNDC();
prel->SetTextFont( 42 );
prel->SetTextColor( 1 );
prel->SetTextSize( 0.04 );
//prel->DrawLatex(0.6, 0.82, "for approval");   // 0.27,0.87
prel->AppendPad();

TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%dinvfb_",lumi) + Form("wband%d_",showOneSigmaExpBand);
//CombinationGlob::imgconv( c, Form("plots/%s",outfile.Data()) );   

////delete leg;
////if (contour!=0) delete contour;
////delete frame;
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


TH2F* AddBorders( const TH2& hist, const char* name=0, const char* title=0)
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


TH2F* FixAndSetBorders( const TH2& hist, const char* name=0, const char* title=0, Double_t val=0 )
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


void DrawContourSameColor( TLegend *leg, TH2F* hist, Int_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE, Bool_t isnobs=kFALSE )
{
    if (nsigma < 1 || nsigma > 3) {
        cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
            << "==> abort" << endl;
        exit(1);
    }
    nsigma--; // used as array index

    Int_t lcol_sigma;
    Int_t fcol_sigma[3];
    Int_t lstyle = 1;
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
        lstyle = 2;
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

    h->SetLineColor( nsigma==1? 1 : lcol_sigma );
    if (isnobs)h->SetLineColor( nsigma==1? 2 : lcol_sigma );
    //h->SetLineStyle( 4 );
    h->SetLineWidth( 2 );
    h->SetLineStyle( lstyle );
    h->Draw( "samecont3" );

    if (linesOnly&&!isnobs)
        if(nsigma==1){ leg->AddEntry(h,"exp. 95% CL limit","l");}
    if (isnobs)
        if(nsigma==1){ leg->AddEntry(h,"obs. 95% CL limit","l");}  
    if (!linesOnly) {
        if(nsigma==0){ leg->AddEntry(h,"- 1 #sigma expectation","l"); }
        if(nsigma==2){ leg->AddEntry(h,"+ 1 #sigma expectation","l");}
    } 
}


void DrawContourSameColorDisc( TLegend *leg, TH2F* hist, Double_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE )
{
    if (nsigma < 0.5 || nsigma > 10.5 ) {
        cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
            << "==> abort" << endl;
        exit(1);
    }

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
        fcol_sigma[2] = CombinationGlob::c_BlueT2;
    }

    // contour plot
    TH2F* h = new TH2F( *hist );
    h->SetContour( 1 );
    double dsignif = double (nsigma);
    h->SetContourLevel( 0, dsignif );

    Int_t mycolor = (nsigma==5   ? 0 : 2);
    Int_t mycolor = (nsigma==2.5 ? 1 : 2);

    if( !second ){
        h->SetFillColor( fcol_sigma[mycolor] );
        if (!linesOnly) h->Draw( "samecont0" );
    }

    h->SetLineColor( (nsigma==2.5) ? 2 : lcol_sigma );

    h->SetLineStyle( nsigma==5 || nsigma==2.5 ? 1 : 2 );
    h->SetLineWidth( nsigma==5 || nsigma==2.5 ? 2 : 1 );

    h->Draw( "samecont3" );

    if(nsigma==5)   { leg->AddEntry(h,"5 #sigma discovery","l"); }
    if(nsigma==6)   { leg->AddEntry(h,"N (int) #sigma discovery","l"); }
    if(nsigma==2.5) { leg->AddEntry(h,"2.5 #sigma discovery","l"); }
}




void DrawContourMassLine(TH2F* hist, Double_t mass, int color=14 )
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





void DrawContourLine95( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2, Int_t linewidth=2 )
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
    //h->GetYaxis()->SetRangeUser(800,2800);
    //h->GetXaxis()->SetRangeUser(800,2400);
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
    cout << "number of countours= " << ncontours << endl;
    TList *list = (TList*)contours->At(0);
    Int_t number_of_lists = list->GetSize();
    cout <<" number_of_lists = " << number_of_lists<< endl;
    if(number_of_lists==0) return gr;

    gr = (TGraph*)list->At(0);
    TGraph* grTmp = new TGraph();
    for (int k = 0 ; k<number_of_lists ; k++){
        grTmp = (TGraph*)list->At(k);
        Int_t N = gr->GetN();
        Int_t N_tmp = grTmp->GetN();
        if(N < N_tmp) gr = grTmp;
    }

    gr->SetName(hist->GetName());
    int N = gr->GetN();
    double x0, y0;

    return gr;
}


void DumpContours( TH2F* hist, ofstream &ContourFile, TFile *RootFile,TString CLsType)
{
    
    TGraph* gr0 = new TGraph();
    TH2F* h = (TH2F*)hist->Clone();
    gr = (TGraph*)gr0->Clone(h->GetName());
    h->SetContour( 1 );
    double pval = CombinationGlob::cl_percent[1];
    double signif = TMath::NormQuantile(1-pval);
    h->SetContourLevel( 0, signif );
    h->Draw("CONT LIST");
    h->SetDirectory(0);
    gPad->Update();
    TObjArray *contours = gROOT->GetListOfSpecials()->FindObject("contours");
    Int_t ncontours     = contours->GetSize();
    cout << "number of countours= " << ncontours << endl;
    TList *list = (TList*)contours->At(0);
    Int_t number_of_lists = list->GetSize();
    cout <<" number_of_lists = " << number_of_lists<< endl;
    
    char buffer[100];
    Double_t xx0, yy0;
    Double_t xarray[500], yarray[500], xarray_new[500], yarray_new[500];
    Int_t counter=0;
    //TGraph* grTmp = new TGraph();
    for (int k = 0 ; k<number_of_lists ; k++){        
        grTmp = (TGraph*)list->At(k);
        Int_t N = grTmp->GetN();
        ContourFile << "countour   "  << k+1 << "\n";
	ContourFile << "data: x : y  \n";
	if(N<10) continue;
	counter++;
	sprintf(buffer,"%s%d",CLsType.Data(),counter);
	TString GraphName= buffer;
	//grTmp->SetName(GraphName.Data());
	//grTmp->Write();
	//TGraph* grDump = new TGraph();
	for(int j=0; j<N; j++) {
          grTmp->GetPoint(j,xx0,yy0);
	  //sprintf(buffer,"%.1f;  %.1f;\n",xx0,yy0);
	  //ContourFile<< buffer;
	  xarray[j]= xx0;
	  yarray[j]= yy0;
        }
	
	int begin_yminus=-999, end_yminus=-999;
	int point_counter=0;
	for(int j=0; j<N; j++){
	  if (yarray[j]<0 && begin_yminus==-999) begin_yminus=j;
	  if (yarray[j]>0 && begin_yminus!=-999 && end_yminus==-999) end_yminus=j;
	  if (begin_yminus!=-999 && end_yminus!=-999){
	    xarray_new[point_counter]= xarray[j];
	    yarray_new[point_counter]= yarray[j];
	    point_counter++;
	    sprintf(buffer,"%.1f;  %.1f;\n",xarray[j],yarray[j]);
	    ContourFile<< buffer;
	  } 
	}
	for(int j=0; j<begin_yminus; ++j){
	  xarray_new[point_counter]= xarray[j];
	  yarray_new[point_counter]= yarray[j];
	  point_counter++;
	  sprintf(buffer,"%.1f;  %.1f;\n",xarray[j],yarray[j]);
	  ContourFile<< buffer;
	}
	TGraph* grDump = new TGraph(point_counter,xarray_new,yarray_new);
	grDump->SetName(GraphName.Data());
	grDump->Write();
    }
  
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
        cout << "contour1 point " << j << "  x= " <<  x1[j] << "   y= " <<  y1[j] << endl;
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
        cout << "contour2 point " << j << "  x= " <<  x2[j] << "   y= " <<  y2[j] << endl;
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
    cout << "nearest edge 1st graph= " <<  nearestedge1 << endl;

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
    cout << "nearest edge 2nd graph= " <<  nearestedge2 << endl;

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
                /*grshade->SetPoint(point,finalx,ylow-100);
                point++;
                grshade->SetPoint(point,xhigh+100,ylow-100);
                point++;
                grshade->SetPoint(point,xhigh+100,firsty);
                point++;*/
                break;  
            case 3:
                grshade->SetPoint(point,xlow-100,finaly);
                point++;
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


TGraph* DrawExpectedBand( TGraph* gr1,  TGraph* gr2, Int_t fillColor, Int_t fillStyle, Int_t cut = 0)
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
        if (x1[i] > cut){
            grshade->SetPoint(i,x1[i],y1[i]);
        }
        if (x2[N-i-1] > cut){
            grshade->SetPoint(N+i,x2[N-i-1],y2[N-i-1]);
        }
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
    grshade->SetMarkerStyle(21);
    grshade->Draw("FC");

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


void Show_SR(TString oredList,  TCanvas *can, float xlow, float xhigh, float ylow, float yhigh, bool useShape)
{
    can->cd();

    TLatex lat;
    //lat.SetTextAlign( 11 );
    lat.SetTextSize( 0.025 );
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
    Float_t m1; // gluino
    Float_t m2; // chargino
    Float_t m3; // lsp
    TBranch *b_m1;
    TBranch *b_m2;
    TBranch *b_m3;
    TBranch *b_fID;
    tree->SetBranchAddress("mchargino", &m2, &b_m2);
    if (oredList.Contains("GG_onestep")) tree->SetBranchAddress("mgluino", &m1, &b_m1);
    else if (oredList.Contains("SS_onestep")) tree->SetBranchAddress("msquark", &m1, &b_m1);
    tree->SetBranchAddress("mlsp", &m3, &b_m3);
    tree->SetBranchAddress("fID",  &fID,  &b_fID);
    
    TString SRFileName="";
    if(oredList.Contains("GG_onestep")) SRFileName="GG_onestep_X05_SR.dat";
    else SRFileName="SS_onestep_X05_SR.dat";
    char buffer[100];
    ofstream myfile(SRFileName);
    myfile << "# <x-coord>    <y-coord>     Signal region \n";

    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
       tree->GetEntry( i );
       
       TString mySR = GetSRName(fID, useShape);
       
       sprintf(buffer,"%d;  %d;  %s;\n",m1,m3,mySR.Data());
       myfile << buffer;
       
       if (oredList.Contains("SS_onestep") && m3>700) continue; 
       if (oredList.Contains("GG_onestep") && m3>800) continue; 

       if (fID > 0)  cout << "  At x = " << m1<< ", y = " << m3<< ", fID = " <<  fID<< endl;

        //lat.DrawLatex(m1,m3,mySR.Data());

        
        if(m1 > xlow+50 &&
        	m1 < xhigh-50 &&
        	m3 > ylow+50 &&
        	m3 < yhigh-50 &&
        	m1-m3 > 50 ) {
            bool right_position= true;
            for(int j=0;j<10; ++j){
              if((m1==275+j*100 && m3==35+20*j) || 
        	 (m1==235+j*100 && m3==75+20*j) || 
        	 (m1==195+j*100 && m3==115+20*j)||
        	 (m1==155+j*100&& m3==155+20*j)){
        	right_position= false;
              }
            }
	    if(m1==315 && m3==235) right_position= false;   
            if (right_position) {
	      lat.DrawLatex(m1,m3,mySR.Data());
            }
	    //lat.DrawLatex(m1,m3,mySR.Data());
        }     
       
    }
    myfile.close();
}


void Show_UL(TString oredList, TCanvas *can, bool observed=false, float xlow, float xhigh, 
        float ylow, float yhigh, bool acceff=false)
{
    can->cd();

    TLatex lat;
    //lat.SetTextAlign( 11 );
    //lat.SetTextSize( 0.0265 );
    lat.SetTextSize( 0.02 );
    lat.SetTextColor( 12 );
    lat.SetTextFont( 42 );

    cout << "Draw signal region labels." << endl;
    //    if (oredList.Contains("GG_onestep"))  gROOT->ProcessLine(".L summary_harvest_tree_description_GG.h+");
    //    else if (oredList.Contains("SS_onestep"))  gROOT->ProcessLine(".L summary_harvest_tree_description_SS.h+");
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
    Float_t UL;
    Float_t m1; // gluino
    Float_t m2; // chargino
    Float_t m3; // lsp
    Float_t xsec; // x-section
    TBranch *b_m1;
    TBranch *b_m2;
    TBranch *b_m3;
    TBranch *b_UL; // upper limit
    TBranch *b_xsec; // x-section
    TBranch *b_fID;
    tree->SetBranchAddress("mchargino", &m2, &b_m2);
    if (oredList.Contains("GG_onestep")) tree->SetBranchAddress("mgluino", &m1, &b_m1);
    else if (oredList.Contains("SS_onestep")) tree->SetBranchAddress("msquark", &m1, &b_m1);
    tree->SetBranchAddress("mlsp", &m3, &b_m3);
    if (observed) tree->SetBranchAddress("upperLimit",  &UL,  &b_UL);
    else tree->SetBranchAddress("expectedUpperLimit",  &UL,  &b_UL);
    tree->SetBranchAddress("xsec", &xsec, &b_xsec);
    tree->SetBranchAddress("fID",  &fID,  &b_fID);
    
    TString ULstring;
    
    TString ULFileName="";
    if(oredList.Contains("GG_onestep")) ULFileName="GG_onestep_X05_UL_SR.dat";
    else ULFileName="SS_onestep_X05_UL_SR.dat";
    ofstream myfile(ULFileName);
    //myfile << "# <x-coord>    <y-coord>     <95 CL cross section upper limit (fb)> \n";
    myfile << "# ################################################### \n";
    myfile << "# AUX FIGURE 23 AND FIGURE 24  \n";
    myfile << "# ################################################### \n";    
    myfile << "*dataset:\n";
    if(oredList.Contains("GG_onestep")) {
      myfile << "*location: Auxiliary Figures 23b, 24b\n";
      myfile << "*dscomment: Observed 95% CL cross-section upper limit for the pair-produced gluinos each decaying via an intermediate chargino1 to two quarks, a W boson and a neutralino1. \n";
      myfile << "*reackey: P P --> GLUINO GLUINO \n";     
    }
    else {
      myfile << "*location: Auxiliary Figures 23d, 24d\n";
      myfile << "*dscomment: Observed 95% CL cross-section upper limit for the pair-produced squarks each decaying via an intermediate chargino1 to quark, a W boson and a neutralino1. \n";
      myfile << "*reackey: P P --> SQUARK SQUARK \n";
    }
    myfile << "*obskey: M\n";
    if(oredList.Contains("GG_onestep")){ 
      myfile << "*qual: RE : P P --> GLUINO < QUARK QUARKBAR W NEUTRALINO1 > GLUINO < QUARK QUARKBAR W NEUTRALINO1 > \n";
      myfile << "*qual: SQRT(S) IN GEV : 8000.0\n";
      myfile << "*qual: . : X=DM(CHARGINO1 - NEUTRALINO1)/DM(GLUINO - NEUTRALINO1) = 0.5  \n";
    }
    else {
      myfile << "*qual: RE : P P --> SQUARK < QUARK W NEUTRALINO1 > SQUARK < QUARK W NEUTRALINO1 >  \n";
      myfile << "*qual: SQRT(S) IN GEV : 8000.0\n";
      myfile << "*qual: . : X=DM(CHARGINO1 - NEUTRALINO1)/DM(SQUARK - NEUTRALINO1) = 0.5  \n";
    }
    myfile << "*yheader: Cross-section limit IN FB : noZ SRs \n";
    if(oredList.Contains("GG_onestep")) myfile << "*xheader: GLUINO MASS IN GEV : NEUTRALINO1 MASS IN GEV\n";
    else myfile << "*xheader: SQUARK MASS IN GEV : NEUTRALINO1 MASS IN GEV\n";
    myfile << "*data: x : x : y : y \n";
 
    if(oredList.Contains("GG_onestep")) tree->BuildIndex("mgluino","mlsp");
    else tree->BuildIndex("msquark","mlsp");
    TTreeIndex *index = (TTreeIndex*)tree->GetTreeIndex();
 
    char buffer[100];
    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
        //tree->GetEntry( i );
	Long64_t local = tree->LoadTree( index->GetIndex()[i] );
        tree->GetEntry(local);
	
	TString mySR = GetSRName(fID, false);
	
	if(UL*xsec>=1000) sprintf(buffer," %d; %d; %.0f; %s;\n",m1,m3,UL*xsec,mySR.Data());
	else if(UL*xsec>=100) sprintf(buffer," %d; %d; %.1f; %s;\n",m1,m3,UL*xsec,mySR.Data());
	else if(UL*xsec>=10) sprintf(buffer," %d; %d; %.2f; %s;\n",m1,m3,UL*xsec,mySR.Data());
	else if(UL*xsec>=1) sprintf(buffer," %d; %d; %.3f; %s;\n",m1,m3,UL*xsec,mySR.Data());
	else if(UL*xsec>=0.1) sprintf(buffer," %d; %d; %.4f; %s;\n",m1,m3,UL*xsec,mySR.Data());
	else sprintf(buffer," %d; %d; %.5f; %s;\n",m1,m3,UL*xsec,mySR.Data());
	myfile << buffer;

	if (oredList.Contains("SS_onestep") && m3>700) continue; 
   	if (oredList.Contains("GG_onestep") && m3>800) continue; 
      	
        if(acceff) sprintf(buffer,"%.1f",UL*xsec);
        else {
            if(UL*xsec<100.) sprintf(buffer,"%.1f",UL*xsec);
            else sprintf(buffer,"%.0f",UL*xsec);
        }
        ULstring=buffer;
        cout << "  At x = " << m1<< ", y = " << m3<< ", UL = " <<  UL
            << ", ULstring= " << ULstring<< endl;
       
        //lat.DrawLatex(m1,m3,ULstring.Data());
       
        if(m1 > xlow+50 &&
        	m1 < xhigh-50 &&
        	m3 > ylow+50 &&
        	m3 < yhigh-50 &&
        	m1-m3 > 50 ) {
            bool right_position= true;
            for(int j=0;j<10; ++j){
        	if((m1==275+j*100 && m3==35+20*j) || 
        		(m1==235+j*100 && m3==75+20*j) || 
        		(m1==195+j*100 && m3==115+20*j)||
        		(m1==155+j*100&& m3==155+20*j)){
        	    right_position= false;
        	}
            }
	    if(m1==315 && m3==235) right_position= false;
            if (right_position && UL*xsec<1000000.){
	      lat.DrawLatex(m1,m3,ULstring.Data());
	    }  
        }     
       

    } 
    myfile <<"*dataend:\n";
    myfile.close();
    
    if(acceff) LegendTitle="Numbers give 95% CL excluded   #sigma*Acc*eff [fb]" ; 
    else LegendTitle="Numbers give 95% CL excluded cross section x BR [fb]" ; 

    TLatex *Leg0;
    if (oredList.Contains("SS_onestep")) Leg0= new TLatex( xhigh+40, ylow + 5, LegendTitle);
    else Leg0= new TLatex(xhigh+60, ylow +5, LegendTitle);
    Leg0->SetTextAngle(90);;
    Leg0->SetTextFont( 42 );
    Leg0->SetTextSize( 0.98*CombinationGlob::DescriptionTextSize);
    Leg0->SetTextColor( 1 );
    Leg0->AppendPad();

}
