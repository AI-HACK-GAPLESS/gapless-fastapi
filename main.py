from fastapi import FastAPI
from api import explain, keyword_analytics, document, custom_server, server_dict
from db.db import Base, engine


app = FastAPI()
app.include_router(explain.router, prefix="/api")
app.include_router(keyword_analytics.router, prefix="/api")
app.include_router(document.router, prefix="/api")
app.include_router(server_dict.router, prefix="/api")
app.include_router(custom_server.router, prefix="/api")

Base.metadata.create_all(bind=engine)
