import copy
import random, math
from groupingModule import BaseGroup, EndingGroup, SectionGroup
from localTypes import Voice, Direction, chordDict, extendedChordDict, primaryChordProgressions, secondaryChordProgressions
from util import degreeOperator, intersection

class MelodyModule():
    def __init__(self, grouping: SectionGroup, voice: Voice) -> None:
        self.grouping = grouping
        self.voice = voice
        self.currentDegree = 1
        self.currentOctave = voice.startOctave
        self.currentChord = 1
        self.hasTension = True
        self.grouping.groupDescent(self.populateBaseGroup)

    def populateBaseGroup(self, baseGroup: BaseGroup):
        moves = self.getMoves(baseGroup.numUnits)
        destination = degreeOperator(self.currentDegree, self.currentOctave, self.getDistance(moves, baseGroup.dir))
        if self.voice.isOutsideRange(*destination):
            baseGroup.dir = Direction(baseGroup.dir.value * -1)
        
        # Adding melody
        for i in range(baseGroup.numUnits):
            degree = self.currentDegree
            octave = self.currentOctave
            baseGroup.degrees.append(degree)
            baseGroup.octaves.append(octave)
            movement = moves[i] * baseGroup.dir.value
            self.currentDegree, self.currentOctave = degreeOperator(degree, octave, movement)
        
        # Adding chords
        availableChords = self.chooseChords(baseGroup.valence, 0)
        indexModifier = max(round(baseGroup.numUnits / baseGroup.numBeats), 1)
        for i in range(min(baseGroup.numBeats, baseGroup.numUnits)):
            melodyDegree = baseGroup.degrees[i * indexModifier]
            nextChord = self.getNextChord(availableChords, melodyDegree)
            baseGroup.availableDegrees.append(self.getAvailableDegrees(nextChord, melodyDegree))
            if melodyDegree not in chordDict[nextChord]:
                self.hasTension = True
            self.currentChord = nextChord

    def populateEndingGroup(self, baseGroup: EndingGroup):
        pass

    def getShortesPath(self, currentDegree: int, currentOctave: int, destinationDegree: int):
        increase = 0
        decrease = 0
        while currentDegree != destinationDegree:
            currentDegree, currentOctave = degreeOperator(currentDegree, currentOctave, 1)
            increase += 1
        while currentDegree != destinationDegree:
            currentDegree, currentOctave = degreeOperator(currentDegree, currentOctave, -1)
            increase -= 1
        if increase < decrease:
            return increase
        else:
            return decrease

    def getMovementGoal(self, arousal: float):
        return random.randint(1, max(math.ceil(arousal + 10 / 2.5), 2))

    def getMoves(self, numUnits: int):
        if random.uniform(0, 1) > 0.5: # Should probably be switched for arousal or arousal diff
            return [1] * (numUnits)
        return [1, random.choice([-2, -3, -4])] + [1] * (numUnits - 2)

    def getEndingMoves(self, numUnits: int):
        goal = self.currentDegree - 1

    def getDistance(self, moves: list[int], direction: Direction):
        distance = 0
        for m in moves:
            distance += m * direction.value
        return distance
    
    def getChordToneChords(self, degree: int):
        chords = []
        for key in chordDict:
            if degree in chordDict[key]: chords.append(key)
        return chords

    def chooseChords(self, valence: float, diff: float):
        chords = [1, 4, 5]
        secondaryTriads = [2, 3, 6]
        if valence > 7.5:
            return chords
        if valence >= 5:
            chords.append(random.choice(secondaryTriads))
            return chords
        if valence < 5:
            chords.append(random.choice(secondaryTriads))
            chords.append(random.choice(secondaryTriads))
            return chords

    def getNextChord(self, availableChords: list[int], melodyDegree: int):
        if self.hasTension:
            availableChords = intersection(self.getChordToneChords(melodyDegree), availableChords)
            self.hasTension = False
        inter = intersection(primaryChordProgressions[self.currentChord], availableChords)
        if inter == []:
            inter = intersection(secondaryChordProgressions[self.currentChord], availableChords)
        return random.choice(inter)

    def getAvailableDegrees(self, chord: int, melodyDegree: int):
        availableDegrees = []
        if melodyDegree in chordDict[chord] and not self.hasTension:
            availableDegrees = copy.copy(extendedChordDict[chord])
            availableDegrees.remove(melodyDegree)
        else:
            availableDegrees = copy.copy(chordDict[chord])
        return availableDegrees
