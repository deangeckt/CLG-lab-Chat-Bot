from typing import List
from bots.gpt.code_switch_strategies.code_switch_strategy import CodeSwitchStrategy
from bots.models.lang_id_bert import LanguageId
from bots.models.nouns_extractor_spacy import NounsExtractor
import codecs


class InsertionalSpanishIncongruent(CodeSwitchStrategy):
    """
        WIP
        this CS strategy uses a different sub strategy / condition per map, but the order of map remains:
        Ins, Nav, Ins, Nav
    """

    def __init__(self, map_index: int):
        super().__init__()
        self.noun_phrase_extractor = NounsExtractor()
        nouns_file = codecs.open('bots/gpt/code_switch_strategies/spanish_nouns_set.txt', "r", "utf-8")
        self.es_to_eng_nouns = {n.strip().split('_')[0]: n.strip().split('_')[1] for n in nouns_file.readlines()}

        # TODO: dont need to check if the noun is MASC or FEM. its decided by the det?
        # https://en.wikipedia.org/wiki/Spanish_determiners
        self.masc_femi_determiners_dict = {
            'al': 'la',  # the singular
            'el': 'la',  # the singular (in the reverse dict la -> el)
            'los': 'las',  # the plural
            'ese': 'esa',  # that
            'este': 'esta',  # this
            'esos': 'esas',  # those
            'estos': 'estas',  # those
            'un': 'una',  # a singular
            'unos': 'unas',  # a plural
            'nuestro': 'nuestra',  # my
            'nuestros': 'nuestras',  # ours
            'vuestro': 'vuestra',  # your
            'vuestros': 'vuestras',  # theirs
            'del': 'de la'  # edge case: to the
        }

        '''
        edge case:
        del loro    (adp noun) -> switch to "de la parrot"  # NO NEED TO CHANGE LOGIC, JUST THE SWAP DICT
        de la perra (adp, det, noun) -> switch to "del parrot" # edge case where u have 3 in the tuple
        '''

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

    def __swap(self, nouns_bot_resp: list, bot_resp: List[str], det_dict: dict):
        for resp_idx, nouns in enumerate(nouns_bot_resp):
            substitutions = []
            for det, noun in nouns:
                if noun.text not in self.es_to_eng_nouns:
                    continue

                if det and det.text in det_dict:
                    substitutions.append({'orig': det.text, 'new': det_dict[det.text], 'idx': det.idx})
                    print(f'{resp_idx}:Swapped det: {det.text} to: {det_dict[det.text]}')

                translated_noun = self.es_to_eng_nouns[noun.text]
                substitutions.append({'orig': noun.text, 'new': translated_noun, 'idx': noun.idx})
                print(f'{resp_idx}:Swapped noun: {noun} to: {translated_noun}')

            bot_resp[resp_idx] = self.__replace_substrings(text=bot_resp[resp_idx], substitutions=substitutions)

    def __congruent(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        e.g.: el fork/la spoon	i.e. all [Spa] DETs match expected gender
        we assume the gender are fine and don't switch
        """
        self.__swap(nouns_bot_resp, bot_resp, det_dict={})

    def __incongruent_1(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        e.g.: LA fork/la spoon	i.e. for MASC Ns only, Spanish DET switches genders
        (prediction: increase task times/decrease enjoyment for regular CSers)
        """
        self.__swap(nouns_bot_resp, bot_resp, self.masc_femi_determiners_dict)

    def __incongruent_2(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        el fork/EL spoon	i.e. for FEM Ns only, Spa DET switches genders
        (prediction: may increase task times/decrease enjoyment for non-CSers, or no effect)
        """
        femi_masc_determiners_dict = {v: k for k, v in self.masc_femi_determiners_dict.items()}
        self.__swap(nouns_bot_resp, bot_resp, femi_masc_determiners_dict)

    def call(self, user_msg: str, bot_resp: List[str]) -> tuple[list[str], bool]:
        nouns_bot_resp = []
        for msg in bot_resp:
            bot_lang: LanguageId = self.lid.identify(msg)
            extracted_nouns = self.noun_phrase_extractor.extract_nouns_with_det(msg, bot_lang) \
                if bot_lang == LanguageId.es else []
            print('extracted_nouns:', extracted_nouns)
            nouns_bot_resp.append(extracted_nouns)

        if not any([len(nouns) for nouns in nouns_bot_resp]):
            return bot_resp, False

        # TODO choose per map - what is the experiment setup? 4 maps but 3 conditions here
        self.__incongruent_1(nouns_bot_resp, bot_resp)

        return bot_resp, False
