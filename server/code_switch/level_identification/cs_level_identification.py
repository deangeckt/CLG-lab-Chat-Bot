import json
import codecs

LANGUAGES = ['en', 'es']
MAJOR_LANGUAGE_CODES = {'en': 'E', 'es': 'S'}
UNCOMMON_WORDS = json.load(open('resources/translation_pairs.json'))


def get_other_lang(lang:str) -> str:
	major_lang_index = LANGUAGES.index(lang)
	return LANGUAGES[major_lang_index-1]

def load_words(filename:str) -> list[str]:
	with codecs.open(filename, 'r', 'utf-8') as f:
		txt_str = f.read()
		list_of_words = txt_str.split()
	f.close()
	return list_of_words


COMMON_WORDS = {'en': load_words('resources/most_common_en_words_without_shared.txt'),
                  'es': load_words('resources/most_common_es_words_without_shared.txt')}

def get_other_lang(lang:str) -> str:
	major_lang_index = LANGUAGES.index(lang)
	return LANGUAGES[major_lang_index-1]

class CSIdentifier(object):
	def __init__(self, translate):
		self.translate = translate

	def __check_phrasal_cs_presence(self, sentence: str, minor_lang: str) -> bool:
		tokens = sentence.split()
		if len(tokens)<=2:
			return False
		else:
			for n in range(len(tokens)-2):
				triplet = ' '.join(tokens[n:n+3])
				if self.translate.detect_lang(triplet) == minor_lang:
					return True
		return False

	@staticmethod
	def __check_lexical_cs_presence(sentence: str, minor_lang: str) -> bool:
		tokens = sentence.split()
		for token in tokens:
			if token in UNCOMMON_WORDS[minor_lang]:
				return True
		return False

	@staticmethod
	def __check_frozen_expression_cs_presence(sentence: str, minor_lang: str) -> bool:
		tokens = sentence.split()
		for token in tokens:
			if token in COMMON_WORDS[minor_lang]:
				return True
		return False

	@staticmethod
	def __clean_sentence(sentence: str) -> str:
		chars_to_remove = '?!,.:"\''
		for char in chars_to_remove:
			sentence = sentence.replace(char, '')
		return sentence.strip()

	def calc_cs_level(self, sentence: str) -> str:
		major_lang = self.translate.detect_lang(sentence)
		major_lang_code = MAJOR_LANGUAGE_CODES[major_lang]
		minor_lang = get_other_lang(major_lang)
		clean_version_of_sentence = self.__clean_sentence(sentence)
		if self.__check_phrasal_cs_presence(clean_version_of_sentence, minor_lang):
			minor_lang_code = 'P'
		elif self.__check_lexical_cs_presence(clean_version_of_sentence, minor_lang):
			minor_lang_code = 'L'
		elif self.__check_frozen_expression_cs_presence(clean_version_of_sentence, minor_lang):
			minor_lang_code = 'T'
		else:
			minor_lang_code = 'N'
		return major_lang_code+minor_lang_code
