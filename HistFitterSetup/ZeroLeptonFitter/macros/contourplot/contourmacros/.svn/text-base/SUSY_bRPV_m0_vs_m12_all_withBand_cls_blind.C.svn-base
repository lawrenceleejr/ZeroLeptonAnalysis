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

void SUSY_bRPV_m0_vs_m12_all_withBand_cls( TString fname0="", TString fname1="",
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

    if(fname1 != "")
        f1 = TFile::Open( fname1, "READ" );
        if(!f1) cout << "Warning: could not open " << fname1 << endl;
    if(fname2 != "")
        f2 = TFile::Open( fname2, "READ" );
        if(!f2) cout << "Warning: could not open " << fname2 << endl;

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
        TGraph* gr_contour_em1s= ContourGraph( contour_em1s )->Clone(); 
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
    double plotrange=2250.;
    TH2F *frame = new TH2F("frame", "m_{gluino} vs. m_{lsp} - ATLAS work in progress", 100, 350.,plotrange, 100, 200., 900. );
    // set common frame style
    CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
    
    frame->SetXTitle( "m_{0} [GeV]" );
    frame->SetYTitle( "m_{1/2} [GeV]" );
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


    Int_t c_myYellow   = TColor::GetColor("#ffe938");
    Int_t c_myRed      = TColor::GetColor("#aa000");

    // turn off yellow band    
    if (showOneSigmaExpBand) TGraph* grshadeExp= DrawExpectedBand( gr_contour_ep1s, gr_contour_em1s, CombinationGlob::c_DarkYellow , 1001 , 0)->Clone();


    if (discexcl==1) {
        //DrawContourLine95( leg, contour_obs,     "Observed limit (#pm1 #sigma^{SUSY}_{theory})", c_myRed, 1, 4 );   // 95% CL_{S}
        
        
        //if (contour_esigxsp1s)
            //DrawContourLine95( leg, contour_esigxsp1s, "", c_myRed, 3, 2 );    // Observed limit #pm 1 #sigma^{SUSY}_{theory}
        //if (contour_esigxsm1s)
            //DrawContourLine95( leg, contour_esigxsm1s, "", c_myRed, 3, 2 );    // Observed limit #pm 1 #sigma^{SUSY}_{theory}
        
        if (!extExpectation) { 
            // Compare the expected limits!
            if (contour_expcls!=0) { 
                //DrawContourLine95( leg, contour_expcls, fname0, CombinationGlob::c_DarkGray, 6 );
                DrawContourLine95( leg, contour_expcls, fname0, CombinationGlob::c_DarkBlueT3, 6 );
            }
            
            if (showOneSigmaExpBand) {
                if (contour_ep1s!=0) {	   
                    DrawContourLine95( leg, contour_ep1s, "", c_myYellow, 1 ); 
                }

                if (contour_em1s!=0)  {	   
                    DrawContourLine95( leg, contour_em1s, "", c_myYellow, 1 );
                }
                DummyLegendExpected(leg, "Expected limit (#pm1 #sigma_{exp})", c_myYellow, 1001, CombinationGlob::c_DarkBlueT3, 6, 2);

            } else {
                //if (contour!=0) DrawContourLine68( leg, contour, "exp. limit 68% CL", CombinationGlob::c_DarkBlueT3, 2 );
                //if (contour!=0) DrawContourLine99( leg, contour, "exp. limit 99% CL", CombinationGlob::c_DarkBlueT3, 3 );
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
    
    TString plottitle="bRPV-MSUGRA: tan #beta = 30, A_{0}= -2m_{0}, #mu>0";
    
    TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025,plottitle );
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
    Leg1->DrawLatex(0.15,0.78, Form("#int L dt = %1.1f fb^{-1},  #sqrt{s}=8 TeV",lumi));  // 0.32,0.87
    if(useShape){
        Leg1->DrawLatex(0.15,0.72, "0-lepton combined, 5-bin");  // 0.32,0.87
    } else {
        Leg1->DrawLatex(0.15,0.72, "0-lepton combined");  // 0.32,0.87
    }    

    Leg1->AppendPad();

    TLatex *Leg2 = new TLatex();
    Leg2->SetNDC();
    Leg2->SetTextAlign( 11 );
    Leg2->SetTextSize( CombinationGlob::DescriptionTextSize );
    Leg2->SetTextColor( 1 );
    Leg2->SetTextFont(70);
    if (prefix!=0) { 
        Leg2->DrawLatex(0.7,0.85,prefix); // 0.15,0.81
        Leg2->AppendPad(); 
    }

    TLatex *atlasLabel = new TLatex();
    atlasLabel->SetNDC();
    atlasLabel->SetTextFont( 42 );
    atlasLabel->SetTextColor( 1 );
    atlasLabel->SetTextSize( 0.05 );
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

    if (prefix!=0) { Leg2->AppendPad(); }

    // redraw axes
    frame->Draw( "sameaxis" );


    //  leg->Draw("same");


    // update the canvas
    double xline=1000.;
    double yline=1000.;
    if (fname0.Contains("SS")) {
        xline=800.; 
        yline=800.;
    }
    TLine *line=new TLine(200.,200.,xline,yline);
    line->SetLineStyle(3);
    //line->Draw();
    c->Update();


    TCanvas *c2=NULL; 
    if(showSR){
        ////draw upper limit x-sections
        //c2= (TCanvas *)c->Clone("upperlimit");
        //Show_UL(fname0, c2, xmin, xmax, ymin, ymax, false, leg);

        std::cout << "--- printing best SRs" << std::endl;
        Show_SR(fname0, c, xmin, xmax, ymin, ymax, useShape, leg);
        
    } else {
       //Show_SR takes care of this normally, do it here if we don't print 
        TMarker marker;
        //marker.SetMarkerColor(4);
        marker.SetMarkerSize(2.5);
        marker.SetMarkerStyle(29);

        if(gridname.Contains("GG")){
            marker.DrawMarker(700, 550);
            marker.DrawMarker(1162, 337);
            marker.DrawMarker(1250, 50);
        } else if(gridname.Contains("SS")){
            marker.DrawMarker(850, 100);
            marker.DrawMarker(450, 400);
        } else if(gridname.Contains("SG")){
            marker.DrawMarker(1425, 525);
            marker.DrawMarker(1612, 37);
        }

        leg->Draw("same");
        // add up/down lines
        TLine *line1;
        TLine *line2;
        if (gridname.Contains("GG")) {
            line1 = new TLine( 972, 1412, 1062, 1412);
            line2 = new TLine( 972, 1355, 1062, 1355);
            cout << "GG line1" << endl;
            
        } else if (gridname.Contains("SS")) {
            line1 = new TLine( 793, 1128, 860, 1128); 
            line2 = new TLine( 793, 1081, 860, 1081); 
            cout << "SS line1" << endl;
        } else if (gridname.Contains("SG")) {
            line1 = new TLine( 1150, 1645, 1260, 1645); 
            line2 = new TLine( 1150, 1565, 1260, 1565); 
            cout << "SG line1" << endl;
        }
/*
        line1->SetLineWidth(2);
        line1->SetLineColor(c_myRed);
        line1->SetLineStyle(3);
        line1->Draw("SAME") ;

        line2->SetLineWidth(2);
        line2->SetLineColor(c_myRed);
        line2->SetLineStyle(3);
        line2->Draw("SAME") ;                
*/
    }

    gPad->RedrawAxis("same");
    c->Update();
    gPad->Update();

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
    TString outfile = TString(Form("%1.2finvfb_",lumi)) + TString(Form("wband%d_",showOneSigmaExpBand)) + TString(Form("showcms%d_",showcms)) + objstring->GetString().ReplaceAll(".root","");
    delete arr;
    TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%1.2finvfb_",lumi) + Form("wband%d_",showOneSigmaExpBand);
    CombinationGlob::imgconv( c, Form("plots/atlascls_m0m12_%s",outfile.Data()) );   
    if(c2) {
        CombinationGlob::imgconv( c2, Form("plots/UpperLimit_%s",outfile.Data()) );
    }

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
    //   TString SR="SRA";
    //   TString meffcut="";
    //   TString momcut="";
    //   TString ismoriond="";
    // //     if (tmp.Contains("ombined") ) SR="Combined"
    //   if (tmp.Contains("SRA") ) SR="SRA";
    //   if (tmp.Contains("SRB") ) SR="SRB";
    //   if (tmp.Contains("SRC") ) SR="SRC";
    //   if (tmp.Contains("SRD") ) SR="SRD";
    //   if (tmp.Contains("SRE") ) SR="SRE";
    //   if (tmp.Contains("meff750") ) meffcut="750";
    //   if (tmp.Contains("meff800") ) meffcut="800";
    //   if (tmp.Contains("meff950") ) meffcut="950";
    //   if (tmp.Contains("meff900") ) meffcut="900";
    //   if (tmp.Contains("meff1000") ) meffcut="1000";
    //   if (tmp.Contains("meff1100") ) meffcut="1100";
    //   if (tmp.Contains("meff1250") ) meffcut="1250";
    //   if (tmp.Contains("meff1350") ) meffcut="1350";
    //   if (tmp.Contains("meff1200") ) meffcut="1200";
    //   if (tmp.Contains("meff1300") ) meffcut="1300";
    //   if (tmp.Contains("meff1400") ) meffcut="1400";
    //   if (tmp.Contains("meff1500") ) meffcut="1500";
    //   if (tmp.Contains("meff1600") ) meffcut="1600";
    //   if (tmp.Contains("meff1700") ) meffcut="1700";
    //   if (tmp.Contains("meff1800") ) meffcut="1800";
    //   if (tmp.Contains("metomeff0.15") ) momcut="0.15";
    //   if (tmp.Contains("metomeff0.2") ) momcut="0.2";
    //   if (tmp.Contains("metomeff0.25") ) momcut="0.25";
    //   if (tmp.Contains("metomeff0.3") ) momcut="0.3";
    //   if (tmp.Contains("metomeff0.35") ) momcut="0.35";
    //   if (tmp.Contains("metomeff0.4") ) momcut="0.4";
    //   if (tmp.Contains("metomeff0.45") ) momcut="0.45";
    //   if (tmp.Contains("metomeff0.5") ) momcut="0.5";
    //   if (tmp.Contains("metomeff0.275") ) momcut="0.275";
    //   else if (tmp.Contains("metomeff0.175") ) momcut="0.175";
    //   else if (tmp.Contains("metomeff0.375") ) momcut="0.375";
    //   else if (tmp.Contains("metomeff0.225") ) momcut="0.225";
    //   else if (tmp.Contains("metomeff0.325") ) momcut="0.325";
    //   else if (tmp.Contains("metomeff0.425") ) momcut="0.425";
    //   if (tmp.Contains("medium") ) meffcut="Medium";
    //   if (tmp.Contains("loose") ) meffcut="Loose";
    //   if (tmp.Contains("tight") ) meffcut="Tight";
    //   if (tmp.Contains("moriond") ) ismoriond=" : MORIOND CUTS";

    //  if (!tmp.Contains("ombined") ) { 
    //     //   cout << " meff cut = " << meffcut << " MET/meff  cut = " << momcut << " for tmp = " << tmp << endl;
    //     // if (tmp.Contains("loose") ||tmp.Contains("medium") ||tmp.Contains("tight") )  { if (!text.IsNull()) leg->AddEntry(h,SR+": "+meffcut+ismoriond,"l"); };
    // //     //  else if (tmp.Contains("ombined") ){ if (!text.IsNull()) leg->AddEntry(h,"Combined"+ismoriond,"l"); }
    // //     else { if (!text.IsNull()) leg->AddEntry(h,SR+": Meff > "+meffcut+" , MET/Meff > "+momcut,"l"); };
    //   }


    if (&text.Contains("Observed")) leg->AddEntry(h,text.Data(),"l");

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

    bool drawMarker;

    for( Int_t i = 0; i < tree->GetEntries(); i++ ){
        drawMarker = false;
        
        tree->GetEntry( i );
        cout << m0 << " " << m12 << " " << fID << endl;
        
        TMarker marker;
        //marker.SetMarkerColor(4);
        marker.SetMarkerSize(2.5);
        marker.SetMarkerStyle(29);

        int _m0 = (int) m0;
        int _m12 = (int) m12;

        if(oredList.Contains("GG")){
            if( (_m0 == 700 && _m12 == 550) || (_m0 == 1162 && _m12 == 337) || (_m0 == 1250 && _m12 == 50) )
                drawMarker = true;
        } else if(oredList.Contains("SS")){
            if( (_m0 == 850 && _m12 == 100) || (_m0 == 450 && _m12 == 400))
                drawMarker = true;
        } else if(oredList.Contains("SG")){
            if( (_m0 == 1425 && _m12 == 525) || (_m0 == 1612 && _m12 == 37))
                drawMarker = true;
        }

        if (drawMarker)
            marker.DrawMarker(m0, m12);

        TString mySR = GetSRName(fID, useShape);
	lat.DrawLatex(m0,m12,mySR.Data());
	     
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
        line1 = new TLine( 793, 1128, 860, 1128); 
        line2 = new TLine( 793, 1081, 860, 1081); 
        cout << "SS line1" << endl;
    } else if (oredList.Contains("SG")) {
        line1 = new TLine( 1150, 1645, 1260, 1645); 
        line2 = new TLine( 1150, 1565, 1260, 1565); 
        cout << "SG line1" << endl;
    }
/*
    line1->SetLineWidth(2);
    line1->SetLineColor(c_myRed);
    line1->SetLineStyle(3);
    line1->Draw("SAME") ;

    line2->SetLineWidth(2);
    line2->SetLineColor(c_myRed);
    line2->SetLineStyle(3);
    line2->Draw("SAME") ;                
*/
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

