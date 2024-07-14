from sqlalchemy import Column, Integer, String, BigInteger, DateTime, DECIMAL, ForeignKey, Date, TIMESTAMP, Enum as SQLEnum
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum
from datetime import datetime


Base = declarative_base()

class Test(Base):
    __tablename__ = "tests"

    id = Column(BigInteger, primary_key=True)
    description = Column(String(256))
    created_at = Column(DateTime)

class SNSType(str, Enum):
    KAKAO = "kakao"
    GOOGLE = "google"

class GenderEnum(Enum):
    male = "male"
    female = "female"
    other = "other"

class ActivityLevelEnum(Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"

class MealTypeEnum(Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    late_night = "late_night"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    sns_type = Column(SQLEnum(SNSType), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    profile_image_url = Column(String(256))
    age = Column(Integer)
    gender = Column(SQLEnum(GenderEnum))
    height_cm = Column(DECIMAL(5, 2))
    weight_kg = Column(DECIMAL(5, 2))
    activity_level = Column(SQLEnum(ActivityLevelEnum))
    daily_calorie_goal = Column(Integer)
    daily_protein_goal = Column(DECIMAL(5, 2))
    daily_fat_goal = Column(DECIMAL(5, 2))
    daily_carb_goal = Column(DECIMAL(5, 2))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    meal_records = relationship("MealRecord", back_populates="user")

class MealRecord(Base):
    __tablename__ = "meal_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    meal_date = Column(Date, nullable=False)
    meal_time = Column(DateTime, nullable=False)
    meal_type = Column(SQLEnum(MealTypeEnum), nullable=False)
    calories = Column(DECIMAL(5, 2), nullable=False)
    protein = Column(DECIMAL(5, 2), nullable=False)
    fat = Column(DECIMAL(5, 2), nullable=False)
    carbs = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="meal_records")
