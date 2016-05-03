import ConfigParser
import os

from ..contours.data import OptimisationCut
from ..inputs.config import InputConfig

from zerolepton.colors import colors

class GridConfig:
    def __init__(self, grid, discovery=True, filename="{0}/settings/grids.cfg".format(os.getenv('ZEROLEPTONFITTER'))):
        self.setDefaults(grid)
        self.useDiscovery = discovery
        self.filename = None

        if not os.path.exists(filename):
            print("Can't find configuration {0}".format(filename))
            print("Using defaults, but be aware that this might crash")
            return

        config = ConfigParser.RawConfigParser()
        config.read(filename)
        if not config.has_section(grid):
            print(colors.WARNING + "GridConfig: The grid {0} is not defined in settings/grids.cfg!".format(grid) + colors.ENDC)
            print(colors.WARNING + "GridConfig: Using defaults, but be aware that this might crash" + colors.ENDC)
            return

        # Overwrite defaults by those given in the file
        vals = dict(config.items(grid))
        for k in list(vars(self).keys()):
            if k not in vals: continue
            # strip out " and ' - ConfigParser returns a raw string
            setattr(self, k, vals[k].replace('"', '').replace("'",""))

        # Fix our own optimisation cuts into a list of OptimisationCuts
        if self.optimisation_cuts != []:
            self.optimisation_cuts = [OptimisationCut(item) for item in self.optimisation_cuts.split(" ")]

        if self.filename is None:
            self.filename = "{0}.root".format(self.name)
            print(colors.WARNING + "GridConfig: warning - no input file was given for this grid. We are going to guess {0} based on the name.".format(self.filename) + colors.ENDC)
        
        inputConfig = InputConfig()
        self.filename = os.path.join(inputConfig.signal, self.filename)
        if not os.path.exists(self.filename) and not self.filename.find("eos")>=0:
            print(colors.WARNING + "GridConfig: warning - input file {0} does not exist".format(self.filename) + colors.ENDC)

        return

    def getSuffix(self):
        if self.useDiscovery:
            return self.listSuffix_discovery

        return self.listSuffix

    @property
    def x(self):
        return self.interpretation.split(":")[0]

    @property
    def y(self):
        return self.interpretation.split(":")[1]

    def setDefaults(self, grid):
        self.name = grid
        self.format = "hypo_"+grid+"_%f_%f"
        self.format_discovery = "hypo_discovery_"+grid+"_%f_%f"
        self.interpretation = "m0:m12"
        self.cutStr = "1"
        self.listSuffix = "__1_harvest_list"
        self.listSuffix_discovery = "_discovery_1_harvest_list"
        self.optimisation_cuts = {}

    def __str__(self):
        return "GridConfig: " + ', '.join("%s=%r" % (key,val) for (key,val) in vars(self).iteritems())
