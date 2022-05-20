import copy
import random

from numpy import sign
from groupingModule import BaseGroup, SectionGroup
from localTypes import Direction, Voice, Motion, VoiceGroup, chordDict, primaryChordProgressions, secondaryChordProgressions
from util import degreeOperator, getNoteFromScaleDegree, intersection

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
        isWellMade = False
        motion = random.choice([Motion.SIMILAR, Motion.COUNTER])
        if self.voice.voiceGroup == VoiceGroup.BASS:
            self.rootMotion(baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords)
            isWellMade = True
        while isWellMade == False:
            isWellMade = self.findDegrees(baseGroup.degrees, baseGroup.octaves, baseGroup.suggestedChords, baseGroup.dir, motion)
            if isWellMade == False:
                motion = Motion(motion.value * -1)
            
    def findStartingDegree(self, availableDegrees: int):
        degree = random.choice(availableDegrees)
        note = getNoteFromScaleDegree(degree, 0)
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
        previousMidiValue = getNoteFromScaleDegree(previousDegree, 0) + 12 * previousOctave
        newMidiValue = getNoteFromScaleDegree(degree, 0) + 12 * octave
        if abs(previousMidiValue - newMidiValue) > 7 or self.isOutsideRange(newMidiValue):
            return degree, octave, False
        return degree, octave, True
    
    def findDegrees(self, degrees: list[int], octaves: list[int], suggestedChords: list[list[int]], dir: Direction, motion: Motion) -> bool:
        for i in range(0, len(degrees)):
            if self.currentDegree == -1:
                degrees[0], octaves[0] = self.findStartingDegree(suggestedChords[0])
                suggestedChords[i].remove(degrees[0])
            else:
                degrees[i], octaves[i], flag = self.findNextDegree(self.currentDegree, self.currentOctave, suggestedChords[i], dir, motion)
                suggestedChords[i].remove(degrees[i])
            self.currentDegree, self.currentOctave = degrees[i], octaves[i]
        if flag == False:
            self.currentDegree, self.currentOctave = -1, self.voice.startOctave
            for i in range(len(suggestedChords)):
                suggestedChords[i].append(degrees[i])
        return flag

    def obliqueMotionOld(self, degrees, octaves, suggestedChords):
        if self.currentMotion == Motion.OBLIQUE:
            firstNote = self.currentDegree
            firstOctave = self.currentOctave
        else:
            self.currentMotion = Motion.OBLIQUE
            firstNote = degrees[0]
            firstOctave = octaves[0]
        for i in range(len(degrees)):
            degrees[i], octaves[i] = firstNote, firstOctave
            updatedChords = self.updateSuggestedChords(degrees[i], suggestedChords[i])
            while updatedChords == []:
                degrees[i], octaves[i] = degreeOperator(degrees[i], octaves[i], -1)
                updatedChords = self.updateSuggestedChords(degrees[i], suggestedChords[i])
            suggestedChords[i] = updatedChords
        self.currentDegree = degrees[-1]
        self.currentOctave = octaves[-1]

    def obliqueMotion(self, degrees, octaves, suggestedChords):
        if self.currentMotion == Motion.OBLIQUE:
            firstNote = self.currentDegree
            firstOctave = self.currentOctave
        else:
            self.currentMotion = Motion.OBLIQUE
            firstNote, firstOctave = self.findStartingDegree(suggestedChords[0])
        for i in range(len(degrees)):
            degrees[i], octaves[i] = firstNote, firstOctave
        self.currentDegree = degrees[-1]
        self.currentOctave = octaves[-1]

    def rootMotion(self, degrees, octaves, suggestedChords):
        for i in range(len(degrees)):
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

    def findClosestOctave(self, currentDegree, previousDegree, octave):
        previousNote = getNoteFromScaleDegree(previousDegree, 0) + 12 * octave
        currentNote = getNoteFromScaleDegree(currentDegree, 0) + 12 * octave
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