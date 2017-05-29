import music21
import os
import json

resultfile = 'Bachsimple.txt'

def readAllBach():
	print('starting to read bach')
	paths = music21.corpus.getComposer('bach')
	for path in paths:
		print('reading '+ path)
		midData = music21.converter.parse(path).flat
		midData = midData.chordify()
		midData = music21.getElementsByClass(music21.chord.Chord)
		


