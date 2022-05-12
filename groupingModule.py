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
        self.notes = []
        self.suggestedChords = []
        self.octaves = []

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
        octaves = []
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                notes += baseGroup.notes
                octaves += baseGroup.octaves
        return notes, octaves

    def groupDescent(self, baseGroupMethod):
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                baseGroupMethod(baseGroup)
