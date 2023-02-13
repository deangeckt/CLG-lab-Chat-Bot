from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

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
	def __init__(self, cs_params: CSParameters=DEFAULT_CS_PARAMS):
		self.cs_params = cs_params

	@abstractmethod
	def predict_next_cs_level(self, current_cs_state: Union[str, None])-> str:
		"""
		This function predicts the next cs level according to the strategy (and cs history in the dialogue etc.)
		@param current_cs_state: last cs level that appeared in the dialogue
		@return: predicted cs level code of the next utterance in the dialogue
		"""
		pass
