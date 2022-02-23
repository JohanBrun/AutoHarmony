from typing import List
from music21 import stream, note


class midiGenerator:
    def buildVoiceStream(self, midiValues: List[int]):
        notes = [note.Note(mv) for mv in midiValues]
        return stream.Stream(notes)

    def buildVoicesScore(self, bass, tenor, alto, soprano):
        return stream.Score([soprano, alto, tenor, bass])