setupATLAS
localSetupROOT

source ./setup.sh

alias mybjobs="bjobs| grep RUN|wc -l;bjobs|wc -l;"
alias go='cd '$PWD 
alias ll='cd ToolKit/Tex; source ./compile.sh; cd -; /bin/cp ToolKit/Tex/Main.pdf .' 

