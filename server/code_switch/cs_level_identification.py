import langid
import json
import codecs

LANGUAGES = ['en', 'es']
langid.set_languages(langs=LANGUAGES)

MAJOR_LANGUAGE_CODES = {'en': 'E', 'es': 'S'}

def get_other_lang(lang):
	major_lang_index = LANGUAGES.index(lang)
	return LANGUAGES[major_lang_index-1]


UNCOMMON_WORDS = json.load(open('translation_pairs.json'))

def load_words(filename):
	with codecs.open(filename, 'r', 'utf-8') as f:
		txt_str = f.read()
		list_of_words = txt_str.split()

	f.close()
	return list_of_words

def test_load_words():
	filename = 'most_common_1000_en_words.txt'
	load_words(filename)

COMMON_WORDS = {'en': load_words('most_common_en_words_without_shared.txt'),
                  'es': load_words('most_common_es_words_without_shared.txt')}

def test_classify():
		str = '¿Cómo se llega a la capital?'
		c = langid.classify(str)
		print(c)

def get_other_lang(lang):
	major_lang_index = LANGUAGES.index(lang)
	return LANGUAGES[major_lang_index-1]

def test_get_other_lang():
	lang = 'en'
	other_lang = get_other_lang(lang)
	print(lang + ": " + other_lang)
	lang = 'es'
	other_lang = get_other_lang(lang)
	print(lang + ": " + other_lang)

def check_phrasal_cs_presence(sentence, minor_lang):
	tokens = sentence.split()
	if len(tokens)<=2:
		return False
	else:
		for n in range(len(tokens)-2):
			triplet = ' '.join(tokens[n:n+3])
			if langid.classify(triplet)[0] == minor_lang:
				return True
	return False

def check_lexical_cs_presence(sentence, minor_lang):
	tokens = sentence.split()
	for token in tokens:
		if token in UNCOMMON_WORDS[minor_lang]:
			return True
	return False

def check_frozen_expression_cs_presence(sentence, minor_lang):
	tokens = sentence.split()
	for token in tokens:
		if token in COMMON_WORDS[minor_lang]:
			return True
	return False

def test_check_phrasal_cs_presence():
	sentence='quiero saltar y cantar de joy'
	minor_lang='eng'
	res = check_phrasal_cs_presence(sentence, minor_lang)


def clean_sentence(sentence):
	chars_to_remove = '?!,.:"\''
	for char in chars_to_remove:
		sentence = sentence.replace(char, '')
	return sentence.strip()

def calc_cs_level(sentence):
	major_lang = langid.classify(sentence)[0]
	major_lang_code = MAJOR_LANGUAGE_CODES[major_lang]
	minor_lang = get_other_lang(major_lang)
	clean_version_of_sentence = clean_sentence(sentence)
	if check_phrasal_cs_presence(clean_version_of_sentence, minor_lang):
		minor_lang_code = 'P'
	elif check_lexical_cs_presence(clean_version_of_sentence, minor_lang):
		minor_lang_code = 'L'
	elif check_frozen_expression_cs_presence(clean_version_of_sentence, minor_lang):
		minor_lang_code = 'T'
	else:
		minor_lang_code = 'N'

	return major_lang_code+minor_lang_code

def test_calc_level():
	sentence = '¿Cómo se llega a la capital?'
	cs_level = calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")
	sentence = 'how do i get to the jirafa?'
	cs_level = calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")
	sentence = 'how do i get to the end of the map?!'
	cs_level = calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")
def run_tests():
	test_classify()
	test_calc_level()
	test_get_other_lang()
	test_check_phrasal_cs_presence()
	test_load_words()

if __name__ == '__main__':
	run_tests()
	print("Finished!")