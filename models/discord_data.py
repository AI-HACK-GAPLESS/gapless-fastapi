# models/discord.py
from sqlalchemy import Column, Integer, String
from db.db import Base
class DiscordKeyword(Base):
    __tablename__ = "discord_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True)
    count = Column(Integer, default=1)
