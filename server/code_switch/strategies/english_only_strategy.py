from code_switch.strategies.cs_strategies import CSStrategy, CSParameters

class EnglishOnlyStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=None):
		CSStrategy.__init__(self)

	@staticmethod
	def predict_next_cs_level(current_cs_level=None):
		return 'EN'

