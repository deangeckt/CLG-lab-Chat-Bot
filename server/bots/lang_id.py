from singleton_decorator import singleton
from codeswitch.codeswitch import LanguageIdentification
from enum import Enum


class LanguageId(str, Enum):
    mix = "mix"
    eng = "eng"
    es = 'es'


@singleton
class LangId:
    def __init__(self):
        self.lid = LanguageIdentification('spa-eng')

    @staticmethod
    def __cs_clf_heuristic(langs: list) -> LanguageId:
        if LanguageId.eng in langs and LanguageId.es in langs:
            return LanguageId.mix
        if LanguageId.eng in langs:
            return LanguageId.eng
        else:
            return LanguageId.es

    def identify(self, user_msg) -> LanguageId:
        # https://huggingface.co/sagorsarker/codeswitch-spaeng-lid-lince
        result = self.lid.identify(user_msg)
        langs = []
        for r in result:
            lng = r['entity']
            if lng == 'en':
                langs.append(LanguageId.eng)
            elif lng == 'spa':
                langs.append(LanguageId.es)
        return self.__cs_clf_heuristic(langs)
