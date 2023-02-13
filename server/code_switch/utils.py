import codecs

def load_words(filename:str) -> list[str]:
	"""
	This function gets a text filename and returns a list of words
	@param filename: the required file to load
	@return: list of words
	"""
	with codecs.open(filename, 'r', 'utf-8') as f:
		txt_str = f.read()
		list_of_words = txt_str.split()
	f.close()
	return list_of_words

def hazard(r: list[int], s: int) -> float:
	"""
	This function calculates the value of the hazard function
	(i.e. the probability of an event of change in the next random selection)
	after a sequence of consecutive of no-change events
	@param r: a list of relative frequency of sub-sequences of consecutive no-change events
	@param s: current sub-sequence of no-change events
	@return: a probability of change in the next trial
	"""
	num, den = 1.0, 1.0
	if s < len(r):
		num = r[s]
		den = sum([r[n] for n in range(len(r)) if n >= s])
	return num / den



if __name__ == '__main__':
	test_hazard()