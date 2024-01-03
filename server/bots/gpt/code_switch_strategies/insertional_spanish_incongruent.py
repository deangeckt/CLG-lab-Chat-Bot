from typing import List, Union
from bots.gpt.code_switch_strategies.code_switch_strategy import CodeSwitchStrategy
from bots.models.lang_id_bert import LanguageId
from bots.models.nouns_extractor_spacy import NounsExtractor
import codecs
from spacy.tokens import Token


class InsertionalSpanishIncongruent(CodeSwitchStrategy):
    """
        this CS strategy uses a different sub strategy / condition per map, but the order of map remains: Ins, Nav, Ins, Nav
        1. Nouns are always translated from ES to ENG
        2. DET (or edge case or ADP) are gender switched according to condition
        3. ADJ are gender switched to align with new DET gender
    """

    def __init__(self, map_index: int):
        super().__init__()
        self.map_index = map_index
        self.noun_phrase_extractor = NounsExtractor()
        nouns_file = codecs.open('bots/gpt/code_switch_strategies/spanish_nouns_set.txt', "r", "utf-8")
        self.es_to_eng_nouns = {n.strip().split('_')[0]: n.strip().split('_')[1] for n in nouns_file.readlines()}

        # https://en.wikipedia.org/wiki/Spanish_determiners
        self.masc_femi_determiners_dict = {
            'el': 'la',  # the singular
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
            #### ADP
            'del': 'de la',  # to the
            'al': 'a la',  # of / to the (al = a + el shortcut)
        }

    @staticmethod
    def __replace_substrings(text: str, substitutions: list[dict]) -> str:
        substitutions = sorted(substitutions, key=lambda d: d['idx'])
        result = list(text)
        offset = 0

        for sub in substitutions:
            orig_substring = sub['orig']
            switch_substring = sub['new']
            index = sub['idx'] + offset

            result[index:index + len(orig_substring)] = list(switch_substring)
            offset += len(switch_substring) - len(orig_substring)

        return ''.join(result)

    @staticmethod
    def __swap_adj_gender(adj_list: list[Token], to_gender: str):
        """
        switch_to: Fem, Masc
        """
        substitutions = []
        for adj in adj_list:
            gender = adj.morph.get('Gender')
            if not gender:
                continue
            gender = gender[0]
            if gender == to_gender:
                continue

            masc_prefix = ['o', 'n', 'or']
            fem_prefix = 'a'

            if to_gender == 'Masc':
                switched = adj.lemma_
            else:
                if adj.text[-1] not in masc_prefix:
                    continue
                switched = adj.text[:len(adj.text) - 1] + fem_prefix

            print(f'Swapped adj: {adj.text} to: {switched}')
            substitutions.append({'orig': adj.text, 'new': switched, 'idx': adj.idx})

        return substitutions

    def __swap(self, nouns_bot_resp: list, bot_resp: List[str], det_dict: dict, to_gender: Union[str, None]):
        for resp_idx, nouns in enumerate(nouns_bot_resp):
            substitutions = []
            for adj_list, det, noun in nouns:
                noun_text = noun['text']
                noun_idx = noun['idx']
                if noun_text not in self.es_to_eng_nouns:
                    continue

                det_text = det['text']
                det_idx = det['idx']

                if det_text in det_dict:
                    substitutions.append({'orig': det_text, 'new': det_dict[det_text], 'idx': det_idx})
                    print(f'{resp_idx}:Swapped det: {det_text} to: {det_dict[det_text]}')

                translated_noun = self.es_to_eng_nouns[noun_text]
                print(f'{resp_idx}:Swapped noun: {noun_text} to: {translated_noun}')
                substitutions.append({'orig': noun_text, 'new': translated_noun, 'idx': noun_idx})

                if to_gender is not None:
                    substitutions.extend(self.__swap_adj_gender(adj_list, to_gender))

            bot_resp[resp_idx] = self.__replace_substrings(text=bot_resp[resp_idx], substitutions=substitutions)

    def __congruent(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        e.g.: el fork/la spoon	i.e. all [Spa] DETs match expected gender
        we assume the gender are fine and don't switch
        """
        self.__swap(nouns_bot_resp, bot_resp, det_dict={}, to_gender=None)

    def __incongruent_1(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        e.g.: LA fork/la spoon	i.e. for MASC Ns only, Spanish DET switches genders
        (prediction: increase task times/decrease enjoyment for regular CSers)
        """
        self.__swap(nouns_bot_resp, bot_resp, self.masc_femi_determiners_dict, to_gender='Fem')

    def __incongruent_2(self, nouns_bot_resp: list, bot_resp: List[str]):
        """
        el fork/EL spoon	i.e. for FEM Ns only, Spa DET switches genders
        (prediction: may increase task times/decrease enjoyment for non-CSers, or no effect)
        """
        femi_masc_determiners_dict = {v: k for k, v in self.masc_femi_determiners_dict.items()}
        self.__swap(nouns_bot_resp, bot_resp, femi_masc_determiners_dict, to_gender='Masc')

    def call(self, user_msg: str, bot_resp: List[str]) -> tuple[list[str], bool]:
        nouns_bot_resp = []
        for msg in bot_resp:
            bot_lang: LanguageId = self.lid.identify(msg)
            print()
            print(bot_lang, msg)
            extracted_nouns = self.noun_phrase_extractor.extract_nouns_with_det(msg, bot_lang) \
                if bot_lang == LanguageId.es else []
            print('extracted_nouns:', extracted_nouns)
            nouns_bot_resp.append(extracted_nouns)

        if not any([len(nouns) for nouns in nouns_bot_resp]):
            return bot_resp, False

        # TODO experiment settings not decided yet
        if self.map_index % 2 == 0:
            self.__incongruent_1(nouns_bot_resp, bot_resp)
        else:
            self.__incongruent_2(nouns_bot_resp, bot_resp)

        return bot_resp, False
