from code_switch.generation.cs_generation import CSGeneration

class ENGeneration(CSGeneration):
	def __init__(self):
		CSGeneration.__init__(self)

	def generate(self, bot_response_english):
		return bot_response_english, 'EN'
