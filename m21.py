from music21 import *
import os
import json

resFile = 'result.txt'

#---functions---#
def doSomethingTo(midFile):
	print('Doing something...')
	midData = converter.parse(midFile).flat
	midChordify = midData.chordify()
	# midChordify.show();

	chordList = []
	singleExists = False
	brokenChord = []
	brokenChordPos = 1
	
	for a in midChordify:
		if isinstance(a, chord.Chord):
			
			x = a.root().nameWithOctave
			y = harmony.chordSymbolFigureFromChord(a, True)[0]
			z = a.offset%4.0 + 1
			
			# if it's a single note (y = pedal),
			# - check if there's a previous single note. if any, try to combine them and insert into chordlist
			# - otherwise save it for the next iteration
			if y == 'pedal':
				if singleExists == True:
					brokenChord.append(x)
					x = chord.Chord(brokenChord).root().nameWithOctave
					y = harmony.chordSymbolFigureFromChord(chord.Chord(brokenChord), True)[0]
					
					# chordList.append([x, y, brokenChordPos])
					chordList.append(y)
					
					# reset
					singleExists = False
					brokenChord = []
					
				else:
					singleExists = True
					brokenChord.append(y)
					brokenChordPos = z

			
			else:			
				# chordList.append([x, y, z])
				chordList.append(y)
				
				# reset. just in case
				singleExists = False
				brokenChord = []
			
	print chordList
	with open(resFile, 'a') as savefile:
		json.dump(chordList, savefile)
	
	
''' Runs m21() -- open midi file and spits sumthin' '''
def main():
	print('It s alive!')
	
	# path to midi files
	path = 'midi/'
	for filename in os.listdir(path):
		print filename
		midFile = path + filename
		doSomethingTo(midFile)


''' If run as script, execute main '''
if __name__ == '__main__':
    import sys
    main()