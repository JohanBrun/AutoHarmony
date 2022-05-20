from enum import Enum
from functools import total_ordering
import math

class Direction(Enum):
    ASCENDING = 1
    DESCENDING = -1
    STRAIGHT = 0

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
        VoiceGroup.SOPRANO: (58, 82),
        VoiceGroup.ALTO:    (51, 75),
        VoiceGroup.TENOR:   (46, 70),
        VoiceGroup.BASS:    (39, 63)
    }

    def __init__(self, voiceGroup: VoiceGroup) -> None:
        self.voiceGroup = voiceGroup
        self.voiceRange = self.RANGES[voiceGroup]
        self.startingRange = (self.voiceRange[0] + 6, self.voiceRange[1] - 6)
        self.startOctave = math.ceil((3 * self.voiceRange[0] + self.voiceRange[1]) / 48)

chordDict: dict = {
    1: [1, 3, 5],
    2: [2, 4, 6],
    3: [3, 5, 7],
    4: [4, 6, 1],
    5: [5, 7, 2],
    6: [6, 1, 3]
}

primaryChordProgressions = {
    1: [2, 4, 6],
    2: [3, 5],
    3: [1, 4, 6],
    4: [2, 5],
    5: [1, 3, 6],
    6: [2, 4]
}

secondaryChordProgressions = {
    1: [3, 5],
    2: [1, 4, 6],
    3: [2, 5],
    4: [1, 3, 6],
    5: [2, 4],
    6: [1, 3, 5]
}

