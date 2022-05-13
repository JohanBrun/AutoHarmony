import copy
from groupingModule import SectionGroup
from harmonyModule import HarmonyModule
from melodyModule import MelodyModule, Voice, VoiceGroup
from midiModule import MidiModule
from music21 import stream, instrument

def main():
    soprano = Voice(VoiceGroup.SOPRANO, ((58, 82)))
    alto = Voice(VoiceGroup.ALTO, (51, 75))
    tenor = Voice(VoiceGroup.TENOR, (46, 70))
    bass = Voice(VoiceGroup.BASS, ((39, 63)))

    compositionS = SectionGroup(3)
    MelodyModule(compositionS, soprano)

    compositionA = copy.deepcopy(compositionS)
    HarmonyModule(compositionA, alto)
    
    compositionT = copy.deepcopy(compositionA)
    HarmonyModule(compositionT, tenor)
    
    compositionB = copy.deepcopy(compositionT)
    HarmonyModule(compositionB, bass)
    """"
    s = stream.Stream([sopranoStream, altoStream, tenorStream, bassStream])
    """
    midiModule = MidiModule()

    sopranoStream = midiModule.getStream(compositionS, soprano.voiceGroup)
    altoStream = midiModule.getStream(compositionA, alto.voiceGroup)
    tenorStream = midiModule.getStream(compositionT, tenor.voiceGroup)
    bassStream = midiModule.getStream(compositionB, bass.voiceGroup)

    s = stream.Stream([sopranoStream, altoStream, tenorStream, bassStream])
    s.show()

if __name__ == '__main__':
    main()

