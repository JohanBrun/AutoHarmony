from music21 import stream, note, chord, instrument
from groupingModule import SectionGroup
from localTypes import VoiceGroup
from util import getRoot, getNoteFromScaleDegree


class MidiModule:
    streamMatrix = []

    def buildVoiceStream(self, midiValues: list[int]):
        notes = [note.Note(mv) for mv in midiValues]
        return stream.Stream(notes)

    def buildVoicesScore(self, bass, tenor, alto, soprano):
        return stream.Score([soprano, alto, tenor, bass])

    def buildVoiceStreamFromChords(self, midiValues: list[int]):
        s = stream.Stream()
        for c in midiValues:
            s.append(chord.Chord(c))
        return s

    def getStream(self, composition: SectionGroup, voiceGroup: VoiceGroup):
        s = stream.Stream()
        s.insert(self.getInstrument(voiceGroup))
        degrees, octaves = composition.flatten()
        for degree, octave in zip(degrees, octaves):
            n = note.Note(getNoteFromScaleDegree(degree, 0) + octave * 12)
            n.quarterLength = 4
            s.append(n)
        self.streamMatrix.append(s)
        return s

    def getChords(self):
        for j in range(len(self.streamMatrix[0])):
            c = chord.Chord([self.streamMatrix[0][j], self.streamMatrix[1][j], self.streamMatrix[2][j]])
            print(c.fullName)

    def getInstrument(self, voiceGroup: VoiceGroup):
        if voiceGroup == VoiceGroup.SOPRANO:
            return instrument.Soprano()
        elif voiceGroup == VoiceGroup.ALTO:
            return instrument.Alto()
        elif voiceGroup == VoiceGroup.TENOR:
            return instrument.Tenor()
        elif voiceGroup == VoiceGroup.BASS:
            return instrument.Bass()