from sqlalchemy import Boolean, Column, Integer, String, Long, DateTime, DECIMAL, ForeignKey, Date, TIMESTAMP, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime


Base = declarative_base()

class Test(Base):
    __tablename__ = "tests"

    id = Column(Long, primary_key=True)
    description = Column(String)
    created_at = Column(DateTime)

class MealTypeEnum(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    late_night = "late_night"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    meal_records = relationship("MealRecord", back_populates="user")

class MealRecord(Base):
    __tablename__ = 'meal_records'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    meal_date = Column(Date, nullable=False)
    meal_time = Column(DateTime, nullable=False)
    meal_type = Column(Enum(MealTypeEnum), nullable=False)
    calories = Column(DECIMAL(5, 2), nullable=False)
    protein = Column(DECIMAL(5, 2), nullable=False)
    fat = Column(DECIMAL(5, 2), nullable=False)
    carbs = Column(DECIMAL(5, 2), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="meal_records")
