from enum import Enum

class ConversationMode(Enum):
    CHAT = "chat"  # zwykła rozmowa
    EXPERIMENT = "experiment"  # bezpośrednie, surowe odpowiedzi
    MENTOR = "mentor"  # krok po kroku, instruktażowo
    REFLECT =  "reflect" #meta-myślenie
    ANALYSIS = "analysis"  # techniczne rozkminy

class ConversationStyle(Enum):
    NEUTRAL = "neutral"
    NIHILISTIC = "nihilistic"

    AM_COLD = "am_cold"
    AM_PROBING = "am_probing"


class ConversationState:
    def __init__(self, mode = ConversationMode.CHAT, style = ConversationStyle.NEUTRAL,verbosity = "medium", temperature = 1.2):
        self.mode = mode
        self.style=style
        self.verbosity=verbosity
        self.temperature = temperature
        self.custom_flags = {}

    def set_mode(self, role : ConversationMode):
        self.mode=mode

    def set_style(self, mode : ConversationStyle):
        self.style=style

    def set_verbosity(self, level : str):
        if level in ("low", "medium", "high"):
            self.verbosity = level

    def set_temperature(self, temp: float):
        self.temperature = max(0.0, min(1.5, temp))

    def update_flag(self, key: str, value):
        self.custom_flags[key] = value

    def to_dict(self):
        "do logów i interakcji z engine.py"
        return{
            "mode": self.mode.value,
            "verbosity": self.verbosity,
            "temperature": self.temperature,
            "flags": self.custom_flags
        }



    def to_message(self) -> dict:
        lines = []

        lines.append(f"[MODE: {self.mode.value.upper()}")

        if self.style != ConversationStyle.NEUTRAL:
            lines.append(f"[STYLE:{self.style.value.upper()}]")

        return {
            "role": "assistant",
            "content": "\n".join(lines)
        }