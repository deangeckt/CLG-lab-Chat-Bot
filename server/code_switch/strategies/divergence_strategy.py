import random

from code_switch.strategies.cs_strategies import CSStrategy, CSParameters, DEFAULT_CS_PARAMS

class DivergenceStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=DEFAULT_CS_PARAMS):
		CSStrategy.__init__(self, cs_params)
		self.cs_levels = list(self.cs_params.keys())
		self.probabilities = [self.cs_params[cs_level].probability for cs_level in self.cs_levels]

	def predict_next_cs_level(self, current_cs_state=None):
		if current_cs_state is None:
			return random.choices(self.cs_levels, weights=self.probabilities)[0]
		if current_cs_state[0] == 'E': # Major-Language == English -> Return Spanish Response
			spanish_cs_level_options = [cs_level for cs_level in self.cs_levels if cs_level[0]=='S']
			spanish_cs_level_probabilities = [self.cs_params[cs_level].probability for cs_level in self.cs_levels if cs_level[0]=='S']
			return random.choices(spanish_cs_level_options, weights=spanish_cs_level_probabilities)[0]
		elif current_cs_state[0] == 'S': # Major-Language == Spanish -> Return English Response
			english_cs_level_options = [cs_level for cs_level in self.cs_levels if cs_level[0]=='E']
			english_cs_level_probabilities = [self.cs_params[cs_level].probability for cs_level in self.cs_levels if cs_level[0]=='E']
			return random.choices(english_cs_level_options, weights=english_cs_level_probabilities)[0]
		else:
			return random.choices(self.cs_levels, weights=self.probabilities)[0]
