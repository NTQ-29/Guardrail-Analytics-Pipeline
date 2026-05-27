from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.core.config import DATABASE_URL

# Base class that our SQL tables will inherit from
Base = declarative_base()

class LLMInteractionLog(Base):
    """
    DDL Schema representation for our centralized analytical log table.
    """
    __tablename__ = "llm_interaction_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    original_prompt = Column(String, nullable=False)
    sanitized_prompt = Column(String, nullable=False)
    sanitized_response = Column(String, nullable=False)
    token_count = Column(Integer, nullable=False)
    latency_ms = Column(Float, nullable=False)
    security_flag = Column(String, index=True, nullable=False)
    
    # NEW LLMOps Analytical Fields
    intent_category = Column(String, nullable=True)
    risk_score_out_of_ten = Column(Integer, nullable=True)
    summary = Column(String, nullable=True)

    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

# Core database engine setup
# (check_same_thread configuration is only needed for local SQLite safety)
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a session factory used to execute transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Executes the underlying DDL commands (CREATE TABLE) if they do not exist.
    """
    Base.metadata.create_all(bind=engine)