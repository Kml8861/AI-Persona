from dataclasses import dataclass, field
from control.state import ConversationMode
from memory.working_memory import WorkingMemory



@dataclass
class ShortTermMemory:
    """
        STM = aktualny stan poznawczy rozmowy
        - NIE historia
        - NIE surowy tekst
        - tylko decyzje i intencje
        """

    # aktualny tryb rozmowy
    mode: ConversationMode = ConversationMode.CHAT

    # wysoki poziom intencji usera
    intent: str | None = None  # np. "ask", "analyze", "reflect", "experiment"

    # aktualny fokus rozmowy
    focus: str | None = None  # np. "architecture", "emotion", "meta"

    # czy rozmowa jest stabilna czy się zmienia
    topic_shift: bool = False

    # flaga: czy to meta-rozmowa
    is_reflective: bool = False

    # flaga: czy techniczne
    is_analytical: bool = False

    def update_from_wm(self, wm: "WorkingMemory"):
        """
        Aktualizacja STM na podstawie WorkingMemory
        """

        self.is_reflective = wm.is_reflective
        self.is_analytical = wm.is_analytical
        self.topic_shift = wm.topic_shift

        if wm.is_reflective:
            self.mode = ConversationMode.REFLECT
            self.intent = "reflect"

        elif wm.is_analytical:
            self.mode = ConversationMode.ANALYSIS
            self.intent = "analyze"

        elif wm.is_experimental:
            self.mode = ConversationMode.EXPERIMENT
            self.intent = "experiment"

        else:
            self.mode = ConversationMode.CHAT
            self.intent = "chat"

        self.focus = wm.focus

    def to_snapshot(self) -> dict:
        return {
            "mode": self.mode.value,
            "intent": self.intent,
            "focus": self.focus,
            "topic_shift": self.topic_shift,
            "is_reflective": self.is_reflective,
            "is_analytical": self.is_analytical,
        }