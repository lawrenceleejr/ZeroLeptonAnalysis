#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

#include "TLorentzVector.h"

float gammaCorWeight(int RunNumber) {
  if (RunNumber >=361039 && RunNumber <= 361061+1)
    return 1.6;//Sherpa MC15
  else return 1.0;
}

