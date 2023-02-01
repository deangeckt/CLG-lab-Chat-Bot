from abc import ABC, abstractmethod
import random

class CSGeneration(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def generate(self, bot_response_english: str)-> tuple[str, str]:
			pass

class ENGeneration(CSGeneration):
	def __init__(self):
		pass

	def generate(self, bot_response_english):
		return bot_response_english, 'EN'

class ETGeneration(CSGeneration):
	def __init__(self, list_of_spanish_starts: list[str]):
		self.list_of_spanish_starts = list_of_spanish_starts
	def generate(self, bot_response_english):
		es_addition_at_start = random.choices(self.list_of_spanish_starts)[0]
		return es_addition_at_start + ' ' + bot_response_english, 'ET'

class ELGeneration(CSGeneration):
	def __init__(self, translation_pairs):
		self.translation_pairs = translation_pairs
	def generate(self, bot_response_english):
		bot_response_el = bot_response_english
		replacement_found = False
		for english_token in self.translation_pairs['en']:
			if bot_response_english.find(english_token) > 0:  # Found in text
				replacement_found = True
				break

		for english_token, spanish_token in zip(self.translation_pairs['en'], self.translation_pairs['es']):
			bot_response_el = bot_response_el.replace(english_token, spanish_token)

		if replacement_found:
			final_cs_level = 'EL'
		else:
			final_cs_level = 'EN'
		return bot_response_el, final_cs_level

class EPGeneration(CSGeneration):
	def __init__(self, translate):
		self.translate = translate

	def generate(self, bot_response_english):
		return self.translate.translate_to_spa(bot_response_english), 'EN'

class SPGeneration(CSGeneration):
	def __init__(self, translate):
		self.translate = translate

	def generate(self, bot_response_english):
		return self.translate.translate_to_spa(bot_response_english), 'SN'

class SLGeneration(CSGeneration):
	def __init__(self, translate, translation_pairs):
		self.translate = translate
		self.translation_pairs = translation_pairs

	def generate(self, bot_response_english):
		bot_response_sl = self.translate.translate_to_spa(bot_response_english)
		replacement_found = False
		for spanish_token in self.translation_pairs['es']:
			if bot_response_sl.find(spanish_token) > 0:  # Found in text
				replacement_found = True
				break

		for spanish_token, english_token in zip(self.translation_pairs['es'], self.translation_pairs['en']):
			bot_response_sl = bot_response_sl.replace(spanish_token, english_token)

		if replacement_found:
			final_cs_level = 'SL'
		else:
			final_cs_level = 'SN'
		return bot_response_sl, final_cs_level

class STGeneration(CSGeneration):
	def __init__(self, translate, list_of_english_starts: list[str]):
		self.translate = translate
		self.list_of_english_starts = list_of_english_starts

	def generate(self, bot_response_english):
		bot_response_spanish = self.translate.translate_to_spa(bot_response_english)
		en_addition_at_start = random.choices(self.list_of_english_starts)[0]
		return en_addition_at_start + ' ' + bot_response_spanish, 'ST'

class SNGeneration(CSGeneration):
	def __init__(self, translate):
		self.translate = translate

	def generate(self, bot_response_english):
		return self.translate.translate_to_spa(bot_response_english), 'SN'