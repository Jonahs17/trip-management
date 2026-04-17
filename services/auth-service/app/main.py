from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


@app.on_event("startup")
def on_startup():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)