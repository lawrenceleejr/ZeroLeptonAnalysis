void CopyDir(TDirectory *source,bool doSource2) {
   //copy all objects and subdirs of directory source as a subdir of the current directory

   TDirectory *savdir = gDirectory;
   //TDirectory *adir = savdir->mkdir(source->GetName());
   //adir->cd();

   //loop on all entries of this directory
   TKey *key;
   TIter nextkey(source->GetListOfKeys());
   while ((key = (TKey*)nextkey())) {

     if( TString(key->GetName()) == TString("Z_SRAll") ){
      continue;
     }

	if(doSource2){
     if( TString(key->GetName()).Contains("Data_CRY")  == 0 ){
      continue;
     }
	}


      const char *classname = key->GetClassName();
      TClass *cl = gROOT->GetClass(classname);
      if (!cl) continue;
      if (cl->InheritsFrom(TDirectory::Class())) {
         source->cd(key->GetName());
         TDirectory *subdir = gDirectory;
         savdir->cd();
         CopyDir(subdir, doSource2);
         savdir->cd();
      } else if (cl->InheritsFrom(TTree::Class())) {
         TTree *T = (TTree*)source->Get(key->GetName());
         savdir->cd();
         TTree *newT = T->CloneTree(-1,"fast");
         newT->Write();
      } else {
         source->cd();
         TObject *obj = key->ReadObj();
         savdir->cd();
           obj->Write("Z_SRAll");
         
         delete obj;
     }
  }
  savdir->SaveSelf(kTRUE);
  savdir->cd();
}

// Test
void fuckThePolice()
{
  TFile* source = new TFile("Zjets.root.bkup");
  TFile* source2 = new TFile("Data_Nov11.root");

  TFile* dest = new TFile("Zjets.new.root","recreate");
  
  dest->cd();
  CopyDir(source,0);
  CopyDir(source2,1);
  
  std::cout << "Before close " << endl;

  source->Close();
  dest->Close();
  
  std::cout << "After close " << endl;
}
