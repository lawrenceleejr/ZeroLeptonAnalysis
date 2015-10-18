#include "contourmacros/CombinationGlob.C"
#include "contourmacros/SUSY_m0_vs_m12_all_withBand_cls.C"
#include "TColor.h"
#include <algorithm>

//#include "../Tevatron/msugra_oldlim.C"
#include "contourmacros/legend.C"

#include "contourmacros/Gt.C"


 void SUSY_m0_vs_m12_all_withBand_cls_Gtt( TString fname = "mudat_list.root",// nominal
                                      TString name = "Gbb",               // name plot
                                      const char* prefix="test",
					  const float& lumi = 20)

{
   // set style and remove existing canvas'
   CombinationGlob::Initialize();
   
   cout << "--- Plotting m0 versus m12 " << endl;
   
   // --- prepare
   // open reference files, and retrieve histogram
  cout << "--- Reading root base file: " << fname << endl;



  TString fname_TP = fname;
  TString fname_TM = fname;
  fname_TP.ReplaceAll("Nominal","Up");
  fname_TM.ReplaceAll("Nominal","Down");
 
  std::cout << "Names of files:: " << std::endl;

  std::cout << fname << std::endl;
  //std::cout << fname_TP << std::endl;
  //std::cout << fname_TM << std::endl;



   // open reference files, and retrieve histogram
   
  TFile* f_NT = TFile::Open( fname, "READ" );
  if (!f_NT) {
    cout << "*** Error: could not retrieve NO THEORY histogram: " << hname0 << " in file: " << f_NT->GetName() ;
    return;
  }
    
  TFile* f_TP = TFile::Open( fname_TP, "READ" );
  if (!f_TP) {
    cout << "*** Error: could not retrieve NO THEORY PLUS histogram: " << hname0 << " in file: " << f_TP->GetName() ;
    return;
  }
    
  TFile* f_TM = TFile::Open( fname_TM, "READ" );
  if (!f_TM) {
    cout << "*** Error: could not retrieve NO THEORY MINUS histogram: " << hname0 << " in file: " << f_TM->GetName() ;
    return;
  }
  
    
   
  // NT
  TH2F* hist0_NT = (TH2F*)f_NT->Get("sigp1clsf"); 
  TH2F* hist1_NT = (TH2F*)f_NT->Get("sigp1expclsf");
  TH2F* hist3_NT = (TH2F*)f_NT->Get("sigclsu1s");
  TH2F* hist5_NT = (TH2F*)f_NT->Get("sigclsd1s");
  TH2F* hist6_NT = (TH2F*)f_NT->Get("sigp1ref");
  if (hist0_NT!=0) hist0_NT->SetDirectory(0);
  if (hist1_NT!=0) hist1_NT->SetDirectory(0);
  if (hist3_NT!=0) hist3_NT->SetDirectory(0);
  if (hist5_NT!=0) hist5_NT->SetDirectory(0);
  if (hist6_NT!=0) hist6_NT->SetDirectory(0);  


// NT

  TH2F* contour_exp_NT = ( hist1_NT!=0 ?  FixAndSetBorders( *hist1_NT, "contour_exp_NT", "contour_exp_NT", 0 ) : 0 );
  TH2F* contour_obs_NT = ( hist0_NT!=0 ?  FixAndSetBorders( *hist0_NT, "contour_exp_NT", "contour_exp_NT", 0 ) : 0 );
  TH2F* contour_ep1s_NT  = ( hist3_NT!=0 ? FixAndSetBorders( *hist3_NT, "contour_ep1s_NT", "contour_ep1s_NT", 0 ) : 0 );
  TH2F* contour_em1s_NT  = ( hist5_NT!=0 ? FixAndSetBorders( *hist5_NT, "contour_em1s_NT", "contour_em1s_NT", 0 ) : 0 );



  TGraph* gr_contour_ep1s = ContourGraph( contour_ep1s_NT )->Clone(); 
  TGraph* gr_contour_em1s = ContourGraph( contour_em1s_NT )->Clone(); 
   
 f_NT->Close(); 
  if (contour_exp_NT==0) { 
      cout << "contour exp is zero" << endl;
      return;
  }
 if (contour_obs_NT==0) { 
      cout << "contour obs is zero" << endl;
      return;
  }

  // Stuff for TP
  TH2F* hist0_TP = (TH2F*)f_TP->Get( "sigp1clsf" );
  TH2F* hist1_TP = (TH2F*)f_TP->Get( "sigp1expclsf" );
  if (hist0_TP!=0) hist0_TP->SetDirectory(0);
  if (hist1_TP!=0) hist1_TP->SetDirectory(0);

  TH2F* contour_exp_TP     = ( hist1_TP!=0 ? FixAndSetBorders( *hist1_TP, "contour_exp_TP", "contour_exp_TP", 0 ) : 0);
  TH2F* contour_obs_TP     = ( hist0_TP!=0 ? FixAndSetBorders( *hist0_TP, "contour_obs_TP", "contour_obs_TP", 0 ) : 0);
  f_TP->Close();

 // Stuff for TM
 TH2F* hist0_TM = (TH2F*)f_TM->Get( "sigp1clsf" );
 TH2F* hist1_TM = (TH2F*)f_TM->Get( "sigp1expclsf" );
 if (hist0_TM!=0) hist0_TM->SetDirectory(0);
 if (hist1_TM!=0) hist1_TM->SetDirectory(0);
 
 TH2F* contour_exp_TM     = ( hist1_TM!=0 ? FixAndSetBorders( *hist1_TM, "contour_exp_TM", "contour_exp_TM", 0 ) : 0);
 TH2F* contour_obs_TM     = ( hist0_TM!=0 ? FixAndSetBorders( *hist0_TM, "contour_obs_TM", "contour_obs_TM", 0 ) : 0);
 // f_TM->Close();
 
 
   // set text style
   gStyle->SetPaintTextFormat(".2g");
   if (hist0_NT!=0) hist0_NT->SetMarkerStyle(21);
   if (hist0_NT!=0) hist0_NT->SetMarkerSize(1.5);
   Float_t nsigmax(0)
   if (hist0_NT!=0) nsigmax = hist0_NT->GetMaximum();
   
   // --- draw
   
   // create canvas
   TCanvas* c = new TCanvas( "c", "A scan of m_{0} versus m_{12}", 0, 0, CombinationGlob::StandardCanvas[0], CombinationGlob::StandardCanvas[1] );  
  //c->SetGrayscale();

  // create and draw the frame
  TH2F *frame = new TH2F("frame", "m_{0} vs m_{12} - ATLAS work in progress", 100, 400., 1500., 100, 0., 1100. );

  // set common frame style
  CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
  

// set common frame style
  CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
  

  frame->SetXTitle( "m_{#tilde{g}} [GeV]" );
  frame->SetYTitle( "m_{#tilde{#chi}_{1}^{0}} [GeV]" );
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

  //  TLegend *leg = new TLegend(0.7,0.77,0.95,0.915);
  TLegend *leg = new TLegend(0.58,0.68,0.87,0.915);

  leg->SetTextSize( 1.1*CombinationGlob::DescriptionTextSize );
  leg->SetTextFont( 42 );
  leg->SetFillColor( 0 );
  leg->SetFillStyle(1001);

  //bjet_2011(leg);
  Gtt_HCP_3b_exp(leg);
  TGraph* grshadeExp = DrawExpectedBand( gr_contour_ep1s, gr_contour_em1s, CombinationGlob::c_DarkYellow , 1001   , 0)->Clone();
 
      
  if (contour_exp_NT!=0) DrawContourLine95( leg, contour_exp_NT, "", CombinationGlob::c_DarkBlueT3,6);

  if (contour_ep1s_NT!=0) DrawContourLine95( leg, contour_ep1s_NT, "", CombinationGlob::c_DarkYellow, 3 ,2);
  if (contour_em1s_NT!=0) DrawContourLine95( leg, contour_em1s_NT, "", CombinationGlob::c_DarkYellow, 3 ,2);
  DummyLegendExpected(leg, "Expected limit #pm1 #sigma_{exp}",  CombinationGlob::c_DarkYellow, 1001,  CombinationGlob::c_DarkBlueT3, 6, 2);
  if (contour_obs_NT!=0) DrawContourLine95( leg, contour_obs_NT, "Observed limit #pm 1 #sigma^{SUSY}_{Theory}", CombinationGlob::c_DarkRed,1,4);
  if (contour_obs_TP!=0) DrawContourLine95( leg, contour_obs_TP, "", CombinationGlob::c_DarkRed,3,3);
  if (contour_obs_TM!=0) DrawContourLine95( leg, contour_obs_TM, "",  CombinationGlob::c_DarkRed ,3,3); 
	
  //leg->AddEntry(contour_obscls_NT__2,"3 b-jets, 4.7 fb^{-1} at 7 TeV","l");
  leg->AddEntry(contour_exp_NT__4,"3 b-jets (Exp), 12.8 fb^{-1}","l");
 
 TLegend* oldleg;
  oldleg = Gt(300,1100,100,700); //100, 350., 650., 100, 160., 400.
 Gtt_HCP_3b_exp(leg);
  //SSDileptonGtt(leg);
  //LeptonBjet(leg);
  //Multijets(leg);	
  //bjet_2011(leg);
  //CMS(leg);

 
  TLatex *theoreticallyExcl = new TLatex( 500 , 200, "#tilde{g} #rightarrow t#bar{t}+#tilde{#chi}_{1}^{0} forbidden" );
 theoreticallyExcl->SetTextAlign( 11 );
 //  theoreticallyExcl->SetTextSize( CombinationGlob::DescriptionTextSize );
 theoreticallyExcl->SetTextSize(0.04);
 theoreticallyExcl->SetTextColor( 1 );
 theoreticallyExcl->SetTextFont( 42 );
 theoreticallyExcl->SetTextAngle(33);
theoreticallyExcl->AppendPad();	


  
  
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
  TString t1b = "Gtt" ;
  Float_t nbkg(0);
  //if( hist5!=0) nbkg = hist5->GetMaximum();
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
  
  TLatex *Leg0 = new TLatex( xmin, ymax + dy*0.025, "#tilde{g}#tilde{g}  production, #tilde{g} #rightarrow t#bar{t}+#tilde{#chi}_{1}^{0}, m(#tilde{q}) >> m(#tilde{g})" );
  Leg0->SetTextAlign( 11 );
  Leg0->SetTextFont( 42 );
  Leg0->SetTextSize( 1.05*CombinationGlob::DescriptionTextSize);
  Leg0->SetTextColor( 1 );
  Leg0->AppendPad();
  
  TLatex *Leg1 = new TLatex(xmin+690, ymax + dy*0.025, "L^{int} = 20.1 fb^{-1}, #sqrt{s}=8 TeV");
  Leg1->SetTextAlign( 11 );
  Leg1->SetTextFont( 42 );
  Leg1->SetTextSize( 1.05*CombinationGlob::DescriptionTextSize );
  Leg1->SetTextColor( 1 );
   Leg1->AppendPad();
  
  TLatex *Leg2 = new TLatex();
  Leg2->SetNDC();
  Leg2->SetTextAlign( 11 );
  Leg2->SetTextSize( 1.1*CombinationGlob::DescriptionTextSize );
  Leg2->SetTextColor( 1 );
  Leg2->SetTextFont(42);
  if (prefix!=0) { 
    Leg2->DrawLatex(0.16,0.79,prefix); // 0.15,0.81
    Leg2->AppendPad(); 
  }
  TLatex *Leg3 = new TLatex();
  Leg3->SetNDC();
  Leg3->SetTextAlign( 11 );
  Leg3->SetTextSize( 1.1*CombinationGlob::DescriptionTextSize );
  Leg3->SetTextColor( 1 );
  Leg3->SetTextFont(42);
  Leg3->DrawLatex(0.58,0.64,"All limits at 95% CL"); // 0.15,0.81
  Leg3->AppendPad(); 
 
 


  TLatex *atlasLabel = new TLatex();
  atlasLabel->SetNDC();
  atlasLabel->SetTextFont( 72 );
  atlasLabel->SetTextColor( 1 );
  atlasLabel->SetTextSize( 0.05 );
  atlasLabel->DrawLatex(0.16,0.86, "ATLAS"); // 0.15,0.87
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
  // update the canvas
 
  DrawRedBand(leg);	

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

 TLatex *prel = new TLatex();
  prel->SetNDC();
  prel->SetTextFont( 42 );
  prel->SetTextColor( 1 );
  prel->SetTextSize( 0.05 );
  prel->DrawLatex(0.29, 0.86, "Preliminary");   // 0.27,0.87
  prel->AppendPad();

  TString prefixsave = TString(prefix).ReplaceAll(" ","_");
  CombinationGlob::imgconv( c, Form("plots/%s",name.Data()) );   

  ////delete leg;
  ////if (contour!=0) delete contour;
  ////delete frame;
}
