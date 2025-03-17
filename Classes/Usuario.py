import pytz

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "User"

    id = Column("userId", Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column("userEmail", String, nullable=False, unique=True)
    username = Column("userName", String, nullable=False, unique=True)
    senha = Column("userSenha", String, nullable=False)
    userCreateTime = Column("userCreateTime", DateTime, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')))

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
