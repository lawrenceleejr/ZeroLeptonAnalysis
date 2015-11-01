#include "contourmacros/CombinationGlob.C"
// MACRO FOR DRAWING TEVATRON EXCLUSION LINES IN SQUARK-GLUINO SPACE
//
// Instructions for use:
// 1. Create a new TCanvas before calling this function.
// 2. Call old_limits(...), specifying the intended x- and y-axis maximum values (this assumes origin at 0,0), and the x- and y-axis labels.
// 3. Draw any other plots over the top.
//
// These limits are mostly relevant with the upper RH corner between (500,500) and (2000,2000).

TLegend* sqgl_oldlim(double xmax = 1000., double ymax = 1000., TString xlabel = TString("m_{#tilde{g}} [GeV]"), TString ylabel = TString("m_{#tilde{q}} [GeV]")){

  // Draw exclusion regions for previous experiments (mainly Tevatron)

  TGraph* g_exc_lep = new TGraph(4);
  g_exc_lep->SetPoint(0,xmax+100,100);
  g_exc_lep->SetPoint(1,xmax+100,0);
  g_exc_lep->SetPoint(2,0,0);
  g_exc_lep->SetPoint(3,0,100);
  g_exc_lep->SetLineColor(CombinationGlob::c_DarkGray);  
  g_exc_lep->SetFillColor(CombinationGlob::c_BlueT1);  
  g_exc_lep->GetXaxis()->SetRangeUser(0,xmax);
  g_exc_lep->GetXaxis()->SetTitle(xlabel.Data());
  g_exc_lep->GetXaxis()->SetLabelSize(0.03);
  g_exc_lep->GetYaxis()->SetRangeUser(0,ymax);
  g_exc_lep->GetYaxis()->SetTitle(ylabel.Data());
  g_exc_lep->GetYaxis()->SetLabelSize(0.03);
  g_exc_lep->GetYaxis()->SetTitleOffset(1.35);
//   Double_t l3x = ymax > 1000 ? 0.85*xmax : 0.75*xmax;
//   Double_t l3y = ymax > 1000 ? 125 : 25;

  TGraph* g_exc_fnal1 = new TGraph(10);
  g_exc_fnal1->SetPoint(0,0,ymax+100);
  g_exc_fnal1->SetPoint(1,190,ymax+100);
  g_exc_fnal1->SetPoint(2,190,330);
  g_exc_fnal1->SetPoint(3,270,250);
  g_exc_fnal1->SetPoint(4,300,300);
  g_exc_fnal1->SetPoint(5,500,200);
  g_exc_fnal1->SetPoint(6,565,150);
  g_exc_fnal1->SetPoint(7,510,100);
  g_exc_fnal1->SetPoint(8,510,0);
  g_exc_fnal1->SetPoint(9,0,0);
  g_exc_fnal1->SetFillColor(CombinationGlob::c_DarkOrange); //SetFillColor(CombinationGlob::c_DHiggsGreen);
  g_exc_fnal1->SetLineColor(CombinationGlob::c_DarkGray);
  g_exc_fnal1->GetXaxis()->SetRangeUser(0,xmax);
  g_exc_fnal1->GetXaxis()->SetTitle(xlabel.Data());
  g_exc_fnal1->GetXaxis()->SetLabelSize(0.03);
  g_exc_fnal1->GetYaxis()->SetRangeUser(0,ymax);
  g_exc_fnal1->GetYaxis()->SetTitle(ylabel.Data());
  g_exc_fnal1->GetYaxis()->SetLabelSize(0.03);
  g_exc_fnal1->GetYaxis()->SetTitleOffset(1.35);
//   Double_t fnx = xmax > 1000 ? 500 : (xmax > 250 ? 200 : 0.75*xmax);
//   Double_t fny = xmax > 1000 ? 225 : 125;

  TGraph* g_exc_cdf = new TGraph(15);
  g_exc_cdf->SetPoint(0,0,ymax+100);
  g_exc_cdf->SetPoint(1,280,ymax+100);
  g_exc_cdf->SetPoint(2,280,560);
  g_exc_cdf->SetPoint(3,284,480);
  g_exc_cdf->SetPoint(4,305,462);
  g_exc_cdf->SetPoint(5,312,417);
  g_exc_cdf->SetPoint(6,333,408);
  g_exc_cdf->SetPoint(7,340,378);
  g_exc_cdf->SetPoint(8,345,380);
  g_exc_cdf->SetPoint(9,390,390);
  g_exc_cdf->SetPoint(10,430,390);
  g_exc_cdf->SetPoint(11,420,380);
  g_exc_cdf->SetPoint(12,300,267);
  g_exc_cdf->SetPoint(13,300,0);
  g_exc_cdf->SetPoint(14,0,0);
  g_exc_cdf->SetFillColor(kRed+0);//(CombinationGlob::c_DarkOrange);
  g_exc_cdf->SetLineColor(CombinationGlob::c_DarkGray);
  g_exc_cdf->GetXaxis()->SetRangeUser(0,xmax);
  g_exc_cdf->GetXaxis()->SetTitle(xlabel.Data());
  g_exc_cdf->GetXaxis()->SetLabelSize(0.03);
  g_exc_cdf->GetYaxis()->SetRangeUser(0,ymax);
  g_exc_cdf->GetYaxis()->SetTitle(ylabel.Data());
  g_exc_cdf->GetYaxis()->SetLabelSize(0.03);
  g_exc_cdf->GetYaxis()->SetTitleOffset(1.35);
//   Double_t cdx = xmax > 1000 ? 500 : (xmax > 250 ? 200 : 0.75*xmax);
//   Double_t cdy = xmax > 1000 ? 225 : 125;

  TGraph* g_exc_d0 = new TGraph(10);
  g_exc_d0->SetPoint(0,0,ymax+100);
  g_exc_d0->SetPoint(1,308,ymax);
  g_exc_d0->SetPoint(2,308,460);
  g_exc_d0->SetPoint(3,320,430);
  g_exc_d0->SetPoint(4,350,400);
  g_exc_d0->SetPoint(5,435,390);
  g_exc_d0->SetPoint(6,310,290);
  g_exc_d0->SetPoint(7,50,50);
  g_exc_d0->SetPoint(8,xmax,0);
  g_exc_d0->SetPoint(9,0,0);
  //g_exc_d0->SetFillColor(CombinationGlob::c_VLightOrange); //c_BlueT5);
  g_exc_d0->SetFillColor(kAzure-4); //c_BlueT5);
  g_exc_d0->SetLineColor(CombinationGlob::c_DarkGray);
  g_exc_d0->GetXaxis()->SetRangeUser(0,xmax);
  g_exc_d0->GetXaxis()->SetTitle(xlabel.Data());
  g_exc_d0->GetXaxis()->SetLabelSize(0.03);
  g_exc_d0->GetYaxis()->SetRangeUser(0,ymax);
  g_exc_d0->GetYaxis()->SetTitle(ylabel.Data());
  g_exc_d0->GetYaxis()->SetLabelSize(0.03);
  g_exc_d0->GetYaxis()->SetTitleOffset(1.35);
//   Double_t d0x = xmax > 1000 ? 375 : (xmax > 250 ? 200 : 0.75*xmax);
//   Double_t d0y = xmax > 1000 ? 425 : 325;
 
  
//   TLegend *leg = new TLegend(0.53,0.55,0.85,0.675);
//   leg->SetTextSize( 0.0265 );
//   leg->SetTextFont( 42 );
//   leg->SetFillStyle(1001);
//   leg->SetFillColor(kWhite);
//   leg->SetBorderSize(0);

//   leg->AddEntry(g_exc_lep,"LEP 2 #tilde{q}","F");
//   leg->AddEntry(g_exc_fnal1,"Tevatron, Run I","F");
//   leg->AddEntry(g_exc_d0,"D0, Run II","F");
//   leg->AddEntry(g_exc_cdf,"CDF, Run II","F");

//   TLatex bracket;
//   bracket.SetTextSize(0.15);
//   bracket.SetTextFont( 132 );
//   bracket.DrawLatex(1550,1085,"}");
//   TLatex msugra;
//   msugra.SetTextSize( 0.0265 );
//   msugra.SetTextFont( 42 );
//   msugra.DrawLatex(1685,1125,"#splitline{MSUGRA /}{CMSSM}");

  // #tilde{g},#tilde{q}

  g_exc_d0->Draw("FSAME");
  g_exc_d0->Draw("LSAME");
  g_exc_cdf->Draw("FSAME");
  g_exc_cdf->Draw("LSAME");
  //g_exc_fnal1->Draw("FSAME");
  //g_exc_fnal1->Draw("LSAME");
  g_exc_lep->Draw("FSAME"); //AFSAME
  g_exc_lep->Draw("LSAME"); //AFSAME
  
  //  leg->Draw();
  
  TLatex leplabel;
  leplabel.SetTextFont( 42 );
  leplabel.SetTextSize(0.03);
  //leplabel.DrawLatex(1500,125,"LEP2  #tilde{q}");

  TLatex tevlabel;
  tevlabel.SetTextSize(0.03);
  tevlabel.SetTextAngle(90);
  tevlabel.SetTextFont( 42 );
  tevlabel.SetTextSize(0.03);
  //tevlabel.DrawLatex(165,450,"Tevatron, Run I");
  tevlabel.DrawLatex(270,585,"CDF, Run II, tan#beta = 5, #mu<0");
  tevlabel.DrawLatex(348,585,"D0, Run II, tan#beta = 3, #mu<0");
  //tevlabel.DrawLatex(375,750,"D0, Run II");


  //leg->AddEntry( d0graph,  "D0 #tilde{g}, #tilde{q}, tan#beta=3, #mu<0, 2.1 fb^{-1}","F" );
  //leg->AddEntry( cdfgraph, "CDF #tilde{g}, #tilde{q}, tan#beta=5, #mu<0, 2 fb^{-1}","F" );                                                                                
  gPad->RedrawAxis();

  //  return leg;
}
