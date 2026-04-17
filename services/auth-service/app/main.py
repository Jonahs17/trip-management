from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.db.database import Base, engine
from sqlalchemy.exc import OperationalError
import time

app = FastAPI()

def init_db():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("DB connected and tables created")
            return
        except OperationalError:
            print("Waiting for DB...")
            time.sleep(2)
        
    print("Could not connect to DB after retries")

init_db()

app.include_router(auth_router)