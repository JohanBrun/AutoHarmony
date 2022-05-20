from enum import Enum
import random, math
from groupingModule import BaseGroup, SectionGroup
from localTypes import Voice, VoiceGroup, Direction, chordDict
from util import degreeOperator

class MelodyModule():
    currentDegree = 1

    def __init__(self, grouping: SectionGroup, voice: Voice) -> None:
        self.grouping = grouping
        self.voice = voice
        self.grouping.groupDescent(self.populateBaseGroup)

    def populateBaseGroup(self, baseGroup: BaseGroup):
        voiceRange = self.voice.voiceRange
        octave = self.voice.startOctave

        for i in range(baseGroup.numBeats):
            # Check for edges of range
            if (octave == math.floor(voiceRange[0] / 12)): baseGroup.dir = Direction.ASCENDING
            if (octave == math.ceil(voiceRange[1] / 12)): baseGroup.dir = Direction.DESCENDING

            # Add current degree
            degree = self.currentDegree
            baseGroup.degrees.append(degree)
            baseGroup.octaves.append(octave)
            # baseGroup.suggestedChords.append(self.getSuggestedChords(degree))
            baseGroup.suggestedChords.append(self.getSuggestedChords2())

            # Move to next degree
            movement = 0
            if (baseGroup.dir == Direction.ASCENDING):
                movement = 1
            elif (baseGroup.dir == Direction.DESCENDING):
                movement = -1
            self.currentDegree, octave = degreeOperator(degree, octave, movement)

        self.voice.startOctave = octave
    
    def getSuggestedChords(self, degree: int):
        chords = []
        for key in chordDict:
            if degree in chordDict[key]: chords.append(key)
        return chords

    def getSuggestedChords2(self):
        return [1, 2, 3, 4, 5, 6]