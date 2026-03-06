
from db.session import SessionLocal
from db.models import ChatMemory, UserFact

class MemoryStore:
    def __init__(self, max_turns=3):
        self.max_turns = max_turns

    def add(self, user_id, user_msg, bot_msg):
        db = SessionLocal()
        db.add(ChatMemory(
            user_id=user_id,
            user_message=user_msg,
            bot_message=bot_msg
        ))
        db.commit()
        db.close()

    def get_history(self, user_id):
        db = SessionLocal()
        messages = (
            db.query(ChatMemory)
            .filter(ChatMemory.user_id == user_id)
            .order_by(ChatMemory.created_at.desc())
            .limit(self.max_turns)
            .all()
        )
        db.close()

        history = ""
        for m in reversed(messages):
            history += f"User: {m.user_message}\n"
            history += f"Assistant: {m.bot_message}\n"
        return history
    
    def save_fact(self, user_id, key, value):
        db = SessionLocal()
        db.add(UserFact(user_id=user_id, key=key, value=value))
        db.commit()
        db.close()

    def get_facts(self, user_id):
        db = SessionLocal()
        facts = db.query(UserFact).filter(UserFact.user_id == user_id).all()
        db.close()

        return {f.key: f.value for f in facts}
