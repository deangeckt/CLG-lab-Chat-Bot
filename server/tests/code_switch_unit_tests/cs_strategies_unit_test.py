import os
os.chdir('../../code_switch')

from code_switch.strategies.cs_strategies import CSOption

from code_switch.strategies.english_only_strategy import EnglishOnlyStrategy
from code_switch.strategies.spanish_only_strategy import SpanishOnlyStrategy
from code_switch.strategies.random_strategy import RandomStrategy
from code_switch.strategies.goldfish_strategy import GoldfishStrategy
from code_switch.strategies.tit_for_tat_strategy import TitForTatStrategy
from code_switch.strategies.divergence_strategy import DivergenceStrategy

cs_params = {
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

strategies = \
	{"Random": RandomStrategy,
	 "Goldfish": GoldfishStrategy,
	 "Tit-For-Tat": TitForTatStrategy,
	 "English-Only": EnglishOnlyStrategy,
	 "Spanish-Only": SpanishOnlyStrategy,
	 "Divergence": DivergenceStrategy
	 }

for strategy_name, strategy_object in strategies.items():
	cs = None
	current_stragtegy = strategy_object(cs_params) # class init
	print(strategy_name + " Strategy:")
	for _ in range(10):
		cs = current_stragtegy.predict_next_cs_level(cs)
		print(cs)
