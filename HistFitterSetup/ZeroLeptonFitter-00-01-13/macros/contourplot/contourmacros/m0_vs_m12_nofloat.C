//#include "contourmacros/CombinationGlob.C"
#include "CombinationGlob.C"
#include "TROOT.h"
#include "TColor.h"
#include "summary_harvest_tree_description.h"

void initialize() {
  gROOT->ProcessLine(".L summary_harvest_tree_description.h+");
  gSystem->Load("libSusyFitter.so");
}


const char*
m0_vs_m12_nofloat(const char* textfile = 0, TH2D* inputHist = 0, const char* rootfile = "m0m12_nofloat.root", TString id1="m0",TString id2="m12", int   nbinsX=21,int nbinsY=17, float minX=20,float maxX=860, float minY=92.5, float maxY=347.5)
{
   // set combination style and remove existing canvas'
   CombinationGlob::Initialize();

   initialize();

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
   
   if (inputHist!=NULL){
     TH2D *clonehclPmin2=(TH2D*)inputHist->Clone();
     TH2D* hist = DrawUtil::triwsmooth( tree, "p1:m12:m0", "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1", clonehclPmin2 );}
   else{
     TH2D* hist = DrawUtil::triwsmooth( tree, "p1:m12:m0", "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1", inputHist);}


   if (hist!=0) {
     hist->Smooth();
     hist->Write();
     delete hist; hist=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }




   if (inputHist!=NULL){
     TH2D *clonesigp1=(TH2D*)inputHist->Clone();
     TH2D* sigp1 = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p1):m12:m0", "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)", clonesigp1 );}
   else{
     TH2D* sigp1 = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p1):m12:m0", "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)", inputHist );}

   if (sigp1!=0) {
     sigp1->Smooth();
     sigp1->Write();
     delete sigp1; sigp1=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   if (inputHist!=NULL){
      TH2D *clonep0exp=(TH2D*)inputHist->Clone();
      TH2D* p0exp = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p0exp):m12:m0", "p0exp" , "One-sided significance p0 (exp)", "(p0exp>0 && p0exp<=1)", clonep0exp );}
   else{
      TH2D* p0exp = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(p0exp):m12:m0", "p0exp" , "One-sided significance p0 (exp)", "(p0exp>0 && p0exp<=1)", inputHist );}
   
   if (p0exp!=0) {
      p0exp->Smooth();
      p0exp->Write();
      delete p0exp; p0exp=0;
   } else {
      cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   if (inputHist!=NULL){
      TH2D *clonep0expraw=(TH2D*)inputHist->Clone();
      TH2D* p0expraw = DrawUtil::triwsmooth( tree, "p0exp:m12:m0", "p0expraw" , "One-sided significance p0 (exp)", "(p0exp>0 && p0exp<=1)", clonep0expraw );}
   else{
      TH2D* p0expraw = DrawUtil::triwsmooth( tree, "p0exp:m12:m0", "p0expraw" , "One-sided significance p0 (exp)", "(p0exp>0 && p0exp<=1)", inputHist );}
   
   if (p0expraw!=0) {
      p0expraw->Smooth();
      p0expraw->Write();
      delete p0expraw; p0expraw=0;
   } else {
      cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   // cls:clsexp:clsu1s:clsd1s

   if (inputHist!=NULL){
     TH2D *clonep1clsf=(TH2D*)inputHist->Clone();
     TH2D* p1clsf = DrawUtil::triwsmooth( tree, "CLs:m12:m0", "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1", clonep1clsf );}
   else{
     TH2D* p1clsf = DrawUtil::triwsmooth( tree, "CLs:m12:m0", "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1", inputHist );
   }


   if (p1clsf!=0) {
     p1clsf->Smooth();
     p1clsf->Write();
     delete p1clsf; p1clsf=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


   if (inputHist!=NULL){
     TH2D *clonesigp1clsf=(TH2D*)inputHist->Clone();
     TH2D* sigp1clsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLs ):m12:m0", "sigp1clsf" , "One-sided significance of observed CLs", "p1>0 && p1<=1",clonesigp1clsf );}
   else{
     TH2D* sigp1clsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLs ):m12:m0", "sigp1clsf" , "One-sided significance of observed CLs", "p1>0 && p1<=1", inputHist );}


   if (sigp1clsf!=0) {
     sigp1clsf->Smooth();
     sigp1clsf->Write();
     delete sigp1clsf; sigp1clsf=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   if (inputHist!=NULL){
     TH2D *clonesigp1expclsf=(TH2D*)inputHist->Clone();
     TH2D* sigp1expclsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLsexp ):m12:m0", "sigp1expclsf" , "One-sided significance of expected CLs", "p1>0 && p1<=1", clonesigp1expclsf );}
   else{
     TH2D* sigp1expclsf = DrawUtil::triwsmooth( tree, "StatTools::GetSigma( CLsexp ):m12:m0", "sigp1expclsf" , "One-sided significance of expected CLs", "p1>0 && p1<=1", inputHist );}
   

   if (sigp1expclsf!=0) {
     sigp1expclsf->Smooth();
     sigp1expclsf->Write();
     delete sigp1expclsf; sigp1expclsf=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

   if (inputHist!=NULL){
     TH2D *clonesigclsu1s=(TH2D*)inputHist->Clone();
     TH2D* sigclsu1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsu1s):m12:m0", "sigclsu1s" , "One-sided significance of expected CLs (+1 sigma)", "clsu1s>0", clonesigclsu1s );}
   else{
     TH2D* sigclsu1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsu1s):m12:m0", "sigclsu1s" , "One-sided significance of expected CLs (+1 sigma)", "clsu1s>0", inputHist );}

   if (sigclsu1s!=0) {
     sigclsu1s->Smooth();
     sigclsu1s->Write();
     delete sigclsu1s; sigclsu1s=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

  if (inputHist!=NULL){
     TH2D *clonesigclsd1s=(TH2D*)inputHist->Clone();
     TH2D* sigclsd1s = DrawUtil::triwsmooth( tree , "StatTools::GetSigma(clsd1s):m12:m0", "sigclsd1s" , "One-sided significance of expected CLs (-1 sigma)", "clsd1s>0",clonesigclsd1s );}
   else{
     TH2D* sigclsd1s = DrawUtil::triwsmooth( tree, "StatTools::GetSigma(clsd1s):m12:m0", "sigclsd1s" , "One-sided significance of expected CLs (-1 sigma)", "clsd1s>0", inputHist );}
   if (sigclsd1s!=0) {
     sigclsd1s->Smooth();
     sigclsd1s->Write();
     delete sigclsd1s; sigclsd1s=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


   ///////////////////////////////////////////////////// upper limit * cross section plots

  if (inputHist!=NULL){
     TH2D *cloneupperlimit=(TH2D*)inputHist->Clone();
     TH2D* UpperLimit = DrawUtil::triwsmooth( tree, "upperLimit:m12:m0", "upperLimit" , "upperlimit","1", cloneupperlimit);}
   else{
     TH2D* UpperLimit = DrawUtil::triwsmooth( tree, "upperLimit:m12:m0", "upperLimit" , "upperlimit","1", inputHist);}


   if (UpperLimit!=0) {
     UpperLimit->Smooth();
     UpperLimit->Write();
     delete UpperLimit; UpperLimit=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }

 
  if (inputHist!=NULL){
     TH2D *cloneexpectedUpperlimit=(TH2D*)inputHist->Clone();
     TH2D* ExpectedUpperLimit = DrawUtil::triwsmooth( tree, "expectedUpperLimit:m12:m0", "expectedUpperLimit" , "expectedUpperlimit","1", cloneexpectedUpperlimit);}
   else{
     TH2D* ExpectedUpperLimit = DrawUtil::triwsmooth( tree, "expectedUpperLimit:m12:m0", "expectedUpperLimit" , "expectedUpperlimit","1", inputHist);}


   if (ExpectedUpperLimit!=0) {
     ExpectedUpperLimit->Smooth();
     ExpectedUpperLimit->Write();
     delete ExpectedUpperLimit; ExpectedUpperLimit=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }


  if (inputHist!=NULL){
     TH2D *clonexsec=(TH2D*)inputHist->Clone();
     TH2D* xsec = DrawUtil::triwsmooth( tree, "xsec:m12:m0", "xsec" , "xsec","1", clonexsec);}   
   else{
     TH2D* xsec = DrawUtil::triwsmooth( tree, "xsec:m12:m0", "xsec" , "xsec","1", inputHist);}


   if (xsec!=0) {
     xsec->Smooth();
     xsec->Write();
     delete xsec; xsec=0;
   } else {
     cout << "Cannot make smoothed significance histogram. Exit." << endl;
   }
   
  if (inputHist!=NULL){
     TH2D *cloneexcludedXsec=(TH2D*)inputHist->Clone();
     TH2D* excludedXsec = DrawUtil::triwsmooth( tree, "excludedXsec:m12:m0", "excludedXsec" , "excludedXsec","1", cloneexcludedXsec);}
   else{
     TH2D* excludedXsec = DrawUtil::triwsmooth( tree, "excludedXsec:m12:m0", "excludedXsec" , "excludedXsec","1", inputHist);}


   if (excludedXsec!=0) {
     excludedXsec->Smooth();
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

