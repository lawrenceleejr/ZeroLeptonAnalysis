import itertools
import os
import sys
import time

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0444) >> 2    # copy R bits to X
    os.chmod(path, mode)

def myreplace(l1, l2, element):
    idx = l1.index(element)
    if idx >= 0:
        return l1[:idx] + l2 + l1[idx+1:]

    # print "WARNING idx negative"
    return l1

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def cartesian_product(dicts):
    #return (dict(itertools.izip(dicts, x)) for x in itertools.product(*dicts.itervalues()))
    for x in itertools.product(*dicts.itervalues()):
        yield dict(itertools.izip(dicts, x)) 

def addWeight(oldList, newWeight):
    newList = deepcopy(oldList)
    newList.append(newWeight)
    return newList

def wait(sec):
    os.system('setterm -cursor off')
    while sec > 0:
        sys.stdout.write(str(sec) + '...     \r')
        sys.stdout.flush()
        sec -= 1
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            os.system('setterm -cursor on')
            print
            sys.exit()
    os.system('setterm -cursor on')
