from typing import Optional, List, Dict


class WorkingMemory:
    """
    WM = lokalna interpretacja bieżącego inputu
    Resetowana co turę
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.topic: str | None = None
        self.intent: str | None = None

        self.is_reflective = False
        self.is_analytical = False
        self.is_experimental = False

        self.topic_shift = False
        self.focus: str | None = None

    def update(self, text: str):
        self.reset()
        t = text.lower()
        self._detect_topic(t)
        self._detect_intent(t)
        self._detect_mode(t)

        self.focus = self.topic

    def _detect_topic(self, t: str):
        if any(k in t for k in ["architecture", "system", "design"]):
            self.topic = "architecture"
            self.is_analytical = True

    def _detect_intent(self, t: str):
        if any(k in t for k in ["what should we do", "next step", "plan"]):
            self.is_reflective = True

    def _detect_mode(self, t: str):
        if any(k in t for k in ["what if", "experiment"]):
            self.is_experimental = True

    def to_snapshot(self) -> dict:
        return {
            "topic": self.topic,
            "focus": self.focus,
            "is_reflective": self.is_reflective,
            "is_analytical": self.is_analytical,
            "is_experimental": self.is_experimental,
        }


