#include "contourmacros/CombinationGlob.C"
#include "TMarker.h"
#include "TColor.h"
#include <algorithm>
#include "contourmacros/ol1.C"
#include "contourmacros/cdftanb5.C"
#include "contourmacros/d0tanb3muneg.C"
#include "contourmacros/GetSRName.C"

#include "contourmacros/SUSY12limits_GG.C"
#include "contourmacros/SUSY12limits_SS.C"
#include "contourmacros/SUSY12limits_SG.C"

void SUSY_SM_direct_all_withBand_cls_blind( TString fname0="", TString fname1="",
        TString fname2="",
        TString gridname="",
        const char* prefix="test",
        const float& lumi = 20.3,
        bool showsig = true,
        int discexcl = 1,
        int showtevatron = 0,
        int showcms = 0,
        int showOneSigmaExpBand = 0,
        bool showSR = false,
        bool useShape = false,
        bool show7TeV = true,
        TString fname_xsec2 = "",
        TString fname_xsec4 = "",
        TString fname_xsec8 = "",
        int channel = -1,
        TString hname0 = "sigp1clsf",
        TString hname1 = "sigp1expclsf",
        TString hname3 = "sigclsu1s",
        TString hname5 = "sigclsd1s",
        TString hname6 = "sigp1ref",
        TString fnameMass= "contourmacros/mSugraGridtanbeta10_gluinoSquarkMasses.root")
{
    
    // set style and remove existing canvas'
    CombinationGlob::Initialize();

    cout << "--- Plotting m0 versus m12 " << endl;

    // --- prepare
    // open reference files, and retrieve histogram
    cout << "--- Reading root base file: " << fname0 << endl;
    TFile* f0 = TFile::Open( fname0, "READ" );
    if (!f0) {
        cout << "*** Error: could not retrieve histogram: " << hname0 << " in file: " << f0->GetName() 
            << " ==> abort macro execution" << endl;
        return;
    }
    
    TFile *f1; TFile *f2;
    TFile *fxsec2;
    TFile *fxsec4;
    TFile *fxsec8;

    if(fname1 != ""){
        f1 = TFile::Open( fname1, "READ" );
        if(!f1) cout << "Warning: could not open " << fname1 << endl;
    }
    
    if(fname2 != "") {
        f2 = TFile::Open( fname2, "READ" );
        if(!f2) cout << "Warning: could not open " << fname2 << endl;
    }

    // open files with xsec/2, /4, /8 if present
    if(fname_xsec2 != TString("") ) {
        fxsec2 = TFile::Open( fname_xsec2, "READ" );
        if(!fxsec2) cout << "Warning: could not open " << fname_xsec2 << endl;
    }
    
    if(fname_xsec4 != "") {
        fxsec4 = TFile::Open( fname_xsec4, "READ" );
        if(!fxsec4) cout << "Warning: could not open " << fname_xsec4 << endl;
    }
    
    if(fname_xsec8 != "") {
        fxsec8 = TFile::Open( fname_xsec8, "READ" );
        if(!fxsec8) cout << "Warning: could not open " << fname_xsec8 << endl;
    }

    TH2F* histecls = (TH2F*)f0->Get( "sigp1expclsf" ); 
    TH2F* histocls = (TH2F*)f0->Get( "sigp1clsf" ); 
    if (histecls!=0) histecls->SetDirectory(0);
    if (histocls!=0) histocls->SetDirectory(0);

    TH2F* histe_esigxsp1s;
    if (fname1 != "" && f1)  {
        histe_esigxsp1s = (TH2F*)f1->Get( hname0 );
        cout << "Read up histogram " << histe_esigxsp1s << endl;
    }

    TH2F* histe_esigxsm1s;
    if (fname2 != "" && f2) { 
        histe_esigxsm1s = (TH2F*)f2->Get( hname0 ); 
        cout << "Read down histogram " << histe_esigxsm1s << endl;
    }

    TH2F* histecls_xsec2;
    if (fname_xsec2 != "" && fxsec2) { 
        histecls_xsec2 = (TH2F*)fxsec2->Get( "sigp1expclsf" ); 
        cout << "Read histogram for xsec/2 " << histecls_xsec2 << endl;
    }
    
    TH2F* histecls_xsec4;
    if (fname_xsec4 != "" && fxsec4) { 
        histecls_xsec4 = (TH2F*)fxsec4->Get( "sigp1expclsf" ); 
        cout << "Read histogram for xsec/4 " << histecls_xsec4 << endl;
    }
    
    TH2F* histecls_xsec8;
    if (fname_xsec8 != "" && fxsec8) { 
        histecls_xsec8 = (TH2F*)fxsec8->Get( "sigp1expclsf" ); 
        cout << "Read histogram for xsec/8 " << histecls_xsec8 << endl;
    }

    if (histe_esigxsp1s!=0) histe_esigxsp1s->SetDirectory(0);
    if (histe_esigxsm1s!=0) histe_esigxsm1s->SetDirectory(0);

    TH2F* contour_esigxsp1s
        = ( histe_esigxsp1s!=0 ? FixAndSetBorders( *histe_esigxsp1s, "contour_esigxsp1s", "contour_esigxsp1s", 0 ) : 0);
    TH2F* contour_esigxsm1s
        = ( histe_esigxsm1s!=0 ? FixAndSetBorders( *histe_esigxsm1s, "contour_esigxsm1s", "contour_esigxsm1s", 0 ) : 0);

    //    TFile* f3 = TFile::Open( fname3, "READ" );
    TH2F* histe(0);
    TH2F* histe_u1s(0);
    TH2F* histe_d1s(0);

    //    TFile* f4 = TFile::Open( fname4, "READ" );

    bool extExpectation = 0;

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

    TH2F* histe_esigxsp1s; 
    if (fname1!="" && f1) histe_esigxsp1s  = (TH2F*)f1->Get( hname0 ); 
    TH2F* histe_esigxsm1s; 
    if (fname2!="" && f2) histe_esigxsm1s  = (TH2F*)f2->Get( hname0 ); 

    if (fname1!="" &&histe_esigxsp1s!=0) histe_esigxsp1s->SetDirectory(0);
    if (fname2!="" && histe_esigxsm1s!=0) histe_esigxsm1s->SetDirectory(0);

    TH2F* contour_esigxsp1s
        = ( histe_esigxsp1s!=0 ? FixAndSetBorders( *histe_esigxsp1s, "contour_esigxsp1s", "contour_esigxsp1s", 0 ) : 0);
    TH2F* contour_esigxsm1s
        = ( histe_esigxsm1s!=0 ? FixAndSetBorders( *histe_esigxsm1s, "contour_esigxsm1s", "contour_esigxsm1s", 0 ) : 0);

    TH2F* contour         = ( hist1!=0 ? FixAndSetBorders( *hist1, "contour", "contour", 0 ) : 0);
    TH2F* contour_obs     = ( hist0!=0 ? FixAndSetBorders( *hist0, "contour_obs", "contour_obs") : 0 );

    TH2F* contour_ep1s    = ( hist3!=0 ? FixAndSetBorders( *hist3, "contour", "contour", 0 ) : 0 );
    TH2F* contour_em1s    = ( hist5!=0 ? FixAndSetBorders( *hist5, "contour", "contour", 0 ) : 0 );

    // For Band
    if (showOneSigmaExpBand){
        TGraph* gr_contour_ep1s = ContourGraph( contour_ep1s )->Clone(); 
        TGraph* gr_contour_em1s = ContourGraph( contour_em1s )->Clone(); 
    }
    TH2F* contour_exp(0);
    if (histe!=0)     { contour_exp     = FixAndSetBorders( *histe, "contour_exp", "contour_exp", 0 ); } 
    TH2F* contour_au1s(0);
    if (histe_u1s!=0) {  contour_au1s   = FixAndSetBorders( *histe_u1s, "contour", "contour", 0 ); }
    TH2F* contour_ad1s(0);
    if (histe_d1s!=0) {  contour_ad1s   = FixAndSetBorders( *histe_d1s, "contour", "contour", 0 ); }


    TH2F* contour_expcls(0);
    if (histecls!=0)     { contour_expcls     = FixAndSetBorders( *histecls, "contour_expcls", "contour_expcls", 0 ); }
    TH2F* contour_obscls(0);
    if (histocls!=0)     { contour_obscls     = FixAndSetBorders( *histocls, "contour_obscls", "contour_obscls", 0 ); }

    TH2F* contour_expcls_xsec2(0);
    if (histecls_xsec2!=0)     { contour_expcls_xsec2 = FixAndSetBorders( *histecls_xsec2, "contour_expcls_xsec2", "contour_expcls_xsec2", 0 ); }
    TH2F* contour_expcls_xsec4(0);
    if (histecls_xsec4!=0)     { contour_expcls_xsec4 = FixAndSetBorders( *histecls_xsec4, "contour_expcls_xsec4", "contour_expcls_xsec4", 0 ); }
    TH2F* contour_expcls_xsec8(0);
    if (histecls_xsec8!=0)     { contour_expcls_xsec8 = FixAndSetBorders( *histecls_xsec8, "contour_expcls_xsec8", "contour_expcls_xsec8", 0 ); }

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
    TCanvas* c = new TCanvas( "c", "A scan of "+gridname, 0, 0, 
            CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[1] );  
    //c->SetGrayscale();

    // create and draw the frame
    double plotrange=1500.;
    if (gridname.Contains("SS") ) plotrange=1100;
    if (gridname.Contains("SG") ) plotrange=1800;

    double plotrangey = plotrange;
    if (gridname.Contains("SS") ) plotrangey=750;

    TH2F *frame = new TH2F("frame", "m_{gluino} vs. m_{lsp} - ATLAS work in progress", 100, 200., plotrange, 100, 20., plotrangey );
    // set common frame style
    CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
    if (gridname.Contains("SS"))    frame->SetXTitle( "m_{#tilde{q}} [GeV]" );
    else frame->SetXTitle( "m_{#tilde{g}} [GeV]" );

    frame->SetYTitle( "m_{#tilde{#chi}}_{1}^{0} [GeV]" );
    frame->GetYaxis()->SetTitleOffset(1.35);

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

    TLegend *leg = new TLegend(0.6,0.7,0.92,0.9);

    leg->SetTextSize( CombinationGlob::DescriptionTextSize );
    leg->SetTextSize( 0.03 );
    leg->SetTextFont( 42 );
    leg->SetFillColor( 0 );
    leg->SetFillStyle(1001);

    if (false && channel==1) { // electron

        cout << "removing islands in electron channel ..." << endl;
        // contour line is drawn for values at 1.64485
        TAxis* ax = contour_obs->GetXaxis();
        TAxis* ay = contour_obs->GetYaxis();
        /*     
               contour_em1s

               for (int xbin = 1; xbin <= contour_obs->GetNbinsX(); xbin++) {
               for (int ybin = 1; ybin <= contour_obs->GetNbinsY(); ybin++) {
        // island 2
        if ( ax->GetBinCenter( xbin) > 420. && ax->GetBinCenter( xbin) < 480. &&
        ay->GetBinCenter( ybin) > 140. && ay->GetBinCenter( ybin) < 160. ) {
        cout << "Found spot here: " << xbin << " (" << ax->GetBinCenter( xbin)  << "), "
        << ybin << " (" << ay->GetBinCenter( ybin) << "), "
        << " value: " << contour->GetBinContent(xbin,ybin) <<   endl;
        cout << "   HACK : Setting above point by hand to 1.50 (!)" << endl;
        contour->SetBinContent(xbin, ybin, 1.50);
        }
        }
        }
        */

    }

    if (false && channel==2) { // combined
        cout << "removing islands in combined channel ..." << endl;
    }


    /////////////////////////////////////////////////////////
    //// add 2011 results 

    if (gridname.Contains("SS") && show7TeV){
        TGraph *graphSS1 = new TGraph(51);
        graphSS1->SetName("Graph");
        graphSS1->SetTitle("Graph");
        graphSS1->SetFillColor(75);

        graphSS1->SetLineColor(kBlue-10);
        graphSS1->SetFillColor(kBlue-10);
        graphSS1->SetFillStyle(3944);
        graphSS1->SetLineWidth(2);
        graphSS1->SetMarkerStyle(20);
        graphSS1->SetMarkerSize(1.2);
        graphSS1->SetLineColor(kGray+1);

        graphSS1->SetPoint(0,64.375,22.04389819);
        graphSS1->SetPoint(1,84.70280313,41.7);
        graphSS1->SetPoint(2,93.125,49.84389819);
        graphSS1->SetPoint(3,113.4528031,69.5);
        graphSS1->SetPoint(4,121.875,77.64389819);
        graphSS1->SetPoint(5,142.2028031,97.3);
        graphSS1->SetPoint(6,142.2028031,125.1);
        graphSS1->SetPoint(7,150.625,133.2438982);
        graphSS1->SetPoint(8,170.9528031,152.9);
        graphSS1->SetPoint(9,179.375,161.0438982);
        graphSS1->SetPoint(10,199.7028031,180.7);
        graphSS1->SetPoint(11,208.125,188.8438982);
        graphSS1->SetPoint(12,228.2475785,208.5);
        graphSS1->SetPoint(13,236.875,216.8423415);
        graphSS1->SetPoint(14,255.140251,236.3);
        graphSS1->SetPoint(15,265.625,246.4382965);
        graphSS1->SetPoint(16,282.4690948,264.1);
        graphSS1->SetPoint(17,294.375,275.6124926);
        graphSS1->SetPoint(18,323.125,280.1352838);
        graphSS1->SetPoint(19,351.875,274.1757194);
        graphSS1->SetPoint(20,380.625,281.4941452);
        graphSS1->SetPoint(21,409.375,283.1356723);
        graphSS1->SetPoint(22,438.125,284.3945027);
        graphSS1->SetPoint(23,466.875,280.7593791);
        graphSS1->SetPoint(24,495.625,272.9694978);
        graphSS1->SetPoint(25,524.375,264.9253007);
        graphSS1->SetPoint(26,527.4655544,264.1);
        graphSS1->SetPoint(27,553.125,258.4109218);
        graphSS1->SetPoint(28,581.875,261.971704);
        graphSS1->SetPoint(29,587.6169422,264.1);
        graphSS1->SetPoint(30,610.625,270.6606192);
        graphSS1->SetPoint(31,639.375,280.8202822);
        graphSS1->SetPoint(32,666.3950395,291.9);
        graphSS1->SetPoint(33,668.125,292.622736);
        graphSS1->SetPoint(34,674.7129134,291.9);
        graphSS1->SetPoint(35,696.875,287.4484);
        graphSS1->SetPoint(36,725.625,279.9139235);
        graphSS1->SetPoint(37,746.1204832,264.1);
        graphSS1->SetPoint(38,754.375,252.3618429);
        graphSS1->SetPoint(39,759.9961765,236.3);
        graphSS1->SetPoint(40,755.3168396,208.5);
        graphSS1->SetPoint(41,754.375,206.0768763);
        graphSS1->SetPoint(42,744.8922766,180.7);
        graphSS1->SetPoint(43,735.5991675,152.9);
        graphSS1->SetPoint(44,744.7015449,125.1);
        graphSS1->SetPoint(45,754.375,100.8113556);
        graphSS1->SetPoint(46,755.6129347,97.3);
        graphSS1->SetPoint(47,754.375,94.41115182);
        graphSS1->SetPoint(48,743.9661555,69.5);
        graphSS1->SetPoint(49,735.941132,41.7);
        graphSS1->SetPoint(50,733.7263353,13.9);
        graphSS1->SetFillStyle(4001);
        graphSS1->Draw("FSAME");



        graphSS2 = new TGraph(40);
        graphSS2->SetName("Graph");
        graphSS2->SetTitle("Graph");
        graphSS2->SetFillColor(75);

        ci = TColor::GetColor("#0000ff");
        graphSS2->SetLineColor(kBlue);
        graphSS2->SetLineStyle(2);
        graphSS2->SetLineWidth(2);
        graphSS2->SetMarkerStyle(20);
        graphSS2->SetMarkerSize(1.2);
        graphSS2->SetPoint(0,206.3388084,13.9);
        graphSS2->SetPoint(1,196.9223978,41.7);
        graphSS2->SetPoint(2,194.7261341,69.5);
        graphSS2->SetPoint(3,208.125,89.16141267);
        graphSS2->SetPoint(4,214.3953237,97.3);
        graphSS2->SetPoint(5,212.0614192,125.1);
        graphSS2->SetPoint(6,208.125,140.4845256);
        graphSS2->SetPoint(7,206.6624467,152.9);
        graphSS2->SetPoint(8,205.0711819,180.7);
        graphSS2->SetPoint(9,208.125,183.6529094);
        graphSS2->SetPoint(10,234.579462,208.5);
        graphSS2->SetPoint(11,236.875,210.7196854);
        graphSS2->SetPoint(12,256.5812457,236.3);
        graphSS2->SetPoint(13,265.625,245.0449172);
        graphSS2->SetPoint(14,290.8662301,264.1);
        graphSS2->SetPoint(15,294.375,267.4928279);
        graphSS2->SetPoint(16,323.125,273.8008206);
        graphSS2->SetPoint(17,351.875,275.7504261);
        graphSS2->SetPoint(18,380.625,282.3905443);
        graphSS2->SetPoint(19,409.375,287.0538545);
        graphSS2->SetPoint(20,438.125,291.5194542);
        graphSS2->SetPoint(21,466.875,286.2796868);
        graphSS2->SetPoint(22,495.625,276.1859037);
        graphSS2->SetPoint(23,524.375,268.7727268);
        graphSS2->SetPoint(24,545.0149509,264.1);
        graphSS2->SetPoint(25,553.125,260.7592629);
        graphSS2->SetPoint(26,577.5044482,236.3);
        graphSS2->SetPoint(27,578.4083584,208.5);
        graphSS2->SetPoint(28,581.875,204.4611982);
        graphSS2->SetPoint(29,610.625,199.542589);
        graphSS2->SetPoint(30,639.375,193.093769);
        graphSS2->SetPoint(31,653.3444738,180.7);
        graphSS2->SetPoint(32,668.125,165.8256358);
        graphSS2->SetPoint(33,680.506621,152.9);
        graphSS2->SetPoint(34,696.875,129.5723992);
        graphSS2->SetPoint(35,699.4354068,125.1);
        graphSS2->SetPoint(36,709.7302619,97.3);
        graphSS2->SetPoint(37,712.8639087,69.5);
        graphSS2->SetPoint(38,713.9291238,41.7);
        graphSS2->SetPoint(39,717.0584797,13.9);
        //graphSS2->Draw("same c");  

    }

    if (gridname.Contains("GG")){
        TGraph *graphGG1 = new TGraph(74);
        graphGG1->SetName("Graph");
        graphGG1->SetTitle("Graph");
        graphGG1->SetFillColor(75);

        graphGG1->SetLineColor(kBlue-10);
        graphGG1->SetFillColor(kBlue-10);
        graphGG1->SetFillStyle(3944);
        graphGG1->SetLineWidth(2);
        graphGG1->SetMarkerStyle(20);
        graphGG1->SetMarkerSize(1.2);
        graphGG1->SetLineColor(kGray+1);

        graphGG1->SetPoint(0,64.375,22.04389819);
        graphGG1->SetPoint(1,84.70280313,41.7);
        graphGG1->SetPoint(2,93.125,49.84389819);
        graphGG1->SetPoint(3,113.4528031,69.5);
        graphGG1->SetPoint(4,121.875,77.64389819);
        graphGG1->SetPoint(5,142.2028031,97.3);
        graphGG1->SetPoint(6,142.2028031,125.1);
        graphGG1->SetPoint(7,150.625,133.2438982);
        graphGG1->SetPoint(8,170.9528031,152.9);
        graphGG1->SetPoint(9,179.375,161.0438982);
        graphGG1->SetPoint(10,199.7028031,180.7);
        graphGG1->SetPoint(11,208.125,188.8438982);
        graphGG1->SetPoint(12,228.4528031,208.5);
        graphGG1->SetPoint(13,236.875,216.6438982);
        graphGG1->SetPoint(14,257.093601,236.3);
        graphGG1->SetPoint(15,265.625,244.5494919);
        graphGG1->SetPoint(16,280.4512627,264.1);
        graphGG1->SetPoint(17,294.375,277.5636486);
        graphGG1->SetPoint(18,306.5040741,291.9);
        graphGG1->SetPoint(19,323.125,307.9717126);
        graphGG1->SetPoint(20,336.7464009,319.7);
        graphGG1->SetPoint(21,351.875,334.3286975);
        graphGG1->SetPoint(22,367.6095969,347.5);
        graphGG1->SetPoint(23,380.625,360.0853289);
        graphGG1->SetPoint(24,397.4933724,375.3);
        graphGG1->SetPoint(25,409.375,386.7890173);
        graphGG1->SetPoint(26,426.322014,403.1);
        graphGG1->SetPoint(27,438.125,414.5129743);
        graphGG1->SetPoint(28,455.0017993,430.9);
        graphGG1->SetPoint(29,466.875,442.3808689);
        graphGG1->SetPoint(30,484.7734532,458.7);
        graphGG1->SetPoint(31,495.625,469.1929739);
        graphGG1->SetPoint(32,515.8892774,486.5);
        graphGG1->SetPoint(33,524.375,494.7053248);
        graphGG1->SetPoint(34,548.7777731,514.3);
        graphGG1->SetPoint(35,553.125,518.5035794);
        graphGG1->SetPoint(36,581.875,522.9872579);
        graphGG1->SetPoint(37,588.5682665,514.3);
        graphGG1->SetPoint(38,589.2998995,486.5);
        graphGG1->SetPoint(39,593.4830887,458.7);
        graphGG1->SetPoint(40,610.625,446.5581341);
        graphGG1->SetPoint(41,639.375,449.2483605);
        graphGG1->SetPoint(42,668.125,448.4200317);
        graphGG1->SetPoint(43,696.875,436.5055147);
        graphGG1->SetPoint(44,715.2523188,430.9);
        graphGG1->SetPoint(45,725.625,429.6719176);
        graphGG1->SetPoint(46,744.2442613,430.9);
        graphGG1->SetPoint(47,754.375,431.7061117);
        graphGG1->SetPoint(48,783.125,436.9605466);
        graphGG1->SetPoint(49,811.875,442.0523816);
        graphGG1->SetPoint(50,839.0239206,430.9);
        graphGG1->SetPoint(51,840.625,429.4902084);
        graphGG1->SetPoint(52,869.375,411.640305);
        graphGG1->SetPoint(53,898.125,406.080462);
        graphGG1->SetPoint(54,914.3966803,403.1);
        graphGG1->SetPoint(55,926.875,397.9876688);
        graphGG1->SetPoint(56,944.184723,375.3);
        graphGG1->SetPoint(57,955.625,358.5246948);
        graphGG1->SetPoint(58,961.7976442,347.5);
        graphGG1->SetPoint(59,973.1241977,319.7);
        graphGG1->SetPoint(60,970.506716,291.9);
        graphGG1->SetPoint(61,967.9280771,264.1);
        graphGG1->SetPoint(62,977.9823421,236.3);
        graphGG1->SetPoint(63,970.3069202,208.5);
        graphGG1->SetPoint(64,957.1372407,180.7);
        graphGG1->SetPoint(65,955.625,167.9015223);
        graphGG1->SetPoint(66,953.323935,152.9);
        graphGG1->SetPoint(67,955.625,145.6670048);
        graphGG1->SetPoint(68,963.9885691,125.1);
        graphGG1->SetPoint(69,955.625,111.4280012);
        graphGG1->SetPoint(70,950.3381433,97.3);
        graphGG1->SetPoint(71,936.0235113,69.5);
        graphGG1->SetPoint(72,937.8282889,41.7);
        graphGG1->SetPoint(73,950.549451,13.9);
        graphGG1->SetFillStyle(4001);
        graphGG1->Draw("FSAME");

        graphGG2 = new TGraph(72);
        graphGG2->SetName("Graph");
        graphGG2->SetTitle("Graph");
        graphGG2->SetFillColor(75);

        ci = TColor::GetColor("#0000ff");
        graphGG2->SetLineColor(kBlue);
        graphGG2->SetLineStyle(2);
        graphGG2->SetLineWidth(2);
        graphGG2->SetMarkerStyle(20);
        graphGG2->SetMarkerSize(1.2);
        graphGG2->SetPoint(0,205.9953237,13.9);
        graphGG2->SetPoint(1,193.5662091,41.7);
        graphGG2->SetPoint(2,195.8829867,69.5);
        graphGG2->SetPoint(3,208.125,83.91001916);
        graphGG2->SetPoint(4,222.3486601,97.3);
        graphGG2->SetPoint(5,208.125,124.0106567);
        graphGG2->SetPoint(6,207.7778388,125.1);
        graphGG2->SetPoint(7,199.153974,152.9);
        graphGG2->SetPoint(8,199.8049004,180.7);
        graphGG2->SetPoint(9,208.125,188.7451745);
        graphGG2->SetPoint(10,226.050471,208.5);
        graphGG2->SetPoint(11,236.875,218.9668489);
        graphGG2->SetPoint(12,250.9059097,236.3);
        graphGG2->SetPoint(13,265.625,250.5327203);
        graphGG2->SetPoint(14,283.6569135,264.1);
        graphGG2->SetPoint(15,294.375,274.4639236);
        graphGG2->SetPoint(16,308.8300469,291.9);
        graphGG2->SetPoint(17,323.125,305.7225981);
        graphGG2->SetPoint(18,339.9729378,319.7);
        graphGG2->SetPoint(19,351.875,331.2087767);
        graphGG2->SetPoint(20,372.5792512,347.5);
        graphGG2->SetPoint(21,380.625,355.2798892);
        graphGG2->SetPoint(22,404.5685915,375.3);
        graphGG2->SetPoint(23,409.375,379.9475881);
        graphGG2->SetPoint(24,435.1062338,403.1);
        graphGG2->SetPoint(25,438.125,406.0190157);
        graphGG2->SetPoint(26,466.1707984,430.9);
        graphGG2->SetPoint(27,466.875,431.5809323);
        graphGG2->SetPoint(28,471.0132577,430.9);
        graphGG2->SetPoint(29,466.875,421.9520287);
        graphGG2->SetPoint(30,457.9400942,403.1);
        graphGG2->SetPoint(31,466.875,398.9999501);
        graphGG2->SetPoint(32,495.625,398.8306643);
        graphGG2->SetPoint(33,506.0333726,403.1);
        graphGG2->SetPoint(34,524.375,413.6659315);
        graphGG2->SetPoint(35,553.125,427.4242184);
        graphGG2->SetPoint(36,560.0038386,430.9);
        graphGG2->SetPoint(37,581.875,445.9495212);
        graphGG2->SetPoint(38,610.625,451.0095233);
        graphGG2->SetPoint(39,639.375,453.7625795);
        graphGG2->SetPoint(40,668.125,453.0922957);
        graphGG2->SetPoint(41,694.409016,430.9);
        graphGG2->SetPoint(42,696.875,429.825471);
        graphGG2->SetPoint(43,725.625,425.5415008);
        graphGG2->SetPoint(44,754.375,428.5030927);
        graphGG2->SetPoint(45,764.9532796,430.9);
        graphGG2->SetPoint(46,783.125,435.7640621);
        graphGG2->SetPoint(47,811.875,444.004815);
        graphGG2->SetPoint(48,840.625,438.1668333);
        graphGG2->SetPoint(49,848.684983,430.9);
        graphGG2->SetPoint(50,869.375,415.0339404);
        graphGG2->SetPoint(51,889.929072,403.1);
        graphGG2->SetPoint(52,898.125,397.0652773);
        graphGG2->SetPoint(53,919.1121248,375.3);
        graphGG2->SetPoint(54,926.875,365.1872445);
        graphGG2->SetPoint(55,939.6434121,347.5);
        graphGG2->SetPoint(56,954.1795846,319.7);
        graphGG2->SetPoint(57,955.625,314.9210114);
        graphGG2->SetPoint(58,962.5621472,291.9);
        graphGG2->SetPoint(59,969.1129977,264.1);
        graphGG2->SetPoint(60,969.5581772,236.3);
        graphGG2->SetPoint(61,976.3290954,208.5);
        graphGG2->SetPoint(62,984.375,190.6276179);
        graphGG2->SetPoint(63,988.5394113,180.7);
        graphGG2->SetPoint(64,984.375,159.346088);
        graphGG2->SetPoint(65,983.2229254,152.9);
        graphGG2->SetPoint(66,984.2437796,125.1);
        graphGG2->SetPoint(67,984.375,123.6702593);
        graphGG2->SetPoint(68,986.7546832,97.3);
        graphGG2->SetPoint(69,987.8864758,69.5);
        graphGG2->SetPoint(70,989.6368779,41.7);
        graphGG2->SetPoint(71,990.4322256,13.9);
        //graphGG2->Draw("c same");   
    }





    Int_t c_myYellow   = TColor::GetColor("#ffe938");
    Int_t c_myRed      = TColor::GetColor("#aa000");
    // For band   
    if (showOneSigmaExpBand){
        TGraph* grshadeExp= DrawExpectedBand( gr_contour_ep1s, gr_contour_em1s, CombinationGlob::c_DarkYellow , 1001 , 0)->Clone();
    }

    if (discexcl==1) {
        if (!extExpectation) { 
            // Compare the expected limits!
            if (contour_expcls!=0) { 
                DrawContourLine95( leg, contour_expcls, "", CombinationGlob::c_DarkBlueT3, 6, 3 );
            }
            
            if (showOneSigmaExpBand) {
                if (contour_ep1s!=0) {	   
                    DrawContourLine95( leg, contour_ep1s, "", c_myYellow, 1 ); 
                }

                if (contour_em1s!=0)  {	   
                    DrawContourLine95( leg, contour_em1s, "", c_myYellow, 1 );
                }
                
                if(fname0.Contains("N2")){
                    DummyLegendExpected(leg, "Expected limit (#sigma/2, #pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 3 );
                } else if(fname0.Contains("N4")){
                    DummyLegendExpected(leg, "Expected limit (#sigma/4, #pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 3 );
                } else if(fname0.Contains("N8")){
                    DummyLegendExpected(leg, "Expected limit (#sigma/8, #pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 3 );
                } else {
                    DummyLegendExpected(leg, "Expected limit (#pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 3 );
                }

            } else {
                //if (contour!=0) DrawContourLine68( leg, contour, "exp. limit 68% CL", CombinationGlob::c_DarkBlueT3, 2 );
                //if (contour!=0) DrawContourLine99( leg, contour, "exp. limit 99% CL", CombinationGlob::c_DarkBlueT3, 3 );
            }
            
            if (contour_expcls_xsec2!=0) { 
                DrawContourLine95( leg, contour_expcls_xsec2, "Expected limit (#sigma/2)", c_myRed, 6 );
            }
            if (contour_expcls_xsec4!=0) { 
                DrawContourLine95( leg, contour_expcls_xsec4, "Expected limit (#sigma/4)", c_myRed, 4 );
            }
            if (contour_expcls_xsec8!=0) { 
                DrawContourLine95( leg, contour_expcls_xsec8, "Expected limit (#sigma/8)", c_myRed, 8 );
            }
            

        } else { // expectation from asimov
            if (contour_exp!=0) DrawContourLine95( leg, contour_exp, "Median expected limit", CombinationGlob::c_DarkBlueT3, 6);
            if (showOneSigmaExpBand) {
                if (contour_au1s!=0) DrawContourLine95( leg, contour_au1s, "Expected limit #pm1#sigma", CombinationGlob::c_DarkBlueT3, 3 );
                if (contour_ad1s!=0) DrawContourLine95( leg, contour_ad1s, "", CombinationGlob::c_DarkBlueT3, 3 );
            }
        }
    }



    // plot tevatron limits
    TGraph* lep2slep(0);
    TGraph* lep2char(0);
    TGraph* d0o(0);
    TGraph* d0graph(0);
    TGraph* cdfgraph(0);
    TGraph* atlas(0);
    TGraph* atlasexp(0);

    if (showtevatron==1 && discexcl==1) {
        lep2char = ol1();
        d0graph = d0tanb3muneg();
        cdfgraph = cdftanb5();
        //atlas = ATLAS10_1lepton();
        //atlasexp = ATLAS10_1leptonexp();
    }

    //:w(void) stautanb3();

    TGraph* cmscurve(0);
    if (showcms==1) { 
        //cmscurve = cmsoff();
        cmscurve = cms();
    }


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

    // text1a->SetTextColor( 1 ); //CombinationGlob::c_VDarkGreen );
    text1b->SetTextColor( 1 ); //CombinationGlob::c_VDarkGreen );
    text1c->SetTextColor( 1 );
    text1b->SetTextFont( 42 ); //CombinationGlob::c_VDarkGreen );

    // text1a->SetTextAlign( 11 );
    text1b->SetTextAlign( 11 );
    text1c->SetTextAlign( 11 );

    //  text1a->SetTextSize( CombinationGlob::DescriptionTextSize + textSizeOffset );
    text1b->SetTextSize( CombinationGlob::DescriptionTextSize  );
    text1c->SetTextSize( CombinationGlob::DescriptionTextSize  );
    
    TString plottitle="";
    if (gridname.Contains("SS")) plottitle="#tilde{q}#tilde{q} production; #tilde{q}#rightarrow q #tilde{#chi}_{1}^{0}";
    if (gridname.Contains("SG")) plottitle="#tilde{q}#tilde{g} production; #tilde{q}#rightarrow q #tilde{#chi}_{1}^{0}, #tilde{g}#rightarrow q q #tilde{#chi}_{1}^{0}";
    if (gridname.Contains("GG")) plottitle="#tilde{g}#tilde{g} production; #tilde{g}#rightarrow q q #tilde{#chi}_{1}^{0}";
    
    TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025,plottitle );
    Leg0->SetTextAlign( 11 );
    Leg0->SetTextFont( 42 );
    Leg0->SetTextSize( CombinationGlob::DescriptionTextSize);
    Leg0->SetTextColor( 1 );
    Leg0->AppendPad();

    if (gridname.Contains("SG")){
        TLatex *Leg0a = new TLatex( xmax-dx*0.13, ymax + dy*0.025, "m_{#tilde{q}}=0.96m_{#tilde{g}}" );
        Leg0a->SetTextAlign( 11 );
        Leg0a->SetTextFont( 42 );
        Leg0a->SetTextSize( CombinationGlob::DescriptionTextSize);
        Leg0a->SetTextColor( 1 );
        Leg0a->AppendPad();
    }


    TLatex *Leg1 = new TLatex();
    Leg1->SetNDC();
    Leg1->SetTextAlign( 11 );
    Leg1->SetTextFont( 42 );
    Leg1->SetTextSize( CombinationGlob::DescriptionTextSize );
    Leg1->SetTextColor( 1 );
    Leg1->DrawLatex(0.15,0.78, Form("#int L dt = %1.1f fb^{-1},  #sqrt{s}=8 TeV",lumi));  // 0.32,0.87
    if(useShape){
        Leg1->DrawLatex(0.15,0.72, "0 leptons, 2-6 jets, 5-bin");  // 0.32,0.87
    } else {
        Leg1->DrawLatex(0.15,0.72, "0 leptons, 2-6 jets");  // 0.32,0.87
    }    

    Leg1->AppendPad();

    TLatex *Leg2 = new TLatex();
    Leg2->SetNDC();
    Leg2->SetTextAlign( 11 );
    Leg2->SetTextSize( CombinationGlob::DescriptionTextSize );
    Leg2->SetTextColor( 1 );
    Leg2->SetTextFont(70);
    //if (prefix!=0) { 
        //Leg2->DrawLatex(0.7,0.85,prefix); // 0.15,0.81
        //Leg2->AppendPad(); 
    //}

    TLatex *atlasLabel = new TLatex();
    atlasLabel->SetNDC();
    atlasLabel->SetTextFont( 42 );
    atlasLabel->SetTextColor( 1 );
    atlasLabel->SetTextSize( 0.05 );
    //atlasLabel->DrawLatex(0.15,0.87, "#bf{#it{ATLAS}} Preliminary"); // 0.15,0.87
    //atlasLabel->DrawLatex(0.15,0.87, "#bf{#it{ATLAS}} Work in progress"); // 0.15,0.87
    atlasLabel->DrawLatex(0.15,0.87, "#bf{#it{ATLAS}} Internal"); // 0.15,0.87

    atlasLabel->AppendPad();

    //// draw number of signal events
    if (nsigmax>0 && showsig) {  hist1->Draw("textsame"); }
    //else {
    //  // draw grid for clarity
    //  c->SetGrid();
    //}
    //reddraw cahnnel label
    //  c->SetGrid();

    //if (prefix!=0) { Leg2->AppendPad(); }

    // redraw axes
    frame->Draw( "sameaxis" );


    //  leg->Draw("same");


    // update the canvas
    double xline=1000.;
    double yline=1000.;
    if (fname0.Contains("SS")) {
        xline=700.; 
        yline=700.;
    }
    TLine *line=new TLine(200.,200.,xline,yline);
    line->SetLineStyle(3);
    line->Draw();
    c->Update();


    if (gridname.Contains("GG") && show7TeV){
        graphGG1->Draw("LSAME");
        graphGG2->Draw("LSAME");
        leg->AddEntry(graphGG1,"Observed limit (4.7 fb^{-1}, 7 TeV)","f");
        leg->AddEntry(graphGG2,"Expected limit (4.7 fb^{-1}, 7 TeV)","l"); 
        
        //contour_SUSY12_GG_obscls->SetLineColor(kBlue-10);
        //contour_SUSY12_GG_obscls->SetFillColor(kBlue-10);
        //contour_SUSY12_GG_obscls->SetFillStyle(3944);
        //contour_SUSY12_GG_obscls->SetLineWidth(2);
        //contour_SUSY12_GG_obscls->SetMarkerStyle(20);
        //contour_SUSY12_GG_obscls->SetMarkerSize(1.2);
        //contour_SUSY12_GG_obscls->SetLineColor(kGray+1);
       
        cout << contour_SUSY12_GG_obscls << endl;
        contour_SUSY12_GG_obscls->Draw("SAME");

    }
    if (gridname.Contains("SS") && show7TeV){ 
        graphSS1->Draw("LSAME");
        graphSS2->Draw("LSAME");

        //graphSS2->SetLineStyle(1);

        leg->AddEntry(graphSS1,"Observed limit (4.7 fb^{-1}, 7 TeV)","f");
        leg->AddEntry(graphSS2,"Expected limit (4.7 fb^{-1}, 7 TeV)","l");  
    }

    TCanvas *c2=NULL; 
    if(showSR){
        ////draw upper limit x-sections
        c2= (TCanvas *)c->Clone("upperlimit");
        Show_UL(fname0, c2, xmin, xmax, ymin, ymax, false, leg);

        std::cout << "--- printing best SRs" << std::endl;
        Show_SR(fname0, c, xmin, xmax, ymin, ymax, useShape, leg);
        
    } else {
       //Show_SR takes care of this normally, do it here if we don't print 
        TMarker marker;
        //marker.SetMarkerColor(4);
        marker.SetMarkerSize(2.5);
        marker.SetMarkerStyle(29);

        if(gridname.Contains("GG")){
            marker.DrawMarker(800, 650);
            marker.DrawMarker(1425, 75);
            marker.DrawMarker(1087, 562);
        } else if(gridname.Contains("SS")){
            marker.DrawMarker(475, 425);
            marker.DrawMarker(1000, 100);
            marker.DrawMarker(400, 250);
        } else if(gridname.Contains("SG")){
            marker.DrawMarker(1612, 337);
        }

        leg->Draw("same");
        //// add up/down lines
        //TLine *line1;
        //TLine *line2;
        //if (gridname.Contains("GG")) {
            //line1 = new TLine( 972, 1412, 1062, 1412);
            //line2 = new TLine( 972, 1355, 1062, 1355);
            //cout << "GG line1" << endl;
            
        //} else if (gridname.Contains("SS")) {
            //line1 = new TLine( 734, 707, 796, 707); 
            //line2 = new TLine( 734, 676, 796, 676); 
            //cout << "SS line1" << endl;
        //} else if (gridname.Contains("SG")) {
            //line1 = new TLine( 1150, 1645, 1260, 1645); 
            //line2 = new TLine( 1150, 1565, 1260, 1565); 
            //cout << "SG line1" << endl;
        //}

        //line1->SetLineWidth(2);
        //line1->SetLineColor(c_myRed);
        //line1->SetLineStyle(3);
        //line1->Draw("SAME") ;

        //line2->SetLineWidth(2);
        //line2->SetLineColor(c_myRed);
        //line2->SetLineStyle(3);
        //line2->Draw("SAME") ;                
    }

    gPad->RedrawAxis("same");
    c->Update();  

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

    // create plots
    // store histograms to output file
    TObjArray* arr = fname0.Tokenize("/");
    TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
    TString outfile = TString(Form("%1.2finvfb_",lumi)) + TString(prefix) + TString(Form("wband%d_",showOneSigmaExpBand)) + TString(Form("showcms%d_",showcms)) + objstring->GetString().ReplaceAll(".root","");
    delete arr;
    
    
    TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%1.2finvfb_",lumi) + Form("wband%d_",showOneSigmaExpBand);
    CombinationGlob::imgconv( c, Form("plots/atlascls_m0m12_%s",outfile.Data()) );   
    if(c2) {
        CombinationGlob::imgconv( c2, Form("plots/UpperLimit_%s",outfile.Data()) );
    }

    //TLatex *prel = new TLatex();
    //prel->SetNDC();
    //prel->SetTextFont( 42 );
    //prel->SetTextColor( 1 );
    //prel->SetTextSize( 0.05 );
    //prel->DrawLatex(0.15, 0.81, "Preliminary");   // 0.27,0.87
    //prel->AppendPad();

    //TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%dinvfb_",lumi) + Form("wband%d_",showOneSigmaExpBand);
    //CombinationGlob::imgconv( c, Form("plots/m0m12cls_%s",outfile.Data()) );   

    ////delete leg;
    ////if (contour!=0) delete contour;
    ////delete frame;
}


void MirrorBorders( TH2& hist ) {
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


TH2F* AddBorders( const TH2& hist, const char* name=0, const char* title=0) {
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
    TString tmp = TString(text.Data());

    //if (&text.Contains("Observed")) 
    if (text != ""){
        leg->AddEntry(h,text.Data(),"l");
    }

    //if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l"); 

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
        //cout<<"grshade x1="<< x1[i] <<" y1="<<y1[i]<<endl;

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
    grshade->SetMarkerStyle(21);
    grshade->Draw("F");

    return grshade;
}

void Show_SR(TString oredList,  TCanvas *can, float xlow, float xhigh, float ylow, float yhigh, bool useShape, TLegend *leg)
{
    Int_t c_myRed      = TColor::GetColor("#aa000");
    
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

    TMarker marker;
    //marker.SetMarkerColor(4);
    marker.SetMarkerSize(2.5);
    marker.SetMarkerStyle(29);
    
    if(oredList.Contains("GG")){
        marker.DrawMarker(800, 650);
        marker.DrawMarker(1425, 75);
        marker.DrawMarker(1087, 562);
    } else if(oredList.Contains("SS")){
        marker.DrawMarker(475, 425);
        marker.DrawMarker(1000, 100);
        marker.DrawMarker(400, 250);
    } else if(oredList.Contains("SG")){
        marker.DrawMarker(1612, 337);
    }

    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
        drawMarker = false;
        
        tree->GetEntry( i );
        cout << m0 << " " << m12 << " " << fID << endl;
        
        int _m0 = (int) m0;
        int _m12 = (int) m12;
        

        TString mySR = GetSRName(fID, useShape);

        //// be 10% outside the edges
        //if( (m0 > (xhigh-xlow)/30.0 + xlow) &&
                //(m0 < xhigh - (xhigh-xlow)/30.0) &&
                //(m12 > (yhigh-ylow)/30.0 + ylow) &&
                //(m12 < yhigh - (yhigh-ylow)/30.0)
                //) {

            //if (oredList.Contains("SS") && _m0-_m12 == 50){
                //cout << m0 << " " << m12 << " --> " << m0-m12 << endl;
            //} else if (oredList.Contains("GG") && (_m0-_m12 ==75 || _m0-_m12 == 25)){
                //cout << m0 << " " << m12 << " --> " << m0-m12 << endl;
            //} else if (oredList.Contains("SG") && (_m0-_m12 ==75 || _m0-_m12 == 25)){
                //cout << m0 << " " << m12 << " --> " << m0-m12 << endl;
            //} else {
                //lat.DrawLatex(m0, m12, mySR.Data());
            //}
        //}
       
        // blinded, just draw everything
        lat.DrawLatex(m0, m12, mySR.Data());

        //if(!(m1>500 && (m1-m2==25 || m2== m3+25 || m1-m2==50))) lat.DrawLatex(m1,x,mySR.Data());      
    }
    
    leg->Draw("same");
    // add up/down lines
    TLine *line1;
    TLine *line2;
    if (oredList.Contains("GG")) {
        line1 = new TLine( 972, 1412, 1062, 1412);
        line2 = new TLine( 972, 1355, 1062, 1355);
        cout << "GG line1" << endl;
        
    } else if (oredList.Contains("SS")) {
        line1 = new TLine( 734, 707, 796, 707); 
        line2 = new TLine( 734, 676, 796, 676); 
        cout << "SS line1" << endl;
    } else if (oredList.Contains("SG")) {
        line1 = new TLine( 1150, 1645, 1260, 1645); 
        line2 = new TLine( 1150, 1565, 1260, 1565); 
        cout << "SG line1" << endl;
    }

    // for observed lines, not needed in blinded version

    //line1->SetLineWidth(2);
    //line1->SetLineColor(c_myRed);
    //line1->SetLineStyle(3);
    //line1->Draw("SAME") ;

    //line2->SetLineWidth(2);
    //line2->SetLineColor(c_myRed);
    //line2->SetLineStyle(3);
    //line2->Draw("SAME") ;                
}

void Show_UL(TString oredList, TCanvas *can, float xlow, float xhigh,
        float ylow, float yhigh, bool acceff=false, TLegend *leg) {
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
    tree->SetBranchAddress("xsec", &xsec, &b_xsec);

    TString ULstring;
    char buffer[20];
    
    TMarker marker;
    //marker.SetMarkerColor(4);
    marker.SetMarkerSize(2.5);
    marker.SetMarkerStyle(29);
    
    if(oredList.Contains("GG")){
        marker.DrawMarker(800, 650);
        marker.DrawMarker(1425, 75);
        marker.DrawMarker(1087, 562);
    } else if(oredList.Contains("SS")){
        marker.DrawMarker(475, 425);
        marker.DrawMarker(1000, 100);
        marker.DrawMarker(400, 250);
    } else if(oredList.Contains("SG")){
        marker.DrawMarker(1612, 337);
    }

    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
        drawMarker = false;

        tree->GetEntry( i );
        cout << m0 << " " << m12 << " " << fID << endl;
        
        int _m0 = (int) m0;
        int _m12 = (int) m12;

        if(acceff) sprintf(buffer,"%.1f",UL*xsec);
        else {
            if(UL*xsec<100.) sprintf(buffer,"%.1f",UL*xsec);
            else sprintf(buffer,"%.0f",UL*xsec);
        }
        ULstring=buffer;
        cout << "  At x = " << m0 << ", y = " << m12 << ", UL = " <<  UL << ", ULstring= " << ULstring << endl;

        //// be 10% outside the edges
        //if( (m0 > (xhigh-xlow)/30.0 + xlow) &&
                //(m0 < xhigh - (xhigh-xlow)/30.0) &&
                //(m12 > (yhigh-ylow)/30.0 + ylow) &&
                //(m12 < yhigh - (yhigh-ylow)/30.0)) {

            //if (oredList.Contains("SS") && _m0-_m12 == 50){
                //cout << m0 << " " << m12 << " --> " << m0-m12 << endl;
            //} else if (oredList.Contains("GG") && (_m0-_m12 ==75 || _m0-_m12 == 25)){
                //cout << m0 << " " << m12 << " --> " << m0-m12 << endl;
            //} else if (oredList.Contains("SG") && (_m0-_m12 ==75 || _m0-_m12 == 25)){
                //cout << m0 << " " << m12 << " --> " << m0-m12 << endl;
            //} else if(oredList.Contains("SG") && _m0 == 450 && _m12 == 150) {
                ////remove a ridiculous point
                //cout << "SG grid (450,150) unphysical UL -> remove!" << endl;
            //} else {
                //lat.DrawLatex(m0, m12, ULstring.Data());
            //}
        //}
        
        // blinded, just show all
        lat.DrawLatex(m0, m12, ULstring.Data());

    }
    TString LegendTitle;
    if(acceff) LegendTitle="Numbers give 95% CL_{s} excluded   #sigma*Acc*eff [fb]" ;
    else LegendTitle="Numbers give 95% CL_{s} excluded cross section x BR [fb]" ;

    TLatex *Leg0 = new TLatex( xhigh+40, ylow + 5, LegendTitle);
    Leg0->SetTextAngle(90);;
    Leg0->SetTextFont( 42 );
    Leg0->SetTextSize( 0.98*CombinationGlob::DescriptionTextSize);
    Leg0->SetTextColor( 1 );
    Leg0->AppendPad();

    leg->Draw("same");
    // add up/down lines
    TLine *line1;
    TLine *line2;
    if (oredList.Contains("GG")) {
        line1 = new TLine( 972, 1412, 1062, 1412);
        line2 = new TLine( 972, 1355, 1062, 1355);
        cout << "GG line1" << endl;

    } else if (oredList.Contains("SS")) {
        line1 = new TLine( 734, 707, 796, 707);
        line2 = new TLine( 734, 676, 796, 676);
        cout << "SS line1" << endl;
    } else if (oredList.Contains("SG")) {
        line1 = new TLine( 1150, 1645, 1260, 1645);
        line2 = new TLine( 1150, 1565, 1260, 1565);
        cout << "SG line1" << endl;
    }

    line1->SetLineWidth(2);
    line1->SetLineColor(c_myRed);
    line1->SetLineStyle(3);
    line1->Draw("SAME") ;

    line2->SetLineWidth(2);
    line2->SetLineColor(c_myRed);
    line2->SetLineStyle(3);
    line2->Draw("SAME") ;

}

void DummyLegendExpected(TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth) {

    TGraph* gr = new TGraph();
    gr->SetFillColor(fillColor);
    gr->SetFillStyle(fillStyle);
    gr->SetLineColor(lineColor);
    gr->SetLineStyle(lineStyle);
    gr->SetLineWidth(lineWidth);
    leg->AddEntry(gr,what,"LF");
}

