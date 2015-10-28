#!/usr/bin/env python

import math
import os
import pickle
import pprint
import sys 
import socket
from optparse import OptionParser

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro("contourmacros/GetSRName.C")

from summary_harvest_tree_description import treedescription
from array import array
    
SignalDBDir = "/afs/cern.ch/user/m/marijam/public/SignalDBs/"
if socket.getfqdn().find("nikhef") != -1:
    SignalDBDir = "/glusterfs/atlas4/users/gbesjes/ZeroLepton-00-00-53_Light/"

def readData(options, filename):
    try:
        f = open(filename)
    except: 
        print "Cannot open file %s" % filename
        return

    print "Reading data from %s" % filename

    dummy,description = treedescription()
    allpar = description.split(':')
    
    #extend this to more pars on gridname if wanted
    par1_s = "m0"
    par2_s = "m12"
    par3_s = ""

    data = {}
    for l in f.readlines():
        d = l.strip().split()
       
        selectpar = "expectedUpperLimit" # makes NO sense to use something different here
        pval = float( d[allpar.index(selectpar)]) 
        par1 = int(float( d[allpar.index(par1_s)]))
        par2 = int(float( d[allpar.index(par2_s)]))
        key = "%d_%d" % (par1, par2)
      
        # float strings -> so make them float, then an int to throw away .0000 and then to bool
        failedcov =  bool(int(float(d[allpar.index("failedcov")])))  # Mediocre cov matrix quality
        covqual = int(float(d[allpar.index("covqual")]))             # covqual
        failedfit = bool(int(float(d[allpar.index("failedfit")])))   # Fit failure
        failedp0 = bool(int(float(d[allpar.index("failedp0")])))     # Base p0 ~ 0.5 (this can reject good fits)!
        fitstatus = bool(int(float(d[allpar.index("fitstatus")])))   # Fit status from Minuit
        nofit = bool(int(float(d[allpar.index("nofit")])))           # Whether there's a fit present
 
        if failedfit or failedcov:
            print "WARNING: fit failed for %s" % key
            continue

        if covqual < 3 and covqual != -1:
            print "WARNING: covqual=%d for %s" % (covqual, key)
            continue

        if par3_s != "":
            par3 = int(float( d[allpar.index(par3_s)]))
            key = "%d_%d_%d" % (par1, par2, par3)

        # this whole block is stolen from makeContoursNew.py. Do we need a module for this? Yes, we do.... --GJ, 4 feb 15

        if selectpar == "expectedUpperLimit" and pval < 0.00001:
            print "INFO: %s removing %s < 0.00001 for %s" % (filename, selectpar, key)
            continue
       
        # 110 is 20 times our default step -> this is almost certainly a bug
        if selectpar == "expectedUpperLimit" and pval == 110.0:
            print "INFO: %s removing expUL==110.0 for %s" % (filename, key)
            continue

        # if -1sig, -2sig == 0 and +1sig, 2sig == 100 -> almost certainly a bug too
        if selectpar == "expectedUpperLimit" and float(d[allpar.index("expectedUpperLimitMinus1Sig")]) == 0.0 and float(d[allpar.index("expectedUpperLimitMinus2Sig")]) == 0.0 and float(d[allpar.index("expectedUpperLimitPlus1Sig")]) == 100.0 and float(d[allpar.index("expectedUpperLimitPlus2Sig")]) == 100.0:
            print "INFO: %s removing point %s with expULMinus1Sig == expULMinus2Sig == 0 and expULPlus1Sig == expULPlus2Sig == 100" % (filename, key)
            continue

        if selectpar == "expectedUpperLimit" and float(d[allpar.index("upperLimit")]) == 0.0:
            print "INFO: %s removing obsUL=0.0 for %s" % (filename, key)
            continue

        # throw away points with CLsexp > 0.99 and UL < 1.0 and CLs=-1 and UL<1 when merging on UL                      
        CLsExp = float( d[allpar.index("CLsexp")])
        if selectpar == "expectedUpperLimit" and pval < 1.0 and (CLsExp>0.99 or CLsExp<0) and float( d[allpar.index("upperLimit")])<1:                   
            if CLsExp>0.99: print "INFO: %s replacing CLsexp with 0.01 since UL < 1.0  and CLsexp=1 for %s" % (filename, key)
            elif CLsExp<0: print "INFO: %s replacing CLsexp with 0.01 since UL < 1.0  and CLsexp=-1 for %s" % (filename, key)
            d[allpar.index("CLsexp")] = str(0.01)
            d[allpar.index("CLs")] = str(0.01)
            d[allpar.index("clsu1s")] = str(0.01)
            d[allpar.index("clsd1s")] = str(0.01)
            d[allpar.index("p1")] = str(0.01)

        data[key] = d

    f.close()
    return data

def useThisPoint(options, par1, par2, par3=0):
    #print "Use this point?", par1, par2
    if (options.gridname == "Gluino_gluon" or options.gridname == "SM_SS_direct") and not options.vertical and par2 == 0:
        print "Found %d_%d" % (par1, par2)
        return True
    
    if (options.gridname == "Gluino_gluon" or options.gridname == "SM_SS_direct") and options.vertical and par1 == 450:
        print "Found %d_%d" % (par1, par2)
        return True

    return False

def readCrossSections(options):
    xsecs = {}
   
    procs = [3] # our default grid is SM_SS_direct, so set it to a sensible value
    
    if options.gridname == "Gluino_gluon":
        procs = [1] 
    
    picklefile = open('signalPointPickle2012.pkl', 'rb')
    pointdict = pickle.load(picklefile)
    picklefile.close()

    if not options.gridname in pointdict:
        print "Cannot find grid %s in the points dictionary! Bailing out..." % options.gridname
        sys.exit()

    DSIDs = {}
    for key, info in pointdict[options.gridname].items():
        DSIDs["%s_%s" % (info[0], info[1])] = key

    SignalDBFile = "%s/SignalDB_%s.root" % (SignalDBDir, options.gridname)
    NLO = ROOT.TFile.Open(SignalDBFile)
    if not NLO:
        print "Cannot open tree with xsecs!"
        sys.exit()
    
    myMap = NLO.Get("runNumToXsec")
    for key in DSIDs:
        xsec = []
        for proc in procs:
            newkey = "%d:%d" % (DSIDs[key], proc)
            vec = myMap.GetValue(newkey)
            if vec:
                xsecPerProc = float(vec[0])
                xsecRelUncert = float(vec[1])
                xsec.append( [xsecPerProc, xsecRelUncert] )
        xsecs[key] = xsec

    return xsecs

def makeXsecData(options, data):
    dummy,description = treedescription()
    allpar = description.split(':')

    xsecdata = {}
    xsecs = readCrossSections(options)

    if data == {}:
        print "Your data array is empty! Exiting"
        sys.exit()

    for key in data:
        # extend here to par3 if needed
        (par1, par2) = (int(x) for x in key.split("_"))
        if not useThisPoint(options, par1, par2):
            print "Skipping %s" % key
            continue
        
        CLsexp = float(data[key][allpar.index("CLsexp")])
        upperLimit = float(data[key][allpar.index("upperLimit")])
        expectedUpperLimit = float(data[key][allpar.index("expectedUpperLimit")])
        
        expectedUpperLimitMinus1Sig = float(data[key][allpar.index("expectedUpperLimitMinus1Sig")])
        expectedUpperLimitPlus1Sig = float(data[key][allpar.index("expectedUpperLimitPlus1Sig")])
        
        expectedUpperLimitMinus2Sig = float(data[key][allpar.index("expectedUpperLimitMinus2Sig")])
        expectedUpperLimitPlus2Sig = float(data[key][allpar.index("expectedUpperLimitPlus2Sig")])
        
        fID = int(float(data[key][allpar.index("fID")]))

        #print "-1: %.3f, -2: %.3f" % (expectedUpperLimitMinus1Sig, expectedUpperLimitMinus2Sig)

        # TODO need to extract this plus uncertainty from SignalDB
        # NOTE: hardcoded for 1 proc, hence the extra [0]
        xsec = xsecs[key][0][0]*1000
        xsecUp = (1+xsecs[key][0][1]) * xsec
        xsecDown = (1-xsecs[key][0][1]) * xsec

        print "%s: xsec=%.2e relunc=%.2e up=%.2e down=%.2e" % (key, xsec, xsecs[key][0][1], xsecUp, xsecDown)

        xsec2 = xsec/2
        xsec4 = xsec/4
        xsec8 = xsec/8

        xsec2Up = xsecUp/2
        xsec4Up = xsecUp/4
        xsec8Up = xsecUp/8
        
        xsec2Down = xsecDown/2
        xsec4Down = xsecDown/4
        xsec8Down = xsecDown/8

        xsecdata[key] = {"upperLimit": upperLimit, "expectedUpperLimit" : expectedUpperLimit, "expectedUpperLimitMinus1Sig" : expectedUpperLimitMinus1Sig,
                         "expectedUpperLimitPlus1Sig" : expectedUpperLimitPlus1Sig, "expectedUpperLimitMinus2Sig" : expectedUpperLimitMinus2Sig,
                         "expectedUpperLimitPlus2Sig" : expectedUpperLimitPlus2Sig, "xsec" : xsec, "xsecUp" : xsecUp, "xsecDown" : xsecDown, "xsec2": xsec2, 
                         "xsec2Up" : xsec2Up, "xsec2Down" : xsec2Down,
                         "xsec4Up" : xsec4Up, "xsec4Down" : xsec4Down,
                         "xsec8Up" : xsec8Up, "xsec8Down" : xsec8Down,
                         "xsec4": xsec4, "xsec8": xsec8, "fID" : fID, "CLsexp": CLsexp}

    return xsecdata

def makeGraphs(options, xsecData):
    #extend for other grids... 

    sortedData = {}
    for key in sorted(xsecData):
        (par1, par2) = (int(x) for x in key.split("_"))
        
        # sort this by whatever you want on the x-axis
        if not options.vertical:
            sortedData[par1] = xsecData[key]
        else:
            sortedData[par2] = xsecData[key]

    # build arrays for TGraph2D
    xval = array("f")
    xsec = array("f")
    xsecUp = array("f")
    xsecDown = array("f")
    xsec2 = array("f")
    xsec2Up = array("f")
    xsec2Down = array("f")
    xsec4 = array("f")
    xsec4Up = array("f")
    xsec4Down = array("f")
    xsec8 = array("f")
    xsec8Up = array("f")
    xsec8Down = array("f")
    UL = array("f")
    expUL = array("f")
    expULPlus1Sig = array("f")
    expULMinus1Sig = array("f")
    expULPlus2Sig = array("f")
    expULMinus2Sig = array("f")
    zeroes = array("f")

    for key in sorted(sortedData):
        # key is whatever goes on x-axis

        #if sortedData[key]["expectedUpperLimit"] == -1.0 or sortedData[key]["expectedUpperLimit"] == 110.0:
            #continue
       
        if sortedData[key]["expectedUpperLimit"] == sortedData[key]["expectedUpperLimitMinus1Sig"]: #100% uncertainty
            continue

        x = sortedData[key]["xsec"]
        myExpUL = sortedData[key]["expectedUpperLimit"]*x
        print "%d: CLs=%.8f expUL=%.3f => UL*xsec = %.3f (best SR=%d, xsec=%.1f)" % (key, sortedData[key]["CLsexp"], sortedData[key]["expectedUpperLimit"], myExpUL, sortedData[key]["fID"], x)

        expUL.append(myExpUL)
        xval.append(float(key))

        xsec.append(sortedData[key]["xsec"])
        xsecUp.append( abs(sortedData[key]["xsecUp"] - sortedData[key]["xsec"]) ) 
        xsecDown.append( abs(sortedData[key]["xsecDown"] - sortedData[key]["xsec"]) ) 
        xsec2.append(sortedData[key]["xsec2"])
        xsec2Up.append( abs(sortedData[key]["xsec2Up"] - sortedData[key]["xsec2"]) ) 
        xsec2Down.append( abs(sortedData[key]["xsec2Down"] - sortedData[key]["xsec2"]) ) 
        xsec4.append(sortedData[key]["xsec4"])
        xsec4Up.append( abs(sortedData[key]["xsec4Up"] - sortedData[key]["xsec4"]) ) 
        xsec4Down.append( abs(sortedData[key]["xsec4Down"] - sortedData[key]["xsec4"]) ) 
        xsec8.append(sortedData[key]["xsec8"])
        xsec8Up.append( abs(sortedData[key]["xsec8Up"] - sortedData[key]["xsec8"]) ) 
        xsec8Down.append( abs(sortedData[key]["xsec8Down"] - sortedData[key]["xsec8"]) ) 
        zeroes.append(0.0)
        
        UL.append(sortedData[key]["upperLimit"]*x)

        ref = myExpUL
        expULPlus1Sig.append(abs(sortedData[key]["expectedUpperLimitPlus1Sig"]*x-ref))
        expULMinus1Sig.append(abs(sortedData[key]["expectedUpperLimitMinus1Sig"]*x-ref))
        expULPlus2Sig.append(abs(sortedData[key]["expectedUpperLimitPlus2Sig"]*x-ref))
        expULMinus2Sig.append(abs(sortedData[key]["expectedUpperLimitMinus2Sig"]*x-ref))

    
    #print "========="
    for i in range(0, len(xval)-1):
        #print "%d:" % (xval[i])
        print "%d: %.3f +%.3f -%.3f (++%.3f --%.3f)" % (xval[i], expUL[i], expULPlus1Sig[i], expULMinus1Sig[i], expULPlus2Sig[i], expULMinus2Sig[i]) 

    graphs = {}
    print "print type(xval)", type(xval)
    print len(xval)

    graphs["xsec"] = ROOT.TGraphAsymmErrors(len(xval), xval, xsec, zeroes, zeroes, xsecUp, xsecDown)
    graphs["xsec2"] = ROOT.TGraphAsymmErrors(len(xval), xval, xsec2, zeroes, zeroes, xsec2Up, xsec2Down)
    graphs["xsec4"] = ROOT.TGraphAsymmErrors(len(xval), xval, xsec4, zeroes, zeroes, xsec4Up, xsec4Down)
    graphs["xsec8"] = ROOT.TGraphAsymmErrors(len(xval), xval, xsec8, zeroes, zeroes, xsec8Up, xsec8Down)
    graphs["UL"] = ROOT.TGraphAsymmErrors(len(xval), xval, UL, zeroes, zeroes, zeroes, zeroes)
    
    graphs["expUL"] = ROOT.TGraphAsymmErrors(len(xval), xval, expUL, zeroes, zeroes, zeroes, zeroes)
    graphs["expUL1Sig"] = ROOT.TGraphAsymmErrors(len(xval), xval, expUL, zeroes, zeroes, expULMinus1Sig, expULPlus1Sig)
    graphs["expUL2Sig"] = ROOT.TGraphAsymmErrors(len(xval), xval, expUL, zeroes, zeroes, expULMinus2Sig, expULPlus2Sig) 

    #graphs["expUL"] = ROOT.TGraphAsymmErrors(len(xval), xval, expUL, zeroes, zeroes, expULMinus1Sig, expULPlus1Sig)
    #graphs["expUL2Sig"] = ROOT.TGraphAsymmErrors(len(xval), xval, expUL, zeroes,zeroes,  expULMinus2Sig, expULPlus2Sig)

    return graphs

def makeLegend():
    labelPosX = 0.78
    xmin_leg  = labelPosX
    xdiff_leg = 0.22
    ymax_leg  = 0.91
    ydiff_leg = 0.32 + 0.005
    textSize = 0.04

    leg = ROOT.TLegend(xmin_leg, ymax_leg-ydiff_leg, xmin_leg+xdiff_leg, ymax_leg, "", "NDC")
    leg.SetFillStyle(0)
    leg.SetTextSize(textSize)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    return leg

def makeStyle():
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptTitle(0)

    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetPadColor(0)
    ROOT.gStyle.SetFillStyle(0)

    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPaperSize(20,26)
    ROOT.gStyle.SetPadTopMargin(0.06)
    ROOT.gStyle.SetPadRightMargin(0.02)
    ROOT.gStyle.SetPadBottomMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.10)

    # use bold lines and markers
    ROOT.gStyle.SetMarkerStyle(21)
    ROOT.gStyle.SetMarkerSize(0.3)
    #ROOT.gStyle.SetHistLineWidth(1.85)
    ROOT.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes
  
    ROOT.gROOT.ForceStyle()

    return 

def makePlots(options, graphs, SR, outputFilename, doObs=False, bestSRXsecData = {}):
    # SR=-1 means combined!

    print options.gridname
    print graphs
    
    graphsBestSRs = {}
    for fID in bestSRXsecData:
        g = makeGraphs(options, bestSRXsecData[fID])
        graphsBestSRs[fID] = g

    pprint.pprint(graphsBestSRs)

    markerSize = 0.8

    makeStyle()
    canvas = ROOT.TCanvas("c","c", 0, 0, 700, 500)
    
    # start with this one so the labels on all plots are identical
    g_xsec = graphs["xsec"]
    g_xsec.SetLineStyle(1)
    g_xsec.SetLineWidth(3)
    g_xsec.SetLineColor(ROOT.kAzure+5)
    g_xsec.SetFillColor(ROOT.kAzure+5)
    ROOT.gStyle.SetHatchesLineWidth(2)
    g_xsec.SetFillStyle(3004)
    g_xsec.Draw("AL3")
    
    if not options.vertical:
        g_xsec.SetMinimum(0.5)
        g_xsec.SetMaximum(100000)
        g_xsec.GetXaxis().SetLimits(50, 1500)
        if options.gridname == "Gluino_gluon": g_xsec.GetXaxis().SetLimits(50, 1700)
        g_xsec.GetXaxis().SetTitle("m_{#tilde{q}} (GeV)")
        if options.gridname == "Gluino_gluon": g_xsec.GetXaxis().SetTitle("m_{#tilde{g}} (GeV)")
    else:     
        g_xsec.SetMinimum(25)
        g_xsec.SetMaximum(300000)
        g_xsec.GetXaxis().SetLimits(0, 400)
        g_xsec.GetXaxis().SetTitle("m_{#tilde{#chi}_{1}^{0}} (GeV)")
    
    g_xsec.GetXaxis().SetTitleOffset(1.2)
    g_xsec.GetYaxis().SetTitle("95% CL limit #sigma #times BR (fb)")

    g_2s = graphs["expUL2Sig"]
    g_2s.SetLineColor(ROOT.kYellow)
    g_2s.SetFillColor(ROOT.kYellow)
    g_2s.GetXaxis().SetMoreLogLabels(1)
    g_2s.GetXaxis().SetNoExponent(1)
    g_2s.Draw("l3")
    g_2s.GetXaxis().SetRangeUser(0, 2000)
    g_2s.GetXaxis().SetLimits(0, 2000)

    g_2s.GetXaxis().SetMoreLogLabels(1)
    g_2s.GetXaxis().SetNoExponent(1)

    g_1s = graphs["expUL1Sig"]
    g_1s.SetLineColor(ROOT.kGreen)
    g_1s.SetFillColor(ROOT.kGreen)
    g_1s.Draw("l3")
    #g_1s.GetXaxis().SetRangeUser(0, 2000)
    #g_1s.GetXaxis().SetLimits(0, 2000)
    
    # plot it again to be on top
    g_xsec.Draw("L3")

    g_obs = graphs["UL"]
    g_obs.SetLineStyle(1)
    g_obs.SetLineWidth(3)
    g_obs.SetMarkerSize(markerSize)
    if doObs: g_obs.Draw("lp")
   
    g_exp = graphs["expUL"]
    g_exp.SetLineStyle(2)
    g_exp.SetLineWidth(3)
    g_exp.Draw("l")
    #g_exp.GetXaxis().SetRangeUser(0, 2000)
    #g_exp.GetXaxis().SetLimits(0, 2000)
   
#    if graphsBestSRs == {}:
    g_xsec2 = graphs["xsec2"]
    g_xsec2.SetLineStyle(4)
    g_xsec2.SetLineWidth(3)
    g_xsec2.SetLineColor(ROOT.kAzure+5)
#    g_xsec2.Draw("l")
       #g_xsec2.GetXaxis().SetRangeUser(0, 2000)
        #g_xsec2.GetXaxis().SetLimits(0, 2000)
    
    g_xsec4 = graphs["xsec4"]
    g_xsec4.SetLineStyle(3)
    g_xsec4.SetLineWidth(3)
    g_xsec4.SetLineColor(ROOT.kAzure+5)
#    g_xsec4.Draw("l")
        #g_xsec4.GetXaxis().SetRangeUser(0, 2000)
        #g_xsec4.GetXaxis().SetLimits(0, 2000)
        
    g_xsec8 = graphs["xsec8"]
    g_xsec8.SetLineStyle(2)
    g_xsec8.SetLineWidth(3)
    g_xsec8.SetLineColor(ROOT.kAzure+5)
    g_xsec8.SetFillColor(ROOT.kAzure+5)
    ROOT.gStyle.SetHatchesLineWidth(2)
    g_xsec8.SetFillStyle(3004)
    if options.gridname == "SM_SS_direct": g_xsec8.Draw("l3")
        #g_xsec8.GetXaxis().SetRangeUser(0, 2000)
        #g_xsec8.GetXaxis().SetLimits(0, 2000)

    i=0
    colors = {0: ROOT.kRed, 1: ROOT.kOrange, 2: ROOT.kMagenta, 3: ROOT.kBlue, 4: ROOT.kRed+4, 5: ROOT.kMagenta-10, 6: ROOT.kRed-9}
    if options.plotBestSRs:
        for fID in graphsBestSRs:
            graphsBestSRs[fID]["expUL"].SetLineWidth(2)
            graphsBestSRs[fID]["expUL"].SetLineStyle(5)
            graphsBestSRs[fID]["expUL"].SetLineColor(colors[i])
            graphsBestSRs[fID]["expUL"].Draw("lsame")
            i = i+1 

    leg = makeLegend()
    if doObs: leg.AddEntry(g_obs, "Observed","lp")
    
    leg.AddEntry(g_exp, "Expected","l")
    if options.plotBestSRs:
        for fID in graphsBestSRs:
            leg.AddEntry(graphsBestSRs[fID]["expUL"], "%s" % ROOT.GetSRName(fID), "l")

    leg.AddEntry(g_1s, "#pm1 #sigma","f")
    leg.AddEntry(g_2s, "#pm2 #sigma","f")
    if options.gridname == "SM_SS_direct": leg.AddEntry(g_xsec, "#sigma_{#tilde{q}#tilde{q}} (8 #tilde{q})", "lf")
    elif options.gridname == "Gluino_gluon": leg.AddEntry(g_xsec, "#sigma_{#tilde{g}#tilde{g}}", "lf")
    
#    if graphsBestSRs == {}:
#    leg.AddEntry(g_xsec2, "4 squarks", "l")
#    leg.AddEntry(g_xsec4, "2 squarks", "l")
    if options.gridname == "SM_SS_direct": leg.AddEntry(g_xsec8, "#sigma_{#tilde{q}#tilde{q}} (1 #tilde{q})", "lf")
    
    leg.Draw()
   
    atlasLabel = ROOT.TLatex()
    atlasLabel.SetNDC()
    atlasLabel.SetTextFont( 42 )
    atlasLabel.SetTextColor( 1 )
    atlasLabel.SetTextSize( 0.05 )
    atlasLabel.DrawLatex(0.40,0.84, "#bf{#it{ATLAS}} Internal")
    atlasLabel.AppendPad() 
    
    Leg0 = ROOT.TLatex()
    Leg0.SetNDC()
    Leg0.SetTextAlign( 11 )
    Leg0.SetTextFont( 42 )
    Leg0.SetTextSize( 0.035) 
    Leg0.SetTextColor( 1 )
    if not options.vertical:
        if options.gridname == "SM_SS_direct": Leg0.DrawLatex(0.10,0.96, "#tilde{q}#tilde{q} production; #tilde{q}#rightarrow q #tilde{#chi}_{1}^{0}; m_{#chi_{1}^{0}} = 0 GeV")
        elif options.gridname == "Gluino_gluon": Leg0.DrawLatex(0.10,0.96, "#tilde{g}#tilde{g} production; #tilde{g}#rightarrow g #tilde{#chi}_{1}^{0}; m_{#chi_{1}^{0}} = 0 GeV")
    else:
        if options.gridname == "SM_SS_direct": Leg0.DrawLatex(0.10,0.96, "#tilde{q}#tilde{q} production; #tilde{q}#rightarrow q #tilde{#chi}_{1}^{0}; m_{#tilde{q}} = 450 GeV")
        elif options.gridname == "Gluino_gluon": Leg0.DrawLatex(0.10,0.96, "#tilde{g}#tilde{g} production; #tilde{g}#rightarrow g #tilde{#chi}_{1}^{0}; m_{#tilde{q}} = 450 GeV")

    Leg0.AppendPad()
  

    Leg1 = ROOT.TLatex()
    Leg1.SetNDC()
    Leg1.SetTextAlign( 11 )
    Leg1.SetTextFont( 42 )
    Leg1.SetTextSize( 0.035) 
    Leg1.SetTextColor( 1 )
    Leg1.DrawLatex(0.40,0.77, "#int L dt = 20.3 fb^{-1},  #sqrt{s}=8 TeV")
    Leg1.AppendPad()
    
    Leg2 = ROOT.TLatex()
    Leg2.SetNDC()
    Leg2.SetTextAlign( 11 )
    Leg2.SetTextFont( 42 )
    Leg2.SetTextSize( 0.035) 
    Leg2.SetTextColor( 1 )
    
    if SR ==-1:
       Leg2.DrawLatex(0.40,0.70, "0 leptons, 2-6 jets")
    else:
       Leg2.DrawLatex(0.40,0.70, "0 leptons, 2-6 jets, %s" % ROOT.GetSRName(SR) )
    Leg2.AppendPad()
    
#    g_xsec.Draw("axis,same")
    canvas.SetLogy(1)
    canvas.Print(outputFilename)
    canvas.Print(outputFilename.replace("pdf", "eps"))

    return

def findBestSRs(xsecData):
    retval = []
    for key in xsecData:
        if xsecData[key]["fID"] in retval: continue
        retval += [xsecData[key]["fID"]] 

    return retval

def readBestSRData(options, infoFilename, bestSRs):
    try:
        f = open(infoFilename)
    except:
        print "Cannot open info file %s" % infoFilename
        return

    filenames = {}
    for l in f.readlines():
        (fID, filename) = l.strip().split(" : ")
        if not int(fID) in bestSRs: continue
        if int(fID) in filenames: continue
        filenames[int(fID)] = "Outputs/%s_%s_fixSigXSecNominal__1_harvest_list" % (options.gridname, filename)

    bestSRXsecData = {}
    for fID in filenames:
        data = readData(options, filenames[fID])
        bestSRXsecData[fID] = makeXsecData(options, data)

    return bestSRXsecData

def main():
    parser = OptionParser()
    
    # the options default to the sq-sq grid. don't change the defaults but implement the proper code to add a new grid!
    parser.add_option("-f", "--filename", help="filename", default="Outputs/SM_SS_direct_combined_fixSigXSecNominal__1_harvest_list")
    parser.add_option("-g", "--gridname", help="name of grid (be sure to implement code!)", default="SM_SS_direct")
    parser.add_option("-v", "--vertical", help="fixed squark mass instead of fixed neutralino mass", action='store_true', default=False)

    parser.add_option("-b", "--plotBestSRs", help="plot best SRs", action='store_true', default=False)

    (options, args) = parser.parse_args(sys.argv[1:])

    # check if the grid was changed but the filename wasn't, if not: try a simple replacement
    if options.gridname != "SM_SS_direct" and "SM_SS_direct" in options.filename:
        # assuming the structure hasn't changed, just replace the grid name. 
        # if you deviate from this structure, you should have used -f !
        options.filename = options.filename.replace("SM_SS_direct", options.gridname)

    filename = options.filename
    infoFilename = "%s_infoFile" % options.filename

    if not os.path.exists(filename):
        print "Input file %s does not exist!" % (filename)
        sys.exit()
    
    if not os.path.exists(infoFilename):
        print "Input infoFile %s does not exist!" % (infoFilename)
        sys.exit()
    
    data = readData(options, filename)
    xsecData = makeXsecData(options, data)
    graphs = makeGraphs(options, xsecData)
    
    bestSRs = findBestSRs(xsecData)
    #bestSRs = range(1,16)
    bestSRXsecData = readBestSRData(options, infoFilename, bestSRs)
    
    ## determine all available x values to use later 
    #xData = []
    #for x in sorted(bestSRXsecData):
        #print x
        #xval = int(x.split("_")[0])
        #xData.append(xval)

    #bestGraphs = {}
    #for fID in bestSRXsecData:
        #bestGraphs[fID] = makeGraphs(options, bestSRXsecData[fID])
        #for x in sorted(xsecData):
            #xval = int(x.split("_")[0])
            #yval = bestGraphs[fID]["expUL"].Eval(xval)
            
            ##print "x=%d" % xval
            
            #print "SR=%s, x=%d, y=%.3e, BEST y=%.3e" % (ROOT.GetSRName(fID), xval, bestGraphs[fID]["expUL"].Eval(xval), graphs['expUL'].Eval(xval))
            ##pprint.pprint(xsecData)
            #if yval < graphs['expUL'].Eval(xval):
                #print "SR: %s, x=%.2f: FOUND SMALLER VAL: %.2f < %.2f" % (ROOT.GetSRName(fID), xval, yval, graphs['expUL'].Eval(xval))
   
                ##pprint.pprint(bestGraphs[fID])
                ##sys.exit()

                ### for some reason this messes up the plot? -> yields weird spikes 
                ##pprint.pprint(xsecData[x])
                ##print "REPLACING %.2e with %.2e" % (xsecData[x]['expectedUpperLimit'], yval / xsecData[x]['xsec'])
                ##xsecData[x]['expectedUpperLimit'] = yval #/ xsecData[x]['xsec']
                ##xsecData[x]['expectedUpperLimitMinus1Sig'] = bestGraphs[fID]["expULMinus1Sig"].Eval(xval)
                ##xsecData[x]['expectedUpperLimitMinus2Sig'] = bestGraphs[fID]["expULMinus2Sig"].Eval(xval)
                ##xsecData[x]['expectedUpperLimitMinus1Sig'] = bestGraphs[fID]["expULPlus1Sig"].Eval(xval)
                ##xsecData[x]['expectedUpperLimitMinus2Sig'] = bestGraphs[fID]["expULPlus2Sig"].Eval(xval)
                ##pprint.pprint(xsecData[x])
                ###xsecData[x]['CLsexp'] = bestGraphs[fID]["CLsexp"].Eval(xval)
                ##xsecData[x]['upperLimit'] = bestGraphs[fID]["UL"].Eval(xval) / xsecData[x]['xsec']
                ##xsecData[x]['fID'] = fID

    # remake best graphs & plot
    graphs = makeGraphs(options, xsecData)
    doObs = True
    outputname="plots/%s_mn0.pdf" % options.gridname
    if options.vertical:
        outputname="plots/%s_mg450.pdf" % options.gridname
    makePlots(options, graphs, -1, outputname, doObs, bestSRXsecData)

    pprint.pprint(bestSRXsecData[5])

    sys.exit()
    
    for fID in bestSRXsecData:
        bestGraphs[fID] = makeGraphs(options, bestSRXsecData[fID])
        # replace xsec plot by combined one, for ranges
        g["xsec"] = graphs["xsec"] 
        g["xsec2"] = graphs["xsec2"] 
        g["xsec4"] = graphs["xsec4"] 
        g["xsec8"] = graphs["xsec8"] 
        makePlots(options, g, fID, "plots/%s_xsec_%d.pdf" % (options.gridname, fID) )
    
    return

if __name__ == '__main__':
    main()
