from abc import ABC, abstractmethod
import random

class CSGeneration(ABC):
	def __init__(self):
		pass

	def generate(self, bot_response_english: str) -> tuple[str, str]:
		"""
		@param: bot_response_english: str = The chatbot's response in English
		@return: bot_response_cs: str = The chatbot's response in Spanglish
		@return: actual_cs_level: str = The code of the CS level that was actually applied*
		*in some conditions, the required CS level could not be generated.
		"""
		pass