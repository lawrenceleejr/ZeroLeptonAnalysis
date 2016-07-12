//vim: ts=4 sw=4
//#include "SUSY_m0_vs_m12_all.C"
//#include "SUSY_m0_vs_m12_all_witobs_merged.C"
#include "contourmacros/SUSY_GttOnShell_withBand_cls.C"
//#include "contourmacros/SUSY_gtt_all_witobs_merged_newUncertainties_alaCMS_MatthiasVersion_0lepton.C"

//
//#include "SUSY_m0_vs_m12_all_noobs.C"

void makecontourplots_Gtt(const TString& combo = "all") {
    bool showsignal(false);
    int  discexcl; // 0=discovery, 1=exclusion
    bool showtevatron(false);
    bool doOneSigmaBand(false);

    SUSY_gtt_all_witobs_merged(
            "combined_SUSY12_Gtt_5bin_Nominal__1_harvest_list.root",
            "combined_SUSY12_Gtt_5bin_Up__1_harvest_list.root",
            "combined_SUSY12_Gtt_5bin_Down__1_harvest_list.root",
            "SR", 5.8, showsignal, discexcl=1, 
            "",
            showtevatron, "0 leptons, 2-6 jets");

    return;

}
