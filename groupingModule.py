from enum import Enum
import random

class Direction(Enum):
    ASCENDING = 1
    DESCENDING = 2
    STRAIGHT = 3


class GroupingModule:
    def __init__(self) -> None:
        composition = SectionGroup(3)
    
class BaseGroup:
    def __init__(self, numBeats: int, dir: Direction) -> None:
        assert numBeats > 1
        self.numBeats = numBeats
        self.dir = dir
        self.notes = []

class PhraseGroup:
    def __init__(self, numGroups: int, contour: list[Direction]) -> None:
        assert numGroups == len(contour)
        self.numGroups = numGroups
        self.contour = contour
        self.groups = []
        for dir in contour:
            self.groups.append(BaseGroup(4, dir))

class SectionGroup:
    def __init__(self, numGroups: int) -> None:
        self.numGroups = numGroups
        self.groups = []
        for i in range(self.numGroups):
            contour, numSubGroups = self.buildContour()
            self.groups.append(PhraseGroup(numSubGroups, contour))

    def buildContour(self):
        contour = []
        for i in range(3):
            contour.append(random.choice([Direction.ASCENDING, Direction.DESCENDING, Direction.STRAIGHT]))
        return contour, len(contour)

    def flatten(self):
        notes = []
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                notes += baseGroup.notes
        return notes
