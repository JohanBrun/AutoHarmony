from random import choice, uniform
from numpy.random import default_rng
rng = default_rng()
from localTypes import Direction

class GroupingModule:
    def __init__(self) -> None:
        composition = SectionGroup(3)
    
class BaseGroup:
    index = 0

    def __init__(self, dir: Direction, meanVA: tuple[float, float]) -> None:
        self.dir = dir
        self.degrees = []
        self.octaves = []
        self.chords = []
        self.availableDegrees = []
        self.valence, self.arousal = meanVA
        self.numUnits, self.numBeats, self.durations = self.generateRythm(meanVA[1], uniform(-2,2))
        self.index += 1

    def generateVA(self, meanVA: tuple[int, int]):
        meanValence, meanArousal = meanVA
        valence = rng.laplace(meanValence, 0.1, 4)
        arousal = rng.laplace(meanArousal, 0.1, 4)
        return valence, arousal

    def generateRythm(self, arousal: float, diff: float):
        numUnits = 0
        numBeats = 0
        durations = 0
        if arousal < -5:
            numUnits = 1
            numBeats = 4
        if arousal < 0:
            numUnits = 2
            numBeats = 4
        if arousal >= 0:
            numUnits = 4
            numBeats = 4
        if arousal > 5:
            numUnits = 4
            numBeats = 2
        durations = numUnits * [numBeats / numUnits]
        if diff < -1 and arousal > -5:
            numUnits -= 1
            durations.pop(-1)
            durations[-1] *= 2
        if diff > 1 and arousal < 5:
            numUnits += 1
            durations[0] /= 2
            durations.insert(0, durations[0])
        return numUnits, numBeats, durations

class PhraseGroup:
    index = 0

    def __init__(self, numGroups: int, avgVA: tuple[float, float]) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.contour = self.buildContour()
        self.groups: list[BaseGroup] = []
        self.valenceMeans, self.arousalMeans = self.generateVAMeans(avgVA)
        for dir, meanValence, meanAoursal in zip(self.contour, self.valenceMeans, self.arousalMeans):
            self.groups.append(BaseGroup(dir, (meanValence, meanAoursal)))
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
        durations = []
        valence = []
        arousal = []
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                degrees += baseGroup.degrees
                octaves += baseGroup.octaves
                durations += baseGroup.durations
                valence.append(baseGroup.valence)
                arousal.append(baseGroup.arousal)
        return degrees, octaves, durations, valence, arousal

    def groupDescent(self, baseGroupMethod):
        for phraseGroup in self.groups:
            for baseGroup in phraseGroup.groups:
                baseGroupMethod(baseGroup)

    def generateAvgVA(self) -> tuple[list[float], list[float]]:
        meanValence, meanArousal = uniform(2, 8), uniform(-8, 8)
        return rng.laplace(meanValence, 0.1, self.numGroups), rng.laplace(meanArousal, 0.1, self.numGroups)
