import music21


sign = lambda a: (a>0) - (a<0)

def moveFrom(prevchord, pitchclassset, prevbass, laterbass):
	newpitches = []
	newpitchClasses = []
	bassMovement = laterbass.pitch.midi - prevbass.pitch.midi #assumes music21 representation
	# if bassmovement is positive, then bass is moving up, we should favor downwards movements
	#else we favor upwards movements
	prevpitchclassset = prevchord.orderedPitchClasses
	possibleMoves = {x:sorted([sign(min(x, y) - max(-x%12, -y%12))*min((((x-y)%12), ((y-x)%12)), key=abs) for y in pitchclassset], key=abs) for x in prevpitchclassset}
	# print('possiblemoves')
	# print(possibleMoves)
	#this will give a list of priorities for each thing to do based on distance
	for pitch in prevchord.pitches:
		# print('looking at pitch', pitch.pitchClass)
		moves = possibleMoves[pitch.pitchClass]
		if (bassMovement > 0):
			moves = [x for x in moves if x <= 0] + [x for x in moves if x > 0]
		elif (bassMovement < 0):
			moves = [x for x in moves if x >= 0]  + [x for x in moves if x <0]
		# print('moves are ', moves)
		if moves[0] is 0:
			# print('the note', pitch, 'stays the same')
			newpitches.append((pitch, 0))
			newpitchClasses.append(pitch.pitchClass)
		else:
			index = 0
			isNotFound = True
			while isNotFound:
				# if ((bassMovement > 0) and moves[index] > 0):
				# 	print('parallel motion')					
				# 	if (index >= len(moves) -1):
				# 			newPitch = pitch.transpose(moves[index], inPlace=False)
				# 			newpitches.append((newPitch, moves[index]))
				# 			newpitchClasses.append(newPitch.pitchClass)
				# 			isNotFound= False
				# 	else:
				# 		index = index + 1
				# elif ((bassMovement < 0) and moves[index] < 0):
				# 	print('parallel motion')
				# 	if (index >= len(moves) -1):
				# 			newPitch = pitch.transpose(moves[index], inPlace=False)
				# 			newpitches.append((newPitch, moves[index]))
				# 			newpitchClasses.append(newPitch.pitchClass)
				# 			isNotFound= False
				# 	else:
				# 		index = index + 1
				# else:
					possibleMove = moves[index]
					# print('possible move is', possibleMove)
					newPitch = pitch.transpose(possibleMove, inPlace=False)
					if len(newpitches) < len(pitchclassset):
						# print('were still adding new pitches')
						# print(newPitch.pitchClass not in newpitchClasses)
						# print('already gotten')
						# print(newpitchClasses)
						if (newPitch.pitchClass not in newpitchClasses) or (index >= len(moves)-1):
							print('we dont have this pitch yet')
							newpitches.append((newPitch, moves[index]))
							newpitchClasses.append(newPitch.pitchClass)
							isNotFound= False
						else:
							index = index+1
					else:
						newpitches.append((newPitch, moves[index]))
						newpitchClasses.append(newPitch.pitchClass)
						isNotFound = False
	omitted = [x for x in pitchclassset if x not in newpitchClasses]
	if omitted:
		for x in omitted:
			newPitch = music21.pitch.Pitch(x)
			newpitches.append((newpitches, "random"))
	newchord = music21.chord.Chord([a for (a,b) in newpitches])
	return newchord

cChord = music21.chord.Chord(['E4', 'G4', 'C4'])
gmajor = [2, 7, 11]
aminor = [0, 4, 9]
cnote = music21.note.Note('C3')
gnote = music21.note.Note('G3')
anote = music21.note.Note('A2')

newVoicing = moveFrom(cChord, gmajor, cnote, gnote)
print(newVoicing)
otherVoicing = moveFrom(cChord, aminor, cnote, anote)
print(otherVoicing)




