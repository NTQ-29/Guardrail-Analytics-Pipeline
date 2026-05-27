import os
from dotenv import load_dotenv

load_dotenv()

# If a real POSTGRES_URL environment variable is set up in .env, use it. 
# Otherwise, fall back to a local, lightweight SQLite file for development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./guardrail_logs.db")