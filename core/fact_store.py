from db.session import SessionLocal
from db.models import UserFact


class UserFactStore:
    def add_fact(self, user_id: int, key: str, value: str):
        db = SessionLocal()
        try:
            fact = UserFact(
                user_id=user_id,
                fact_key=key,
                fact_value=value
            )
            db.add(fact)
            db.commit()
        finally:
            db.close()

    def get_facts(self, user_id: int):
        db = SessionLocal()
        try:
            rows = (
                db.query(UserFact)
                .filter(UserFact.user_id == user_id)
                .all()
            )
            return {r.fact_key: r.fact_value for r in rows}
        finally:
            db.close()
