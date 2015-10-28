source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
source ${ATLAS_LOCAL_ROOT_BASE}/packageSetups/atlasLocalROOTSetup.sh  --rootVersion=5.34.19-x86_64-slc6-gcc47-opt

MYHERE=$PWD
cd ../HistFitter-00-00-42/
source setup.sh
cd $MYHERE
source setup.sh

alias mybjobs="bjobs| grep RUN|wc -l;bjobs|wc -l;"
alias saveDir="~/Scripts/saveDirLXPLUS.sh . ZLFitter"
alias go='cd '$PWD 
alias ll='cd ToolKit/Tex; source ./compil.sh; cd -' 