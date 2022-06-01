import copy
import sys
from groupingModule import SectionGroup
from harmonyModule import HarmonyModule
from melodyModule import MelodyModule
from localTypes import Voice, VoiceGroup
from midiModule import checkChords, getStream, showStream
import matplotlib.pyplot as plt
import random


def main():
    seed = random.randint(0, sys.maxsize)
    random.seed(seed)
    print(seed)
    showVA = True

    soprano = Voice(VoiceGroup.SOPRANO)
    alto    = Voice(VoiceGroup.ALTO)
    tenor   = Voice(VoiceGroup.TENOR)
    bass    = Voice(VoiceGroup.BASS)

    compositionS = SectionGroup(3)
    MelodyModule(compositionS, soprano)

    compositionB = copy.deepcopy(compositionS)
    HarmonyModule(compositionB, bass)

    compositionA = copy.deepcopy(compositionB)
    HarmonyModule(compositionA, alto)
    
    compositionT = copy.deepcopy(compositionA)
    HarmonyModule(compositionT, tenor)
    
    sopranoStream   = getStream(compositionS, soprano.voiceGroup)
    altoStream      = getStream(compositionA, alto.voiceGroup)
    tenorStream     = getStream(compositionT, tenor.voiceGroup)
    bassStream      = getStream(compositionB, bass.voiceGroup)
    showStream(sopranoStream, altoStream, tenorStream, bassStream)
    # checkChords(compositionS, compositionA, compositionT, compositionB)

    if showVA:
        _, _, _, valence, arousal = compositionS.flatten()
        fig, ax = plt.subplots()
        ax.set_title('Valence')
        ax.plot(valence, linewidth=2.0)

        fig, ax = plt.subplots()
        ax.set_title('Arousal')
        ax.plot(arousal, linewidth=2.0)

        plt.show()

if __name__ == '__main__':
    main()

