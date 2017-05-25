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
	itIsAStep = False
	
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
				print(str(a.offset) + ' [CHORD] solid chord found -> ' + currChordName)
				chordList.append(currChordName)
				if singleExists:
					print('... previous single notes ignored')
				
				# reset
				singleExists = False
				singleNotes = []
				itIsAStep = False
			else:
				if singleExists == False:
					# found a new single note, activate the tracker
					print(str(a.offset) + ' [NOTE] new single note found: ')
					singleExists = True
					singleNotes = a.pitchNames
					for b in a.pitches:
						lastPitch = b
					print singleNotes
					
				else:
					# found consecutive single note, add to tracker ONLY if it's a new note
					# i.e consecutive similar notes would be ignored
					# AND it's not a step from the last entry
					for b in a.pitches:
						print(str(a.offset) + ' [NOTE] consecutive single note found -> ' + b.name)
						itIsAStep = False
						
						if noOfNotes == 1:
							intervalOfNewNote = interval.Interval(lastPitch, b)
							itIsAStep = intervalOfNewNote.isStep
							
						if b not in singleNotes and not itIsAStep:
							print('a new unique note AND not a step')
							singleNotes.append(b.name)
							lastPitch = b
							print singleNotes
						
					if len(singleNotes) >= 3:
						# if the notes in the tracker can be identified as a chord, add that to chordList
						# and reset the tracker
						currChordName = harmony.chordSymbolFigureFromChord(chord.Chord(singleNotes), False)
						print(str(a.offset) + ' [CHORD] found a chord yay -> ' + currChordName)
						chordList.append(currChordName)
						# reset
						singleExists = False
						singleNotes = []
						itIsAStep = False
			
	print('-----')
	print('Result:')
	print chordList
	print('----------')
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