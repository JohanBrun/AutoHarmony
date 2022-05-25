from localTypes import chordDict
    
def getRoot(keySignature: int):
    if keySignature < 0:
        root = keySignature * -5
    else:
        root = keySignature * 7
    return root

def getMidiValueFromScaleDegree(degree: int, ks: int):
    majorScale = (0, 2, 4, 5, 7, 9, 11)
    return getRoot(ks) + majorScale[degree - 1]

def findClosestDegree(chord: str, previousDegree: int):
    distance = 127
    closestDegree = previousDegree
    for degree in chordDict[chord]:
        if abs(degree - previousDegree) < distance:
            distance = abs(degree - previousDegree)
            closestDegree = degree
    return closestDegree
    
def degreeOperator(degree: int, octave: int, change: int) -> tuple[int, int]:
    degree += change
    if degree > 7:
        degree -= 7
        octave += 1
    if degree < 1:
        degree += 7
        octave -= 1
    return degree, octave

def intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3