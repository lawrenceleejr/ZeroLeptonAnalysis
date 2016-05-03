########################################################
#
########################################################

class Parameter:
    def __init__(self,name,fullName,min,max):
        self.name=name
        self.fullName=fullName
        self.min=min
        self.max=max
        return

class Grid:
    def __init__(self, name, basename="",parList=[]):
        self.name=name
        if basename=="":
            self.basename=name
        else:
            self.basename=basename
        self.parList=parList
        return


allGrids={}

########################################################
# SS_direct
########################################################

par1=Parameter("m1","m(#chi^{0}_{1}) [GeV]",0,1000)
par0=Parameter("m0","m(#tilde{g}) [GeV]",600,2050)
gridGG_direct=Grid("GG_direct",parList=[par0,par1])
allGrids[gridGG_direct.name] = gridGG_direct


par1=Parameter("m1","m(#chi^{0}_{1}) [GeV]",0,750)
par0=Parameter("m0","m(#tilde{q}) [GeV]",400,1300)
gridSS_direct=Grid("SS_direct",parList=[par0,par1])
allGrids[gridSS_direct.name] = gridSS_direct



par1=Parameter("m2","m(#chi^{0}_{1}) [GeV]",0,800)
#par1=Parameter("m1","m(#chi^{#pm}_{1}) [GeV]",0,1800)
par0=Parameter("m0","m(#tilde{g}) [GeV]",200,1700)
gridGG_onestepCC_x05=Grid("GG_onestepCC_x05","GG_onestepCC",parList=[par0,par1])
allGrids[gridGG_onestepCC_x05.name] = gridGG_onestepCC_x05


#par1=Parameter("m2","m(#chi^{0}_{1}) [GeV]",0,1400)
par1=Parameter("m1","m(#chi^{#pm}_{1}) [GeV]",0,1600)
par0=Parameter("m0","m(#tilde{g}) [GeV]",1200,1600)
gridGG_onestepCC_mchi1060=Grid("GG_onestepCC_mchi1060","GG_onestepCC",parList=[par0,par1])
allGrids[gridGG_onestepCC_mchi1060.name] = gridGG_onestepCC_mchi1060


#par1=Parameter("m2","m(#chi^{0}_{1}) [GeV]",0,1400)
par1=Parameter("m1","m(#chi^{0}_{2}) [GeV]",100,1500)
par0=Parameter("m0","m(#tilde{g}) [GeV]",1000,1700)
gridSM_GG_N2_mchi101=Grid("SM_GG_N2_mchi101","SM_GG_N2",parList=[par0,par1])
allGrids[gridSM_GG_N2_mchi101.name] = gridSM_GG_N2_mchi101
