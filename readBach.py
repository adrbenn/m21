import music21
import os
import json


# for fn in filenameList:
#     s = converter.parse(fn)
#     k = s.analyze('key')
#     i = interval.Interval(k.tonic, pitch.Pitch('C'))
#     sNew = s.transpose(i)

resultfile = 'Bachneural.txt'
majorFile = 'Bachmajor.txt'
minorFile = 'Bachminor.txt'

def readAllBach():
	print('starting to read bach')
	paths = os.listdir('/Users/jonathanadam/Documents/muscomm/finalproject/m21/bachmidi')
	paths = ['/Users/jonathanadam/Documents/muscomm/finalproject/m21/bachmidi/' + x for x in paths]
	annotatedBassChords = []
	annotatedMajorChords = []
	annotatedMinorChords = []
	with open(resultfile,'w') as output:


		for path in paths:
			print('reading '+ path)
			midData = music21.converter.parse(path).flat

			#Normalize to C - note we're not minoring majoring yet
			k = midData.analyze('key')
			if(k.mode == 'minor'):
				i = music21.interval.Interval(k.tonic, music21.pitch.Pitch('A'))
			else:
				i = music21.interval.Interval(k.tonic, music21.pitch.Pitch('C'))
			midData = midData.transpose(i)


			midData = midData.chordify()
			midData = midData.getElementsByClass(music21.chord.Chord)

			allChords = [''.join([chr(p.midi) for p in x.pitches]) for x in midData]

			# simplifiedBass = [chr(x.bass().midi) for x in midData]
			# simplifiedChords = [x.orderedPitchClassesString[1:-1] for x in midData]
			# simplifiedBass = [x.bass().name for x in midData]

			# simplifiedChords = [sorted(set(x.pitchClasses)) for x in midData]
			# simplifiedChords = [','.join([str(y) for y in x]) for x in simplifiedChords]

			# bassAndChords = [j for i in zip(simplifiedBass, simplifiedChords) for j in i]
			bassAndChords = allChords

			finalString = ' '.join(bassAndChords)
			finalString = finalString+ '\n'
			output.write(finalString)
			# print(finalString)
			# annotatedBassChords.append(finalString)
			# if (k.mode == 'minor'):
			# 	annotatedMinorChords.append(finalString)
			# if (k.mode == 'major'):
			# 	annotatedMajorChords.append(finalString)

		# annotatedMinorChords = [x+'\n' for x in annotatedMinorChords]
		# annotatedMajorChords = [x + '\n' for x in annotatedMajorChords]

	# with open(majorFile, 'w') as output:
	# 	output.writelines(annotatedMajorChords)
	# with open(minorFile, 'w') as output:
	# 	output.writelines(annotatedMinorChords)


def main():
	readAllBach()


if __name__ == '__main__':
	main()

