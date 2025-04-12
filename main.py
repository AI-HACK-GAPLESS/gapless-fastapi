from fastapi import FastAPI
from api import explain

app = FastAPI()
app.include_router(explain.router, prefix="/api")