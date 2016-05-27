#!/usr/bin/env python

import json
from array import array
from math import *

from optparse import OptionParser
import sys, os, string, shutil, pickle, subprocess, copy

from ROOT import *
import ROOT
ROOT.gROOT.SetBatch(True) # Turn off online histogram drawing
gStyle.SetOptStat(0)


ROOT.gSystem.Load("libSusyFitter.so")

################################################################
from ChannelsDict import *
#from ZLFitterConfig import *
#zlFitterConfig = ZLFitterConfig() 
from Grid import *


################################################################
parser = OptionParser()
parser.add_option("-d", "--discovery",action="store_true", default=False)
parser.add_option("-i", "--inputDir", help="", default = "Outputs/")
parser.add_option("-g", "--gridName", help="", default = "GG_direct")
parser.add_option("-o", "--doOring", help="", default = False, action="store_true")
parser.add_option("-r", "--doRef", help="", default = False, action="store_true")


colors=[1,kOrange,kRed,kViolet,kBlue,kPink+10,kAzure,kCyan,kGreen,kYellow,kMagenta]*100

(options, args) = parser.parse_args()

################################################################

if options.gridName not in allGrids.keys():
    print "Unknown grid!!!"
    sys.exit()

par0Name=allGrids[options.gridName].parList[0].name
par1Name=allGrids[options.gridName].parList[1].name
if len(allGrids[options.gridName].parList)>2:
    par2Name=allGrids[options.gridName].parList[2].name

################################################################
fomName="CLsexp"
if options.discovery:
    fomName="p0exp"
res="Nominal"

#level=array('d', [TMath.NormQuantile(0.95)])#TMath::NormQuantile(0.95)=1.64

if not options.discovery:
    level=array('d', [log(0.05)])
else:
    level=array('d', [3])


################################################################
def doOring(allInfo):

    mapOR={}
    for anaName,info in allInfo.items():
        #if anaName.find("SRs")>=0: continue
        for i in range(len(info[0])):
            x=info[0][i]
            y=info[1][i]
            z=info[2][i]
            point=(x,y)            
            if point not in mapOR.keys():
                mapOR[point]=(z,anaName)
            else:
                if not options.discovery:
                    if mapOR[point][0]>z: mapOR[point]=(z,anaName)
                else:
                    if mapOR[point][0]<z: mapOR[point]=(z,anaName)
            
    xList=[]
    yList=[]
    zList=[]
    nameList=[]
    
    for point,info in mapOR.items():
        xList.append(point[0])
        yList.append(point[1])
        zList.append(info[0])
        nameList.append(info[1])
            
    return (xList,yList,zList,nameList)


def getInfo(data,gridName):


    xList=[]
    yList=[]
    zList=[]


    for element in data:   

        x=element[par0Name]
        y=element[par1Name]

        if x<xmin: continue
        if x>xmax: continue
        if y<ymin: continue
        if y>ymax: continue


        if not options.discovery:
            z=log(element[fomName])
        else:
            if str(element[fomName])=="-nan":
                print "SKIP",x,y
                continue
            z=sqrt(2)*TMath.ErfInverse(1-2*element[fomName])



        if gridName == "GG_onestepCC_x05" and element[par1Name]==60:
            continue
        if gridName == "GG_onestepCC_mchi1060" and element["m2"]!=60:
            continue      
        if gridName == "SM_GG_N2_mchi101" and element["m2"]!=1:
            continue      
        
        print x,y,z

        xList.append(x)
        yList.append(y)
        zList.append(z)


    return (xList,yList,zList)
    

################################################################
def createContour(allList,color=1,style=1,width=1):


    canvas=TCanvas()
    xArray=array("f", allList[0])
    yArray=array("f", allList[1])
    zArray=array("f", allList[2])



    graph = TGraph2D(len(xArray),xArray,yArray,zArray)        
    graph.Draw("surf1");
    #canvas.Print("toto.gif") 
    hist=graph.GetHistogram()
    hist.SetTitle("")
    hist.Draw("colz")
    hist.Draw("text,same")
    #canvas.Print("tutu"+str(color)+".gif")

    hist.SetContour(len(level),level) 

    hist.SetLineWidth(width)
    hist.SetLineColor(color)
    hist.SetLineStyle(style)

    hist.Draw("cont3,same")    
    #canvas.Print("toto"+str(color)+".gif")

    return (hist,graph)




################################################################
all=[]
canvas = TCanvas()
leg= TLegend(0.5,0.65,0.99,0.99);
leg= TLegend(0.75,0.65,0.99,0.99);
leg.SetTextFont( 42 );
leg.SetFillColor( 0 );
leg.SetTextSize(0.03);

ymin=allGrids[options.gridName].parList[1].min
ymax=allGrids[options.gridName].parList[1].max
xmin=allGrids[options.gridName].parList[0].min
xmax=allGrids[options.gridName].parList[0].max

frame = TH2F("frame","frame",1,xmin,xmax,1,ymin,ymax)
frame.SetTitle("")
frame.GetYaxis().SetTitle(allGrids[options.gridName].parList[1].fullName)
frame.GetXaxis().SetTitle(allGrids[options.gridName].parList[0].fullName)
frame.Draw()

allInfo={}
counter=0

#allChannelsDict=pickle.load(open('%sOptiChannels.pkl' % options.gridName,'r'))
allChannelsDict=finalChannelsDict


for anaName in sorted(allChannelsDict.keys()):
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "% ",anaName
    
    # reject some of the analysis
    doPreselection=False
    if doPreselection:
        #remove paper signal regions except 2jl
        #if anaName  in ["SR2jm","SR2jt","SR4jt","SR5j","SR6jm","SR6jt"]: continue
        keep=False
        if anaName  in ["SR2jl","SR2jm","SR2jt","SR4jt","SR5j","SR6jm","SR6jt"]: keep=True      
        # myAna=[]
        # if anaName  in myAna: keep=True
        #if keep==False: continue
    

    counter+=1
    fileName= options.inputDir+"/ZL_"+anaName+"_"+allGrids[options.gridName].basename+"_Output_fixSigXSec"+res+"_hypotest__1_harvest_list.json"

    data = []  
    if not os.path.isfile(fileName):
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "SKIPPING",fileName
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        continue
    with open(fileName) as f:
        print fileName
        data = [json.loads(line) for line in f]

    info=getInfo(data[0],gridName=options.gridName)
    allInfo[anaName]=info
    style=1
    color=colors[counter]
    style=2
    # if anaName.find("SR")<0:
    #     #color=14
    #     style=2
    # else:
    #     print "."
    #     style=2
    #     #color=2

    hist=createContour(info,color=color,style=style,width=1)
    all.append(hist)
    canvas.cd()
    hist[0].Draw("same,cont3")
    leg.AddEntry(hist[0],anaName,"L")



if options.doRef:
    base="References/ref"
    if options.discovery:
        base+="p0"
    refInfo=pickle.load(open(base+"_"+options.gridName+".pkl",'r'))
    histREF=createContour(refInfo,color=1,width=3)
    histREF[0].SetLineStyle(2)
    histREF[0].Draw("same,cont3")
    leg.AddEntry(histREF[0],"Reoptimized","L")


if options.doOring:
    oringInfo=doOring(allInfo)
    print oringInfo
    histOR=createContour(oringInfo,color=1,width=3)
    histOR[0].SetLineStyle(1)
    histOR[0].Draw("same,cont3")
    leg.AddEntry(histOR[0],"ORING","L")
    
    base="ref"
    if options.discovery:
        base+="p0"
    pickle.dump( oringInfo, open(base+"_"+options.gridName+".pkl", "wb" ) )
    selectedAna=[]
    for i in range(len(oringInfo[0])):
        x=oringInfo[0][i]
        y=oringInfo[1][i]
        z=oringInfo[2][i]
        anaName=oringInfo[3][i]
        latex = ROOT.TLatex()
        latex.SetTextColor(2)
        latex.SetTextSize(0.02)
        
        selectedAna.append(anaName)
        mystr=anaName.replace("SR","")
        #mystr="_"+str(round(exp(z),2))
        latex.DrawLatex(x,y,mystr)
        #latex.DrawLatex(x,y,"o")

    #print best analysis
    print sorted(list(set(selectedAna)))


# histREF=createContour(oringInfo,color=1)
# histREF[0].Draw("same,cont3")
# leg.AddEntry(histREF[0],"REFING","L")


leg.Draw()
canvas.Print(options.gridName+".gif")
canvas.Print(options.gridName+".pdf")



