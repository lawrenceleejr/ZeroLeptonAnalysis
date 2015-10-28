#include "contourmacros/SUSY_Gluino_Stop_charm_withBand_cls.C"
//#include "contourmacros/SUSY_Gluino_Stop_charm_withBand_cls_expOnly.C"

void makecontourplots_Gluino_Stop_charm(const TString& combo = "all", bool useShape=false)  {
    bool showsignal(false);
    int  discexcl; // 0=discovery, 1=exclusion
    bool doOneSigmaBand(true);
    bool showfixSigXSecBand(true);
    int applyfix(0);
    bool showSR(true);
    bool showtevatron(false);

    const char *plottitle;
    if(useShape)
        plottitle = "0 leptons, 2-6 jets, 5-bin";
    else
        plottitle = "0 leptons, 2-6 jets";
        
    TString comboUp(combo);
    TString comboDown(combo);

    comboUp.ReplaceAll("Nominal", "Up");
    comboDown.ReplaceAll("Nominal", "Down");

    SUSY_gtt_all_witobs_merged(
                            combo,
                            comboUp, //comboUp,
                            comboDown, //comboDown,
                            "SR", 15, showsignal, discexcl=1, 
                            "",
                            showtevatron, 
                            plottitle, showSR, useShape);


    return;

}
