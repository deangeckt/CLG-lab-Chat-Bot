from code_switch.generation.cs_generation import CSGeneration

class ELGeneration(CSGeneration):
	def __init__(self, translation_pairs):
		CSGeneration.__init__(self)
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
