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

f=open("Main.tex",'w')
f.write(begin)
f.write("\n")
#f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{plotSR}\\end{tabular}\\end{center}\\end{figure}\n")

#f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{summaryMU}\\end{tabular}\\end{center}\\end{figure}\n")
#f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{summaryNP}\\end{tabular}\\end{center}\\end{figure}\n")

#f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{SummaryPull}\\end{tabular}\\end{center}\\end{figure}\n")

f.write("\\clearpage\n")


for ana in sorted(allChannelsDict.keys()):
    f.write("\\include{yield_"+ana+"}\n")


f.write("\\clearpage\n")
for ana in sorted(allChannelsDict.keys()):
    f.write("\\include{systtable_"+ana+"}\n")


    
f.write("\\clearpage\n")
for ana in sorted(allChannelsDict.keys()):
    f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{histpull_"+ana+"}\\end{tabular}\\end{center}\\end{figure}\n")
    


#f.write("\\clearpage\n")
#for ana in sorted(allChannelsDict.keys()):
#    f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{MU_"+ana+"}\\end{tabular}\\end{center}\\end{figure}\n")


#f.write("\\clearpage\n")
#for ana in sorted(allChannelsDict.keys()):
#    f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{NP_"+ana+"}\\end{tabular}\\end{center}\\end{figure}\n")


#f.write("\\clearpage\n")
#for ana in sorted(allChannelsDict.keys()):
#    f.write("\\begin{figure}[H]\\begin{center}\\begin{tabular}{cc}\\includegraphics[width=1\\textwidth]{corr_"+ana+"}\\end{tabular}\\end{center}\\end{figure}\n")


f.write(end)
