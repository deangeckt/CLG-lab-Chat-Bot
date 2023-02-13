import langid
from langid import classify
from google.cloud import translate_v2 as translate
import html
from singleton_decorator import singleton


@singleton
class Translate:
	def __init__(self):
		self.translate_client = translate.Client()

	def translate_to_eng(self, user_msg) -> str:
		# TODO: tmp version of english only for friends
		return user_msg
		detected_lng = self.translate_client.detect_language(user_msg)
		# we don't translate only when the model is 100% sure that its english!
		# we don't want to miss CS sentences with some Spanish in them
		# langId doesn't do a good job compared to google
		if detected_lng['language'] == 'en' and detected_lng['confidence'] == 1:
			return user_msg

		response = self.translate_client.translate(user_msg, target_language='en', source_language='es')
		translated_text = response['translatedText']
		translated_text = html.unescape(translated_text)
		print('tr:', translated_text)
		return translated_text

	def translate_to_spa(self, en_msg: str) -> str:
		# TODO: tmp version of english only for friends
		return en_msg
		response = self.translate_client.translate(en_msg, target_language='es', source_language='en')
		translated_text = response['translatedText']
		translated_text = html.unescape(translated_text)
		return translated_text

	def detect_lang(self, user_msg: str) -> str:
		# TODO: tmp version of english only for friends
		return langid.classify(user_msg)[0]
		# return self.translate_client.detect_language(user_msg)['language']