from fastapi import FastAPI, status, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session

from app.security.pii import PIISecurityScanner
from app.analytics.models import init_db, SessionLocal, LLMInteractionLog
from app.models.anomaly import score_anomaly
from app.core.llmops import LLMOpsAnalyzer

app = FastAPI(
    title="GuardRail Analytics Pipeline",
    description="Intelligent, Secure Ingestion Engine for LLMOps Insights",
    version="3.0.0"
)

init_db()
security_scanner = PIISecurityScanner()
llmops_analyzer = LLMOpsAnalyzer()

class LLMLogInput(BaseModel):
    user_id: str
    prompt: str
    response: str
    token_count: int
    latency_ms: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "online", "system": "Security, MLOps, & LLMOps Engine Fully Integrated"}

@app.post("/api/v1/logs", status_code=status.HTTP_201_CREATED)
def ingest_llm_log(log_data: LLMLogInput, db: Session = Depends(get_db)):
    
    # 1. Cybersecurity Check
    if security_scanner.detect_prompt_injection(log_data.prompt):
        return {
            "status": "rejected",
            "reason": "Security Policy Violation: Suspected Prompt Injection Attack",
            "timestamp": datetime.utcnow().isoformat()
        }

    # 2. Privacy Masking Layer
    safe_prompt = security_scanner.sanitize_text(log_data.prompt)
    safe_response = security_scanner.sanitize_text(log_data.response)
    
    # 3. MLOps Layer (Local Isolation Forest)
    ml_anomaly_score = score_anomaly(log_data.token_count, log_data.latency_ms)
    
    if safe_prompt != log_data.prompt:
        flag = "PII_REDACTED"
    elif ml_anomaly_score < 0:
        flag = "ANOMALY_DETECTED"
    else:
        flag = "CLEAN"

    # 4. LLMOps Layer (Cloud Gemini Context Enrichment)
    # This calls the cloud, extracts structured data, and parses it automatically
    llm_insights = llmops_analyzer.analyze_log_context(safe_prompt)

    # 5. Data Engineering DB Mapping
    db_log = LLMInteractionLog(
        user_id=log_data.user_id,
        original_prompt=log_data.prompt,
        sanitized_prompt=safe_prompt,
        sanitized_response=safe_response,
        token_count=log_data.token_count,
        latency_ms=log_data.latency_ms,
        security_flag=flag,
        
        # Mapping our structured AI insights to real SQL columns
        intent_category=llm_insights.get("intent_category"),
        risk_score_out_of_ten=llm_insights.get("risk_score_out_of_ten"),
        summary=llm_insights.get("summary"),
        
        processed_at=datetime.utcnow()
    )

    # 6. Database Commit Transaction
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return {
        "status": "success",
        "generated_id": db_log.id,
        "security_classification": flag,
        "ai_insights": llm_insights,
        "metrics": {
            "calculated_anomaly_score": round(ml_anomaly_score, 4)
        }
    }