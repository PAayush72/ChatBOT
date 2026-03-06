from db.session import engine
from db.models import ChatMemory, Base

Base.metadata.create_all(bind=engine)
print("Database tables created")
