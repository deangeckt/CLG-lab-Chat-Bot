from code_switch.cs_level_identification import load_words, get_other_lang, check_phrasal_cs_presence, check_lexical_cs_presence, check_frozen_expression_cs_presence, calc_cs_level

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

def test_check_phrasal_cs_presence():
	sentence='quiero saltar y cantar de joy'
	minor_lang='eng'
	res = check_phrasal_cs_presence(sentence, minor_lang)

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
	test_calc_level()
	test_get_other_lang()
	test_check_phrasal_cs_presence()
	test_load_words()

if __name__ == '__main__':
	run_tests()
	print("Finished!")