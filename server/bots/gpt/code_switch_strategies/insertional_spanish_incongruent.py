from typing import List
from bots.gpt.code_switch_strategies.code_switch_strategy import CodeSwitchStrategy
from bots.models.lang_id_bert import LanguageId
from bots.models.nouns_extractor_spacy import NounsExtractor


class InsertionalSpanishIncongruent(CodeSwitchStrategy):
    """
        WIP
        this CS strategy uses a different sub strategy / condition per map, but the order of map remains:
        Ins, Nav, Ins, Nav
    """

    def __init__(self, map_index: int):
        super().__init__()
        self.noun_phrase_extractor = NounsExtractor()

    @staticmethod
    def __replace_substrings(text: str, substitutions: list[dict]) -> str:
        result = list(text)
        offset = 0

        for sub in substitutions:
            orig_substring = sub['orig']
            switch_substring = sub['new']
            index = sub['idx'] + offset

            result[index:index + len(orig_substring)] = list(switch_substring)
            offset += len(switch_substring) - len(orig_substring)

        return ''.join(result)


    def __congruent(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        e.g.: el fork/la spoon	i.e. all [Spa] DETs match expected gender
        we assume the gender are fine and don't switch
        """
        for resp_idx, nouns in enumerate(nouns_bot_resp):
            substitutions = []
            for det, noun in nouns:
                translated_noun = self.translate.translate_to_eng(noun.text).lower()
                substitutions.append({'orig': noun.text, 'new': translated_noun, 'idx': noun.idx})
                print(f'{resp_idx}:Swapped noun: {noun} to: {translated_noun}')

            bot_resp[resp_idx] = self.__replace_substrings(text=bot_resp[resp_idx], substitutions=substitutions)


    def __incongruent_1(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        e.g.: LA fork/la spoon	i.e. for MASC Ns only, Spanish DET switches genders
        (prediction: increase task times/decrease enjoyment for regular CSers)
        """
        masc_nouns_det_swap = {'el': 'la'}
        for resp_idx, nouns in enumerate(nouns_bot_resp):
            substitutions = []
            for det, noun in nouns:
                translated_noun = self.translate.translate_to_eng(noun.text).lower()
                if det and det.text in masc_nouns_det_swap: # TODO: and noun is MASC
                    substitutions.append({'orig': det.text, 'new': 'la', 'idx': det.idx})
                    print(f'{resp_idx}:Swapped masc det: {det.text} to: la')

                substitutions.append({'orig': noun.text, 'new': translated_noun, 'idx': noun.idx})
                print(f'{resp_idx}:Swapped noun: {noun} to: {translated_noun}')

            bot_resp[resp_idx] = self.__replace_substrings(text=bot_resp[resp_idx], substitutions=substitutions)


    def __incongruent_2(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        el fork/EL spoon	i.e. for FEM Ns only, Spa DET switches genders
        (prediction: may increase task times/decrease enjoyment for non-CSers, or no effect)
        """
        masc_nouns_det_swap = {'la': 'el'}
        for resp_idx, nouns in enumerate(nouns_bot_resp):
            substitutions = []
            for det, noun in nouns:
                translated_noun = self.translate.translate_to_eng(noun.text).lower()
                if det and det.text in masc_nouns_det_swap: # TODO: and noun is FEM
                    substitutions.append({'orig': det.text, 'new': 'el', 'idx': det.idx})
                    print(f'{resp_idx}:Swapped fem det: {det.text} to: el')

                substitutions.append({'orig': noun.text, 'new': translated_noun, 'idx': noun.idx})
                print(f'{resp_idx}:Swapped noun: {noun} to: {translated_noun}')

            bot_resp[resp_idx] = self.__replace_substrings(text=bot_resp[resp_idx], substitutions=substitutions)

    def call(self, user_msg: str, bot_resp: List[str]) -> tuple[list[str], bool]:
        nouns_bot_resp = []
        for msg in bot_resp:
            bot_lang: LanguageId = self.lid.identify(msg)
            extracted_nouns = self.noun_phrase_extractor.extract_nouns_with_det(msg, bot_lang) \
                if bot_lang == LanguageId.es else []
            print(extracted_nouns)
            nouns_bot_resp.append(extracted_nouns)

        if not any([len(nouns) for nouns in nouns_bot_resp]):
            return bot_resp, False

        # TODO choose per map
        # TODO: add dicts -  nouns, genders ,translates
        self.__incongruent_2(nouns_bot_resp, bot_resp)

        return bot_resp, False
