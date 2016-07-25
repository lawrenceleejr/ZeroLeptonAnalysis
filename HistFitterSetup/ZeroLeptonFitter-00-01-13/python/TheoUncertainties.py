#######################################
# The uncertainties in this file are the
# uncertainties on the transfer factor
#######################################

def getError(channelName, regionName, sysDict):
    error = 0
    #print "toto"
    #print sysDict
    if (channelName,regionName) in sysDict.keys():
        error = sysDict[(channelName,regionName)]
    elif ("default","default") in sysDict.keys():
        error = sysDict[("default","default")]
    return error


#######################################
#Diboson
#######################################
dibosonFlatSysDict = {}
dibosonFlatSysDict[("default","default")] = 0.50

#######################################
#Z+jets
#######################################
# Sherpa vs MadGraph
zTheoSysGeneratorDict = {}
zTheoSysGeneratorDict[("default","default")] = 0.11
# zTheoSysGeneratorDict[("SR2jl","SR")]= -0.0492965028609
# zTheoSysGeneratorDict[("SR2jm","SR")]= -0.0370988518057
# zTheoSysGeneratorDict[("SR2jt","SR")] = -0.155169680736
# zTheoSysGeneratorDict[("SR4jt","SR")]= -0.21787914673
# zTheoSysGeneratorDict[("SR5j","SR")]= 0.0923664820396
# zTheoSysGeneratorDict[("SR6jm","SR")]= -0.160137123349
# zTheoSysGeneratorDict[("SR6jt","SR")]= 0.276153830015


#######################################
#W+jets
#######################################
# SHerpa vs MadGraph
wTheoSysGeneratorDict = {}
wTheoSysGeneratorDict[("default","default")] = 0.10
wTheoSysGeneratorDict[("SR2jl","SR")]= -0.137045746682
wTheoSysGeneratorDict[("SR2jm","SR")]= -0.290595308464
wTheoSysGeneratorDict[("SR2jt","SR")]= 0.381580286919
wTheoSysGeneratorDict[("SR4jt","SR")]= 0.419408662966
wTheoSysGeneratorDict[("SR5j","SR")]= 0.0955335300997
wTheoSysGeneratorDict[("SR6jm","SR")]= 0.0359964709075
wTheoSysGeneratorDict[("SR6jt","SR")]= 0.546637484457


#######################################
#Top
#######################################
# PowhegPythia vs aMcAtNloHerwigppE
topTheoSysGeneratorDict = {}
topTheoSysGeneratorDict[("default","default")] = 0.10
topTheoSysGeneratorDict[("SR2jl","SR")]= -0.0270272272382
topTheoSysGeneratorDict[("SR2jm","SR")]= 0.349636497148
topTheoSysGeneratorDict[("SR2jt","SR")]= 0.461538513093
topTheoSysGeneratorDict[("SR4jt","SR")]= 1.0
topTheoSysGeneratorDict[("SR5j","SR")]= -0.762753262497
topTheoSysGeneratorDict[("SR6jm","SR")]= -0.517948585602
topTheoSysGeneratorDict[("SR6jt","SR")]= -1.55128217279


#Additionnal radiation
topTheoSysRadDict= {}
topTheoSysRadDict[("default","default")] = (0.1,0.1)
topTheoSysRadDict[("SR2jl","SR")]=( 0.0142020364542 , -0.201620192291 )
topTheoSysRadDict[("SR2jm","SR")]=( 0.186026896402 , -0.245470948202 )
topTheoSysRadDict[("SR2jt","SR")]=( 0.125000113877 , 0.0569949678427 )
topTheoSysRadDict[("SR4jt","SR")]=( 0.346846851333 , -0.237373681417 )
topTheoSysRadDict[("SR5j","SR")]=( 0.188578327358 , -0.188673048593 )
topTheoSysRadDict[("SR6jm","SR")]=( 0.106187637855 , -0.453252653384 )
topTheoSysRadDict[("SR6jt","SR")]=( -0.479054176483 , -0.353741257356 )


#PowhegPythia vs PowhegHerwig
topTheoSysPowhegHerwigDict= {}
topTheoSysPowhegHerwigDict[("default","default")] = 0.1
topTheoSysPowhegHerwigDict[("SR2jl","SR")]= 0.00132307230229
topTheoSysPowhegHerwigDict[("SR2jm","SR")]= -0.266853972654
topTheoSysPowhegHerwigDict[("SR2jt","SR")]= -0.105263077168
topTheoSysPowhegHerwigDict[("SR4jt","SR")]= 0.664750955402
topTheoSysPowhegHerwigDict[("SR5j","SR")]= 0.028225738458
topTheoSysPowhegHerwigDict[("SR6jm","SR")]= 0.244110848105
topTheoSysPowhegHerwigDict[("SR6jt","SR")]= 0.416849812194


# Tune P2012 vs A14
topTheoSysA14Dict= {}
topTheoSysA14Dict[("default","default")] = 0.1
topTheoSysA14Dict[("SR2jl","SR")]= -0.0729149044195
topTheoSysA14Dict[("SR2jm","SR")]= -0.126971311478
topTheoSysA14Dict[("SR2jt","SR")]= -0.10526311211
topTheoSysA14Dict[("SR4jt","SR")]= 0.151515168029
topTheoSysA14Dict[("SR5j","SR")]= 0.250880763878
topTheoSysA14Dict[("SR6jm","SR")]= 0.209849710805
topTheoSysA14Dict[("SR6jt","SR")]= 0.0245097704868


