import sys
import math
from collections import Counter
import unigram

import counts
import golden_section_search

#Stores some precomputed information, such as counts, sum and number of wordtypes
class BigramData:
	def __init__(self, unigram_counts, bigram_counts, alpha=1, beta=1):
		self.unigram_counts = unigram_counts
		self.num_word_types = len(self.unigram_counts.keys()) + 1 # for unknown
		self.sum_counts = sum(self.unigram_counts.values())
		self.bigram_counts = bigram_counts
		self.alpha = alpha
		self.beta = beta

#Same as unigram: create an object that holds the bigram data
def make_bigram_data(training_data, alpha=1, beta = 1):
	unigram_data = unigram.make_unigram_data(training_data, alpha)
	counts = Counter()
	with open(training_data, 'r') as input_file:
		for line in input_file:
			bigrams = extract_bigrams(line)
			counts.update(bigrams)
			unigram_data.unigram_counts['<S>'] +=2 #start and stop of each line
	bigram_data = BigramData(unigram_data.unigram_counts, counts, unigram_data.alpha, beta)
	return bigram_data

#Based on the parameters, finds the bigram probability
def compute_smoothed_bigram_probability(bigram, bigram_data, beta=None):
	if (beta==None):
		beta = bigram_data.beta
	smoothed_unigram = unigram.compute_smoothed_unigram_probability(bigram[1], bigram_data)
	n_wo = bigram_data.unigram_counts[bigram[0]] # Number of bigrams == number of word count, except for stop symbol
	if bigram[0] == '<S>': 
		n_wo = n_wo/float(2)
	probability = (bigram_data.bigram_counts[bigram] + beta * smoothed_unigram)/ float(n_wo + beta)
	assert probability > 0
	return probability

#Input: one string, a UnigramData object and optionally alpha
#Computes the probability of that string based on the data
def compute_line_probability(line, bigram_data, beta=None):
	if (beta==None):
		beta = bigram_data.alpha
	bigrams = extract_bigrams(line)
	log_probability = 0 
	for bigram in bigrams:
			probability = compute_smoothed_bigram_probability(bigram, bigram_data, beta)
			log_probability += math.log(probability)
	return log_probability

# Input: a file, 
def compute_bigram_corpus_probability(corpus, bigram_data, beta=None):
		corpus.seek(0)
		log_probability = 0
		for line in corpus:
			log_probability += compute_line_probability(line, bigram_data, beta)
		return log_probability

def likelihood_beta(bigram_data, held_out_data):
	def compute_probability(beta):
		return compute_bigram_corpus_probability(held_out_data, bigram_data, beta)
	return compute_probability

def extract_bigrams(line):
	words = line.split()
	words = ['<START>'] + words + ['<END>']
	bigrams = zip(words, words[1:])
	return bigrams	

def main():

	training = sys.argv[1]

	unigram_data = unigram.make_unigram_data(training)
	bigram_data = make_bigram_data(training)
	
	# try:
	# 	training = sys.argv[1]
	# 	held_out = sys.argv[2]
	# 	test_data = sys.argv[3]
	# 	good_bad = sys.argv[4]

	# 	#Make unigram and bigram - unigram just to optimize alpha again
	# 	unigram_data = unigram.make_unigram_data(training)
	# 	bigram_data = make_bigram_data(training)

	# 	#Test one: Just compute bigrams and see how far we get
	# 	with open(test_data) as test_file:
	# 		probability = compute_bigram_corpus_probability(test_file, bigram_data)
	# 		print(probability)

	# 	optimized_beta = 1
	# 	optimized_alpha = 1


	# 	# Test two: optimize alpha with unigram, optimize beta with bigrams, and try again
	# 	with open(test_data) as test_file:
	# 		with open(held_out) as held_out_file:
	# 			alpha_likelihood_function = unigram.likelihood_alpha(unigram_data, held_out_file)
	# 			optimized_alpha = golden_section_search.golden_section_search(alpha_likelihood_function)
	# 			bigram_data.alpha = optimized_alpha
	# 		with open(held_out) as held_out_file:
	# 			beta_likelihood_function = likelihood_beta(bigram_data, held_out_file)
	# 			optimized_beta = golden_section_search.golden_section_search(beta_likelihood_function)
	# 			probability = compute_bigram_corpus_probability(test_file, bigram_data, optimized_beta)
	# 			print(probability)


	# 	# Test three: try to see what the proportion of good and bad are
	# 	with open(good_bad) as good_bad_file:
	# 		total = 0
	# 		good = 0
	# 		for line in good_bad_file:
	# 			try:
	# 				line2 = good_bad_file.next()
	# 				prob1 = compute_line_probability(line, bigram_data, optimized_beta)
	# 				prob2 = compute_line_probability(line2, bigram_data, optimized_beta)
	# 				total +=1
	# 				if (prob1 > prob2):
	# 					good +=1
	# 			except StopIteration:
	# 				break
			
	# 		print(good/float(total))

	# 	#Test four and five: declare optimized alpha and beta
	# 	print(optimized_alpha)
	# 	print(optimized_beta)
	# except:
	# 	print('please use the right format for the inputs')





if __name__ == '__main__':
	main()








