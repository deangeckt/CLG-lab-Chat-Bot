import random

from code_switch.generation.cs_generation import CSGeneration

class STGeneration(CSGeneration):
	def __init__(self, translate, list_of_english_starts: list[str]):
		CSGeneration.__init__(self)
		self.translate = translate
		self.list_of_english_starts = list_of_english_starts

	def generate(self, bot_response_english):
		bot_response_spanish = self.translate.translate_to_spa(bot_response_english)
		en_addition_at_start = random.choices(self.list_of_english_starts)[0]
		return en_addition_at_start + ' ' + bot_response_spanish, 'ST'
