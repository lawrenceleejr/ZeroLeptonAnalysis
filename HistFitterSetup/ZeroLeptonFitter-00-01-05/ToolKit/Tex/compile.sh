#rm -f *tex
#rm -f *ps
#rm -f *pdf

mv ../../*pdf .;mv ../../*eps .; mv ../../*tex .;
python $ZEROLEPTONFITTER/ToolKit/Tex/CreateLatex.py
pdflatex Main.tex;