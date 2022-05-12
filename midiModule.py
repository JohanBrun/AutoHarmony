from music21 import stream, note, chord
from groupingModule import SectionGroup
from util import getRoot, getNoteFromScaleDegree


class MidiModule:
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

def getStream(composition: SectionGroup):
    s = stream.Stream()
    for degree, octave in composition.flatten():
        n = note.Note(getNoteFromScaleDegree(degree, 0) + octave * 12)
        s.append(n)
    return s