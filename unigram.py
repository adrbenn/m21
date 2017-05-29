import sys
import math

import counts
import golden_section_search

#Stores some precomputed information, such as counts, sum and number of wordtypes
class UnigramData:
	def __init__(self, counts, alpha=1):
		self.unigram_counts = counts
		self.num_word_types = len(self.unigram_counts.keys()) + 1 # for unknown
		self.sum_counts = sum(self.unigram_counts.values())
		self.alpha = alpha

# Collects the unigram data
def make_unigram_data(training_data, alpha=1):
	unigram_data = UnigramData(counts.count_words(training_data), alpha)
	return unigram_data

#Computes the smoothed probability for one particular unigram
def compute_smoothed_unigram_probability(word, unigram_data, alpha=None):
	if (alpha==None):
		alpha = unigram_data.alpha
	probability = (unigram_data.unigram_counts[word] + alpha)/float(unigram_data.sum_counts + alpha*unigram_data.num_word_types)
	return probability

#Input: one string, a UnigramData object and optionally alpha
#Computes the probability of that string based on the data
def compute_line_probability(line, unigram_data, alpha=None):
	if (alpha==None):
		alpha = unigram_data.alpha
	words = line.split()
	log_probability = 0 
	for word in words:
			probability = compute_smoothed_unigram_probability(word, unigram_data, alpha)
			log_probability += math.log(probability)
	return log_probability

# computes a log probability from a corpus based on the given unigram_data
def compute_unigram_corpus_probability(corpus, unigram_data, alpha=None):
		log_probability = 0
		for line in corpus:
			log_probability += compute_line_probability(line, unigram_data, alpha)
		return log_probability

#Likelihood function, to be optimized using gss
def likelihood_alpha(unigram_data, held_out_data):
	held_out_lines = held_out_data.read().splitlines()
	def compute_probability(alpha):
		return compute_unigram_corpus_probability(held_out_lines, unigram_data, alpha)
	return compute_probability
		



def main():

	try:
		training = sys.argv[1]
		held_out = sys.argv[2]
		test_data = sys.argv[3]
		good_bad = sys.argv[4]

		#First test: Just make a model and compute the log probability of english-senate-2
		unigram_data = make_unigram_data(training)
		with open(test_data) as test_file:
			probability = compute_unigram_corpus_probability(test_file, unigram_data)
			print(probability)

		#Second test: optimize alpha, and retest the data 
		optimized_alpha = 1
		with open(test_data) as test_file:
			with open(held_out) as held_out_file:
				alpha_likelihood_function = likelihood_alpha(unigram_data, held_out_file)
				optimized_alpha = golden_section_search.golden_section_search(alpha_likelihood_function)
				probability = compute_unigram_corpus_probability(test_file, unigram_data, optimized_alpha)
				print(probability)

		#Third test: distinguish good from bad sentences
		with open(good_bad) as good_bad_file:
			total = 0
			good = 0
			for line in good_bad_file:
				try:
					line2 = good_bad_file.next()
					prob1 = compute_line_probability(line, unigram_data, optimized_alpha)
					prob2 = compute_line_probability(line2, unigram_data, optimized_alpha)
					total +=1
					if (prob1 > prob2):
						good +=1
				except StopIteration:
					break
			print(good/float(total))

		#Fourth test: declare the optimized alpha
		print (optimized_alpha)
	except:
		print('Please follow the correct format for the inputs.')



if __name__ == '__main__':
	main()








