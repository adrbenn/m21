from music21 import *


#---functions---#
def startReading(resFile):
	print('Start reading ' + resFile + ' ...')
	
	s = stream.Stream()
	# addedChord = []
	
	with open(resFile) as f:
		lines = f.read().splitlines()
	
	for line in lines:
		chdGroups = line.split(' ')
		# print chdGroups
		
		for chd in chdGroups:
			ntGroup = []
			for nt in chd:
				ntAdded = ord(nt)
				if ntAdded not in ntGroup:
					ntGroup.append(ntAdded)
			print ntGroup
			s.append(chord.Chord(ntGroup))
		
		print('Rest added')
		s.append(note.Rest())
	
	s.show()

	
''' Runs readResult() -- parse HMM result into midi  '''
def main():
		
	# i/o settings
	resFile = 'neural_epoch50.txt'
	startReading(resFile)


''' If run as script, execute main '''
if __name__ == '__main__':
    import sys
    main()