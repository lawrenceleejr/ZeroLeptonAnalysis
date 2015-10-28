#include "contourmacros/SUSY_SM_direct_all_withBand_cls.C"
//#include "contourmacros/SUSY_SM_direct_all_withBand_cls_blind.C"

void makecontourplots_direct(const TString& combo = "all", const TString& gridName="", const TString& prefix="", const bool useShape=false, const bool show7TeV=true, 
        const TString& fname_2="", const TString& fname_4="", const TString& fname_8="")
{
    bool showsignal(false);
    int  discexcl=1; // 0=discovery, 1=exclusion
    bool showtevatron(false);
    bool showcms(false);
    bool doOneSigmaBand(true);
    bool showfixSigXSecBand(true);
    bool showSR(true);

    TString comboUp(combo);
    TString comboDown(combo);

    TString fname_2_up(fname_2);
    TString fname_2_down(fname_2);
    TString fname_4_up(fname_4);
    TString fname_4_down(fname_4);
    TString fname_8_up(fname_8);
    TString fname_8_down(fname_8);

    comboUp.ReplaceAll("Nominal", "Up");
    comboDown.ReplaceAll("Nominal", "Down");
    fname_2_up.ReplaceAll("Nominal", "Up");
    fname_2_down.ReplaceAll("Nominal", "Down");
    fname_4_up.ReplaceAll("Nominal", "Up");
    fname_4_down.ReplaceAll("Nominal", "Down");
    fname_8_up.ReplaceAll("Nominal", "Up");
    fname_8_down.ReplaceAll("Nominal", "Down");

    cout << "show7TeV = " << show7TeV << endl;

    (void) SUSY_SM_direct_all_withBand_cls(combo,
            comboUp,
            comboDown,
            gridName,
            prefix,
            20.3, showsignal, discexcl, showtevatron, showcms, doOneSigmaBand, showSR, useShape, show7TeV,
            fname_2,
            fname_4,
            fname_8,
            fname_2_up,
            fname_4_up,
            fname_8_up,
            fname_2_down,
            fname_4_down,
            fname_8_down
            );

    //(void) SUSY_SM_direct_all_withBand_cls_blind(combo,
            //comboUp,
            //comboDown,
            //gridName,
            //prefix,
            //20.3, showsignal, discexcl, showtevatron, showcms, doOneSigmaBand, showSR, useShape, show7TeV,
            //fname_2,
            //fname_4,
            //fname_8);
    return;
}
