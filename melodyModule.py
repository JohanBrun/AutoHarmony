from enum import Enum
import random, math
from groupingModule import BaseGroup, SectionGroup
from localTypes import Voice, VoiceGroup, Direction, chordDict
from util import degreeOperator

class MelodyModule:
    currentDegree = 1

    def __init__(self, composition: SectionGroup, voice: Voice) -> None:
        self.composition = composition
        self.voice = voice
        # if voice.voiceGroup == VoiceGroup.SOPRANO: self.currentDegree = 5
        if voice.voiceGroup == VoiceGroup.ALTO: self.currentDegree = 3
        if voice.voiceGroup == VoiceGroup.TENOR: self.currentDegree = 5
        self.composition.groupDescent(self.populateBaseGroup)

    def populateBaseGroup(self, baseGroup: BaseGroup):
        voiceRange = self.voice.voiceRange
        octave = self.voice.startOctave

        for i in range(baseGroup.numBeats):
            # Check for edges of range
            if (octave == math.floor(voiceRange[0] / 12)): baseGroup.dir = Direction.ASCENDING
            if (octave == math.ceil(voiceRange[1] / 12)): baseGroup.dir = Direction.DESCENDING

            # Add current degree
            degree = self.currentDegree
            baseGroup.notes.append(degree)
            baseGroup.octaves.append(octave)
            baseGroup.suggestedChords.append(self.getSuggestedChords(degree))

            # Move to next degree
            movement = 0
            if (baseGroup.dir == Direction.ASCENDING):
                movement = 1
            elif (baseGroup.dir == Direction.DESCENDING):
                movement = -1
            elif (baseGroup.dir == Direction.STRAIGHT):
                movement = random.choice([-1, 0, 1])
            self.currentDegree, octave = degreeOperator(degree, octave, movement)
            
        self.voice.startOctave = octave
    
    def getSuggestedChords(self, degree: int):
        chords = []
        for key in chordDict:
            if degree in chordDict[key]: chords.append(key)
        return chords