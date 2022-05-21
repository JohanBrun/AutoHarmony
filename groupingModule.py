import random
from localTypes import Direction

class GroupingModule:
    def __init__(self) -> None:
        composition = SectionGroup(3)
    
class BaseGroup:
    def __init__(self, numBeats: int, dir: Direction) -> None:
        assert numBeats > 1
        self.numBeats = numBeats
        self.dir = dir
        self.degrees = []
        self.octaves = []
        self.suggestedChords = []

class PhraseGroup:
    def __init__(self, numGroups: int) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.contour = self.buildContour()
        self.groups = []
        for dir in self.contour:
            self.groups.append(BaseGroup(4, dir))

    def buildContour(self):
        contour = []
        for i in range(self.numGroups):
            contour.append(random.choice([Direction.ASCENDING, Direction.DESCENDING]))
        return contour

class SectionGroup:
    def __init__(self, numGroups: int) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.groups = []
        for i in range(self.numGroups):
            self.groups.append(PhraseGroup(self.numGroups))

    def flatten(self):
        degrees = []
        octaves = []
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                degrees += baseGroup.degrees
                octaves += baseGroup.octaves
        return degrees, octaves

    def groupDescent(self, baseGroupMethod):
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                baseGroupMethod(baseGroup)
