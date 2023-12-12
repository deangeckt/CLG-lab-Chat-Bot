from typing import List

import spacy
from spacy.tokens import Doc
from bots.gpt.code_switch_strategies.code_switch_strategy import CodeSwitchStrategy
from bots.lang_id_bert import LanguageId


class InsertionalNounPhraseTest(CodeSwitchStrategy):
    """
    """
    def __init__(self):
        super().__init__()
        # TODO: singleton wrapper
        self.en_nlp = spacy.load("en_core_web_sm")
        self.es_nlp = spacy.load("es_core_news_md")


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

    def __extract_noun_phrase(self, text, lang) -> list[str]:
        if lang == LanguageId.mix: return []
        nlp = self.en_nlp if lang == LanguageId.eng else self.es_nlp
        doc = nlp(text)
        doc = self.__merge_phrases(doc)

        nouns = []
        for token in doc:
            if token.pos_ == 'NOUN':
                nouns.append(token.text)
        return nouns


    def call(self, user_msg: str, bot_resp: List[str]) -> tuple[list[str], bool]:
        nouns = []
        for msg in bot_resp:
            bot_lang = self.lid.identify(msg)
            nouns.extend(self.__extract_noun_phrase(msg, bot_lang))

        return bot_resp, False

