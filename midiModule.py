from music21 import stream, note, chord, instrument
from groupingModule import SectionGroup
from localTypes import VoiceGroup
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

def getStream(composition: SectionGroup, voiceGroup: VoiceGroup):
    s = stream.Stream()
    s.insert(getInstrument(voiceGroup))
    degrees, octaves = composition.flatten()
    roman = ['I', 'ii', 'iii', 'IV', 'V', 'vi']
    for degree, octave in zip(degrees, octaves):
        n = note.Note(getNoteFromScaleDegree(degree, 0) + octave * 12)
        n.quarterLength = 4
        if voiceGroup == VoiceGroup.BASS:
            n.addLyric(roman[degree-1])
        s.append(n)
    return s

def getInstrument(voiceGroup: VoiceGroup):
    if voiceGroup == VoiceGroup.SOPRANO:
        return instrument.Soprano()
    elif voiceGroup == VoiceGroup.ALTO:
        return instrument.Alto()
    elif voiceGroup == VoiceGroup.TENOR:
        return instrument.Tenor()
    elif voiceGroup == VoiceGroup.BASS:
        return instrument.Bass()

def addChordNames(stream: stream.Stream):
    roman = ['I', 'ii', 'iii', 'IV', 'V', 'vi']
    for n in zip(stream):
        try:
            n.insertLyric('Chord')
        except:
            pass
    return stream