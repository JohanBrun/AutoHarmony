import random, copy
from groupingModule import BaseGroup, SectionGroup
from localTypes import Voice, Motion, VoiceGroup, chordDict
from util import degreeOperator

class HarmonyModule:
    currentMotion = None
    finalChords = []
    def __init__(self, composition: SectionGroup, voice: Voice) -> None:
        self.composition = composition
        self.voice = voice
        self.composition.groupDescent(self.harmonize)
        print(self.finalChords)
        self.currentDegree = 1
        self.currentOctave = voice.startOctave

    def harmonize(self, baseGroup: BaseGroup):
        if self.voice.voiceGroup == VoiceGroup.ALTO:
            self.parallelMotion(baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords)
        if self.voice.voiceGroup == VoiceGroup.TENOR:
            self.obliqueMotion(baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords)
        if self.voice.voiceGroup == VoiceGroup.BASS:
            self.rootMotion(baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords)
            
    def parallelMotion(self, degrees, octaves, suggestedChords):
        for i in range(len(degrees)):
            degrees[i], octaves[i] = degreeOperator(degrees[i], octaves[i], -2)
            suggestedChords[i] = self.updateSuggestedChords(degrees[i], suggestedChords[i])

    def obliqueMotion(self, degrees, octaves, suggestedChords):
        if self.currentMotion == Motion.OBLIQUE:
            firstNote = self.currentDegree
            firstOctave = self.currentOctave
        else:
            self.currentMotion = Motion.OBLIQUE
            firstNote = degrees[0]
            firstOctave = octaves[0]
        for i in range(len(degrees)):
            degrees[i], octaves[i] = firstNote, firstOctave
            updatedChords = self.updateSuggestedChords(degrees[i], suggestedChords[i])
            while updatedChords == []:
                degrees[i], octaves[i] = degreeOperator(degrees[i], octaves[i], -1)
                updatedChords = self.updateSuggestedChords(degrees[i], suggestedChords[i])
            suggestedChords[i] = updatedChords
        self.currentDegree = degrees[-1]
        self.currentOctave = octaves[-1]

    def rootMotion(self, degrees, octaves, suggestedChords):
        for i in range(len(degrees)):
            chord = random.choice(suggestedChords[i])
            self.finalChords.append(chord)
            degrees[i] = chordDict[chord][0]
            if i == 0: octaves[i] = self.voice.startOctave - 1
            elif degrees[i] - degrees[i - 1] > 4:
                octaves[i] = octaves[i - 1] - 1
            elif degrees[i] - degrees[i - 1] < -4:
                octaves[i] = octaves[i - 1] + 1
            else:
                octaves[i] = octaves[i - 1]


    def updateSuggestedChords(self, degree: int, chords: list[str]):
        newChords = []
        for key in chords:
            if degree in chordDict[key]:
                newChords.append(key)
        return newChords
    
