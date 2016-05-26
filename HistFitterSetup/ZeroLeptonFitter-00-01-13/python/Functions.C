#include <vector>
#include <algorithm>
#include <iostream>
//#include <map>
using namespace std;

#include "TLorentzVector.h"

// std::map<std::string, float kappa> kappaMap;
// kappaMap[""] = 1.55
// kappaMap["SRG"] = 1.55
// kappaMap["SRC"] = 1.55
// kappaMap["SRS"] = 2.00

//Can't use a map for some reason
auto kappaMapFunction = [](std::string region){
  if (region == "" )    return 1.55;
  if (region == "SRG" ) return 1.55;
  if (region == "SRC" ) return 1.55;
  if (region == "SRS" ) return 2.00;
};

float gammaCorWeight(int RunNumber, std::string region = "") {
  if (RunNumber >=361039 && RunNumber <= 361061+1)
    return kappaMapFunction(region);//kappaMap[region];//Sherpa MC15
  else return 1.0;
}

