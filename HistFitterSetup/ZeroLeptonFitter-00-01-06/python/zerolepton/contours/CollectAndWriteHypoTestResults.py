import copy
import json
import math
import os
import re
import sys

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
#ROOT.gInterpreter.GenerateDictionary("map<TString, float>","stdmap");
ROOT.gInterpreter.GenerateDictionary("std::map<TString, float>", "map;TString;float")


from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, 'e') # we want 7-decimal floats

ROOT.gSystem.Load('{0}/lib/libSusyFitter.so'.format(os.getenv('HISTFITTER'))) # temporary for OS X 10.11

from logger import Logger
log = Logger("CollectAndWriteHypoTestResults")

def CollectAndWriteHypoTestResults(filename, format, interpretation, cuts="1", rejectFailedPrefit=True, outputDir="", prefix=""):
    if outputDir == "":
        outputDir = os.getcwd()

    if not os.path.exists(outputDir):
        try:
            os.makedirs(outputDir)
        except:
            log.error("Could not make output dir {0}".format(outputDir))
            return

    # construct workspace and output file names
    cutString = "_{0}".format(cuts)
    cutString = cutString.replace(" ","_")
    cutString = cutString.replace(">","G")
    cutString = cutString.replace("<","L")
    cutString = cutString.replace("=","E")
    cutString = cutString.replace("&","A")
    cutString = cutString.replace("|","O")
    cutString = cutString.replace("!","N")

    # collect p-values, store rootfile if needed
    summary = CollectHypoTestResults( filename, format, interpretation, cuts, rejectFailedPrefit )

    # store harvest in text file
    (listname, ext) = os.path.splitext(os.path.basename(filename))

    if not prefix.startswith("_"):
        prefix = "_{0}".format(prefix)

    outputFilename = os.path.join(outputDir, listname + prefix + cutString)
    outputFilename += "_harvest_list.json"

    WriteResultSetJSON( summary, outputFilename )

def GetMatchingWorkspaces(f, filename, format, interpretation, cutString):
    wsNameMap = {}

    if f.IsZombie():
        return wsNameMap

    log.debug("1   format = {0}".format(format))
    searchFilename = False
    if format.startswith("filename+"):
        format = format.replace("filename+","");
        searchFilename = True;

    log.debug("2   format = {0}".format(format))

    fullWSName = ""
    if searchFilename:
        split = format.split(":")
        if len(split) == 2:
            fullWSName = split[1]
    log.debug("3   fullWSName = {0}".format(fullWSName))

    # Does format have as many placeholders as interpretation?
    if format.count("%") != len(interpretation.split(":")):
        log.error("No valid interpretation string <{0}> with format <{1}>, for file <{2}>".format(interpretation, format, filename))
        return wsNameMap

    wsidVec = interpretation.split(":")
    log.debug("4   len(wsidVec) = {0}".format(len(wsidVec)))
    for i, x in enumerate(wsidVec):
        log.debug("    wsidVec[{0}] = {1}".format(i, x))

    listOfKeys = f.GetListOfKeys()
    log.debug("4   len(listOfKeys) = {0}".format(listOfKeys.GetEntries()))

    # Construct the regexp we will match with
    pattern = format.replace("%f", "[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?")
    #pattern = format.replace("%f", numeric_const_pattern)
    rx = re.compile(pattern, re.VERBOSE)

    ## The formula for the cut string
    cut = ROOT.TEasyFormula(cutString)

    # Now actually loop over the file content
    keymap = {}
    for i, key in enumerate(listOfKeys):
        keyName = key.GetName()
        keyCycle = key.GetCycle()
        # Make a map of name -> cycle. Always has the highest cycle!
        if not keyCycle in keymap or keyCycle < keymap[keyName]:
            keymap[keyName] = keyCycle

        wsName = "{0};{1}".format(keyName, keymap[keyName])
        wsNameSearch = copy.copy(wsName)
        log.debug(" 5.1   i = {0} wsnameSearch = {1}".format(i, wsNameSearch))

        # search by name of the entry
        if searchFilename and fullWSName != "":
            log.debug(" 5.2   searchFilename && !fullWSName.IsNull() = {0}".format(searchFilename and fullWSName != ""))
            log.debug(" 5.3   TString(key->GetName())) = {0}".format(keyName))
            if fullWSName != keyName:
                continue

        log.debug(" 5.4  searchFilename = {0}".format(searchFilename))
        if searchFilename:
            wsNameSearch = "{0}_{1}".format(infile, wsNameSearch)

        log.debug(" 5.5  wsnameSearch = {0}".format(wsNameSearch))

        # Now actually find the pieces in the name
        args = ()
        match = rx.match(wsNameSearch.split(";")[0]) # the cycle is not important
        if match is not None: args = filter(None, match.groups())

        if len(args) != len(wsidVec):
            # this point doesn't have enough floats for the intepretation
            continue

        if cutString != "1":
            # Set the cut
            for (str, val) in zip(wsidVec, args):
                cut.SetValue(str, float(val))

            # Do we pass the cut?
            if not cut.GetBoolValue(): continue

        wsid = "_".join( "%s=%s" % (str,val) for (str,val) in zip(wsidVec, args))
        wsNameMap[wsid] = wsName;

    if cutString != "1":
        del cut

    del listOfKeys
    return wsNameMap

def ParseWorkspaceID(idString):
    retval = {}
    if len(idString) < 3: return retval
    if idString.count("=") == 0: return retval

    for x in idString.split("_"):
        data = x.split("=")
        if len(data) == 1: continue

        retval[data[0]] = float(data[1])

    return retval

def CollectHypoTestResults( filename, format, interpretation, cutString="1", rejectFailedPrefit=False ):
    limitResults = []
    if filename == "" or format == "" or interpretation == "":
        return limitResults

    f = ROOT.TFile(filename, "READ")
    if f.IsZombie():
        log.error("Cannot open file {0}".format(filename))
        f.Close()
        return limitResults

    # collect all hypotest results in input file
    wsNameMap = GetMatchingWorkspaces(f, filename, format, interpretation, cutString)
    if len(wsNameMap) == 0:
        f.Close()
        return limitResults

    counter_failed_fits = 0
    counter_failed_status = 0
    counter_not_great_fits = 0
    counter_badcovquality = 0
    counter_probably_bad_fit = 0

    for wsId in wsNameMap:
        name = wsNameMap[wsId]

        ht = GetHypoTestResultFromFile(f, name)
        if ht is None:
            continue

        if ht.ArraySize() == 0:
            log.warning("Fit result {0} has failed HypoTestInverterResult - cannot use result. Skip.".format(ht.GetName()))
            ht.IsA().Destructor(ht)
            del ht
            continue

        # Check the fit result
        fitName = name.replace("hypo_discovery_", "fitTo_")
        fitName = fitName.replace("hypo_", "fitTo_")

        fitResult = GetFitResultFromFile(f, fitName)
        log.info("At fit point {0}".format(fitName))
        noFit = False
        if fitResult is None: noFit = True

        failed_status = False
        if fitResult is not None and fitResult.status() != 0:
            log.warning("Fit failed for point {0}. Result has been flagged as failed fit.".format(fitName))
            counter_failed_status += 1
            failed_status = True

        fitStatus = -1
        if fitResult is not None:
            fitStatus = fitResult.status()

        failed_cov = False
        dodgy_cov = False

        covQual = -1
        if fitResult:
            covQual = fitResult.covQual()
            if covQual < 1.1:
                log.warning("Fit result {0} has bad covariance matrix quality! Result has been flagged as failed fit.".format(fitName))
                counter_badcovquality += 1
                failed_cov = True
            elif covQual < 2.1:
                log.warning("Fit result {0} has mediocre covariance matrix quality. Result has been flagged as failed cov matrix.".format(fitName))
                counter_not_great_fits += 1
                dodgy_cov = True

        failed_fit = failed_status or failed_cov or dodgy_cov
        if failed_fit: counter_failed_fits += 1

        if rejectFailedPrefit and failed_fit:
            ht.IsA().Destructor(ht)
            del ht
            if fitResult:
                fitResult.IsA().Destructor(fitResult)
                del fitResult
            continue

        failed_p0half = False
        result = ROOT.RooStats.get_Pvalue(ht)

        # Keeping bad points for now, this also rejects bad fits
        if math.fabs(result.GetP0() - 0.5) < 0.0001 and result.GetSigma0() < 0.0001:
            log.warning("One of the base fits _may_ have failed for point (or may not): {0} : {1} {2} Flagged as p0=0.5.".format(fitName, result.GetP0(), result.GetSigma0()) )
            failed_p0half = True

        failMap = {}
        failMap["nofit"]        = float(noFit)
        failMap["failedstatus"] = float(failed_status)
        failMap["fitstatus"]    = float(fitStatus)
        failMap["failedcov"]    = float(failed_cov)
        failMap["dodgycov"]     = float(dodgy_cov)
        failMap["covqual"]      = float(covQual)
        failMap["failedfit"]    = float(failed_fit)
        failMap["failedp0"]     = float(failed_p0half);

        coords = ParseWorkspaceID(wsId)
        coords_map = ROOT.std.map('TString, float')()

        failMap_map = ROOT.std.map('TString, float')()

        for key,value in coords.items() :
            coords_map[key] = value
        for key,value in failMap.items() :
            failMap_map[key] = value

        result.AddMetaData(coords_map)
        result.AddMetaData(failMap_map)

        # Now get the data - this segfaults if we do it directly
#        keys = result.GetKeys()
#        data = result.GetData()
#        summary = {k: data[k] for k in keys}

#        limitResults.append(summary)

        ht.IsA().Destructor(ht)
        del ht
        if fitResult:
            fitResult.IsA().Destructor(fitResult)
            del fitResult

        pass

    if counter_failed_status > 0 or counter_badcovquality > 0:
        log.warning("{0} failed fit status and {1} fit(s) with bad covariance matrix quality were counted".format(counter_failed_status, counter_badcovquality))
    if counter_probably_bad_fit > 0 or counter_not_great_fits > 0:
        log.warning("{0} fit(s) with a bad p-value and {1} fit(s) with mediocre covariance matrix quality were counted".format(counter_probably_bad_fit, counter_not_great_fits))
    if any([True if x > 0 else False for x in (counter_failed_status, counter_badcovquality, counter_probably_bad_fit, counter_not_great_fits)]):
        log.warning("All but the ones with mediocre covariance matrix quality were rejected from the final results list.")
    log.info("{0} failed fits".format(counter_failed_fits))

    f.Close()
    del f

    return limitResults

def WriteResultSetJSON(limitResults, filename ):
    if len(limitResults) == 0:
        return

    log.info("Storing results of {0} scan points as JSON".format(len(limitResults)))
    dirname = os.path.dirname(os.path.abspath(filename))
    if not os.path.exists(dirname):
        log.warning("Output dir {0} does not exist. Making it.".format(dirname))
        try:
            os.makedirs(dirname)
        except:
            log.error("Could not make output dir {0}".format(dirname))
            return

    try:
        with open(filename, 'w') as outfile:
           json.dump(limitResults, outfile)
    except:
        log.error("Error opening file {0}".format(filename))
        return

    log.info("JSON list file stored as {0}".format(filename))
    for result in limitResults:
        del result
    del limitResults

    pass

def GetHypoTestResultFromFile(f, name):
    return GetObjectFromFile(f, name, "RooStats::HypoTestInverterResult")

def GetFitResultFromFile(f, name):
    return GetObjectFromFile(f, name, "RooFitResult")

def GetObjectFromFile(f, name, type):
    if f.IsZombie():
        return None

    result = f.Get(name)
    if not result or result is None or result.ClassName() != type:
        log.error("Cannot open {1} {0}".format(name, type))
        return None

    return result
