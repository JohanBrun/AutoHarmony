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
    def __init__(self, numGroups: int, contour: list[Direction]) -> None:
        assert numGroups > 1 and numGroups == len(contour)
        self.numGroups = numGroups
        self.contour = contour
        self.groups = []
        for dir in contour:
            self.groups.append(BaseGroup(4, dir))

class SectionGroup:
    def __init__(self, numGroups: int) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.groups = []
        for i in range(self.numGroups):
            contour, numSubGroups = self.buildContour()
            self.groups.append(PhraseGroup(numSubGroups, contour))

    def buildContour(self):
        contour = []
        for i in range(self.numGroups):
            contour.append(random.choice([Direction.ASCENDING, Direction.DESCENDING]))
        return contour, len(contour)

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
