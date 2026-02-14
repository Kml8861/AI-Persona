from typing import List
from control.state import ConversationMode, ConversationStyle
from memory.short_term_memory import ShortTermMemory
from control.affect_state import AffectState



class BehaviorDecision:
    def __init__(
        self,
        mode: ConversationMode | None = None,
        style: ConversationStyle | None = None,
        verbosity: str | None = None,
        temperature_shift: float | None = None,
        flags: dict | None = None,
        reason: str | None = None,
    ):
        self.mode = mode
        self.style = style
        self.verbosity = verbosity
        self.temperature_shift = temperature_shift
        self.flags = flags or {}
        self.reason = reason




class BehaviorManager:
    """
    Minimalna logika decyzji z STM + AffectState + LTM
    """

    def decide(self, wm, stm, ltm_events, affect: AffectState) -> BehaviorDecision:
        # 1. Decyzja na podstawie STM
        if stm.mode == ConversationMode.REFLECT:
            decision = BehaviorDecision(
                mode=ConversationMode.REFLECT,
                style=ConversationStyle.AM_COLD,
                verbosity="medium",
                temperature_shift=-0.1
            )
        else:
            decision = BehaviorDecision(
                mode=stm.mode,
                style=ConversationStyle.NEUTRAL,
                verbosity="medium"
            )

        # 2. Modyfikacja decyzji przez AffectState
        joy = affect.vector.get("joy", 0)
        sadness = affect.vector.get("sadness", 0)
        if joy > 0.5:
            decision.style = ConversationStyle.AM_PHILOSOPHICAL
            decision.temperature_shift += 0.2
        elif sadness > 0.4:
            decision.style = ConversationStyle.AM_COLD
            decision.temperature_shift -= 0.2

        # 3. Możliwość uwzględnienia LTM (np. wspomnienia emocjonalne)
        for e in ltm_events:
            if e.type == LTMEventType.EMOTION and e.importance > 0.5:
                decision.flags["remembered_emotion"] = e.content

        return decision
