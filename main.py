import copy
from groupingModule import SectionGroup
from harmonyModule import HarmonyModule
from melodyModule import MelodyModule, Voice, VoiceGroup
from midiModule import addChordNames, getStream
from music21 import stream

def main():
    soprano = Voice(VoiceGroup.SOPRANO, ((58, 82)))
    alto    = Voice(VoiceGroup.ALTO, (51, 75))
    tenor   = Voice(VoiceGroup.TENOR, (46, 70))
    bass    = Voice(VoiceGroup.BASS, ((39, 63)))

    compositionS = SectionGroup(3)
    MelodyModule(compositionS, soprano)

    compositionB = copy.deepcopy(compositionS)
    HarmonyModule(compositionB, bass)

    compositionA = copy.deepcopy(compositionS)
    HarmonyModule(compositionA, alto)
    
    compositionT = copy.deepcopy(compositionA)
    HarmonyModule(compositionT, tenor)
    
    sopranoStream = getStream(compositionS, soprano.voiceGroup)
    altoStream = getStream(compositionA, alto.voiceGroup)
    tenorStream = getStream(compositionT, tenor.voiceGroup)
    bassStream = getStream(compositionB, bass.voiceGroup)

    bassStream = addChordNames(bassStream)

    s = stream.Stream([sopranoStream, altoStream, tenorStream, bassStream])
    s.show()

if __name__ == '__main__':
    main()

