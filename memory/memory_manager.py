from memory.working_memory import WorkingMemory
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory, LTMEventType, LTMEvent
from control.affect_state import AffectState


class MemoryManager:
    """
    Koordynator pamięci:
    - WorkingMemory: bieżące fakty, temat, intencja
    - ShortTermMemory: stan poznawczy rozmowy
    - LongTermMemory: pamięć długoterminowa (planowane)
    """
    def __init__(self):
        self.wm = WorkingMemory()
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()
        self.affect = AffectState(vector={})

    def update(self, user_input: str):
        # 1. Aktualizacja WM
        self.wm.update(user_input)

        # 2. Aktualizacja STM na podstawie WM
        self.stm.update_from_wm(self.wm)

        # 3. Aktualizacja LTM
        if self.wm.topic_shift:
            self.consolidate_to_ltm()

        self.affect.update_from_memory(
            self.wm.to_snapshot(),
            self.stm.to_snapshot(),
            self.ltm.recall()
        )

    def consolidate_to_ltm(self):

        snapshot = self.stm.to_snapshot()
        if not (snapshot.get("is_reflective") or snapshot.get("is_analytical")):
            return

        content = f"Conversation focused on {self.stm.focus}"
        if self.ltm.events and self.ltm.events[-1].content == content:
            return


        event = LTMEvent(
            type=LTMEventType.EXPERIENCE,
            content=f"Conversation focused on {self.stm.focus}",
            importance=0.4
        )
        self.ltm.store(event)

        self.affect.update_from_memory(
            self.wm.to_snapshot(),
            self.stm.to_snapshot(),
            self.ltm.recall()
        )

    def get_behavior_inputs(self):
        return (
            self.wm,
            self.stm,
            self.ltm.recall(),
            self.affect
        )

    def snapshot(self):
        return {
            "wm": self.wm.to_snapshot(),
            "stm": self.stm.to_snapshot(),
            "ltm": self.ltm.recall(),
            "affect": self.affect.vector
        }

