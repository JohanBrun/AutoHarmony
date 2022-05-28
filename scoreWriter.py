from music21 import *


tenorStream  = stream.Stream(note.Note("G3"))
tenorStream.insert(clef.Treble8vbClef())
bassStream = stream.Stream(note.Note("E3"))
bassStream.insert(clef.BassClef())
s = stream.Stream([tenorStream, bassStream])
s.show()