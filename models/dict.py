from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from db.db import Base


class Dict(Base):
    __tablename__ = 'dicts'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer,
                       ForeignKey('servers.id'), nullable=False)
    keyword = Column(String, nullable=False)
    description = Column(String, nullable=False)

    server = relationship("Server", back_populates="dicts")