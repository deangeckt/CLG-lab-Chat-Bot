import os
os.chdir('../../code_switch')

from google_cloud.translate import Translate
from code_switch.level_identification.cs_level_identification import CSIdentifier, load_words, get_other_lang

def test_load_words():
	filename = 'resources/most_common_1000_en_words.txt'
	load_words(filename)

def test_get_other_lang():
	lang = 'en'
	other_lang = get_other_lang(lang)
	print(lang + ": " + other_lang)
	lang = 'es'
	other_lang = get_other_lang(lang)
	print(lang + ": " + other_lang)


def test_calc_level():
	translate = Translate()
	cs_level_identifier = CSIdentifier(translate)

	sentence = 'how do i get to the end of the map?!'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

	sentence = 'hola, how do i get to the end of the map?!'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

	sentence = 'hi there, Cómo se llega a la capital?'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

	sentence = 'how do i get to the jirafa?'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

	sentence = '¿Cómo se llega to the carrot?'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

	sentence = 'well, Cómo se llega to the carrot?'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

	sentence = '¿Cómo se llega a la capital?'
	cs_level = cs_level_identifier.calc_cs_level(sentence)
	print(sentence + " (" + cs_level + ")")

def run_tests():
	test_get_other_lang()
	test_load_words()
	test_calc_level()

if __name__ == '__main__':
	run_tests()
	print("Finished!")