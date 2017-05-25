from music21 import *
import os
import json

resFile = 'result.txt'

#---functions---#
def doSomethingTo(midFile):
	print('Reading ' + midFile + ' ...')
	midData = converter.parse(midFile).flat
	midChordify = midData.chordify()
	midChordify.show('text');

	chordList = []
	singleExists = False
	singleNotes = []
	
	print('-----')
	
	for a in midChordify:
		if isinstance(a, chord.Chord):
		
			noOfNotes = len(a.pitchNames)
			currChordName = harmony.chordSymbolFigureFromChord(a, False)
			
			# print(currChordName)
			# print(a.pitchNames)
			# print(noOfNotes)
		
			if noOfNotes >= 3:
				# add the chord name, and reset the singles tracking
				print(str(a.offset) + ' solid chord found -> ' + currChordName)
				chordList.append(currChordName)
				singleExists = False
				singleNotes = []
			else:
				if singleExists == False:
					# found a new single note, activate the tracker
					print(str(a.offset) + ' new single note found')
					singleExists = True
					singleNotes = a.pitchNames
				else:
					# found consecutive single note, add to tracker ONLY if it's a new note
					# i.e consecutive similar notes would be ignored
					for b in a.pitchNames:
						print(str(a.offset) + ' consecutive single note found -> ' + b)
						if b not in singleNotes:
							singleNotes.append(b)
						
					if len(singleNotes) >= 3:
						# if the notes in the tracker can be identified as a chord, add that to chordList
						# and reset the tracker
						currChordName = harmony.chordSymbolFigureFromChord(chord.Chord(singleNotes), False)
						print(str(a.offset) + ' found a chord yay -> ' + currChordName)
						chordList.append(currChordName)
						singleExists = False
						singleNotes = []
			
	print('-----')
	print('Result:')
	print chordList
	with open(resFile, 'a') as savefile:
		json.dump(chordList, savefile)
	
	
''' Runs m21() -- open midi file and spits sumthin' '''
def main():
	print('It s alive!')
	
	# path to midi files
	path = 'midi/'
	for filename in os.listdir(path):
		midFile = path + filename
		doSomethingTo(midFile)


''' If run as script, execute main '''
if __name__ == '__main__':
    import sys
    main()