from music21 import stream, note, instrument, clef, tempo, key
from groupingModule import SectionGroup
from localTypes import VoiceGroup
from util import getMidiValueFromScaleDegree

def getStream(composition: SectionGroup, voiceGroup: VoiceGroup):
    s = stream.Stream()
    s.insert(getInstrument(voiceGroup))
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

def getNoteFromDegree(degree: int, octave: int, ks: key.KeySignature):
    n = note.Note(getMidiValueFromScaleDegree(degree, 0) + octave * 12)
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