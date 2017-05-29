import music21
import itertools
import math
import sys
from collections import *

sigma_estimates = {}
tau_estimates = {}
pos_per_word = {}
sigma_totals = {}

class Viterbi_State:
	def __init__(self, y, mu, prev):
		self.y = y
		self.mu = mu
		self.prev = prev


def count_words(input_filename):
	tau_counts = Counter()
	sigma_counts = Counter()
	tau_totals = Counter()
	sigma_totals = Counter()
	word_counts = Counter()
	consecutive_sigma = defaultdict(list)
	pos_per_word = defaultdict(list)
	with open(input_filename, 'r') as input_file:
		for line in input_file:
			words = line.split()[0::2]
			tags = line.split()[1::2]
			tag_endings = ['*START*'] + tags + ['*STOP*']
			tag_bigrams = zip(tag_endings, tag_endings[1:])
			tau_counts.update(zip(tags, words))
			word_counts.update(words)
			tau_totals.update(tag_endings)
			sigma_counts.update(tag_bigrams)
			sigma_totals.update(tag_endings)
			for (tag, word) in zip(tags, words):
				if tag not in pos_per_word[word]:
					pos_per_word[word].append(tag)


	return (sigma_counts, sigma_totals,tau_counts, tau_totals, pos_per_word)

def find_max(sigma, word, viterbi):
	best_mu = float("-inf")
	best_prev = None
	for states in viterbi[-1]:
		mu = states.mu + math.log(sigma_estimates.get((states.y, sigma), 0.000000000000000000000001)) + math.log(tau_estimates.get((sigma, word), tau_estimates.get((sigma, '*UNK*'))))
		if mu > best_mu:
			best_mu = mu
			best_prev = states
	return Viterbi_State(sigma, best_mu, best_prev)



def calculate_viterbi_sequence(line):
	viterbi = [[Viterbi_State('*START*', 0, None)]]
	for word in line:
		viterbi_results = []
		if (word != '*STOP*'):
			sigma_collection = pos_per_word.get(word, sigma_totals)
			for sigma in sigma_collection:
				viterbi_element = find_max(sigma, word, viterbi)
				if viterbi_element.mu > float('-inf'):
					viterbi_results.append(viterbi_element)
				else: 
					print('oooh dear')
		else:
			viterbi_element = find_max('*STOP*', word, viterbi)
			viterbi_results = [viterbi_element]
		viterbi.append(viterbi_results)

	mus = [[x.mu for x in sublist] for sublist in viterbi]
	final_sequence = [viterbi[-1][0]]
	prev = final_sequence[-1].prev
	while prev is not None:
		final_sequence.append(prev)
		prev = final_sequence[-1].prev
	final_sequence.reverse()
	final_sequence = final_sequence[1:]
	labels = [x.y for x in final_sequence]
	return labels


def create_labelled_string(line):
	print('line is')
	print(line)
	labels = calculate_viterbi_sequence(line)
	iters = [iter (line[:-1]), iter(labels[:-1])]
	final_list = list(it.next() for it in itertools.cycle(iters))
	return " ".join(final_list)

def tag_tagged_file(input_file, output_file):
	for line in input_file:
		words = line.split()
		words = [x[0] for x in words]
		# words = [chr(music21.note.Note(x).pitch.midi) for x in words]
		words.append('*STOP*')
		labelled_string = create_labelled_string(words)
		output_file.write(labelled_string + '\n')



def main():
	global tau_estimates
	global sigma_estimates
	global pos_per_word
	global sigma_totals
	training = sys.argv[1]
	test = sys.argv[2]
	output = sys.argv[3]
	print('output is ', output)
	(sigma_counts, all_sigmas, tau_counts,tau_totals, word_pos) = count_words(training)
	pos_per_word = word_pos
	sigma_totals = all_sigmas


	for (y, y_dash) in sigma_counts:
		sigma_estimates[(y, y_dash)] = sigma_counts[(y, y_dash)]/float(sigma_totals[y])

	for (y, x) in tau_counts:
		tau_estimates[(y, x)] = tau_counts[(y, x)]/float(tau_totals[y])

	tau_estimates[('*STOP*', '*STOP*')] = 1
	tau_estimates[('*START*', '*START*')] = 1

	for y in tau_totals:
		tau_estimates[(y, '*UNK*')] = 1/float(tau_totals[y])

	with open(test) as f1:
		with open(output, 'w') as f2:
			tag_tagged_file(f1, f2)


if __name__ == '__main__':
	main()

