#!/usr/bin/env python
# usage : 

__doc__ = """

"""

#from AnaList import *
from allChannelsDict import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess





begin="""\\documentclass[landscape,12pt,a4paper]{article}
\\usepackage[landscape]{geometry}
\\usepackage{cite,mcite}
\\usepackage{graphicx}
\\usepackage{subfigure}
\\usepackage{atlasphysics}
\\usepackage{atlas_title,ifthen}
\\usepackage{helvet}

\\def\\atlasnote#1{\\def\\mydocversion{{\\large ATL-#1}}}
\\def\\preprint#1{\\def\\mydocversion{{\\large #1}}}
\\def\\thedate{\\today}

\\newlength{\\capindent}
\\setlength{\\capindent}{0.5cm}
\\newlength{\\capwidth}
\\setlength{\\capwidth}{\\textwidth}
\\addtolength{\\capwidth}{-2\\capindent}
\\newlength{\\figwidth}
\\setlength{\\figwidth}{\\textwidth}
\\addtolength{\\figwidth}{-2.0cm}
\\newcommand{\\icaption}[2][!*!,!]{\\hspace*{\\capindent}%
  \\begin{minipage}{\\capwidth}
    \\ifthenelse{\\equal{#1}{!*!,!}}%
      {\\caption{#2}}%
      {\\caption[#1]{#2}}
      \\vspace*{3mm}
  \\end{minipage}}

% Shorthand for \\phantom to use in tables
\\newcommand{\\pho}{\\phantom{0}}
\\newcommand{\\bslash}{\\ensuremath{\\backslash}}
\\newcommand{\\BibTeX}{{\\sc Bib\\TeX}}
% Upsilon(1S)
\\newcommand{\\UoneS}{\\ensuremath{\\Upsilon(\\mathrm{1S})}}
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Mes commandes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\newcommand{\\ourintlumi}{{20.3\\ }}
\\newcommand{\\ppb}{\\mbox{\\ensuremath{p\\bar p}}}
\\newcommand{\\invpb}{pb$^{-1}$}
\\newcommand{\\etadet}{\\mbox{\\ensuremath{\\eta_\\mathrm{det}}}}
\\newcommand{\\zdca}{\\mbox{\\ensuremath{z_\\mathrm{DCA}}}}
\\newcommand{\\rdca}{\\mbox{\\ensuremath{r_\\mathrm{DCA}}}}
\\newcommand{\\ptgam}{\\mbox{\\ensuremath{p_{T}^\\gamma}}}
\\newcommand{\\ptZ}{\\mbox{\\ensuremath{p_{T}^Z}}}
\\newcommand{\\ptjet}{\\mbox{\\ensuremath{p_{T}^\\mathrm{jet}}}}
\\newcommand{\\etadetjet}{\\mbox{\\ensuremath{\\eta_\\mathrm{det}^\\mathrm{jet}}}}
\\newcommand{\\zee}{\\mbox{\\ensuremath{Z \\to ee }}}
\\newcommand{\\pythia}{{\\sc PYTHIA}}
\\def\\Ereco{\\ensuremath{E^{\\mathrm{reco}}}}
\\def\\Etrue{\\ensuremath{E^{\\mathrm{true}}}}
\\def\\Mreco{\\ensuremath{M^{\\mathrm{reco}}}}
\\def\\Mtrue{\\ensuremath{M^{\\mathrm{true}}}}
\\def\\bias{\\mathrm{bias}}
\\def\\fit{\\mathrm{fit}}
\\def\\inj{\\mathrm{inj}}
\\def\\reco{\\mathrm{reco}}
\\def\\gen{\\mathrm{gen}}
\\def\\true{\\mathrm{true}}
\\def\\NDF{\\ensuremath{\\mathrm{NDF}}}
%\\newcommand{\\antikt}{\\mbox{\\ensuremath{Anti-K_{T}}}}
\\newcommand{\\antikt}{\\mbox{Anti-K\\ensuremath{_T}}}

\\def\\figpath{Plots}

\\newdimen\\figsize
\\setlength\\figsize{\\hsize}%

\\newdimen\\fullfigsize
\\setlength\\fullfigsize{\\hsize}%

\\long\\def\\twoboxesgap#1#2#3{%
  \\setlength\\figsize{\\hsize}%
  \\addtolength\\figsize{-#3}%
  \\divide\\figsize by 2
  \\vbox{%
  \\makebox{\\parbox[t]{\\figsize}{\\vskip 0.1pt #1}%
           \\hspace{#3}%
           \\parbox[t]{\\figsize}{\\vskip 0.1pt #2}}}}

% This command sets its two arguments in two side-by-side parboxes.
% The widths of the boxes are set to fill the page width, with a
% a gap of 2\\columnsep between them.
\\long\\def\\twoboxes#1#2{\\twoboxesgap{#1}{#2}{2\\columnsep}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is where the document really begins
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\\begin{document}"""

end="""
\end{document}
"""

f=open("ValPlots.tex",'w')
f.write(begin)
f.write("\n")

anaImInterestedIn=['SR2jvl', 'SR2jvt', 'SR4jAp']

lumi=3000.

version=34
oldversion=27
compare=(True if oldversion>32 else False)


kindOfCuts_SR=[
        {"type":"SR","var":["nJets","nJets60all","nbJets","met","metSig","mettrack","mettrack_phi"]},        
        {"type":"SR_no_meffcut","var":["meffincl"]},
        {"type":"SR_no_dphicut","var":["dphi"]},
        {"type":"SR_no_JetpT1cut","var":["jetpT1"]},
        {"type":"SR_no_JetpT2cut","var":["jetpT2"]},
        {"type":"SR_no_JetpT3cut","var":["jetpT3"]},
        {"type":"SR_no_JetpT4cut","var":["jetpT4"]},
        {"type":"SR_no_Apcut","var":["Ap"]},
        {"type":"SR_no_metomeffcut","var":["metomeff2jet","metomeff4jet"]},
        ]

kindOfCuts_CRWT=[
        {"type":"CRW_no_meffcut","var":["meffincl"]},
        {"type":"CRW","var":["nJets",'nJets60all',"nbJets","dphi","met","metSig","metomeff2jet","metomeff4jet","lep1Pt","lep1Eta","lep1Phi","lep1sign","mt","Wpt","Ap","mettrack","mettrack_phi"]},
        {"type":"CRT_no_meffcut","var":["meffincl"]},
        {"type":"CRT","var":["nJets","nbJets","dphi","met","metSig","metomeff2jet","metomeff4jet","lep1Pt","lep1Eta","lep1Phi","lep1sign","mt","Wpt","Ap","mettrack","mettrack_phi"]},

        ]

kindOfCuts_CRY=[
        {"type":"CRY_no_meffcut","var":["meffincl"]},
        {"type":"CRY","var":["nJets",'nJets60all',"dphi","met","metSig","metomeff2jet","metomeff4jet","phPt","phEta","phPhi","phSignal","Ap","mettrack","mettrack_phi","origmet","origmetPhi"]},
        ]

kindOfCuts_CRZ=[
        {"type":"CRZ_no_meffcut","var":["meffincl"]},
        {"type":"CRZ","var":["nJets",'nJets60all',"dphi","met","metSig","metomeff2jet","metomeff4jet","lep1Pt", "lep2Pt", "lep1Eta", "lep2Eta", "lep1Phi", "lep2Phi","lep1sign","lep2sign","llsign","mll","Zpt"]},
        ]


if version<32:
        kindOfCuts_SR=[
                {"type":"SR_no_meffcut","var":["meffincl"]},
                {"type":"SR","var":["nJets","nbJets","met"]},
                {"type":"SR_no_dphicut","var":["dphi"]},
                {"type":"SR_no_JetpT1cut","var":["jetpT1"]},
                {"type":"SR_no_JetpT2cut","var":["jetpT2"]},
                {"type":"SR_no_JetpT3cut","var":["jetpT3"]},
                {"type":"SR_no_JetpT4cut","var":["jetpT4"]},
                {"type":"SR_no_Apcut","var":["Ap"]},
                {"type":"SR_no_metomeffcut","var":["metomeff2jet","metomeff4jet","met"]},
                ]
        
        kindOfCuts_CRWT=[
                {"type":"CRW_no_meffcut","var":["meffincl"]},
                {"type":"CRW","var":["nJets","nbJets","dphi","met","metomeff2jet","metomeff4jet"]},
                {"type":"CRT_no_meffcut","var":["meffincl"]},
                {"type":"CRT","var":["nJets","nbJets","dphi","met","metomeff2jet","metomeff4jet"]},
                ]
        
        kindOfCuts_CRY=[
                {"type":"CRY_no_meffcut","var":["meffincl"]},
                {"type":"CRY","var":["nJets","dphi","met","metomeff2jet","metomeff4jet"]},
                ]
        
        kindOfCuts_CRZ=[
                {"type":"CRZ_no_meffcut","var":["meffincl"]},
                {"type":"CRZ","var":["nJets","dphi","met","metomeff2jet","metomeff4jet"]},
                ]

kindOfCuts=kindOfCuts_SR+kindOfCuts_CRWT+kindOfCuts_CRY+kindOfCuts_CRZ


for ana in sorted(anaImInterestedIn):
        for whichKind in kindOfCuts:
                for varname in (whichKind['var']):

                        if compare: f.write("{\\bf "+varname+": v"+str(version)+((" (on left) vs. v"+str(oldversion)+" (on right)}") if compare else "")+"\\\\")
                        region=whichKind['type'].split("_no")[0]
                        plotname=str('intL%0difb' % (float(lumi)/1000.))+"_"+region+"_"+ana+"_"+varname+"_"+whichKind['type']
                        name="../../Outplots/v"+str(version)+"/"+plotname
                        oldname="../../Outplots/v"+str(oldversion)+"/"+plotname
                        if compare:
                                f.write("{\\bf "+whichKind['type'].replace("_","\_")+" for "+ana.replace("_","\_")+"}\\\\")
                                f.write("{\\bf Plot name: "+plotname.replace("_","\_")+"}")                                
                                f.write("\\begin{figure}[htb]\\begin{minipage}{0.5\\hsize}\\begin{center}\\includegraphics[width=1.0\\textwidth]{"+name+"}\\end{center}\\end{minipage}\\begin{minipage}{0.5\\hsize}\\begin{center}\\includegraphics[width=1.0\\textwidth]{"+oldname+"}\\end{center}\\end{minipage}\\end{figure}\n")
                        else:
                                f.write("\\begin{figure}[htb]\\begin{minipage}{0.9\\hsize}\\begin{center}\\includegraphics[width=0.8\\textwidth]{"+name+"}\\end{center}\\end{minipage}\\caption{"+(("{\\bf "+whichKind['type'].replace("_","\_")+" for "+ana.replace("_","\_")+"} "))+("{\\bf Plot name: "+plotname.replace("_","\_")+"}")+"}\\end{figure}\n")
                        f.write("\\clearpage\n")  

f.write(end)
