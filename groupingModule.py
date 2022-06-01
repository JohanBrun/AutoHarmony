import math
import random
from numpy.random import default_rng
rng = default_rng()
from localTypes import Direction

class SectionGroup():
    def __init__(self, numPhrases: int) -> None:
        assert numPhrases > 1
        self.phrases: list[PhraseGroup] = []
        for i in range(numPhrases):
            self.phrases.append(PhraseGroup(2))

    def flatten(self):
        degrees = []
        octaves = []
        durations = []
        valence = []
        arousal = []
        for phraseGroup in self.phrases:
            for phraseSubGroup in phraseGroup.groups:
                for baseGroup in phraseSubGroup.groups:
                    degrees += baseGroup.degrees
                    octaves += baseGroup.octaves
                    durations += baseGroup.durations
                    valence.append(baseGroup.valence)
                    arousal.append(baseGroup.arousal)
        return degrees, octaves, durations, valence, arousal

    def groupDescent(self, baseGroupMethod):
        for phraseGroup in self.phrases:
            for phraseSubGroup in phraseGroup.groups:
                for baseGroup in phraseSubGroup.groups:
                    baseGroupMethod(baseGroup)

class PhraseGroup:
    def __init__(self, numGroups: int) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.numBaseGroups = numGroups
        self.groups: list[PhraseSubGroup] = []
        contour = self.buildContour()
        meanVs, meanAs = self.generateVAMeans()
        for i in range(self.numGroups - 1):
            self.groups.append(PhraseSubGroup(self.numBaseGroups, (meanVs[i], meanAs[i]), contour[i]))
        self.groups.append(EndingPhrase(self.numBaseGroups, (meanVs[-1], meanAs[-1]), contour[-1]))

    def generateVAMeans(self) -> tuple[list[float], list[float]]:
        meanValence, meanArousal = rng.uniform(0, 10), rng.uniform(-10, 10)
        return (
            rng.normal(meanValence, 0.1, self.numGroups), rng.normal(meanArousal, 0.1, self.numGroups)
        )

    def buildContour(self):
        contour = []
        availableDirections = []
        for i in range(math.ceil((self.numGroups * self.numBaseGroups) / 2)):
            availableDirections += [Direction.ASCENDING, Direction.DESCENDING]
        for i in range(self.numGroups):
            subPhraseContour = []
            for j in range(self.numBaseGroups):
                subPhraseContour += [availableDirections.pop(random.randrange(0, len(availableDirections)))]
            contour.append(subPhraseContour)
        return contour

class PhraseSubGroup:
    def __init__(self, numGroups: int, avgVA: tuple[float, float], contour: list[Direction]) -> None:
        assert numGroups > 1
        self.numGroups = numGroups
        self.contour = contour
        self.groups: list[BaseGroup] = []
        self.valenceMeans, self.arousalMeans = self.generateVAMeans(*avgVA)
        self.diffV = rng.uniform(-2, 2)
        for i in range(self.numGroups):
            self.groups.append(BaseGroup(self.contour[i], (self.valenceMeans[i], self.arousalMeans[i]), self.diffV))

    def generateVAMeans(self, avgValence: float, avgArousal: float):
        return rng.normal(avgValence, 0.1, self.numGroups), rng.normal(avgArousal, 0.1, self.numGroups)

class EndingPhrase(PhraseSubGroup):
    def __init__(self, numGroups: int, avgVA: tuple[float, float], contour) -> None:
        super().__init__(numGroups, avgVA, contour)
        self.groups: list[BaseGroup] = []
        for i in range(self.numGroups - 1):
            self.groups.append(BaseGroup(self.contour[i], (self.valenceMeans[i], self.arousalMeans[i]), self.diffV))
        self.groups.append(EndingGroup(self.contour[i], (self.valenceMeans[i], self.arousalMeans[i]), 0))

    def generateVAMeans(self, avgValence: float, avgArousal: float):
        valenceMeans = rng.normal(avgValence, 0.1, self.numGroups)
        arousalMeans = []
        for i in range(self.numGroups):
            arousalMeans.append(avgArousal - 10 * (i))
        return valenceMeans, arousalMeans

class BaseGroup:
    def __init__(self, dir: Direction, meanVA: tuple[float, float], diffV: float) -> None:
        self.dir = dir
        self.degrees = []
        self.octaves = []
        self.chords = []
        self.availableDegrees = []
        self.valence, self.arousal = meanVA
        self.numUnits, self.numBeats, self.durations = self.generateRythm(meanVA[1], diffV)

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

class EndingGroup(BaseGroup):
    def __init__(self, dir: Direction, meanVA: tuple[float, float], diffV: float) -> None:
        super().__init__(dir, meanVA, diffV)
        