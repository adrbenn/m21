from music21 import *


#---functions---#
def startReading(resFile):
	print('Start reading ' + resFile + ' ...')
	
	s = stream.Stream()
	addedChord = []
	
	with open(resFile) as f:
		lines = f.read().splitlines()
	
	for line in lines:
		a = line.split(' ')
		b = zip(a[0::2], a[1::2])
		
		for pair in b:
			print pair
			addNote = []
			addNote.append(pitch.Pitch(pair[0] + '3'))
			for c in pair[1]:
				if c == 'A':
					d=10
				elif c == 'B':
					d=11
				else:
					d = int(c)
				x = pitch.Pitch(d)
				x.octave = 4
				addNote.append(x)
			chd = chord.Chord(addNote)
			# rem = chd.removeRedundantPitches(inPlace=True)
			print chd
			s.append(chd)
		
		print('Rest added')
		s.append(note.Rest())

	s.show()
	
	
''' Runs readResult() -- parse HMM result into midi  '''
def main():
		
	# i/o settings
	resFile = 'result.txt'
	startReading(resFile)


''' If run as script, execute main '''
if __name__ == '__main__':
    import sys
    main()