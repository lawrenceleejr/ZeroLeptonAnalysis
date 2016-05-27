#rm -f *tex
#rm -f *ps
#rm -f *pdf

mv ../../*pdf .;mv ../../*eps .; mv ../../*tex .;
ls *-0.*pdf| awk -F\-0. '{print "mv "$0 "  "$1"-0"$2}'|zsh
python $ZEROLEPTONFITTER/ToolKit/Tex/CreateLatex.py
pdflatex Main.tex;