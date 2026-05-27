
### a secure data engineering pipeline that's focused on AI observations and guardrails 

# GuardRail Analytics Pipeline

An intelligent, secure, enterprise-grade data engineering and observability pipeline designed to ingest, sanitize, score, and store Large Language Model (LLM) interaction logs at scale. 

This project unifies **Data Engineering, MLOps, LLMOps, Cloud Security, and Data Analytics** into a singular, highly cohesive cloud-native ecosystem.

---

## Architecture Overview

The pipeline acts as a secure proxy and analytical engine for enterprise AI logging:

1. **Secure Ingestion Engine (Data Engineering & FastAPI):** Streamlines application event traffic and runs rigid input validation using Pydantic data schemas.
2. **Threat & Privacy Perimeter (Cloud Security):** Employs Microsoft Presidio NLP engines to dynamically mask PII (Emails, API Keys, SSNs) and implements behavioral signature matching to intercept Prompt Injection attacks.
3. **Machine Learning Inference (MLOps):** Scores numerical system telemetry (latency spikes, token volume anomalies) on the fly using an offline-trained, serialized **Isolation Forest** model.
4. **Cognitive Enrichment (LLMOps):** Routes sanitized logs to the **Google Gemini API**, enforcing deterministic, structured JSON schema outputs to classify user intent.
5. **Analytical Storage (SQL & Data Analytics):** Commits transactions to a local relational database using SQLAlchemy ORM class mapping while simultaneously streaming structured payloads straight into **GCP BigQuery** for massive parallel data warehousing analysis.

---

## Tech Stack & Frameworks

* **Core Runtime:** Python 3.11
* **API Framework:** FastAPI, Uvicorn, Pydantic
* **Data Integration:** SQLAlchemy, PostgreSQL/SQLite
* **Cybersecurity:** Microsoft Presidio Analyzer & Anonymizer Suite
* **Machine Learning & MLOps:** Scikit-Learn (Isolation Forest), Pandas, NumPy, Pickle
* **LLM Orchestration:** Google GenAI SDK (Structured JSON Outputs, Pydantic Validation)
* **Cloud Warehouse:** Google Cloud Platform (GCP) BigQuery
* **DevOps / Containerization:** Docker, GitHub Codespaces

---

## Project Structure

```text
guardrail-analytics-pipeline/
├── app/
│   ├── analytics/
│   │   ├── bigquery.py    # GCP Cloud Warehouse streaming client
│   │   ├── models.py      # SQLAlchemy relational DDL database models
│   │   └── queries.py     # Advanced SQL analytical reports & window functions
│   ├── api/
│   │   └── routes.py      # Core routing logic split endpoints
│   ├── core/
│   │   ├── config.py      # Dynamic environment variable loader
│   │   └── llmops.py      # Google Gemini cloud client & JSON structural schema
│   ├── models/
│   │   ├── artifacts/     # Storage for serialized binary model (.pkl) files
│   │   └── anomaly.py     # Isolation forest training and scoring wrapper
│   ├── security/
│   │   └── pii.py         # Microsoft Presidio PII sanitizer & prompt injection engine
│   └── main.py            # Main ASGI pipeline execution controller
├── Dockerfile             # Multi-stage production container configuration
├── requirements.txt       # Unified project dependency manifesto
└── README.md              # Master project documentation
