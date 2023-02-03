import random

from code_switch.strategies.cs_strategies import CSStrategy, CSParameters, DEFAULT_CS_PARAMS

class RandomStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=DEFAULT_CS_PARAMS):
		CSStrategy.__init__(self, cs_params)
		self.cs_levels = list(self.cs_params.keys())
		self.probabilities = [self.cs_params[cs_level].probability for cs_level in self.cs_levels]

	def predict_next_cs_level(self, current_cs_state=None):
		return random.choices(self.cs_levels, weights=self.probabilities)[0]
