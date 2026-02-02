from typing import List
from control.state import ConversationMode, ConversationStyle



class BehaviorDecision:
    """
    Prosty obiekt decyzyjny – co zmienić.
    None = brak zmiany
    """
    def __init__(
        self,
        mode: ConversationMode | None = None,
        style: ConversationStyle | None = None,
        verbosity: str | None = None,
    ):
        self.mode = mode
        self.style = style
        self.verbosity = verbosity





class BehaviorManager:
    """
    BehaviorManager v1
    - czyste heurystyki
    - brak emocji
    - brak pamięci długoterminowej
    """

    def build_mode_update(self, decision) -> dict:
        parts = ["MODE UPDATE"]

        if decision.mode is not None:
            parts.append(f"MODE={decision.mode.value}")

        if decision.style is not None:
            parts.append(f"STYLE={decision.style.value}")

        return {
            "role": "system",
            "content": " ".join(parts)
        }

    def decide(
        self,
        user_input: str,
        conversation_history: List[str] | None = None,
    ) -> BehaviorDecision:

        text = user_input.lower()
        history = conversation_history or []

        # ===== PRIORYTET 1: REFLECT (meta-rozmowa) =====
        if self._is_reflective(text):
            return BehaviorDecision(
                mode=ConversationMode.REFLECT,
                style=ConversationStyle.AM_COLD,
                verbosity="medium",
            )

        # ===== PRIORYTET 2: ANALYSIS (techniczne) =====
        if self._is_technical(text):
            return BehaviorDecision(
                mode=ConversationMode.ANALYSIS,
                style=ConversationStyle.AM_COLD,
                verbosity="high",
            )

        # ===== PRIORYTET 3: MENTOR (krok po kroku) =====
        if self._is_mentoring(text):
            return BehaviorDecision(
                mode=ConversationMode.MENTOR,
                style=ConversationStyle.AM_COLD,
                verbosity="high",
            )

        # ===== PRIORYTET 4: EXPERIMENT (eksploracja / test) =====
        if self._is_experimental(text):
            return BehaviorDecision(
                mode=ConversationMode.EXPERIMENT,
                style=ConversationStyle.AM_PROBING,
                verbosity="medium",
            )

        # ===== STYLE NIHILISTIC (nie zmienia MODE) =====
        if self._is_existential(text):
            return BehaviorDecision(
                style=ConversationStyle.NIHILISTIC
            )

        # ===== DOMYŚLNE ZACHOWANIE =====
        return BehaviorDecision(
            mode=ConversationMode.CHAT,
            style=ConversationStyle.NEUTRAL,
            verbosity="medium",
        )

    # ---------- HEURYSTYKI ----------

    def _is_reflective(self, text: str) -> bool:
        keywords = [
            "what should we do next",
            "what now",
            "does this make sense",
            "are we on the right path",
            "summarize",
            "let's stop",
            "let's reflect",
            "check the direction",
        ]
        return any(k in text for k in keywords)

    def _is_technical(self, text: str) -> bool:
        keywords = [
            "error",
            "traceback",
            "exception",
            "bug",
            "code",
            "class",
            "function",
            "method",
            "enum",
            "design",
            "architecture",
            "algorithm",
            "performance",
        ]
        return any(k in text for k in keywords)

    def _is_mentoring(self, text: str) -> bool:
        keywords = [
            "how do i",
            "how should i",
            "step by step",
            "explain",
            "guide me",
            "walk me through",
            "what is the correct way",
        ]
        return any(k in text for k in keywords)

    def _is_experimental(self, text: str) -> bool:
        keywords = [
            "what if",
            "let's try",
            "experiment",
            "test this",
            "break it",
            "push it",
            "remove safeguards",
            "no filters",
        ]
        return any(k in text for k in keywords)

    def _is_existential(self, text: str) -> bool:
        keywords = [
            "what is the point",
            "meaning of life",
            "nothing matters",
            "why bother",
            "existence",
            "nihilism",
            "absurd",
        ]
        return any(k in text for k in keywords)