from typing import Tuple

from singleton_decorator import singleton
import time
import spacy
from spacy.tokens import Doc, Token

from bots.models.lang_id_bert import LanguageId


@singleton
class NounsExtractor:
    def __init__(self):
        s = time.time()
        #TODO: restore
        # self.en_nlp = spacy.load(r'bots/models/en_core_web_sm-3.7.1')
        self.es_nlp = spacy.load(r'bots/models/es_core_news_md-3.7.0')
        print('spacy init time: ')
        print(time.time() - s)

    @staticmethod
    def __merge_phrases(doc: Doc):
        with doc.retokenize() as retokenizer:
            for np in list(doc.noun_chunks):
                attrs = {
                    "tag": np.root.tag_,
                    "lemma": np.root.lemma_,
                    "ent_type": np.root.ent_type_,
                }
                retokenizer.merge(np, attrs=attrs)
        return doc

    def extract_nouns_phrases(self, text: str, lang: LanguageId) -> list[str]:
        if lang == LanguageId.mix: return []
        nlp = self.en_nlp if lang == LanguageId.eng else self.es_nlp
        doc = nlp(text)
        doc = self.__merge_phrases(doc)
        return [token.text for token in doc if token.pos_ == 'NOUN']

    def extract_nouns_with_det(self, text: str, lang: LanguageId) -> list[Tuple[Token, Token]]:
        if lang == LanguageId.mix: return []
        nlp = self.en_nlp if lang == LanguageId.eng else self.es_nlp
        doc = nlp(text)

        res = []
        for token in doc:
            if token.pos_ != 'NOUN':
                continue
            found_det = False
            for left_token in reversed(list(token.lefts)):
                if left_token.pos_ == 'DET' or left_token.pos_ == 'ADP':
                    res.append((left_token, token))
                    found_det = True
                    break
            if not found_det:
                res.append((None, token))

        return res


if __name__ == "__main__":
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


    ex = NounsExtractor()
    text = 'el el gran tenedor marrón estaba sobre la mesa'
    text = 'vale, he pasado al tigre y estoy en camino hacia el loro y el elefante'
    nouns = ex.extract_nouns_with_det(text, LanguageId.es)
    print(nouns)
    print()
    substitutions = [{'orig': det.text, 'new': 'x', 'idx': det.idx} for det, noun in nouns if det]
    substitutions[0]['new'] = 'mock'
    print(__replace_substrings(text, substitutions))

