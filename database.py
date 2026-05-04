from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, extract
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

class Admin(Base):
    __tablename__ = 'admins'
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    tags = Column(Text)
    expenses = relationship("Expense", back_populates="category_rel")

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    message_date = Column(DateTime(timezone=True))
    amount = Column(BigInteger)
    currency = Column(String(10))
    raw_text = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category_rel = relationship("Category", back_populates="expenses")

def init_db():
    Base.metadata.create_all(engine)
