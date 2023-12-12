from typing import List
from bots.cs_unit import CSUnit, CodeSwitchStrategyName
from bots.gpt.code_switch_strategies.alternation_align_last_user import AlternationAlignLastUser
from bots.gpt.code_switch_strategies.alternation_random import AlternationRandom
from bots.gpt.code_switch_strategies.alternation_short_ctx import AlternationShortContext
from bots.gpt.code_switch_strategies.alternation_switch_last_user import AlternationSwitchLastUser
from bots.gpt.code_switch_strategies.baseline import Baseline
from bots.gpt.code_switch_strategies.insertional_noun_phrase import InsertionalNounPhraseTest


class CodeSwitchStrategies(CSUnit):
    """
    Alternation strategies translates the whole sentence / turn
    Insertional strategies detect NP and translate only it
    """

    def __init__(self, strategy: CodeSwitchStrategyName, welcome_str: str):
        super().__init__()

        self.strategy = strategy
        self.strategies = {
            CodeSwitchStrategyName.none: Baseline,
            CodeSwitchStrategyName.alternation_random: AlternationRandom(),
            CodeSwitchStrategyName.alternation_short_context: AlternationShortContext(welcome_str),
            CodeSwitchStrategyName.alternation_switch_last_user: AlternationSwitchLastUser(),
            CodeSwitchStrategyName.alternation_align_last_user: AlternationAlignLastUser(),
            CodeSwitchStrategyName.insertional_noun_phrase: InsertionalNounPhraseTest()
        }

        self.is_last_switched = False

    def call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        self.is_last_switched = False
        strategy = self.strategies[self.strategy]
        spanglish_resp, is_switched = strategy.call(user_msg, bot_resp)

        self.is_last_switched = is_switched
        return spanglish_resp

    def is_switched(self) -> bool:
        return self.is_last_switched

    def db_push(self) -> dict:
        pass

    def db_load(self, data):
        pass
