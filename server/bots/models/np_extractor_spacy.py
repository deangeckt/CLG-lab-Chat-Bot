from singleton_decorator import singleton
import time
import spacy
from spacy.tokens import Doc

from bots.models.lang_id_bert import LanguageId


@singleton
class NounPhraseExtractor:
    def __init__(self):
        s = time.time()
        self.en_nlp = spacy.load(f'bots/models/en_core_web_sm-3.7.1')
        self.es_nlp = spacy.load(f'bots/models/es_core_news_md-3.7.0')
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

    def extract(self, text: str, lang: LanguageId) -> list[str]:
        if lang == LanguageId.mix: return []
        nlp = self.en_nlp if lang == LanguageId.eng else self.es_nlp
        doc = nlp(text)
        doc = self.__merge_phrases(doc)
        return [token.text for token in doc if token.pos_ == 'NOUN']