from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, silhouette_score
import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'wallet_score_model.joblib')

# Load the model once at module import
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

def train_fraud_detection_model(data):
    X = data.drop('is_fraud', axis=1)
    y = data['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return model

def cluster_wallets(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(data)
    
    silhouette_avg = silhouette_score(data.drop('cluster', axis=1), data['cluster'])
    print(f'Silhouette Score: {silhouette_avg}')
    
    return kmeans

def evaluate_credit_scoring_model(model, data):
    X = data.drop('credit_score', axis=1)
    y = data['credit_score']
    
    y_pred = model.predict(X)
    print(classification_report(y, y_pred))
    
    return y_pred

def extract_features(wallet_address: str) -> pd.Series:
    # TODO: Implement real feature extraction from blockchain data
    # For now, raise NotImplementedError to force implementation
    raise NotImplementedError("Feature extraction not implemented yet.")

def get_wallet_score(wallet_address: str):
    if model is None:
        raise RuntimeError("ML model not loaded.")
    features = extract_features(wallet_address)
    score = model.predict([features])[0]
    return score

def detect_fraud(wallet_address: str):
    if model is None:
        raise RuntimeError("ML model not loaded.")
    features = extract_features(wallet_address)
    prediction = model.predict([features])[0]
    return bool(prediction)

def analyze_user_patterns(wallet_address: str):
    # TODO: Implement real user pattern analysis
    raise NotImplementedError("User pattern analysis not implemented yet.")