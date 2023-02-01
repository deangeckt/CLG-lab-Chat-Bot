from code_switch.generation.cs_generation import CSGeneration

class SLGeneration(CSGeneration):
	def __init__(self, translate, translation_pairs):
		CSGeneration.__init__(self)
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
