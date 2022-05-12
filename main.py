import copy
from groupingModule import SectionGroup
from harmonyModule import HarmonyModule
from melodyModule import MelodyModule, Voice, VoiceGroup
from midiModule import getStream
from music21 import stream

def main():
    soprano = Voice(VoiceGroup.SOPRANO, ((58, 82)))
    alto = Voice(VoiceGroup.ALTO, (51, 75))
    tenor = Voice(VoiceGroup.TENOR, (46, 70))
    bass = Voice(VoiceGroup.BASS, ((39, 63)))

    compositionS = SectionGroup(3)
    MelodyModule(compositionS, soprano)

    compositionA = copy.deepcopy(compositionS)
    HarmonyModule(compositionA, alto)
    """"
    MelodyModule(compositionA, alto)
    compositionT = SectionGroup(3)
    MelodyModule(compositionT, tenor)
    compositionB = SectionGroup(3)
    MelodyModule(compositionB, bass)
    tenorStream = getStream(compositionT)
    bassStream = getStream(compositionB)
    s = stream.Stream([sopranoStream, altoStream, tenorStream, bassStream])
    """

    sopranoStream = getStream(compositionS)
    altoStream = getStream(compositionA)
    s = stream.Stream([sopranoStream, altoStream])
    s.show()

if __name__ == '__main__':
    main()

