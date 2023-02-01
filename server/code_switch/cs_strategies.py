from abc import ABC, abstractmethod
import random
from dataclasses import dataclass

from code_switch.utils import hazard

@dataclass()
class CSOption:
	probability: float
	transitions: dict
	r: list[float]

@dataclass()
class CSParameters:
	parameters: dict

DEFAULT_CS_PARAMS = {
			"EN": CSOption(probability=0.7,
						   transitions={'ET': 0.1, 'EL': 0.1,'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"ET": CSOption(probability=0.3,
							transitions={'EN': 0.1, 'EL': 0.1,'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.8, 0.15, 0.5]),
			"EL": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'ET': 0.1,'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"EP": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"SP": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"SL": CSOption(probability=0.3,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SP': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.8, 0.15, 0.5]),
			"ST": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"SN": CSOption(probability=0.3,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1},
							r=[0, 0.8, 0.15, 0.5])
		}


class CSStrategy(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def predict_next_cs_level(self, current_cs_state: str)-> str:
		pass

class RandomStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=None):
		if cs_params is None:
			cs_params = DEFAULT_CS_PARAMS

		self.cs_params = cs_params
		self.cs_levels = list(cs_params.keys())
		self.probabilities = [cs_params[cs_level].probability for cs_level in self.cs_levels]

	def predict_next_cs_level(self, current_cs_state=None):
		return random.choices(self.cs_levels, weights=self.probabilities)[0]

class GoldfishStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=None):
		if cs_params is None:
			cs_params = DEFAULT_CS_PARAMS
		self.cs_params = cs_params

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


class TitForTatStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=None):
		if cs_params is None:
			cs_params = DEFAULT_CS_PARAMS
		self.cs_params = cs_params

		self.cs_levels = list(self.cs_params.keys())
		self.probabilities = [cs_params[cs_level].probability for cs_level in self.cs_levels]

	def predict_next_cs_level(self, current_cs_state=None):
		if current_cs_state is None:
			return random.choices(self.cs_levels, weights=self.probabilities)[0]
		return current_cs_state

class EnglishOnlyStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=None):
		pass
	@staticmethod
	def predict_next_cs_level(current_cs_level=None):
		return 'EN'


class SpanishOnlyStrategy(CSStrategy):
	def __init__(self, cs_params: CSParameters=None):
		pass
	@staticmethod
	def predict_next_cs_level(current_cs_level=None):
		return 'SN'

