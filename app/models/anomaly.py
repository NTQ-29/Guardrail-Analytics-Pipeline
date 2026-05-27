import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "artifacts", "anomaly_detector.pkl")

def train_and_pickle_model():
    """
    Simulates baseline operational history, trains an Isolation Forest model,
    and pickles the binary model to disk.
    """
    print("[MLOps]: Starting training simulation...")
    
    # 1. Generate normal historical data (low tokens, typical latency)
    np.random.seed(42)
    normal_tokens = np.random.normal(loc=50, scale=15, size=200)      # average 50 tokens
    normal_latency = np.random.normal(loc=120, scale=30, size=200)    # average 120 ms
    
    # 2. Add a few historical outliers (malicious/broken behavior)
    outlier_tokens = [2500, 4800, 30, 5200]
    outlier_latency = [4500, 8900, 9500, 12]
    
    # Combine into a clean training dataframe
    tokens = np.concatenate([normal_tokens, outlier_tokens])
    latency = np.concatenate([normal_latency, outlier_latency])
    
    X_train = pd.DataFrame({
        "token_count": tokens,
        "latency_ms": latency
    })
    
    # Force positive values for cleanliness
    X_train = X_train.clip(lower=0)

    # 3. Fit the Isolation Forest model
    # contamination=0.02 means we estimate roughly 2% of historical data is anomalous
    model = IsolationForest(contamination=0.02, random_state=42)
    model.fit(X_train)
    
    # 4. Pickle the model object to a binary file
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
        
    print(f"[MLOps]: Model trained successfully and saved to {MODEL_PATH}")

def score_anomaly(token_count: int, latency_ms: float) -> float:
    """
    Loads the pickled model and generates an anomaly score for a single log instance.
    Returns a normalized float where lower scores signify high abnormality.
    """
    # Defensive programming: If model file doesn't exist, build it immediately
    if not os.path.exists(MODEL_PATH):
        train_and_pickle_model()

    # Load the binary pickle file back into active memory
    with open(MODEL_PATH, "rb") as f:
        loaded_model = pickle.load(f)

    # Format the data point exactly how scikit-learn expects it (2D array)
    data_point = pd.DataFrame([{
        "token_count": token_count,
        "latency_ms": latency_ms
    }])

    # .decision_function returns the raw anomaly score. 
    # Negative values = anomalous, Positive values = normal.
    raw_score = loaded_model.decision_function(data_point)[0]
    
    # Return it directly to the data pipeline
    return float(raw_score)

if __name__ == "__main__":
    # If run standalone (python app/models/anomaly.py), train the model
    train_and_pickle_model()