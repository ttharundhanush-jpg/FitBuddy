import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'fitbuddy.db')}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)


class WorkoutPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if user:
            user.name, user.age, user.weight = name, age, weight
            user.goal, user.intensity = goal, intensity
        else:
            db.add(User(id=user_id, name=name, age=age, weight=weight, goal=goal, intensity=intensity))
        db.commit()
    finally:
        db.close()


def save_plan(user_id: int, plan: str, tip: str = ""):
    """Store a fresh plan; replaces any earlier plan (and its update) for this user."""
    db = SessionLocal()
    try:
        row = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if row:
            row.original_plan, row.updated_plan, row.nutrition_tip = plan, None, tip
        else:
            db.add(WorkoutPlan(user_id=user_id, original_plan=plan, nutrition_tip=tip))
        db.commit()
    finally:
        db.close()


def get_user(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter_by(id=user_id).first()
    finally:
        db.close()


def get_plan(user_id: int):
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    finally:
        db.close()


def update_plan(user_id: int, updated: str):
    db = SessionLocal()
    try:
        row = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if row:
            row.updated_plan = updated
            db.commit()
    finally:
        db.close()


def get_all_users():
    db = SessionLocal()
    try:
        return db.query(User).order_by(User.id).all()
    finally:
        db.close()


def get_all_plans():
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).all()
    finally:
        db.close()
