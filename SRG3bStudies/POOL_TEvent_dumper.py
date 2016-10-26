import ROOT
c = ROOT.TChain("CollectionTree")
c.Add("*.ESD.pool.root")
evt = ROOT.POOL.TEvent(ROOT.POOL.TEvent.kPOOLAccess)
evt.readFrom(c)


for i in range(evt.getEntries()):
  evt.getEntry(i)
  ei = evt.retrieve("xAOD::EventInfo","EventInfo")
  met_lht = evt.retrieve("xAOD::MissingETContainer","MET_LocHadTopo")
  print ei.runNumber(), ei.eventNumber(), met_lht["LocHadTopo"].met()
