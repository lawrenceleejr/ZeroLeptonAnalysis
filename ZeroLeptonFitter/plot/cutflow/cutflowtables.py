import os
import sys
from sys import exit
from math import sqrt

from ROOT import gROOT,gSystem,gDirectory

from ROOT import TFile,TObject, TString,TTree, TBranch
from ROOT import TMath,TH2D
import ROOT

class Counter:
  def __init__(self,name):
    self.name = name
    self.counters = {}
    self.counters2 = {}

  def increment(self, cutname, weight):
    if not self.counters.has_key(cutname):
      self.counters[cutname] = 0.
      self.counters2[cutname] = 0.
    self.counters[cutname] += weight
    self.counters2[cutname] += weight*weight


class SignalRegion:
  def __init__(self,name,nJet,dphiCut,ptj2Cut,ptj4Cut,ApCut,metSigCut,metOvmeffCut,meffCut):
    self.name = name
    self.nJet = nJet
    self.dphiCut = dphiCut
    self.ptj2Cut = ptj2Cut
    self.ptj4Cut = ptj4Cut
    self.ApCut = ApCut
    self.metSigCut = metSigCut
    self.metOvmeffCut = metOvmeffCut
    self.meffCut = meffCut
    self.counters = {}
    self.sumweights = 0.
    self.sumweights2 = 0.
    self.samplename = None

  def setCurrentSample(self,samplename):
    self.samplename = samplename
    self.counters[samplename] = Counter(self.name+'-'+samplename)

  def process(self,veto,nJet,jetPt,met,dPhi,dPhiR,meffNJ,meffInc,metSig,Ap,weight,RunNumber):
    if not self.samplename:
      print 'current sample name unknown ! bail out!'
      sys.exit(1)
      
    if not (veto==0 and nJet>=1 and jetPt[1]>200000 and met>200000) : return
    self.counters[self.samplename].increment("Pt1>200 Met>200",weight)

    if nJet < self.nJet: return
    if jetPt[self.nJet] < 60000.: return
    self.counters[self.samplename].increment("Topology",weight)

    if dPhi < self.dphiCut: return
    if self.nJet>3 and dPhiR < 0.2: return
    self.counters[self.samplename].increment("Delta(Phi)",weight)

    if nJet>1 and jetPt[2] < self.ptj2Cut: return
    self.counters[self.samplename].increment("Pt2 cut",weight)

    if nJet>3 and jetPt[4] < self.ptj4Cut: return
    self.counters[self.samplename].increment("Pt4 cut",weight)

    if Ap < self.ApCut: return
    self.counters[self.samplename].increment("Ap cut",weight)
    
    if metSig < self.metSigCut: return
    self.counters[self.samplename].increment("metSig",weight)
    
    if met/meffNJ[self.nJet] < self.metOvmeffCut: return
    self.counters[self.samplename].increment("met/meff",weight)

    if meffInc < self.meffCut: return
    self.counters[self.samplename].increment("meff",weight)

    pass


def printLaTex(samples,SRlist,version):

  wosquark=True
  
  numBkg = 0
  numSig = 0
  for sample in samples:
    if sample.isSignal:
      numSig += 1
    else:
      numBkg += 1

  srnum = 0
  for sr in SRlist:
    srnum += 1
    ftexBkg = open(outdir+'/SR'+sr.name+'_bkg.tex','w')
    ftexSig = open(outdir+'/SR'+sr.name+'_signal.tex','w')
    
    ftexBkg.write('\\begin{table}[htbp] \n')
    ftexBkg.write('\scriptsize \n')
    ftexBkg.write('\\begin{center} \n')
    ftexBkg.write('\\caption{\\label{tab:cutflowbkgSR'+sr.name+'} v'+str(version)+': Event yields with MC stat uncertainties for the top, $W$+jets and $Z$+jets backgrounds in SR'+sr.name+' at '+str(0.001*lumi)+'~fb$^{-1}$.} \n')
    ftexBkg.write('\\begin{tabular}{c|'+'c'*numBkg+'|c}\n')
    ftexBkg.write('\\hline \\hline\n')
    ftexBkg.write('Selections')
    for sample in samples:
      if not sample.isSignal:
        ftexBkg.write(' & '+sample.name )
    ftexBkg.write(' & Total Bkg \\\\ \n')

    ftexSig.write('\\begin{table}[htbp] \n')
    ftexSig.write('\scriptsize \n')
    ftexSig.write('\\begin{center} \n')
    ftexSig.write('\\caption{\\label{tab:cutflowsigSR'+sr.name+'} v'+str(version)+': Event yields with MC stat uncertainties for two signal samples and total backgrounds in SR'+sr.name+' at '+str(0.001*lumi)+'~fb$^{-1}$.} \n')
    ftexSig.write('\\begin{tabular}{cc'+'c'*numSig+'}\n')
    ftexSig.write('\\hline \\hline\n')
    ftexSig.write('Selections ')
    for sample in samples:
      if sample.isSignal:
        ftexSig.write(' & '+sample.name )
    ftexSig.write(' & Total Bkg \\\\ \n')
        
    cuts = [
      ('Pre-selection, $E_{\\rm T}^{\\rm miss}$$>$200 GeV, \\ensuremath{p_{\\mathrm{T}}(\\rm{jet}_{1})}$>$200 GeV ','Pt1>200 Met>200'),
      ('Jet multiplicity','Topology'),
      ('min($\\Delta\\phi(E_{\\rm T}^{\\rm miss}, {\\rm jet}_{1,2,3})$) cut','Delta(Phi)'),
      ('\\ensuremath{p_{\\mathrm{T}}(\\rm{jet}_{2})} cut','Pt2 cut'),
      ('\\ensuremath{p_{\\mathrm{T}}(\\rm{jet}_{4})} cut','Pt4 cut'),
      ('Aplanarity cut','Ap cut'),
      ('$E_{\\rm T}^{\\rm miss}$/$\\sqrt{{\\rm H}_{\\rm T}}$ cut','metSig'),
      ('$E_{\\rm T}^{\\rm miss}$/m$_{\\rm eff}$(Nj) cut','met/meff'),
      ('m$_{\\rm eff}$(incl.) cut','meff'),
      ]
    for cut in cuts:
      sumw  = 0.
      sumw2 = 0.
      ftexBkg.write(cut[0])
      ftexSig.write(cut[0])

      GG_1350_25ns=sr.counters["gluino pair m(gluino,N1)=(1350, 0)~GeV"].counters[cut[1]]
      if not wosquark: SS_900_25ns=sr.counters["squark pair m(squark,N1)=(900, 0)~GeV"].counters[cut[1]]

      GG_1350_25ns_err = sqrt(sr.counters["gluino pair m(gluino,N1)=(1350, 0)~GeV"].counters2[cut[1]])
      if not wosquark: SS_900_25ns_err = sqrt(sr.counters["squark pair m(squark,N1)=(900, 0)~GeV"].counters2[cut[1]])

      print "CUT Name", cut[0]

      for sample in samples:
        w  = sr.counters[sample.name].counters[cut[1]]
        w2 = sr.counters[sample.name].counters2[cut[1]]
        if sample.isSignal:
          ftexSig.write(' & %6.2f $\\pm$ %6.2f' %(w,sqrt(w2)))
        else:
          sumw += w
          sumw2 += w2
          ftexBkg.write(' & %6.2f $\\pm$ %6.2f' %(w,sqrt(w2)))
      ftexBkg.write(' & %6.2f $\\pm$ %6.2f \\\\ \n' %(sumw,sqrt(sumw2)))
      ftexSig.write(' & %6.2f $\\pm$ %6.2f \\\\ \n' %(sumw,sqrt(sumw2)))

    ftexBkg.write('\\hline \\hline\n')
    ftexBkg.write('\\end{tabular}\n')
    ftexBkg.write('\end{center} \n')

    ftexBkg.write('\end{table} \n\n\n')
    ftexBkg.close()

    ftexSig.write('\\hline \\hline\n')
    ftexSig.write('\\end{tabular}\n')
    ftexSig.write('\end{center} \n')

    ftexSig.write('\end{table} \n\n\n')
    ftexSig.close()

  return



def runOnSample(name,filename,treename,SRlist):
  for sr in SRlist:
    sr.setCurrentSample(name)

  f=ROOT.TFile.Open(filename)
  if not f or f.IsZombie():
    print 'Could not open ',filename
    sys.exit(1)
  tree=f.Get(treename)
  if not tree:
    print 'Could not access tree',treename,'in file',filename
    sys.exit(1)

  # get all leaves and branches
  leaves = tree.GetListOfLeaves()
  branches = tree.GetListOfBranches()
  # define dynamically a python class containing root Leaves objects
  class PyListOfLeaves(dict) :
    pass
  # define dynamically a python class containing root Branches objects
  class PyListOfBranches(dict) :
    pass
  # create an istance
  pyl = PyListOfLeaves()
  pyb = PyListOfBranches()
  # add leaves as attributes
  for i in range(0,leaves.GetEntries() ) :
    leaf = leaves.At(i)
    name = leaf.GetName()
    # add dynamically attribute to my class 
    pyl.__setattr__(name,leaf)
    pass
  # add branches as atributes
  for i in range(0,branches.GetEntries() ) :
    branch = branches.At(i)
    name = branch.GetName()
    #print name
    # add dynamically attribute to my class 
    pyb.__setattr__(name,branch)
    pass

  nev = tree.GetEntries()
  for iev in range(0,nev) :
    tree.GetEntry(iev)
    if iev%50000 == 0: print 'Entry',iev
    # get values from the tree using Python class pyl which contains leaves/branches
    # objects 

    RunNumber                     = pyl.RunNumber.GetValue()
    EventNumber                   = pyl.EventNumber.GetValue()
    veto                          = pyl.veto.GetValue()
    eventWeight                   = pyl.eventWeight.GetValue()
    pileupWeight                  = pyl.pileupWeight.GetValue()
    pileupWeightUp                = pyl.pileupWeightUp.GetValue()
    pileupWeightDown              = pyl.pileupWeightDown.GetValue()
    genWeight                     = pyl.genWeight.GetValue()
    normWeight                    = pyl.normWeight.GetValue()
    nJet                          = pyl.nJet.GetValue()
    
    jetPt,jetEta,jetPhi,jetM,meffJet={},{},{},{},{}
    nj = int(round(nJet))
    for i in range(1,nj+1):
      jetPt[i]                    = tree.jetPt[i-1]    
      jetEta[i]                   = tree.jetEta[i-1]    
      jetPhi[i]                   = tree.jetPhi[i-1]    
      jetM[i]                     = tree.jetM[i-1] 
      pass

    met                           = pyl.met.GetValue()
    metPhi                        = pyl.metPhi.GetValue()
    dPhi                          = pyl.dPhi.GetValue()
    dPhiR                         = pyl.dPhiR.GetValue()
    meffInc                       = pyl.meffInc.GetValue()
    hardproc                      = pyl.hardproc.GetValue()
    Ap                            = pyl.Ap.GetValue()
    
    if nj>=1:
      meffJet[1] = tree.jetPt[0] + met
      pass
    if nj>=2:
      meffJet[2] = tree.jetPt[0] + tree.jetPt[1] + met
      pass
    if nj>=3:
      meffJet[3] = tree.jetPt[0] + tree.jetPt[1] + tree.jetPt[2] + met
      pass
    if nj>=4:
      meffJet[4] = tree.jetPt[0] + tree.jetPt[1] + tree.jetPt[2] + tree.jetPt[3] + met
      pass
    if nj>=5:
      meffJet[5] = tree.jetPt[0] + tree.jetPt[1] + tree.jetPt[2] + tree.jetPt[3] + tree.jetPt[4] + met
      pass
    if nj>=6:
      meffJet[6] = tree.jetPt[0] + tree.jetPt[1] + tree.jetPt[2] + tree.jetPt[3] + tree.jetPt[4] + tree.jetPt[5] + met
      pass

    metSigDefinition=(met/1000/TMath.Sqrt((meffInc-met)/1000))
    weight= genWeight*pileupWeight*normWeight*lumi

    for sr in SRlist:
      sr.process(veto,nJet,jetPt,met,dPhi,dPhiR,meffJet,meffInc,metSigDefinition,Ap,weight,RunNumber)

      
lumi=3.*1000.
SR2jvt = SignalRegion('2jvt', 2,1.0,200000.,    -1.0,-1.0,16.0,-1.0,1600000.)
SR4jAp = SignalRegion('4jAp',4,0.4,200000.,150000.0,0.04,-1.0, 0.2,2200000.)
SR5jMoriond  = SignalRegion('5jMoriond',5,0.4,200000.,60000.0,-1.0,-1.0, 0.2,2400000.)
SR4jt  = SignalRegion('4jt',4,0.4,130000.,60000.0,-1.0,-1.0, 0.25,2200000.)
SRlist = [SR2jvt, SR4jAp]



  
# mini-ntuple version
version=31

dirname="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLeptonRun2-00-00-"+str(version)+"/xAOD_13TeV/"
if version>30:
  dirname="root://eosatlas.cern.ch//eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-"+str(version)+"/p1872_13TeV/"
  
outdir="Outcutflow/v"+dirname.split("ZeroLeptonRun2-00-00-")[1].split("/")[0]
print "Output dir: ",outdir

class Sample:
  def __init__(self,name,filename,treename,isSignal):
    self.name = name
    self.filename = filename
    self.treename = treename 
    self.isSignal = isSignal

wosquark=True
    
samples = [
  Sample('$Z$+jets',dirname+'ZMassiveCB.root','Z_SRAll',False),
  Sample('$W$+jets',dirname+'WMassiveCB.root','W_SRAll',False),
  Sample('Top',dirname+'Top.root','Top_SRAll',False),
  Sample('gluino pair m(gluino,N1)=(1350, 0)~GeV',dirname+'GG_direct.root','GG_direct_1350_0_SRAll',True),
]
if not wosquark:
  samples +=[
    Sample('squark pair m(squark,N1)=(900, 0)~GeV',dirname+'SS_direct.root','SS_direct_900_0_SRAll',True),  
    ]

for sample in samples:
  runOnSample(sample.name,sample.filename,sample.treename,SRlist)

printLaTex(samples,SRlist,version)
