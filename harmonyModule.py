import random, copy
from groupingModule import BaseGroup, SectionGroup
from localTypes import Voice, Motion, chordDict
from util import degreeOperator

class HarmonyModule:
    def __init__(self, composition: SectionGroup, voice: Voice) -> None:
        self.composition = composition
        self.voice = voice
        self.composition.groupDescent(self.harmonize)

    def harmonize(self, baseGroup: BaseGroup):
        self.parallelMotion(baseGroup.notes, baseGroup.octaves, baseGroup.suggestedChords)        
            
    def parallelMotion(self, notes, octaves, suggestedChords):
        for i in range(len(notes)):
            notes[i], octaves[i] = degreeOperator(notes[i], octaves[i], -2)
            suggestedChords[i] = self.updateSuggestedChords(notes[i], suggestedChords[i])

    def updateSuggestedChords(self, degree: int, chords: list[str]):
        newChords = []
        for key in chords:
            if degree in chordDict[key]:
                newChords.append(key)
        return newChords
    
