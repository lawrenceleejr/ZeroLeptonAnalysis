import os

def myreplace(l1, l2, element):
    idx = l1.index(element)
    if idx >= 0:
        return l1[:idx] + l2 + l1[idx+1:]
    
    print "WARNING idx negative"
    return l1

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
