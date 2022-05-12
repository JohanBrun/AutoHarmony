from groupingModule import SectionGroup
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
    compositionA = SectionGroup(3)
    MelodyModule(compositionA, alto)
    compositionT = SectionGroup(3)
    MelodyModule(compositionT, tenor)
    compositionB = SectionGroup(3)
    MelodyModule(compositionB, bass)

    sopranoStream = getStream(compositionS)
    altoStream = getStream(compositionA)
    tenorStream = getStream(compositionT)
    bassStream = getStream(compositionB)

    s = stream.Stream([sopranoStream, altoStream, tenorStream, bassStream])
    s.show()
    
if __name__ == '__main__':
    main()

