from collections import Counter

def count_words(input_filename):
	counts = Counter()
	with open(input_filename, 'r') as input_file:
		for line in input_file:
			counts.update(line.split())
	return counts