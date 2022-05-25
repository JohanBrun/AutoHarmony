import copy
from dis import dis
from math import dist
import random

from numpy import sign
from groupingModule import BaseGroup, SectionGroup
from localTypes import Direction, Voice, Motion, VoiceGroup, chordDict, primaryChordProgressions, secondaryChordProgressions
from util import degreeOperator, getMidiValueFromScaleDegree, intersection

class HarmonyModule:
    currentMotion = None
    
    def __init__(self, grouping: SectionGroup, voice: Voice, melodyVoice: Voice) -> None:
        self.grouping = grouping
        self.voice = voice
        self.melodyVoice = melodyVoice
        self.currentDegree = -1
        self.currentOctave = voice.startOctave
        self.grouping.groupDescent(self.harmonize)

    def harmonize(self, baseGroup: BaseGroup):
        print(baseGroup.suggestedChords)
        print(baseGroup.numUnits)
        if baseGroup.numBeats / baseGroup.numUnits < 1:
            baseGroup.numUnits = baseGroup.numBeats
            baseGroup.durations = baseGroup.numUnits * [1]
        baseGroup.degrees = [0] * baseGroup.numUnits
        baseGroup.octaves = [0] * baseGroup.numUnits
        isWellMade = False
        motion = random.choice([Motion.SIMILAR, Motion.COUNTER])
        if self.voice.voiceGroup == VoiceGroup.BASS:
            self.rootMotion(baseGroup)
            isWellMade = True
        if self.hasCommodDegree(baseGroup.suggestedChords):
            self.obliqueMotion(baseGroup)
            isWellMade = True
        while isWellMade == False:
            isWellMade = self.findDegrees(baseGroup, motion)
            if isWellMade == False:
                motion = Motion(motion.value * -1)
            
    def findStartingDegree(self, availableDegrees: int):
        degree = random.choice(availableDegrees)
        note = getMidiValueFromScaleDegree(degree, 0)
        octave = 1
        while note + octave * 12 < self.voice.startingRange[0]:
            octave += 1
        return degree, octave
        
    def findNextDegree(self, previousDegree: int, previousOctave: int, availableDegrees: list[int], dir: Direction, motion: Motion):
        degree, octave = previousDegree, previousOctave
        while degree not in availableDegrees:
            if (dir == Direction.STRAIGHT):
                degree, octave = degreeOperator(degree, octave, random.choice([1, -1]))
            else:
                degree, octave = degreeOperator(degree, octave, dir.value * motion.value)
        previousMidiValue = getMidiValueFromScaleDegree(previousDegree, 0) + 12 * previousOctave
        newMidiValue = getMidiValueFromScaleDegree(degree, 0) + 12 * octave
        if abs(previousMidiValue - newMidiValue) > 7 or self.isOutsideRange(newMidiValue):
            return degree, octave, False
        return degree, octave, True
    
    def findDegrees(self, baseGroup: BaseGroup, motion: Motion) -> bool:
        degrees, octaves, suggestedChords, dir = baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords, baseGroup.dir
        for i in range(0, baseGroup.numUnits):
            if self.currentDegree == -1:
                degrees[0], octaves[0] = self.findStartingDegree(suggestedChords[0])
                suggestedChords[i].remove(degrees[0])
            else:
                degrees[i], octaves[i], flag = self.findNextDegree(self.currentDegree, self.currentOctave, suggestedChords[i], dir, motion)
                suggestedChords[i].remove(degrees[i])
            self.currentDegree, self.currentOctave = degrees[i], octaves[i]
        if flag == False:
            self.currentDegree, self.currentOctave = -1, self.voice.startOctave
            for i in range(baseGroup.numUnits):
                suggestedChords[i].append(degrees[i])
        return flag

    def obliqueMotion(self, baseGroup: BaseGroup):
        degrees, octaves, suggestedChords = baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords
        commonDegrees = self.findCommonDegrees(suggestedChords)
        obliqueDegree = self.findClosestDegree(self.currentDegree, commonDegrees)
        obliqueOctave = self.findClosestOctave(obliqueDegree, self.currentDegree, self.currentOctave)
        for i in range(baseGroup.numUnits):
            degrees[i] = obliqueDegree
            octaves[i] = obliqueOctave
            suggestedChords[i].remove(obliqueDegree)
        self.currentDegree, self.currentOctave = obliqueDegree, obliqueOctave
        
    def rootMotion(self, baseGroup: BaseGroup):
        degrees, octaves, suggestedChords = baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords
        for i in range(baseGroup.numUnits):
            if self.currentDegree == -1:
                chord = random.choice(suggestedChords[i])
                availableDegrees = copy.copy(chordDict[chord])
                degrees[i] = availableDegrees[0]
                octaves[i] = self.voice.startOctave
            else:
                if i == 0:
                    chord = random.choice(suggestedChords[i])
                else:
                    inter = intersection(primaryChordProgressions[chord], suggestedChords[i])
                    if inter == []:
                        inter = intersection(secondaryChordProgressions[chord], suggestedChords[i])
                    chord = random.choice(inter)
                availableDegrees = copy.copy(chordDict[chord])
                degrees[i] = availableDegrees[0]
                octaves[i] = self.findClosestOctave(degrees[i], self.currentDegree, self.currentOctave)
            self.currentDegree, self.currentOctave = degrees[i], octaves[i]
            suggestedChords[i] = availableDegrees

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
        previousNote = getMidiValueFromScaleDegree(previousDegree, 0) + 12 * octave
        currentNote = getMidiValueFromScaleDegree(currentDegree, 0) + 12 * octave
        if (currentNote - previousNote > 6 and currentNote - 12 >= self.voice.voiceRange[0]) or currentNote > self.voice.voiceRange[1]:
            octave -= 1
        elif (currentNote - previousNote < -6 and currentNote + 12 <= self.voice.voiceRange[1]) or currentNote < self.voice.voiceRange[0]:
            octave += 1
        return octave

    def updateSuggestedChords(self, degree: int, chords: list[str]):
        newChords = []
        for key in chords:
            if degree in chordDict[key]:
                newChords.append(key)
        return newChords
    
    def isOutsideRange(self, midiValue: int):
        # print(midiValue, self.voice.voiceRange, midiValue < self.voice.voiceRange[0] or midiValue > self.voice.voiceRange[1])
        return midiValue < self.voice.voiceRange[0] or midiValue > self.voice.voiceRange[1]

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
