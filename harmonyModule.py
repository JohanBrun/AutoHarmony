import copy
import random

from numpy import sign
from groupingModule import BaseGroup, SectionGroup
from localTypes import Direction, Voice, Motion, VoiceGroup
from util import degreeOperator, getMidiValueFromScaleDegree, intersection

class HarmonyModule:
    def __init__(self, grouping: SectionGroup, voice: Voice, melodyVoice: Voice) -> None:
        self.grouping = grouping
        self.voice = voice
        self.melodyVoice = melodyVoice
        self.currentDegree = -1
        self.currentOctave = voice.startOctave
        self.grouping.groupDescent(self.harmonize)

    def harmonize(self, baseGroup: BaseGroup):
        if baseGroup.numBeats / baseGroup.numUnits < 1:
            baseGroup.numUnits = baseGroup.numBeats
            baseGroup.durations = baseGroup.numUnits * [1]
        baseGroup.degrees = [0] * baseGroup.numUnits
        baseGroup.octaves = [0] * baseGroup.numUnits
        motion = random.choice([Motion.SIMILAR, Motion.COUNTER])
        if self.voice.voiceGroup == VoiceGroup.BASS:
            self.rootMotion(baseGroup)
        else:
            self.findDegrees(baseGroup, motion)
            
    def findStartingDegree(self, availableDegrees: int):
        degree = random.choice(availableDegrees)
        note = getMidiValueFromScaleDegree(degree, 0)
        octave = 1
        while note + octave * 12 < self.voice.startingRange[0]:
            octave += 1
        return degree, octave
        
    def findNextDegree(self, previousDegree: int, previousOctave: int, availableDegrees: list[int], dir: Direction, motion: Motion):
        nextDegree, nextOctave = previousDegree, previousOctave
        while nextDegree not in availableDegrees:
            nextDegree, nextOctave = degreeOperator(nextDegree, nextOctave, dir.value * motion.value)
        isLeapTooLarge = self.isLeapTooLarge(previousDegree, previousOctave, nextDegree, nextOctave)
        isOutsideRange = self.voice.isOutsideRange(nextDegree, nextOctave)

        return nextDegree, nextOctave, isLeapTooLarge, isOutsideRange
    
    def findDegrees(self, baseGroup: BaseGroup, motion: Motion) -> bool:
        degrees, octaves, availableDegrees, dir = baseGroup.degrees, baseGroup.octaves, baseGroup.availableDegrees, baseGroup.dir
        i = 0
        while i < baseGroup.numUnits:
            if self.currentDegree == -1:
                degrees[i], octaves[i] = self.findStartingDegree(availableDegrees[i])
                availableDegrees[i].remove(degrees[i])
                self.currentDegree, self.currentOctave = degrees[i], octaves[i]
                i += 1
                continue
            nextDegree, nextOctave, leapTooLarge, outideRange = self.findNextDegree(self.currentDegree, self.currentOctave, availableDegrees[i], dir, motion)
            if outideRange:
                motion = Motion(motion.value * -1)
                continue
            if leapTooLarge:
                oppositeMotion = Motion(motion.value * -1)
                alternateDegree, alternateOctave, leapTooLarge, outideRange = self.findNextDegree(self.currentDegree, self.currentOctave, availableDegrees[i], dir, oppositeMotion)
                if not outideRange:
                    nextDegree, nextOctave = alternateDegree, alternateOctave
            degrees[i], octaves[i] = nextDegree, nextOctave
            availableDegrees[i].remove(degrees[i])
            if len(availableDegrees[i]) > 3:
                availableDegrees[i] = self.reduceAvailableDegrees(availableDegrees[i], degrees[i])
            self.currentDegree, self.currentOctave = degrees[i], octaves[i]
            i += 1
        
    def rootMotion(self, baseGroup: BaseGroup):
        degrees, octaves, availableDegrees = baseGroup.degrees, baseGroup.octaves, baseGroup.availableDegrees
        for i in range(baseGroup.numUnits):
            if self.currentDegree == -1:
                degrees[i] = availableDegrees[i][0]
                octaves[i] = self.voice.startOctave
            else:
                degrees[i] = availableDegrees[i][0]
                octaves[i] = self.findClosestOctave(degrees[i], self.currentDegree, self.currentOctave)
            availableDegrees[i].remove(degrees[i])
            if len(availableDegrees[i]) > 3:
                availableDegrees[i] = self.reduceAvailableDegrees(availableDegrees[i], degrees[i])
            self.currentDegree, self.currentOctave = degrees[i], octaves[i]

    def findClosestDegree(self, currentDegree: int, degrees: list[int]):
        closestDegree = 0
        maxDistance = 8
        for degree in degrees:
            distance = degree - currentDegree
            if distance > 3:
                distance = degree - 8
            elif distance < -3:
                distance = 8 - currentDegree
            distance = abs(distance)
            if distance < maxDistance:
                closestDegree = degree
        return closestDegree

    def findClosestOctave(self, currentDegree: int, previousDegree: int, octave: int):
        previousNote = getMidiValueFromScaleDegree(previousDegree) + 12 * octave
        currentNote = getMidiValueFromScaleDegree(currentDegree) + 12 * octave
        if (currentNote - previousNote > 6 and currentNote - 12 >= self.voice.voiceRange[0]) or currentNote > self.voice.voiceRange[1]:
            octave -= 1
        elif (currentNote - previousNote < -6 and currentNote + 12 <= self.voice.voiceRange[1]) or currentNote < self.voice.voiceRange[0]:
            octave += 1
        return octave

    def hasCommodDegree(self, chordDegrees: list[list[int]]):
        degrees = chordDegrees[0]
        for i in range(1, len(chordDegrees)):
            degrees = intersection(chordDegrees[i], degrees)
            if degrees == []:
                return False
        return True

    def findCommonDegrees(self, chordDegrees: list[list[int]]):
        degrees = chordDegrees[0]
        for i in range(1, len(chordDegrees)):
            degrees = intersection(degrees, chordDegrees[i])
        return degrees

    def reduceAvailableDegrees(self, availableDegrees: list[int], removedDegree):
        if removedDegree not in availableDegrees:
            remainingDegrees = set(availableDegrees)
            for d in remainingDegrees:
                availableDegrees.remove(d)
        return availableDegrees

    def isLeapTooLarge(self, degree, octave, nextDegree, nextOctave):
        midiValue = getMidiValueFromScaleDegree(degree) + 12 * octave
        nextMidiValue = getMidiValueFromScaleDegree(nextDegree) + 12 * nextOctave
        return abs(midiValue - nextMidiValue) > 7
            