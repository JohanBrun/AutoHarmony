from enum import Enum
from functools import total_ordering
import math

from util import getMidiValueFromScaleDegree

class Direction(Enum):
    ASCENDING = 1
    DESCENDING = -1

@total_ordering
class VoiceGroup(Enum):
    SOPRANO = 4
    ALTO = 3
    TENOR = 2
    BASS = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Motion(Enum):
    SIMILAR = 1
    OBLIQUE = 0
    COUNTER = -1
    ROOT = 4

class Voice:
    RANGES = {
        VoiceGroup.SOPRANO: (65, 82),
        VoiceGroup.ALTO:    (51, 75),
        VoiceGroup.TENOR:   (46, 70),
        VoiceGroup.BASS:    (39, 63)
    }

    def __init__(self, voiceGroup: VoiceGroup) -> None:
        self.voiceGroup = voiceGroup
        self.voiceRange = self.RANGES[voiceGroup]
        self.startingRange = (self.voiceRange[0] + 6, self.voiceRange[1] - 6)
        self.startOctave = math.ceil((3 * self.voiceRange[0] + self.voiceRange[1]) / 48)

    def isOutsideRange(self, degree: int, octave: int):
        midiValue = getMidiValueFromScaleDegree(degree) + octave * 12
        return midiValue < self.voiceRange[0] or midiValue > self.voiceRange[1]

chordDict: dict = {
    1: [1, 3, 5],
    2: [2, 4, 6],
    3: [3, 5, 7],
    4: [4, 6, 1],
    5: [5, 7, 2],
    6: [6, 1, 3]
}

extendedChordDict: dict[int, list[int]] = {
    1: [1, 1, 3, 3, 5, 5, 2, 4, 6, 7],
    2: [2, 2, 4, 4, 6, 6, 3, 5, 7, 1],
    3: [3, 3, 5, 5, 7, 7, 4, 6, 1, 2],
    4: [4, 4, 6, 6, 1, 1, 5, 7, 2, 3],
    5: [5, 5, 7, 7, 2, 2, 6, 1, 3, 4],
    6: [6, 6, 1, 1, 3, 3, 7, 2, 4, 5]
}

primaryChordProgressions = {
    1: [1, 2, 4, 6],
    2: [2, 3, 5],
    3: [1, 3, 4, 6],
    4: [2, 4, 5],
    5: [1, 3, 5, 6],
    6: [2, 4, 6]
}

secondaryChordProgressions = {
    1: [1, 3, 5],
    2: [1, 2, 4, 6],
    3: [2, 3, 5],
    4: [1, 3, 4, 6],
    5: [2, 4, 5],
    6: [1, 3, 5, 6]
}

