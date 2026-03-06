# from sqlalchemy import text
# from core.prompt import build_prompt
# from core.llm import LLMEngine
# from core.memory import MemoryStore


# class ChatEngine:
#     def __init__(self, model_path):
#         self.llm = LLMEngine(model_path)
#         self.memory = MemoryStore()

#     def chat_stream(self, user_id: int, user_input: str):
#         history = self.memory.get_history(user_id)
#         prompt = build_prompt(user_input, history)

#         full_response = ""
#         for token in self.llm.stream(prompt):
#             full_response += token
#             yield token

#         if user_id != 0:  # ignore warm-up
#             self.memory.add(user_id, user_input, full_response.strip())


#     def is_remember_intent(text: str) -> bool:
#         keywords = [
#             "remember this",
#             "remember it",
#             "remember that",
#             "save this",
#             "store this"
#         ]
#         text = text.lower()
#         return any(k in text for k in keywords)


# def extract_fact(text: str):
#     """
#     Example:
#     'my name is aayush remember it'
#     -> ('my name', 'aayush')
#     """
#     text = text.lower()

#     for k in ["remember it", "remember this", "remember that"]:
#         text = text.replace(k, "")

#     if " is " in text:
#         key, value = text.split(" is ", 1)
#         return key.strip(), value.strip()

#     return None, None






from core.llm import LLMEngine
from core.memory import MemoryStore
from core.prompt import build_prompt
from core.fact_store import UserFactStore   # 👈 NEW


class ChatEngine:
    def __init__(self, model_path: str):
        self.llm = LLMEngine(model_path)
        self.memory = MemoryStore()
        self.facts = UserFactStore()   # 👈 user_facts handler

    def chat_stream(self, user_id: int, user_input: str):
        """
        Main streaming chat entrypoint
        """

        # 🔹 1. Check remember intent BEFORE LLM
        if self.is_remember_intent(user_input):
            key, value = self.extract_fact(user_input)

            if key and value:
                self.facts.add_fact(user_id, key, value)

                # Optional: short confirmation without LLM
                yield f"✅ I’ll remember that {key} is {value}.\n"

        # 🔹 2. Build prompt using history + stored facts
        history = self.memory.get_history(user_id)
        facts = self.facts.get_facts(user_id)

        prompt = build_prompt(
            user_input=user_input,
            history=history,
            facts=facts
        )

        # 🔹 3. Stream LLM tokens
        full_response = ""
        for token in self.llm.stream(prompt):
            full_response += token
            yield token

        # 🔹 4. Store chat history (always)
        self.memory.add(user_id, user_input, full_response.strip())

    # -----------------------
    # MEMORY HELPERS
    # -----------------------
    @staticmethod
    def is_remember_intent(text: str) -> bool:
        keywords = [
            "remember this",
            "remember it",
            "remember that",
            "save this",
            "store this"
        ]
        text = text.lower()
        return any(k in text for k in keywords)

    @staticmethod
    def extract_fact(text: str):
        """
        Example:
        'indian team captain is suryakumar yadav remember it'
        → ('indian team captain', 'suryakumar yadav')
        """
        text = text.lower()

        for k in ["remember it", "remember this", "remember that"]:
            text = text.replace(k, "")

        if " is " in text:
            key, value = text.split(" is ", 1)
            return key.strip(), value.strip()

        return None, None
