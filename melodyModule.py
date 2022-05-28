import copy
import random, math
from groupingModule import BaseGroup, SectionGroup
from localTypes import Voice, Direction, chordDict, extendedChordDict, primaryChordProgressions, secondaryChordProgressions
from util import degreeOperator, intersection

class MelodyModule():
    def __init__(self, grouping: SectionGroup, voice: Voice) -> None:
        self.grouping = grouping
        self.voice = voice
        self.currentDegree = random.choice([1, 3, 5])
        self.currentOctave = voice.startOctave
        self.grouping.groupDescent(self.populateBaseGroup)

    def populateBaseGroup(self, baseGroup: BaseGroup):
        octave = self.voice.startOctave
        moves = self.getMoves(baseGroup.numUnits)
        availableChords = []
        destination = degreeOperator(self.currentDegree, self.currentOctave, self.getDistance(moves, baseGroup.dir))
        if self.voice.isOutsideRange(*destination):
            baseGroup.dir = Direction(baseGroup.dir.value * -1)
        for i in range(baseGroup.numUnits):
            # Add current degree
            degree = self.currentDegree
            octave = self.currentOctave
            baseGroup.degrees.append(degree)
            baseGroup.octaves.append(octave)
            if (baseGroup.numUnits / baseGroup.numBeats) <= 1.5 or i % 2 == 0:
                availableChords.append(self.chooseChords(baseGroup.valence, 0))

            # Move to next degree
            movement = moves[i] * baseGroup.dir.value
            self.currentDegree, self.currentOctave = degreeOperator(degree, octave, movement)
        baseGroup.chords = self.getProgression(availableChords)
        baseGroup.availableDegrees = self.getAvailableDegrees(baseGroup.chords, baseGroup.degrees)

    def getMovementGoal(self, arousal: float):
        return random.randint(1, max(math.ceil(arousal + 10 / 2.5), 2))

    def getMoves(self, numUnits: int):
        if random.uniform(0, 1) > 0.5: # Should probably be switched for arousal or arousal diff
            return [1] * (numUnits)
        return [1, random.choice([-2, -3, -4])] + [1] * (numUnits - 2)

    def getDistance(self, moves: list[int], direction: Direction):
        distance = 0
        for m in moves:
            distance += m * direction.value
        return distance
    
    def getSuggestedChords(self, degree: int, valence: float, diff: float):
        chords = []
        for key in chordDict:
            if degree in chordDict[key]: chords.append(key)
        return chords

    def chooseChords(self, valence: float, diff: float):
        chords = [1]
        primaryTriads = [4, 5]
        intermediateTriads = [6]
        secondaryTriads = [2, 3]
        chords.append(primaryTriads.pop(random.randint(0, 1)))
        intermediateTriads += primaryTriads
        if valence > 7.5:
            chords.append(primaryTriads[0])
        elif valence > 5:
            chords += intermediateTriads
        elif valence <= 5:
            chords.append(random.choice(intermediateTriads))
            chords.append(random.choice(secondaryTriads))
        return chords 

    def getSuggestedChords2(self):
        return [1, 2, 3, 4, 5, 6]

    def getProgression(self, availableChords: list[list[int]]):
        startingChords = intersection([1, 4, 5, 6], availableChords[0])
        progression = [random.choice(startingChords)]
        for i in range(1, len(availableChords)):
            inter = intersection(primaryChordProgressions[progression[-1]], availableChords[i])
            if inter == []:
                inter = intersection(secondaryChordProgressions[progression[-1]], availableChords[i])
            progression.append(random.choice(inter))
        return progression
        
    def getAvailableDegrees(self, progression: list[int], melodyDegrees: list[int]):
        availableDegrees = []
        for chord, md in zip(progression, melodyDegrees):
            if md in chordDict[chord]:
                availableDegrees.append(copy.copy(extendedChordDict[chord]))
            else:
                availableDegrees.append(copy.copy(chordDict[chord]))
        return availableDegrees
