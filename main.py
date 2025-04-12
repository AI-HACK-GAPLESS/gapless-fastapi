from fastapi import FastAPI
from api import explain
from db.db import Base, engine

app = FastAPI()
app.include_router(explain.router, prefix="/api")

Base.metadata.create_all(bind=engine)
