from music21 import stream, note, instrument, clef, tempo, key
from groupingModule import SectionGroup
from localTypes import VoiceGroup
from util import getMidiValue, getMidiValueFromScaleDegree

def getStream(composition: SectionGroup, voiceGroup: VoiceGroup):
    s = stream.Stream()
    s.insert(instrument.Tenor())
    s.insert(getClef(voiceGroup))
    s.insert(tempo.MetronomeMark(number=80))
    degrees, octaves, durations, _, _ = composition.flatten()
    roman = ['I', 'ii', 'iii', 'IV', 'V', 'vi']
    ks = key.KeySignature(0)
    for degree, octave, duration in zip(degrees, octaves, durations):
        n = getNoteFromDegree(degree, octave, ks)
        n.quarterLength = duration
        if voiceGroup == VoiceGroup.BASS:
            n.addLyric(roman[degree-1])
        s.append(n)
    return s

def checkChords(soprano: SectionGroup, alto: SectionGroup, tenor: SectionGroup, bass: SectionGroup):
    sDegrees, sOctaves, sDurations, _, _ = soprano.flatten()
    aDegrees, aOctaves, aDurations, _, _ = alto.flatten()
    tDegrees, tOctaves, tDurations, _, _ = tenor.flatten()
    bDegrees, bOctaves, bDurations, _, _ = bass.flatten()
    for ad, ao in zip(aDegrees, aOctaves):
        print(getMidiValue(ad, ao))


def showStream(*voiceStreams: stream.Stream):
    s = stream.Stream(list(voiceStreams))
    s.show()
    s.write('midi', 'composition.midi')

def getNoteFromDegree(degree: int, octave: int, ks: key.KeySignature):
    n = note.Note(getMidiValueFromScaleDegree(degree) + octave * 12)
    n.pitch.accidental = ks.accidentalByStep(n.step)
    return n

def getInstrument(voiceGroup: VoiceGroup):
    if voiceGroup == VoiceGroup.SOPRANO:
        return instrument.Tenor()
    elif voiceGroup == VoiceGroup.ALTO:
        return instrument.Tenor()
    elif voiceGroup == VoiceGroup.TENOR:
        return instrument.Tenor()
    elif voiceGroup == VoiceGroup.BASS:
        return instrument.Bass()

def getClef(voiceGroup: VoiceGroup):
    if voiceGroup == VoiceGroup.SOPRANO:
        return clef.TrebleClef()
    elif voiceGroup == VoiceGroup.ALTO:
        return clef.TrebleClef()
    elif voiceGroup == VoiceGroup.TENOR:
        return clef.Treble8vbClef()
    elif voiceGroup == VoiceGroup.BASS:
        return clef.BassClef()

def noteInKeyFromMidiValue(midiValue: int, ks: key.KeySignature):
    n = note.Note(midiValue)
    nStep = n.pitch.step
    rightAccidental = ks.accidentalByStep(nStep)
    n.pitch.accidental = rightAccidental
    return n

