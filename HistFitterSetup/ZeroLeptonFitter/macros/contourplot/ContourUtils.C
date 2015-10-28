//vim: ts=4 sw=4
#include "contourmacros/CombinationGlob.C"
#include "TColor.h"
#include <algorithm>

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


void SetBorders( TH2 &hist, Double_t val=0 ) {
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


TH2F* FixAndSetBorders( const TH2& hist, const char* name=0, const char* title=0, Double_t val=0 ) {
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


void DrawContourSameColor( TLegend *leg, TH2F* hist, Int_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE, Bool_t isnobs=kFALSE ) {
    if (nsigma < 1 || nsigma > 3) {
        cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
            << "==> abort" << endl;
        exit(1);
    }

    nsigma--; // used as array index

    Int_t lcol_sigma;
    Int_t fcol_sigma[3];
    Int_t lstyle = 1;

    if ( color == "pink" ){
        lcol_sigma    = CombinationGlob::c_VDarkPink;
        fcol_sigma[0] = CombinationGlob::c_LightPink;
        fcol_sigma[1] = CombinationGlob::c_LightPink;
        fcol_sigma[2] = CombinationGlob::c_LightPink;
    } else if ( color == "green" ){ // HF
        lcol_sigma    = CombinationGlob::c_VDarkGreen;
        fcol_sigma[0] = CombinationGlob::c_DarkGreen;
        fcol_sigma[1] = CombinationGlob::c_LightGreen;
        fcol_sigma[2] = CombinationGlob::c_VLightGreen;
    } else if ( color == "yellow" ){
        lcol_sigma    = CombinationGlob::c_VDarkYellow;
        fcol_sigma[0] = CombinationGlob::c_DarkYellow;
        fcol_sigma[1] = CombinationGlob::c_DarkYellow;
        fcol_sigma[2] = CombinationGlob::c_White; //c_DarkYellow;
        lstyle = 2;
    } else if ( color == "orange" ){
        lcol_sigma    = CombinationGlob::c_VDarkOrange;
        fcol_sigma[0] = CombinationGlob::c_DarkOrange;
        fcol_sigma[1] = CombinationGlob::c_LightOrange; // c_DarkOrange
        fcol_sigma[2] = CombinationGlob::c_VLightOrange;
    } else if ( color == "gray" ){
        lcol_sigma    = CombinationGlob::c_VDarkGray;
        fcol_sigma[0] = CombinationGlob::c_LightGray;
        fcol_sigma[1] = CombinationGlob::c_LightGray;
        fcol_sigma[2] = CombinationGlob::c_LightGray;
    } else if ( color == "blue" ){
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

void DrawContourLine95( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=1, Int_t linestyle=2, Int_t linewidth=2 ) {
    // contour plot
    TH2F* h = new TH2F( *hist );
    h->SetContour( 1 );
    double pval = CombinationGlob::cl_percent[1];
    cout<< pval<<endl;
    double signif = TMath::NormQuantile(1-pval);
    cout << "signif: " <<signif << endl;
    h->SetContourLevel( 0, signif );

    h->SetLineColor( linecolor );
    h->SetLineWidth( linewidth );
    h->SetLineStyle( linestyle );
    h->Draw( "samecont3" );

    if (!text.IsNull() && leg) leg->AddEntry(h,text.Data(),"l"); 
    //return h;
}

void drawBand(TString fname1){
    TFile* f0 = TFile::Open( fname1, "READ" );

    TString name0_1su = "sigclsu1s";
    TString hname0_1sd = "sigclsd1s";
    
    TH2F* hist0_1su; 
    TH2F* hist0_1sd; 

    hist0_1su = (TH2F*)f0->Get( hname0_1su );
    hist0_1sd = (TH2F*)f0->Get( hname0_1sd );


}

TGraph* ContourGraph( TH2F* hist,double xmin=16, double xmax=90) {

    //temporary canvas
    TCanvas* MOO = new TCanvas( TString::Format("dummy_canvas_%s", hist->GetName()), "A scan of m_{0} versus m_{12}", 0, 0, 650,640);
    MOO->cd();

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

    delete MOO;

    cout << "Generated graph " << gr << " with name " << gr->GetName() << endl;
    return gr;
}

//TGraph DrawExpectedBand( TGraph &gr1,  TGraph gr2, Int_t fillColor, Int_t fillStyle, Int_t cut = 0) {
    //return DrawExpectedBand(*gr1, *gr2, fillColor, fillStyle, cut);
//}

TGraph* DrawExpectedBand( TGraph *gr1,  TGraph *gr2, Int_t fillColor, Int_t fillStyle, Int_t cut = 0) {
//  TGraph* gr1 = new TGraph( *graph1 );
    //  TGraph* gr2 = new TGraph( *graph2 );

    int number_of_bins = max(gr1->GetN(),gr2->GetN());

    const Int_t gr1N = gr1->GetN();
    const Int_t gr2N = gr2->GetN();

    const Int_t N = number_of_bins;
    Double_t x1[N], y1[N], x2[N], y2[N];

    Double_t xx0, yy0;

    std::cout << "grN1 = " << gr1N << " gr2N = " << gr2N << std::endl;

    for(int j=0; j<gr1N; j++) {
        gr1->GetPoint(j,xx0,yy0);
        x1[j] = xx0;
        y1[j] = yy0;
    }
    //if (gr1N < N && gr1N != 0) {
    if (gr1N < N){ 
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
    if (gr2N < N){
        for(int i=gr2N; i<N; i++) {
            x2[i] = x2[gr1N-1];
            y2[i] = y2[gr1N-1];
        }      
    }



    TGraph *grshade = new TGraphAsymmErrors(2*N);

    for (int i=0;i<N;i++) {
        if (x1[i] > cut)
        {
            cout << "Using x1: " << x1[i] << "," << y1[i] << endl;
            grshade->SetPoint(i,x1[i],y1[i]);
        }
        if (x2[N-i-1] > cut)
        {
            cout << "Using x2: " << x2[N-i-1] << "," << y2[N-i-1] << endl;
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

    for(int j=0; j<Nshade; j++) {
        grshade->GetPoint(j,x0,y0);
        if(x0 == 0 && y0 == 0){
            grshade->SetPoint(j, x00, y00);
        }
    }

    //for(int j=0; j<Nshade; j++) {
        //grshade->GetPoint(j,x0,y0);
        //cout << "Punkt " << j << ": " << x0 << "," << y0 << endl;
    //}

    // Now draw the plot... 
    grshade->SetFillStyle(fillStyle);
    grshade->SetFillColor(fillColor);
    //  grshade->SetMarkerStyle(21);
    grshade->Draw("SAME F");


    return grshade;
}

void Q_test() {
    TFile *file = TFile::Open("msugra_0_10_P_SREtight_fixSigXSecNominal__1_harvest_list.root");  
    //  TFile *file = TFile::Open("combined_msugra_Nominal_1_harvest_list.root");  
    TH2F* hist =file->Get("sigp1expclsf");
    //  hist->Draw("colz");  
    TH2F* contour = FixAndSetBorders( *hist, "test", "test", 0 );
    canvas = TCanvas();
    contour->Draw("colz"); 
    TLegend* leg = new TLegend();
    DrawContourLine95( leg, contour, "", 1, 1 ); 
    canvas.Print("toto.gif")
}


