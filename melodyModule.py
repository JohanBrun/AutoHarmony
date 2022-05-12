from enum import Enum
import random, math
from groupingModule import BaseGroup, Direction, SectionGroup


class VoiceGroup(Enum):
    SOPRANO = 1
    ALTO = 2
    TENOR = 3
    BASS = 4

class Voice:
    def __init__(self, voiceGroup: VoiceGroup, voiceRange) -> None:
        self.voiceGroup = voiceGroup
        self.voiceRange = voiceRange
        self.startOctave = (voiceRange[0] + voiceRange[1]) // 24

class MelodyModule:
    currentDegree = 1

    def __init__(self, composition: SectionGroup, voice: Voice) -> None:
        self.composition = composition
        self.voice = voice
        # if voice.voiceGroup == VoiceGroup.SOPRANO: self.currentDegree = 5
        if voice.voiceGroup == VoiceGroup.ALTO: self.currentDegree = 3
        if voice.voiceGroup == VoiceGroup.TENOR: self.currentDegree = 5
        self.groupDescent()

    def groupDescent(self):
        for phraseGroup in self.composition.groups:
            for baseGroup in phraseGroup.groups:
                self.populateBaseGroup(baseGroup)


    def populateBaseGroup(self, baseGroup: BaseGroup):
        voiceRange = self.voice.voiceRange
        octave = self.voice.startOctave

        for i in range(baseGroup.numBeats):
            # Check for edges of range
            if (octave == math.floor(voiceRange[0] / 12)): baseGroup.dir = Direction.ASCENDING
            if (octave == math.ceil(voiceRange[1] / 12)): baseGroup.dir = Direction.DESCENDING

            # Add current degree
            degree = self.currentDegree
            baseGroup.notes.append((degree, octave))

            # Move to next
            if (baseGroup.dir == Direction.ASCENDING):
                self.currentDegree += 1
            elif (baseGroup.dir == Direction.DESCENDING):
                self.currentDegree -= 1
            elif (baseGroup.dir == Direction.STRAIGHT):
                move = random.choice([-1, 0, 1])
                self.currentDegree += move
            if self.currentDegree > 7:
                    self.currentDegree -= 7
                    octave += 1
            if self.currentDegree < 1:
                    self.currentDegree += 7
                    octave -= 1
        self.octave = octave