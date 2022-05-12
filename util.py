import chordModule
from localTypes import chordDict

bassRange       = (39, 63) # E-2, E-4
tenorRange      = (46, 70) # B-2, B-4
altoRange       = (51, 75) # E-3, E-5
sopranoRange    = (58, 82) # B-3, B-5

majorScale = (0, 2, 4, 5, 7, 9, 11)
ks = 0

def genBassNote(chord: str, previous: int = 1):
    d = findClosestDegree(chord, previous)
    n = getNoteFromScaleDegree(d, ks, majorScale)
    n += (bassRange[0] // 12) * 12
    return n

def genTenorNote(chord: str, previous: int = 3):
    d = findClosestDegree(chord, previous)
    n = getNoteFromScaleDegree(d, ks, majorScale)
    n += (tenorRange[0] // 12 + 1) * 12
    return n

def genAltoNote(chord: str, previous: int = 5):
    d = findClosestDegree(chord, previous)
    n = getNoteFromScaleDegree(d, ks, majorScale)
    n += (altoRange[0] // 12 + 1) * 12
    return n

def genSopranoNote(chord: str, previous: int = 1):
    d = findClosestDegree(chord, previous)
    n = getNoteFromScaleDegree(d, ks, majorScale)
    n += (sopranoRange[0] // 12 + 1) * 12
    return n
    
def getRoot(keySignature: int):
    if keySignature < 0:
        root = keySignature * -5
    else:
        root = keySignature * 7
    return root

def getNoteFromScaleDegree(degree: int, ks: int):
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
    
def degreeOperator(degree: int, octave: int, change: int):
    degree += change
    if degree > 7:
        degree -= 7
        octave += 1
    if degree < 1:
        degree += 7
        octave -= 1
    return degree, octave