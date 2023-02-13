from code_switch.generation.cs_generation import CSGeneration

class SPGeneration(CSGeneration):
	def __init__(self, translate):
		CSGeneration.__init__(self)
		self.translate = translate

	def generate(self, bot_response_english):
		return self.translate.translate_to_spa(bot_response_english), 'SN'
