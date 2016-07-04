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
//THIS IS SO UGLY
auto kappaMapFunction = [](int region){
  // if (region == "Meff" ) return 1.55;
  // if (region == "SRG" )  return 1.55;
  // if (region == "SRC" )  return 1.55;
  // if (region == "SRS" )  return 2.00;


  // if (region == 0 )  return 1.55;
  // if (region == 1 )  return 1.55;
  //  if (region == 2 )  return 3.2;
  // if (region == 3 )  return 2.00;
  return 1.50;
};

float gammaCorWeight(int RunNumber, int regionEnum = 0 ){// std::string region = "Meff") {
  if (RunNumber >=361039 && RunNumber <= 361061+1)
    return kappaMapFunction(regionEnum);//kappaMap[region];//Sherpa MC15
  else return 1.0;
}

