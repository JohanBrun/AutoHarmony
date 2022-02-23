import genMidi

majorScale = (0, 2, 4, 5, 7, 9, 11)
ks = 0

bassRange       = (39, 63) # E-2, E-4
tenorRange      = (46, 70) # B-2, B-4
altoRange       = (51, 75) # E-3, E-5
sopranoRange    = (58, 82) # B-3, B-5

cadence = ['I', 'IV', 'V', 'I']
triadDict = {
    'I':    [1, 3, 5],
    'IV':   [4, 6, 1],
    'V':    [5, 7, 2],
}

def genCadence():
    bass = []
    tenor = []
    alto = []
    soprano = []
    for c in cadence:
        bass.append(genBassNote(triadDict[c][0], bass[-1]))
        tenor.append(genTenorNote(triadDict[c][1], tenor[-1]))
        alto.append(genAltoNote(triadDict[c][2], alto[-1]))
        soprano.append(genSopranoNote(triadDict[c][0], soprano[-1]))
    return soprano, alto, tenor, bass

def genCadenceDegrees():
    bass    = [1]
    tenor   = [3]
    alto    = [5]
    soprano = [1]
    for c in cadence:
        bass.append(findClosestDegree(c, bass[-1]))
        tenor.append(findClosestDegree(c, tenor[-1]))
        alto.append(findClosestDegree(c, alto[-1]))
        soprano.append(findClosestDegree(c, soprano[-1]))
    return soprano[1:], alto[1:], tenor[1:], bass[1:]

def degreesToNotes(soprano, alto, tenor, bass):
    print(soprano)
    print(alto)
    print(tenor)
    print(bass)
    for i in range(len(soprano)):
        soprano[i] = getNoteFromScaleDegree(soprano[i], 0, majorScale)
        alto[i] = getNoteFromScaleDegree(alto[i], 0, majorScale)
        tenor[i] = getNoteFromScaleDegree(tenor[i], 0, majorScale)
        bass[i] = getNoteFromScaleDegree(bass[i], 0, majorScale)
    return soprano, alto, tenor, bass

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

def getNoteFromScaleDegree(degree: int, ks: int, scale):
    return getRoot(ks) + scale[degree - 1]

def findClosestDegree(chord: str, previousDegree: int):
    distance = 127
    closestDegree = previousDegree
    for degree in triadDict[chord]:
        if abs(degree - previousDegree) < distance:
            distance = abs(degree - previousDegree)
            closestDegree = degree
    return closestDegree
    


mg = genMidi.midiGenerator()
S, A, T, B = genCadenceDegrees()
S, A, T, B = degreesToNotes(S, A, T, B)
S = mg.buildVoiceStream(S)
A = mg.buildVoiceStream(A)
T = mg.buildVoiceStream(T)
B = mg.buildVoiceStream(B)

score = mg.buildVoicesScore(B, T, A, S)
score.show()