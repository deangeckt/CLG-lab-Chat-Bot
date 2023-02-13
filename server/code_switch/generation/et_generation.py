import random
from code_switch.generation.cs_generation import CSGeneration

class ETGeneration(CSGeneration):
	def __init__(self, list_of_spanish_starts: list[str]):
		CSGeneration.__init__(self)
		self.list_of_spanish_starts = list_of_spanish_starts
	def generate(self, bot_response_english):
		es_addition_at_start = random.choices(self.list_of_spanish_starts)[0]
		return es_addition_at_start + ' ' + bot_response_english, 'ET'
