#include <TFile.h>
#include <TH2D.h>
#include <TF2.h>

double m0m12tomgl(double m0, double m12, const char* fname="common/mSugraGridtanbeta30_gluinoSquarkMasses.root", const char* bname="mSugraGrid_gluinoMasses"){
 return m0m12tomglmsq(m0,m12,fname,bname);
}

double m0m12tomsq(double m0, double m12, const char* fname="common/mSugraGridtanbeta30_gluinoSquarkMasses.root", const char* bname="mSugraGrid_squarkMasses"){
 return m0m12tomglmsq(m0,m12,fname,bname);
}

double m0m12tomglmsq(double m0, double m12, const char* fname, const char* bname){
 TFile tf(fname);  
 TH2D* th_mgl = (TH2D*)tf.Get(bname);
 double xmin = m0-150;
 double xmax = m0+150;
 double ymin = m12-20;
 double ymax = m12+20; 
 TF2 tf2("tf2","[0]*x+[1]*y+[2]",xmin,xmax,ymin,ymax);
 th_mgl->Fit("tf2","QN0R");
 return tf2.Eval(m0,m12); 
}

double m0m12tomgl_nuhmg(double in_mH1sq, double in_m12, 
						const char* fname="/afs/cern.ch/user/m/mamuzic/public/TWiki_NUHMG/NUHMG_points.root", 
						const char* tname="NUHMG_points"){
	// Open file, tree
	TFile *infile = TFile::Open(fname);
	TTree* tree = (TTree*)infile->Get(tname);

	// Get branches
	double mH1sq, m12, mgl, goodpoint, out_mgl; 
	TBranch* b_mH1sq     = tree->GetBranch("MH1sq");
	TBranch* b_m12       = tree->GetBranch("M12");
	TBranch* b_mgl       = tree->GetBranch("Mgluino");
	TBranch* b_goodpoint = tree->GetBranch("GoodPoint");
	b_mH1sq->SetAddress(&mH1sq);
	b_m12->SetAddress(&m12);
	b_mgl->SetAddress(&mgl);
	b_goodpoint->SetAddress(&goodpoint);

	// Loop on tree, put conditions, get mgl
	int n = tree->GetEntries();
	for(int i = 0; i < n; ++i) {
		tree->GetEntry(i);
		if(goodpoint < 1) continue;
		if (mH1sq == in_mH1sq && m12 == in_m12)
			out_mgl = mgl;
		//cout << mH1sq << " " << m12 << " " << mgl << endl;
	}
	infile->Close();
	return out_mgl;
}

double m0m12tomsq_nuhmg(double in_mH1sq, double in_m12, 
						const char* fname="/afs/cern.ch/user/m/mamuzic/public/TWiki_NUHMG/NUHMG_points.root", 
						const char* tname="NUHMG_points"){
	// Open file, tree
	TFile *infile = TFile::Open(fname);
	TTree* tree = (TTree*)infile->Get(tname);

	// Get branches
	double mH1sq=0, m12=0, msq=0, goodpoint=0, out_msq=0; 
	TBranch* b_mH1sq     = tree->GetBranch("MH1sq");
	TBranch* b_m12       = tree->GetBranch("M12");
	TBranch* b_msq       = tree->GetBranch("Msquark");
	TBranch* b_goodpoint = tree->GetBranch("GoodPoint");
	b_mH1sq->SetAddress(&mH1sq);
	b_m12->SetAddress(&m12);
	b_msq->SetAddress(&msq);
	b_goodpoint->SetAddress(&goodpoint);

	// Loop on tree, put conditions, get mgl
	int n = tree->GetEntries();
	for(int i = 0; i < n; ++i) {
		tree->GetEntry(i);
		if(goodpoint < 1) continue;
		if (mH1sq == in_mH1sq && m12 == in_m12) 
			out_msq = msq;
		//cout << mH1sq << " " << m12 << " " << msq << endl;
	}
	infile->Close();
	return out_msq;
}

double m0m12tomh_nuhmg(double in_mH1sq, double in_m12, 
						const char* fname="/afs/cern.ch/user/m/mamuzic/public/TWiki_NUHMG/NUHMG_points.root", 
						const char* tname="NUHMG_points"){
	// Open file, tree
	TFile *infile = TFile::Open(fname);
	TTree* tree = (TTree*)infile->Get(tname);

	// Get branches
	double mH1sq=0, m12=0, mh=0, goodpoint=0, out_mh=0; 
	TBranch* b_mH1sq     = tree->GetBranch("MH1sq");
	TBranch* b_m12       = tree->GetBranch("M12");
	TBranch* b_mh       = tree->GetBranch("Mh");
	TBranch* b_goodpoint = tree->GetBranch("GoodPoint");
	b_mH1sq->SetAddress(&mH1sq);
	b_m12->SetAddress(&m12);
	b_mh->SetAddress(&mh);
	b_goodpoint->SetAddress(&goodpoint);

	// Loop on tree, put conditions, get mgl
	int n = tree->GetEntries();
	for(int i = 0; i < n; ++i) {
		tree->GetEntry(i);
		if(goodpoint < 1) continue;
		if (mH1sq == in_mH1sq && m12 == in_m12) 
			out_mh = mh;
		//cout << mH1sq << " " << m12 << " " << mh << endl;
	}
	infile->Close();
	return out_mh;
}


