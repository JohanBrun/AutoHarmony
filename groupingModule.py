from random import choice, uniform
from numpy.random import default_rng
rng = default_rng()
from localTypes import Direction

class GroupingModule:
    def __init__(self) -> None:
        composition = SectionGroup(3)
    
class BaseGroup:
    index = 0

    def __init__(self, numBeats: int, dir: Direction, meanVA: tuple[float, float]) -> None:
        assert numBeats > 1
        self.numBeats = numBeats
        self.dir = dir
        self.degrees = []
        self.octaves = []
        self.suggestedChords = []
        self.valence, self.arousal = self.generateVA(meanVA)
        self.index += 1

    def generateVA(self, meanVA: tuple[int, int]):
        meanValence, meanArousal = meanVA
        valence = rng.laplace(meanValence, 0.1, self.numBeats)
        arousal = rng.laplace(meanArousal, 0.1, self.numBeats)
        return valence, arousal

class PhraseGroup:
    index = 0

    def __init__(self, numGroups: int, avgVA: tuple[float, float]) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.contour = self.buildContour()
        self.groups: list[BaseGroup] = []
        self.valenceMeans, self.arousalMeans = self.generateVAMeans(avgVA)

        for dir, meanValence, meanAoursal in zip(self.contour, self.valenceMeans, self.arousalMeans):
            self.groups.append(BaseGroup(4, dir, (meanValence, meanAoursal)))
        self.index += 1

    def generateVAMeans(self, avgVA):
        avgValence, avgArousal = avgVA
        valenceMeans = rng.laplace(avgValence, 0.1, self.numGroups)
        arousalMeans = []
        for i in range(self.numGroups):
            arousalMeans.append(avgArousal + i / 4)
        return valenceMeans, arousalMeans

    def buildContour(self):
        contour = []
        for i in range(self.numGroups):
            contour.append(choice([Direction.ASCENDING, Direction.DESCENDING]))
        return contour

class SectionGroup:
    def __init__(self, numGroups: int) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.groups: list[PhraseGroup] = []
        avgV, avgA = self.generateAvgVA()
        for avgV, avgA in zip(avgV, avgA):
            print(avgV, avgA)
            self.groups.append(PhraseGroup(self.numGroups, (avgV, avgA)))

    def flatten(self):
        degrees = []
        octaves = []
        valence = []
        arousal = []
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                degrees += baseGroup.degrees
                octaves += baseGroup.octaves
                valence += list(baseGroup.valence)
                arousal += list(baseGroup.arousal)
        return degrees, octaves, valence, arousal

    def groupDescent(self, baseGroupMethod):
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                baseGroupMethod(baseGroup)

    def generateAvgVA(self) -> tuple[list[float], list[float]]:
        meanValence, meanArousal = uniform(2, 8), uniform(-8, 8)
        return rng.laplace(meanValence, 0.1, self.numGroups), rng.laplace(meanArousal, 0.1, self.numGroups)
