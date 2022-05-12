import chordModule
import midiModule
import util
import random
import copy

midOfRanges = [51, 63, 63, 70]
progression = ['I', 'IV', 'ii', 'V', 'I', 'IV', 'ii', 'V', 'IV', 'I']
chords = []
for i in range(10):
    chord = copy.copy(random.choice(chordModule.chordDict[progression[i]]))
    for i in range(len(chord)):
        chord[i] = util.getNoteFromScaleDegree(chord[i], 0, util.majorScale)
        chord[i] += (midOfRanges[i] // 12) * 12
    chords.append(chord)

mg = midiModule.midiGenerator()
s = mg.buildVoiceStreamFromChords(chords)
s.show()

