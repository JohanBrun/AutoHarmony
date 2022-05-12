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
    'I':    [1, 3, 5, 7],
    'iim':  [2, 4, 6, 1],
    'iiim': [3, 5, 7, 2],
    'IV':   [4, 6, 1, 3],
    'V':    [5, 7, 2, 4],
    'vim':  [6, 1, 3, 5]
}