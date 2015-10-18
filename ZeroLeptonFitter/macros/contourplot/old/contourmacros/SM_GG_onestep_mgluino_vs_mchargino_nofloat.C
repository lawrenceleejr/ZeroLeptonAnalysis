#include "contourmacros/CombinationGlob.C"
#include "TROOT.h"
#include "TColor.h"

void initialize(TString fileName) {
//  if(fileName.Contains("SS_onestep"))  gROOT->ProcessLine(".L summary_harvest_tree_description_SS.h+");
//  else gROOT->ProcessLine(".L summary_harvest_tree_description_GG.h+");
  gROOT->ProcessLine(".L summary_harvest_tree_description.h+");
  gSystem->Load("libSusyFitter.so");
}


const char* SM_GG_onestep_mgluino_vs_mchargino_nofloat(const char* textfile = 0, TH2D* inputHist = 0, const char* rootfile = "mgluinomchargino_nofloat.root", TString id1="mgluino",TString id2="mchargino", int   nbinsX=100,int nbinsY=100, float minX=0,float maxX=1600, float minY=0, float maxY=1600)
{
   // set combination style and remove existing canvas'
   CombinationGlob::Initialize();

   initialize(textfile);

   // get the harvested tree
   TTree* tree = harvesttree( textfile!=0 ? textfile : 0 );
   if (tree==0) { 
     cout << "Cannot open list file. Exit." << endl;
     return;
   }

   // store histograms to output file
   const char* outfile(0);
   if (textfile!=0) {
     TObjArray* arr = TString(textfile).Tokenize("/");
     TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
     outfile = Form("%s%s",objstring->GetString().Data(),".root");
     delete arr;
   } else {
     outfile = rootfile;
   }

   cout << "Histograms being written to : " << outfile << endl;
   TFile* output = TFile::Open(outfile,"RECREATE");
   output->cd();
   
   TString correlation="mchargino:mgluino";
   TString fileName= textfile;
   if (fileName.Contains("SS_onestep")) correlation="mchargino:msquark"; 
   
   
   if (inputHist!=NULL){
     TH2D *clonehclPmin2=(TH2D*)inputHist->Clone();
     TH2D* hist = DrawUtil::triwsmooth( tree, "p1:"+correlation, "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1", clonehclPmin2 );}
     //TH2D* hist = DrawUtil::triwsmooth( tree, "p1:mchargino:mgluino", "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1", clonehclPmin2 );}
   else{
     //TH2D* hist = DrawUtil::triwsmooth( tree, "p1:mchargino:mgluino", "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1", inputHist);}
     TH2D* hist = DrawUtil::triwsmooth( tree,"p1:"+correlation , "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1", inputHist);}


   if (hist!=0) {
     hist->Write();
     delete hist; hist=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }




   if (inputHist!=NULL){
     TH2D *clonesigp1=(TH2D*)inputHist->Clone();
     //TH2D* sigp1 = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p1):mchargino:mgluino", "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)", clonesigp1 );}
     TH2D* sigp1 = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p1):"+correlation, "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)", clonesigp1 );}

   else{
     //TH2D* sigp1 = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p1):mchargino:mgluino", "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)", inputHist );}
     TH2D* sigp1 = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p1):"+correlation, "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)", inputHist );}

   if (sigp1!=0) {
     sigp1->Write();
     delete sigp1; sigp1=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   // cls:clsexp:clsu1s:clsd1s

   if (inputHist!=NULL){
     TH2D *clonep1clsf=(TH2D*)inputHist->Clone();
     //TH2D* p1clsf = DrawUtil::triwsmooth( tree, "CLs:mchargino:mgluino", "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1", clonep1clsf );}
     TH2D* p1clsf = DrawUtil::triwsmooth( tree, "CLs:"+correlation, "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1", clonep1clsf );}
   else{
     //TH2D* p1clsf = DrawUtil::triwsmooth( tree, "CLs:mchargino:mgluino", "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1", inputHist );
     TH2D* p1clsf = DrawUtil::triwsmooth( tree, "CLs:"+correlation, "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1", inputHist );
  }


   if (p1clsf!=0) {
     p1clsf->Write();
     delete p1clsf; p1clsf=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


   if (inputHist!=NULL){
     TH2D *clonesigp1clsf=(TH2D*)inputHist->Clone();
     //TH2D* sigp1clsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLs ):mchargino:mgluino", "sigp1clsf" , "One-sided significalce of observed CLs", "p1>0 && p1<=1",clonesigp1clsf );}
     TH2D* sigp1clsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLs ):"+correlation, "sigp1clsf" , "One-sided significalce of observed CLs", "p1>0 && p1<=1",clonesigp1clsf );}
   else{
     //TH2D* sigp1clsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLs ):mchargino:mgluino", "sigp1clsf" , "One-sided significalce of observed CLs", "p1>0 && p1<=1", inputHist );}
     TH2D* sigp1clsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLs ):"+correlation, "sigp1clsf" , "One-sided significalce of observed CLs", "p1>0 && p1<=1", inputHist );}


   if (sigp1clsf!=0) {
     sigp1clsf->Write();
     delete sigp1clsf; sigp1clsf=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   if (inputHist!=NULL){
     TH2D *clonesigp1expclsf=(TH2D*)inputHist->Clone();
     //TH2D* sigp1expclsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLsexp ):mchargino:mgluino", "sigp1expclsf" , "One-sided significalce of expected CLs", "p1>0 && p1<=1", clonesigp1expclsf );}
     TH2D* sigp1expclsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLsexp ):"+correlation, "sigp1expclsf" , "One-sided significalce of expected CLs", "p1>0 && p1<=1", clonesigp1expclsf );}
   else{
     //TH2D* sigp1expclsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLsexp ):mchargino:mgluino", "sigp1expclsf" , "One-sided significalce of expected CLs", "p1>0 && p1<=1", inputHist );}
     TH2D* sigp1expclsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLsexp ):"+correlation, "sigp1expclsf" , "One-sided significalce of expected CLs", "p1>0 && p1<=1", inputHist );}
   

   if (sigp1expclsf!=0) {
     sigp1expclsf->Write();
     delete sigp1expclsf; sigp1expclsf=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   if (inputHist!=NULL){
     TH2D *clonesigclsu1s=(TH2D*)inputHist->Clone();
     //TH2D* sigclsu1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsu1s):mchargino:mgluino", "sigclsu1s" , "One-sided significalce of expected CLs (+1 sigma)", "clsu1s>0", clonesigclsu1s );}
     TH2D* sigclsu1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsu1s):"+correlation, "sigclsu1s" , "One-sided significalce of expected CLs (+1 sigma)", "clsu1s>0", clonesigclsu1s );}
   else{
     //TH2D* sigclsu1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsu1s):mchargino:mgluino", "sigclsu1s" , "One-sided significalce of expected CLs (+1 sigma)", "clsu1s>0", inputHist );}
     TH2D* sigclsu1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsu1s):"+correlation, "sigclsu1s" , "One-sided significalce of expected CLs (+1 sigma)", "clsu1s>0", inputHist );}

   if (sigclsu1s!=0) {
     sigclsu1s->Write();
     delete sigclsu1s; sigclsu1s=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

  if (inputHist!=NULL){
     TH2D *clonesigclsd1s=(TH2D*)inputHist->Clone();
     //TH2D* sigclsd1s = DrawUtil::triwsmooth( tree , "StatTools::GetSigma(clsd1s):mchargino:mgluino", "sigclsd1s" , "One-sided significalce of expected CLs (-1 sigma)", "clsd1s>0",clonesigclsd1s );}
     TH2D* sigclsd1s = DrawUtil::triwsmooth( tree , "StatTools::GetSigma(clsd1s):"+correlation, "sigclsd1s" , "One-sided significalce of expected CLs (-1 sigma)", "clsd1s>0",clonesigclsd1s );}
   else{
     //TH2D* sigclsd1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsd1s):mchargino:mgluino", "sigclsd1s" , "One-sided significalce of expected CLs (-1 sigma)", "clsd1s>0", inputHist );}
     TH2D* sigclsd1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsd1s):"+correlation, "sigclsd1s" , "One-sided significalce of expected CLs (-1 sigma)", "clsd1s>0", inputHist );}
   if (sigclsd1s!=0) {
     sigclsd1s->Write();
     delete sigclsd1s; sigclsd1s=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


   ///////////////////////////////////////////////////// upper limit * cross section plots

  if (inputHist!=NULL){
     TH2D *cloneupperlimit=(TH2D*)inputHist->Clone();
     //TH2D* UpperLimit = DrawUtil::triwsmooth( tree, "upperLimit:mchargino:mgluino", "upperLimit" , "upperlimit","1", cloneupperlimit);}
     TH2D* UpperLimit = DrawUtil::triwsmooth( tree, "upperLimit:"+correlation, "upperLimit" , "upperlimit","1", cloneupperlimit);}
   else{
     //TH2D* UpperLimit = DrawUtil::triwsmooth( tree, "upperLimit:mchargino:mgluino", "upperLimit" , "upperlimit","1", inputHist);}
     TH2D* UpperLimit = DrawUtil::triwsmooth( tree, "upperLimit:"+correlation, "upperLimit" , "upperlimit","1", inputHist);}


   if (UpperLimit!=0) {
     UpperLimit->Write();
     delete UpperLimit; UpperLimit=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


  if (inputHist!=NULL){
     TH2D *clonexsec=(TH2D*)inputHist->Clone();
     //TH2D* xsec = DrawUtil::triwsmooth( tree, "xsec:mchargino:mgluino", "xsec" , "xsec","1", clonexsec);}   
     TH2D* xsec = DrawUtil::triwsmooth( tree, "xsec:"+correlation, "xsec" , "xsec","1", clonexsec);}   
   else{
     //TH2D* xsec = DrawUtil::triwsmooth( tree, "xsec:mchargino:mgluino", "xsec" , "xsec","1", inputHist);}
     TH2D* xsec = DrawUtil::triwsmooth( tree, "xsec:"+correlation, "xsec" , "xsec","1", inputHist);}


   if (xsec!=0) {
     xsec->Write();
     delete xsec; xsec=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }
   
  if (inputHist!=NULL){
     TH2D *cloneexcludedXsec=(TH2D*)inputHist->Clone();
     //TH2D* excludedXsec = DrawUtil::triwsmooth( tree, "excludedXsec:mchargino:mgluino", "excludedXsec" , "excludedXsec","1", cloneexcludedXsec);}
     TH2D* excludedXsec = DrawUtil::triwsmooth( tree, "excludedXsec:"+correlation, "excludedXsec" , "excludedXsec","1", cloneexcludedXsec);}
   else{
     //TH2D* excludedXsec = DrawUtil::triwsmooth( tree, "excludedXsec:mchargino:mgluino", "excludedXsec" , "excludedXsec","1", inputHist);}
     TH2D* excludedXsec = DrawUtil::triwsmooth( tree, "excludedXsec:"+correlation, "excludedXsec" , "excludedXsec","1", inputHist);}


   if (excludedXsec!=0) {
     excludedXsec->Write();
     delete excludedXsec; excludedXsec=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


   ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   output->Close();
   //if (output!=0) { delete output; output=0; }
   cout << "Done." << endl;

   return outfile;
}

