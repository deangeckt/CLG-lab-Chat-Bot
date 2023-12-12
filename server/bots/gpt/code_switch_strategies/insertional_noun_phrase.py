from typing import List
from bots.gpt.code_switch_strategies.code_switch_strategy import CodeSwitchStrategy
from bots.models.lang_id_bert import LanguageId
from bots.models.np_extractor_spacy import NounPhraseExtractor


class InsertionalNounPhraseTest(CodeSwitchStrategy):
    """
    """

    def __init__(self):
        super().__init__()
        self.noun_phrase_extractor = NounPhraseExtractor()
        # TODO: fill the list, is it ok for the maps?
        self.dict_mock = {'bench', 'dog', 'tiger', 'spider', 'leopard', 'parrot',
                          'elephant', 'rock', 'rocks', 'frog', 'tree', 'twig'}

    # TODO: currently i override the bot history with cs - effect GPT next time...
    def call(self, user_msg: str, bot_resp: List[str]) -> tuple[list[str], bool]:
        nouns_bot_resp = []
        bot_langs = []
        for msg in bot_resp:
            bot_lang: LanguageId = self.lid.identify(msg)
            bot_langs.append(bot_lang)
            nouns_bot_resp.append(self.noun_phrase_extractor.extract(msg, bot_lang))

        candidates = []
        for resp_idx, nouns_per_resp in enumerate(nouns_bot_resp):
            for np in nouns_per_resp:
                if any([token in self.dict_mock for token in np.split(' ')]):
                    candidates.append((np, resp_idx))

        if not candidates:
            return bot_resp, False

        # TODO: all candidates? only one? if so which one? or multiple?

        for selected_np, selected_idx in candidates:
            lang = bot_langs[selected_idx]
            translate_cb = self.translate.translate_to_spa if lang == LanguageId.eng else self.translate.translate_to_eng

            # TODO; should lower? noticed that spanish get be with upper - seems better
            translated_np = translate_cb(selected_np).lower()
            print(f'Translated selected noun phrase: {selected_np} --- to: {translated_np}')

            msg = bot_resp[selected_idx]
            # replace: no need to check if the string is in
            bot_resp[selected_idx] = msg.replace(selected_np, translated_np)

        return bot_resp, True
