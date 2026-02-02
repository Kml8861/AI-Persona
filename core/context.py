from core.tokenizer import TokenCounter
from control.state import ConversationState, ConversationMode

class ConversationContext:
    def __init__(self, max_tokens: int = 1800, mode: str = "accurate"):
        """
        mode: "accurate" - dokładne liczenie tokenów (rola+treść)
              "fast"     - szybkie liczenie tylko treści
        """
        self.tokenizer = TokenCounter()
        self.max_tokens = max_tokens
        self.mode = mode
        self.messages = []


    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def _count_message(self, msg: dict) -> int:
        if self.mode == "fast":
            return self.tokenizer.count_message_fast(msg)
        else:
            return self.tokenizer.count_message_accurate(msg)

    def build(self) -> list:
        """
        Buduje historię wiadomości przycinając ją do max_tokens,
        najnowsze wiadomości mają wyższy priorytet.
        """
        budget = self.max_tokens
        trimmed = []

        # idziemy od końca (najnowsze wiadomości są ważniejsze)
        for msg in reversed(self.messages):
            cost = self._count_message(msg)
            if budget - cost < 0:
                break
            trimmed.append(msg)
            budget -= cost

        trimmed.reverse()
        return trimmed
