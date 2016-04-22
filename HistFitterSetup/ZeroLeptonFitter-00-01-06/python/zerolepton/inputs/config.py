import ConfigParser
import fnmatch
import os
import socket

from ..colors import colors

class InputConfig:
    def __init__(self, filename="{0}/settings/inputs.cfg".format(os.getenv('ZEROLEPTONFITTER'))):
        if not os.path.exists(filename):
            print("Can't find configuration {0}".format(filename))
            print(colors.WARNING + "Using defaults, but be aware that this might crash" + colors.ENDC)
            return

        config = ConfigParser.RawConfigParser()
        config.read(filename)
        if not config.has_section('default'):
            raise Exception("InputConfig: The default block is not defined in settings/inputs.cfg!")
            return

        sectionData = {}
        for section in config.sections():
            sectionData[section] = dict(config.items(section))
            for k in sectionData[section]:
                sectionData[section][k] = sectionData[section][k].replace('"','')

        # Now what's our section?
        hostname = socket.getfqdn()
        print("InputConfig: Attempting to find input settings based on hostname {0}".format(hostname))
        mySection = "default"
        foundSite = False
        for section in sectionData:
            print section
            if "sites" in sectionData[section]:
                print "sites"
                names = sectionData[section]["sites"].replace('"','').lower().split(' ')
                for n in names:
                    if len(fnmatch.filter([hostname], n)) > 0:
                        mySection = section
                        print(colors.OKBLUE + "Hostname match on {0}".format(n) + colors.ENDC)
                        foundSite = True
                        break

                if foundSite:
                    break
                # better matching here
                #if hostname in sectionData[section]["sites"] or sectionData[section]["sites"] in hostname:
                #    mySection = section
                #    break

        setattr(self, 'section', mySection)
        print(colors.OKGREEN + "Loaded settings for site {0}".format(mySection) + colors.ENDC)

        self.site = mySection
        for k in sectionData[mySection]:
            if k == "sites": continue
            # strip out " and ' - ConfigParser returns a raw string
            setattr(self, k, sectionData[mySection][k].replace('"', '').replace("'",""))

        return

    def __str__(self):
        return "InputConfig: " + ', '.join("%s=%r" % (key,val) for (key,val) in vars(self).iteritems())
