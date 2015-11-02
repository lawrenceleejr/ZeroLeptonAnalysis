#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

#include "TLorentzVector.h"

float gammaCorWeight(int RunNumber) {
  if (RunNumber >=177575 && RunNumber <= 177585)
    return 1.20;//Sherpa DC14
  else return 1.0;
}

