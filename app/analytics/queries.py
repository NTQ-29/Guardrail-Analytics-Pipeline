import pandas as pd
from sqlalchemy import text
from app.analytics.models import engine

def run_analytical_query(query_string: str, description: str):
    """
    Executes a raw SQL analytical query against the database 
    and prints the output as a beautiful structured DataFrame.
    """
    print("\n" + "="*60)
    print(f"📊 ANALYTICS REPORT: {description}")
    print("="*60)
    
    # Establish a connection and read the SQL execution results directly into Pandas
    with engine.connect() as connection:
        df = pd.read_sql_query(text(query_string), connection)
        
    if df.empty:
        print("No log data found matching this analytical criteria yet.")
    else:
        print(df.to_string(index=False))

# --- SENIOR-LEVEL SQL QUERY BUFFET ---

# Query 1: Security Risk Rollups using Conditional Aggregations (CASE WHEN)
security_summary_sql = """
SELECT 
    security_flag,
    COUNT(*) as total_interactions,
    ROUND(AVG(latency_ms), 2) as avg_latency_ms,
    SUM(token_count) as total_tokens_consumed,
    -- Senior metric: What percentage of total volume does this security category represent?
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM llm_interaction_logs), 2) as volume_percentage
FROM llm_interaction_logs
GROUP BY security_flag;
"""

# Query 2: Cost & Usage Analytics by User using Aggregate Windows & Metrics
user_cost_sql = """
SELECT 
    user_id,
    COUNT(*) as total_requests,
    SUM(token_count) as accumulated_tokens,
    -- Simulating an enterprise cost metric: $0.0015 per 1,000 input/output tokens
    ROUND(SUM(token_count) * (0.0015 / 1000.0), 5) as estimated_cost_usd,
    AVG(risk_score_out_of_ten) as avg_ai_risk_score,
    MAX(latency_ms) as max_observed_latency_ms
FROM llm_interaction_logs
GROUP BY user_id
ORDER BY estimated_cost_usd DESC;
"""

# Query 3: Deep Context Analysis (Intent Analysis)
intent_distribution_sql = """
SELECT 
    COALESCE(intent_category, 'Unclassified') as intent,
    COUNT(*) as application_count,
    ROUND(AVG(token_count), 1) as avg_tokens_per_intent,
    -- Calculate a running total of tokens within this aggregation
    SUM(SUM(token_count)) OVER (ORDER BY COUNT(*) DESC) as cumulative_token_running_total
FROM llm_interaction_logs
GROUP BY intent_category
ORDER BY application_count DESC;
"""

if __name__ == "__main__":
    # Execute the SQL scripts to pull data definitions and rollups
    run_analytical_query(security_summary_sql, "System Security Posture & Latency Rollups")
    run_analytical_query(user_cost_sql, "User Usage Costs & Associated Risk Profiles")
    run_analytical_query(intent_distribution_sql, "LLMOps Intent Analysis & Cumulative Token Distribution")