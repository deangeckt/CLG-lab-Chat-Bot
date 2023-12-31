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
        # TODO: restore
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

    def extract_nouns_with_det(self, text: str, lang: LanguageId) -> list[Tuple[dict, dict]]:
        """
        valid tuples:
        DET, ..., NOUN
        ADP NOUN (del X, al X)
        ADP, DET,..., NOUN (a la X, de la X)
        """
        if lang == LanguageId.mix: return []
        nlp = self.en_nlp if lang == LanguageId.eng else self.es_nlp
        doc = nlp(text)

        res = []
        for token in doc:
            if token.pos_ != 'NOUN':
                continue

            left_tokens = list(reversed(list(token.lefts)))
            if not left_tokens:
                print(f'no left tokens: {token.text}')
                continue

            det_token = None
            det_token_idx = 0
            for i, left_token in enumerate(left_tokens):
                if left_token.pos_ == 'DET':
                    det_token = left_token
                    det_token_idx = i
                    break

            if det_token is None:
                if left_tokens[0].pos_ == 'ADP' and left_tokens[0].text in ['del', 'al']:
                    res.append(({'text': left_tokens[0].text, 'idx': left_tokens[0].idx},
                                {'text': token.text, 'idx': token.idx}))
                else:
                    print(f'un-handled 1: {token.text}')
            else:
                if (
                        det_token_idx + 1 < len(left_tokens) and
                        det_token.text == 'la' and
                        left_tokens[det_token_idx + 1].pos_ == 'ADP' and
                        left_tokens[det_token_idx + 1].text in ['a', 'de']
                ):
                    res.append(({'text': left_tokens[det_token_idx + 1].text + ' la', 'idx': left_tokens[det_token_idx + 1].idx},
                                {'text': token.text, 'idx': token.idx}))
                else:
                    res.append(({'text': det_token.text, 'idx': det_token.idx},
                                {'text': token.text, 'idx': token.idx}))

        return res


if __name__ == "__main__":

    ex = NounsExtractor()

    texts = [
        # basic:
        ' okay, me veo caminando por el camino hacia el tigre',
        '¡genial! ahora estoy en la pequeña isla con el tigre',

        # edge cases
        'voy a la playa',
        'Voy al parque',
        'He pasado el tigre y voy camino del perro y el elefante.',
        'He pasado el tigre y voy camino de la perra y el elefante.'

    ]
    for t in texts:
        print(t)
        print(ex.extract_nouns_with_det(t, LanguageId.es))
        print()
