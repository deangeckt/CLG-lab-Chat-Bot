from code_switch.strategies.cs_strategies import CSStrategy, CSParameters, DEFAULT_CS_PARAMS

class EnglishOnlyStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=DEFAULT_CS_PARAMS):
		CSStrategy.__init__(self, cs_params)

	@staticmethod
	def predict_next_cs_level(current_cs_level=None):
		return 'EN'

