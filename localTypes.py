from enum import Enum
import math

class Direction(Enum):
    ASCENDING = 1
    DESCENDING = 2
    STRAIGHT = 3

class VoiceGroup(Enum):
    SOPRANO = 1
    ALTO = 2
    TENOR = 3
    BASS = 4

class Motion(Enum):
    PARALLEL = 1
    SIMILAR = 2
    OBLIQUE = 3
    COUNTER = 4
    FILL = 5

class Voice:
    def __init__(self, voiceGroup: VoiceGroup, voiceRange: tuple[int, int]) -> None:
        self.voiceGroup = voiceGroup
        self.voiceRange = voiceRange
        self.startOctave = math.ceil((voiceRange[0] + voiceRange[1]) / 24)

chordDict: dict = {
    1: [1, 3, 5, 7],
    2: [2, 4, 6, 1],
    3: [3, 5, 7, 2],
    4: [4, 6, 1, 3],
    5: [5, 7, 2, 4],
    6: [6, 1, 3, 5]
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

