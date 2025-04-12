# models/slack.py
from sqlalchemy import Column, Integer, String
from db.db import Base

class SlackKeyword(Base):
    __tablename__ = "slack_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True)
    count = Column(Integer, default=1)
