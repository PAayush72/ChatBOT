SYSTEM_PROMPT = """You are a helpful, concise AI assistant.
Answer clearly and accurately.
"""

def build_prompt(user_input, history="", facts=None):
    facts_text = ""
    if facts:
        facts_text = "User Facts (ALWAYS TRUE):\n"
        for k, v in facts.items():
            facts_text += f"- {k}: {v}\n"

    return f"""
You are a local AI assistant.
If user facts are provided, they OVERRIDE your training data.

{facts_text}

Conversation History:
{history}

User: {user_input}
Assistant:
"""
