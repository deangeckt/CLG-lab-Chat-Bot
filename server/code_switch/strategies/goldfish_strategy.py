import random

from code_switch.strategies.cs_strategies import CSStrategy, CSParameters, DEFAULT_CS_PARAMS
from code_switch.utils import hazard

class GoldfishStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=DEFAULT_CS_PARAMS):
		CSStrategy.__init__(self, cs_params)

		self.cs_levels = list(self.cs_params.keys())
		self.probabilities = [cs_params[cs_level].probability for cs_level in self.cs_levels]

		self.len_of_current_subsequence = 1

	def predict_next_cs_level(self, current_cs_state=None):
		if current_cs_state is None:
			return self.__select_random_cs_level()

		r = self.cs_params[current_cs_state].r
		p = hazard(r, s=self.len_of_current_subsequence)
		res = random.choices([True, False], [p, 1 - p])[0]
		if res:  # change state
			next_state = self.__select_next_state(current_cs_state)
			self.len_of_current_subsequence = 1
		else:  # keep current state
			next_state = current_cs_state
			self.len_of_current_subsequence += 1
		return next_state

	def __select_next_state(self, current_state):
		all_next_possible_state_options = []
		all_next_possible_state_probabilities = []
		for next_state_option, next_state_transition_probability in \
				self.cs_params[current_state].transitions.items():

			if not(next_state_option == current_state):
				all_next_possible_state_options.append(next_state_option)
				all_next_possible_state_probabilities.append(next_state_transition_probability)
		next_state = random.choices(all_next_possible_state_options, all_next_possible_state_probabilities)[0]
		return next_state

	def __select_random_cs_level(self):
		return random.choices(self.cs_levels, weights=self.probabilities)[0]
