import ROOT
import math
from ROOT import *
from math import *

class RootOption:
    def __init__(self, gStyle):
        self.gStyle=gStyle;
    def setUpStyle(self):
        self.gStyle.SetOptStat(0);
        icol=0;
        self.gStyle.SetFrameBorderMode(icol);
        self.gStyle.SetFrameFillColor(icol);
        self.gStyle.SetCanvasBorderMode(icol);
        self.gStyle.SetCanvasColor(icol);
        self.gStyle.SetPadBorderMode(icol) ;
        self.gStyle.SetPadColor(icol);  
        self.gStyle.SetStatColor(icol);
        self.gStyle.SetPaperSize(20,26);
        self.gStyle.SetPadTopMargin(0.05);
        self.gStyle.SetPadRightMargin(0.05);
        self.gStyle.SetPadBottomMargin(0.16);
        self.gStyle.SetPadLeftMargin(0.16);
        self.gStyle.SetTitleXOffset(1.4);
        self.gStyle.SetTitleYOffset(1.4);
        font=42;
        tsize=0.05;
        self.gStyle.SetTextFont(font);
        self.gStyle.SetTextSize(tsize);
        self.gStyle.SetLabelFont(font,"x");
        self.gStyle.SetTitleFont(font,"x");
        self.gStyle.SetLabelFont(font,"y");
        self.gStyle.SetTitleFont(font,"y");
        self.gStyle.SetLabelFont(font,"z");
        self.gStyle.SetTitleFont(font,"z");
        self.gStyle.SetLabelSize(tsize,"x");
        self.gStyle.SetTitleSize(tsize,"x");
        self.gStyle.SetLabelSize(tsize,"y");
        self.gStyle.SetTitleSize(tsize,"y");
        self.gStyle.SetLabelSize(tsize,"z");
        self.gStyle.SetTitleSize(tsize,"z");
        self.gStyle.SetMarkerStyle(20);
        self.gStyle.SetMarkerSize(1.2);
        self.gStyle.SetLineStyleString(2,"[12 12]");
        self.gStyle.SetEndErrorSize(0.);
        self.gStyle.SetOptTitle(0);
        self.gStyle.SetOptFit(0);
        self.gStyle.SetPadTickX(1);
        self.gStyle.SetPadTickY(1);
    def setUpPads(self,name,upperPad,lowerPad):
        upperPad=upperPad;
        lowerPad=lowerPad;
        name=name;
        upperPad.SetFillColor(0);
        upperPad.SetBorderMode(0);
        upperPad.SetBorderSize(2);
        if '_logy' in name: upperPad.SetLogy();
        upperPad.SetTickx(1);
        upperPad.SetTicky(1);
        upperPad.SetLeftMargin(0.14);
        upperPad.SetRightMargin(0.05);
        upperPad.SetTopMargin(0.03);
        upperPad.SetBottomMargin(0.1534613);
        upperPad.SetFrameBorderMode(0);
        upperPad.SetFrameBorderMode(0);
        upperPad.Draw();
        lowerPad.SetGridy();
        lowerPad.SetFillColor(0);
        lowerPad.SetBorderMode(0);
        lowerPad.SetBorderSize(2);    
        lowerPad.SetGridy();
        lowerPad.SetFillColor(0);
        lowerPad.SetBorderMode(0);
        lowerPad.SetBorderSize(2);
        lowerPad.SetTickx(1);
        lowerPad.SetTicky(1);
        lowerPad.SetLeftMargin(0.14);
        lowerPad.SetRightMargin(0.05);
        lowerPad.SetTopMargin(0.0125);
        lowerPad.SetBottomMargin(0.37);
        lowerPad.SetFrameBorderMode(0);
        lowerPad.SetFrameBorderMode(0);
        lowerPad.Draw();
         
def setAsymmErrors(hist,graph,varbins=None):
    for iBin in range(1,hist.GetNbinsX()+1):
        obs=hist.GetBinContent(iBin);
        if varbins: obs *= varbins[iBin-1]
        posError = ROOT.TMath.ChisquareQuantile(1. - (1. - 0.68)/2. , 2.* (obs + 1.)) / 2. - obs - 1;
        negError = obs - ROOT.TMath.ChisquareQuantile((1. - 0.68)/2., 2.*obs) / 2.;
        if varbins: obs /= varbins[iBin-1]
        if obs > 0.:
            if varbins:
                posError *= varbins[iBin-1]
                negError *= varbins[iBin-1]
            graph.SetPoint(iBin-1,hist.GetBinCenter(iBin),obs);
            graph.SetPointEXhigh(iBin-1,hist.GetBinWidth(iBin)/2.);
            graph.SetPointEXlow(iBin-1,hist.GetBinWidth(iBin)/2.);
            graph.SetPointEYhigh(iBin-1,posError);
            graph.SetPointEYlow(iBin-1,negError);
        else:
            graph.SetPoint(iBin-1,hist.GetBinCenter(iBin),-1);
            graph.SetPointEXhigh(iBin-1,0);
            graph.SetPointEXlow(iBin-1,0);
            graph.SetPointEYhigh(iBin-1,0);
            graph.SetPointEYlow(iBin-1,0);
        
def GetDataMCRatioOld(dataHisto,mcSumHistos,mcSystHisto,ratio,Allsys_band,Allsys_plusTheo_band):
    for  iBin in range(1, dataHisto.GetNbinsX()+1):
        obs = dataHisto.GetBinContent(iBin);
        posError = ROOT.TMath.ChisquareQuantile(1. - (1. - 0.68)/2. , 2.* (obs + 1.)) / 2. - obs - 1;
        negError = obs - ROOT.TMath.ChisquareQuantile((1. - 0.68)/2., 2.*obs) / 2.;
        if mcSumHistos.GetBinContent(iBin) > 0:
            if obs > 0:
                ratio.SetPoint(iBin-1,dataHisto.GetBinCenter(iBin),obs/mcSumHistos.GetBinContent(iBin));
                ratio.SetPointEXhigh(iBin-1,dataHisto.GetBinWidth(iBin)/2.);
                ratio.SetPointEXlow(iBin-1,dataHisto.GetBinWidth(iBin)/2.);
                ratio.SetPointEYhigh(iBin-1,posError/mcSumHistos.GetBinContent(iBin));
                ratio.SetPointEYlow(iBin-1,negError/mcSumHistos.GetBinContent(iBin));
            else:
                ratio.SetPoint(iBin-1,dataHisto.GetBinCenter(iBin),-1);
                ratio.SetPointEXhigh(iBin-1,0);
                ratio.SetPointEXlow(iBin-1,0);
                ratio.SetPointEYhigh(iBin-1,0);
                ratio.SetPointEYlow(iBin-1,0);
        else:
            ratio.SetPoint(iBin-1,dataHisto.GetBinCenter(iBin),-1);
            ratio.SetPointEXhigh(iBin-1,0);
            ratio.SetPointEXlow(iBin-1,0);
            ratio.SetPointEYhigh(iBin-1,0);
            ratio.SetPointEYlow(iBin-1,0);
        
    varUpDownNoTheory=[]
    varSimmNoTheory=[]
#    print'mcsysthisto', len(mcSystHisto)
    for systHist in mcSystHisto:
        varUpDownNoTheory.append(systHist)
#        print 'add syst',systHist.GetName()
    makeCombinedErrorBand(Allsys_band,mcSumHistos,varUpDownNoTheory,varSimmNoTheory)

def GetDataMCRatio(dataHisto,mcSumHistos,ratio):
    for  iBin in range(1, dataHisto.GetNbinsX()+1):
        obs = dataHisto.GetBinContent(iBin);
        posError = ROOT.TMath.ChisquareQuantile(1. - (1. - 0.68)/2. , 2.* (obs + 1.)) / 2. - obs - 1;
        negError = obs - ROOT.TMath.ChisquareQuantile((1. - 0.68)/2., 2.*obs) / 2.;
        if mcSumHistos.GetBinContent(iBin) > 0:
            if obs > 0:
                ratio.SetPoint(iBin-1,dataHisto.GetBinCenter(iBin),obs/mcSumHistos.GetBinContent(iBin));
                ratio.SetPointEXhigh(iBin-1,dataHisto.GetBinWidth(iBin)/2.);
                ratio.SetPointEXlow(iBin-1,dataHisto.GetBinWidth(iBin)/2.);
                ratio.SetPointEYhigh(iBin-1,posError/mcSumHistos.GetBinContent(iBin));
                ratio.SetPointEYlow(iBin-1,negError/mcSumHistos.GetBinContent(iBin));
            else:
                ratio.SetPoint(iBin-1,dataHisto.GetBinCenter(iBin),-1);
                ratio.SetPointEXhigh(iBin-1,0);
                ratio.SetPointEXlow(iBin-1,0);
                ratio.SetPointEYhigh(iBin-1,0);
                ratio.SetPointEYlow(iBin-1,0);
        else:
            ratio.SetPoint(iBin-1,dataHisto.GetBinCenter(iBin),-1);
            ratio.SetPointEXhigh(iBin-1,0);
            ratio.SetPointEXlow(iBin-1,0);
            ratio.SetPointEYhigh(iBin-1,0);
            ratio.SetPointEYlow(iBin-1,0);
        
def estimSyst(mcSumHistos,mcSystHisto,Allsys_band):
    varUpDownNoTheory=[]
    for sh in mcSystHisto:
        temp_hist=sh.Clone()
        varUpDownNoTheory.append(temp_hist)
        #print 'check',sh.GetBinContent(8)
    #print 'in estimSyst',len(mcSystHisto), len(varUpDownNoTheory)
    makeCombinedErrorBand(Allsys_band,mcSumHistos,varUpDownNoTheory)

def estimSystwTheory(mcSumHistos,mcSystHisto,Allsys_band,Allsys_plusTheory_band):
    varUpDownTheory=[]
    varUpDownNoTheory=[]
    for sh in mcSystHisto:
        #print sh.GetName()
        temp_hist=sh.Clone(sh.GetName()+"_tmp")
        varUpDownTheory.append(temp_hist)
        if 'Total' not in sh.GetName():
            varUpDownNoTheory.append(temp_hist)
        #print 'check',sh.GetBinContent(8)
    #print 'in estimSyst',len(mcSystHisto), len(varUpDownNoTheory)
    #print "SYSTTHEORY"
    makeCombinedErrorBand(Allsys_plusTheory_band,mcSumHistos,varUpDownTheory)
    #print "SYSTNOTHEORY"
    makeCombinedErrorBand(Allsys_band,mcSumHistos,varUpDownNoTheory)
 

def makeCombinedErrorBand(ErrorBand,centralHisto,varUpDown):
#    print 'makecombined',centralHisto.GetNbinsX() iBin in range(0,centralHisto.GetNbinsX()):   
    for  iBin in range(1, centralHisto.GetNbinsX()+1):
        errUp2=0
        errDown2=0
        if centralHisto.GetBinContent(iBin)>0:
            errUp2 +=math.pow(centralHisto.GetBinErrorUp(iBin)/centralHisto.GetBinContent(iBin),2)
            errDown2 +=math.pow(centralHisto.GetBinErrorLow(iBin)/centralHisto.GetBinContent(iBin),2)
            for iUDvar in range(0,len(varUpDown)):
                #print "VARUPDOWN:", varUpDown[iUDvar].GetBinContent(iBin), centralHisto.GetBinContent(iBin), varUpDown[iUDvar].GetName()
                #if "temp" not in varUpDown[iUDvar].GetName():
                if False:
                    errUp2   += math.pow((varUpDown[iUDvar].GetBinContent(iBin)-centralHisto.GetBinContent(iBin))/centralHisto.GetBinContent(iBin),2)
                    errDown2 += math.pow((varUpDown[iUDvar].GetBinContent(iBin)-centralHisto.GetBinContent(iBin))/centralHisto.GetBinContent(iBin),2)
                else:
                    if (varUpDown[iUDvar].GetBinContent(iBin) >= centralHisto.GetBinContent(iBin)):
                        errUp2   += math.pow((varUpDown[iUDvar].GetBinContent(iBin)-centralHisto.GetBinContent(iBin))/centralHisto.GetBinContent(iBin),2)
                    else:
                        errDown2 += math.pow((varUpDown[iUDvar].GetBinContent(iBin)-centralHisto.GetBinContent(iBin))/centralHisto.GetBinContent(iBin),2)
    
#            print 'len(varSimm)',len(varSimm)
#            for iUDvar in range(0,len(varSimm)):
#                errUp2   += math.pow((varSimm[iUDvar].GetBinContent(iBin)-centralHisto.GetBinContent(iBin))/centralHisto.GetBinContent(iBin),2);
#                errDown2 += math.pow((varSimm[iUDvar].GetBinContent(iBin)-centralHisto.GetBinContent(iBin))/centralHisto.GetBinContent(iBin),2);

        ErrorBand.SetPoint(iBin,centralHisto.GetBinCenter(iBin),1);
        ErrorBand.SetPointEXhigh(iBin,centralHisto.GetBinWidth(iBin)/2.); 
        ErrorBand.SetPointEXlow(iBin,centralHisto.GetBinWidth(iBin)/2.); 
        ErrorBand.SetPointEYhigh(iBin,math.sqrt(errUp2));
        #print iBin,errUp2,errDown2
        if errDown2 >= 1.:
            ErrorBand.SetPointEYlow(iBin,0.999);
        else:
            ErrorBand.SetPointEYlow(iBin,math.sqrt(errDown2));
    #print 'errorlow/high',math.sqrt(errDown2),errDown2,math.sqrt(errUp2),errUp2

    
       
def PrintText(name,text):    
    text.SetTextFont(42);
    text.SetTextSize(0.04);
    text.SetTextColor(kBlack);
    text.SetNDC(True);
    # text.DrawLatex(0.65,0.5,"#bf{#it{ATLAS}} Preliminary");
    # text.DrawLatex(0.35,0.93,"#bf{#it{ATLAS}} Preliminary");
    #text.DrawLatex(0.35,0.93,"#bf{#it{ATLAS}} Internal");
    
# def SetLegend(dataHisto,mc,mcHisto,lumi):
#     legend.SetTextSize(0.035);
#     legend.SetFillColor(0);
#     legend.SetBorderSize(0); 
#     legend.AddEntry((TObject*)0,((string)lumi).c_str(), "");
#     legend.AddEntry(&dataHisto,"Data 2012 (#sqrt{s} = 8 TeV)","p");  
#     


def SignificanceFcn(nbSig,nbBkg,nbSigEr,nbBkgEr,erBkgSys=0.2):
    conditionStat=True
    doP0=false
    significance=0.
#    nbBkg=nbBkg*SCALEMC
#    nbBkgEr=nbBkgEr*SCALEMC

    p = RooStats.NumberCountingUtils.BinomialExpP(nbSig, nbBkg, erBkgSys)
    significance = sqrt(2)*TMath.ErfInverse(1-2*p) #????? Z+MET
    if doP0:
        significance=p

    if conditionStat==True and nbBkg>0 and nbBkgEr/nbBkg>0.3:
#        print 'bah on est la bizarre', nbBkg, nbBkgEr/nbBkg
        significance=0
        if doP0:
            significance=100
    return significance


def ComputeSignificance(sigHist,forPlotMcHisto,result):
    forPlotMcHisto.Sumw2()
    for ibin in range(1,result.GetNbinsX()):
        maxbin=forPlotMcHisto.GetNbinsX()+1
        bkg=forPlotMcHisto.Integral(ibin,maxbin)
        bkger=0
        for ibin2 in range(ibin,maxbin+1):
            bkger+=forPlotMcHisto.GetBinError(ibin2)*forPlotMcHisto.GetBinError(ibin2)
        if bkger > 0:
            bkger=sqrt(bkger)
        maxbinsig=sigHist.GetNbinsX()+1
        sig=sigHist.Integral(ibin,maxbinsig)
        siger=0
        signi=SignificanceFcn(sig,bkg,siger,bkger)
        result.SetBinContent(ibin,signi);   
        result.SetBinError(ibin,0.)
#        print 'bin de computesignificance',ibin,result.GetNbinsX(),sig,bkg,signi,sigHist.GetBinContent(ibin)

