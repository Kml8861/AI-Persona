import json
import requests
import threading
from core.context import ConversationContext
from control.state import ConversationState, ConversationMode, ConversationStyle
from control.behavior import BehaviorManager

class CogitoErgoSum:
    def __init__(self, config: dict):
        self.model_name = config["model"]
        self.api_url = config.get("api_url", "http://localhost:11434/api/chat")
        self.stream = config.get("stream", False)
        self.state= ConversationState(
            mode=ConversationMode(config.get("mode", "chat")),
            style=ConversationStyle(config.get("style", "neutral")),
            verbosity=config.get("verbosity", "medium"),
            temperature=config.get("temperature", 1.2)
        )
        self.behavior= BehaviorManager()

        # teraz korzystamy z finalnego ConversationContext
        self.context = ConversationContext(
            max_tokens=config.get("max_tokens", 1800),
            mode=config.get("token_mode", "accurate")  # fast/accurate
        )

        # prewarm w osobnym wątku
        threading.Thread(
            target=self._prewarm,
            daemon=True
        ).start()

    def ask(self, user_input: str) -> str:
        # dodajemy wiadomość użytkownika
        self.context.add("user", user_input)

        decision=self.behavior.decide(user_input)

        if decision.mode or decision.style:
            system_message = self.behavior.build_mode_update(decision)
            self.context.add("system", system_message["content"])

        # wywołanie LLM
        reply = self._call_llm()

        # dodanie odpowiedzi do kontekstu
        self.context.add("assistant", reply)
        return reply

    def _prewarm(self):
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": "Warm up"}
            ],
            "stream": False,
            "options": {
                "num_ctx": 2048
            }
        }

        try:
            requests.post(self.api_url, json=payload, timeout=40)
        except requests.RequestException as e:
            print(f"[Prewarm] Błąd podczas prewarm: {e}")

    def _call_llm(self) -> str:
        payload = {
            "model": self.model_name,
            "messages":
                [self.state.to_message()] + self.context.build(),  # token-aware trimming
            "stream": self.stream,
            "options": {
                "num_ctx": 2048
            }
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                stream=self.stream,
                timeout=180
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Nie udało się połączyć z API: {e}")

        full_reply = ""

        # obsługa streamingu, jeśli self.stream = True
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            if "message" in data:
                token = data["message"]["content"]
                print(token, end="", flush=True)
                full_reply += token

            if data.get("done", False):
                break

        print()
        return full_reply
