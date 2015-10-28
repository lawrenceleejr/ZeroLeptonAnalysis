import json

from collections import namedtuple
from collections import OrderedDict

class ContourData:
    def __init__(self, gridConfig, filenames):
        # data is stored in a list of tuples
        self.data = {}
        self.gridConfig = gridConfig
        self.filenames = filenames

        self.combinedData = {}
        self.filteredData = {}

        self.combineOn = "CLsexp"
        if self.gridConfig.useDiscovery:
            self.combineOn = "p0exp"

        self.readAllFiles()

        # Combine and filter the data immediately.
        # This provides HUGE advantages over doing it on the fly - we don't
        # know which of the methods the user might call.
        # (For huge datasets this will be slow, but we don't have use datasets
        #  typically - all the method would have to keep track of weird caching)
        self.combineData()
        self.filterData()

    def readAllFiles(self):
        self.data = {}
        for f in self.filenames:
            self.data[f] = self.readFile(f)
            for p in self.data[f]:
                self.data[f][p]['fID'] = f

    def readFile(self, filename):
        with open(filename) as f:
            data = json.load(f)

        # Reformat into a dictionary
        Point = namedtuple('Point', ['x', 'y'])
        data = OrderedDict( [ (Point(d[self.gridConfig.x], d[self.gridConfig.y]), d) for d in data])

        return data

    def combineData(self):
        # we get work on a list of tuples (f, dataDict)
        # with f some unique key for the region
        # we return a dictionary
        retval = {}
        for f in self.data:
            regionData = self.data[f]
            for p in regionData:
                if p in retval and retval[p][self.combineOn] < regionData[p][self.combineOn]:
                    continue

                retval[p] = regionData[p]
                retval[p]['fID'] = f 

        self.combinedData = retval

    def writeCombinedData(self, outputFilename):
        with open(outputFilename, 'w') as f:
            # combinedData is a dict - to combine easier -, just write the values
            json.dump(self.combinedData.values(), f)

    def filterData(self):
        # makes a dictionary of cut => filteredData
        if self.gridConfig.optimisation_cuts == {}:
            self.filteredCombinedData = self.combinedData
            self.filteredData = self.data
            return

        self.filteredCombinedData = {cut: cut.filterData(self.combinedData) for cut in self.gridConfig.optimisation_cuts}
        self.filteredData = {}
        for f in self.data:
            # this would become unreadable with a double dict comprehension
            self.filteredData[f] = {cut: cut.filterData(self.data[f]) for cut in self.gridConfig.optimisation_cuts}

    @property
    def contributingRegions(self):
        # Return regions contributing in the merged dataset
        return self._contributingRegions(self.combinedData)

    @property
    def contributingRegionsFiltered(self):
        return {cut: self._contributingRegions(self.filteredCombinedData[cut]) for cut in self.filteredCombinedData}

    # Helper method
    def _contributingRegions(self, data):
        return {x['fID'] for x in data.values()}

class OptimisationCut:
    def __init__(self, cutStr):
        (k,v) = cutStr.split("=")
        self.key = k
        self.value = float(v)

    def filterData(self, data):
        # if we find a "-" in our key, we assume that the key is of the form x-y
        if "-" in self.key:
            (key1, key2) = self.key.split('-')
            return OrderedDict([ (point, vals) for (point, vals) in sorted(data.items()) if float(vals[key1]) - float(vals[key2]) == float(self.value) ]) 

        return OrderedDict([ (point, vals) for (point, vals) in sorted(data.items()) if float(vals[self.key]) == float(self.value) ]) 

    def __str__(self):
        return "OptimisationCut: key={0}, value={1}".format(self.key, self.value)
