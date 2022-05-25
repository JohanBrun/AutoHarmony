import copy
from groupingModule import SectionGroup
from harmonyModule import HarmonyModule
from melodyModule import MelodyModule, Voice, VoiceGroup
from midiModule import getStream
from music21 import stream
import matplotlib.pyplot as plt
import random

def main():
    random.seed(1)
    showVA = False

    soprano = Voice(VoiceGroup.SOPRANO)
    alto    = Voice(VoiceGroup.ALTO)
    tenor   = Voice(VoiceGroup.TENOR)
    bass    = Voice(VoiceGroup.BASS)

    compositionS = SectionGroup(2)
    MelodyModule(compositionS, soprano)

    compositionB = copy.deepcopy(compositionS)
    HarmonyModule(compositionB, bass, soprano)

    compositionA = copy.deepcopy(compositionB)
    HarmonyModule(compositionA, alto, soprano)
    
    compositionT = copy.deepcopy(compositionA)
    HarmonyModule(compositionT, tenor, soprano)
    
    sopranoStream = getStream(compositionS, soprano.voiceGroup)
    altoStream = getStream(compositionA, alto.voiceGroup)
    tenorStream = getStream(compositionT, tenor.voiceGroup)
    bassStream = getStream(compositionB, bass.voiceGroup)

    s = stream.Stream([sopranoStream, altoStream, tenorStream, bassStream])
    s.show()
    s.write('midi', 'composition.midi')

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

