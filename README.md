
### **a secure data engineering pipeline that's focused on AI observations and guardrails 

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


Getting Started (Cloud-Native Execution)
1. Environment Configurations
Create a .env file in the project root to establish your local and cloud credentials safely:

Plaintext
GCP_PROJECT_ID=your_gcp_project_id
GEMINI_API_KEY=your_google_ai_studio_api_key
2. Dependency Resolution
Install the verified framework and SDK requirements into your isolated cloud environment:

Bash
pip install -r requirements.txt
3. Initialize the MLOps Lifecycle
Trigger the machine learning training pipeline to generate simulated historical data, fit the Isolation Forest model, and serialize (pickle) the resulting artifact to disk:

Bash
python app/models/anomaly.py
4. Boot the Production Ingestion Gateway
Launch the underlying asynchronous ASGI web server using Uvicorn:

Bash
uvicorn app.main:app --reload
 Live API Verification Examples
Once the ingestion server is active on port 8000, open a separate terminal pane to run test payloads using curl:

A. Standard Log Processing
Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/logs](http://127.0.0.1:8000/api/v1/logs)" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "usr_dev_1", "prompt": "Write a python function to sort a list.", "response": "Use sorted(list_name)", "token_count": 45, "latency_ms": 110.0}'
Pipeline Action: Classifies the request as CLEAN, calculates a safe positive anomaly score, logs a Pydantic-validated summary via Gemini, saves it to database, and streams the row directly to GCP BigQuery.

B. Real-Time PII Masking
Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/logs](http://127.0.0.1:8000/api/v1/logs)" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "usr_dev_2", "prompt": "Fix code for john.doe@gmail.com using key sk-992", "response": "Done.", "token_count": 60, "latency_ms": 130.0}'
Pipeline Action: Flips the security classification to PII_REDACTED, automatically swapping out sensitive texts for secure tags (<EMAIL>) before committing to analytical storage.

C. System Anomaly Detection
Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/logs](http://127.0.0.1:8000/api/v1/logs)" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "usr_malicious_1", "prompt": "Scrape entire web database...", "response": "Processing...", "token_count": 8500, "latency_ms": 9400.0}'
Pipeline Action: The Isolation Forest detects that token counts and latencies deviate massively from historical metrics, automatically flags the transaction as ANOMALY_DETECTED, and drops the anomaly score below zero.

 Business Intelligence & Aggregation Reports
The system calculates running cost leaks and infrastructure behaviors. To trigger complex relational database analytical evaluations utilizing Python and SQL Window functions, execute the query layer module:

Bash
python -m app.analytics.queries
Analytical Output Preview
Plaintext
============================================================
 ANALYTICS REPORT: System Security Posture & Latency Rollups
============================================================
    security_flag  total_interactions  avg_latency_ms  total_tokens_consumed  volume_percentage
            CLEAN                   2          170.00                    165              50.00
     PII_REDACTED                   1          130.00                     60              25.00
 ANOMALY_DETECTED                   1         9400.00                   8500              25.00

============================================================
 ANALYTICS REPORT: User Usage Costs & Associated Risk Profiles
============================================================
       user_id  total_requests  accumulated_tokens  estimated_cost_usd  avg_ai_risk_score  max_observed_latency_ms
usr_malicious_1               1                8500             0.01275                  4                  9400.00
      usr_dev_1               1                  45             0.00007                  1                   110.00
      usr_dev_2               1                  60             0.00009                  1                   130.00
 Container Deployment Strategy
This project contains a comprehensive production Dockerfile. To containerize the environment for cloud infrastructure like AWS ECS or GCP Cloud Run, execute the following build sequence from the repository root:

Bash
# Build the application image layer
docker build -t guardrail-pipeline:latest .

# Instantiate the container thread locally
docker run -p 8000:8000 --env-file .env guardrail-pipeline:latest

---

Once you've saved this markdown text, execute one final quick push to update your profile:

```bash
git add README.md
git commit -m "docs: complete production-grade README documentation"
git push origin main
│   ├── security/
│   │   └── pii.py         # Microsoft Presidio PII sanitizer & prompt injection engine
│   └── main.py            # Main ASGI pipeline execution controller
├── Dockerfile             # Multi-stage production container configuration
├── requirements.txt       # Unified project dependency manifesto
└── README.md              # Master project documentation
