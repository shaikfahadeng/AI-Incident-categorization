from app import metrics
import threading
from app.sre_monitor import monitor
from prometheus_fastapi_instrumentator import Instrumentator
import csv
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = FastAPI(title="AI Incident Categorization API")
Instrumentator().instrument(app).expose(app)
from pydantic import BaseModel
# Load training data
texts = []
labels = []

with open("data/incidents.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        texts.append(row["text"])
        labels.append(row["category"])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

class Incident(BaseModel):
    text: str
class ServiceNowTicket(BaseModel):
    number: str
    short_description: str
    description: str
    priority: str
# UPDATED CLASSIFIER WITH CONFIDENCE + DECISION
@app.post("/classify")
def classify_incident(incident: Incident):
    metrics.TOTAL_REQUESTS += 1

    try:
        X_new = vectorizer.transform([incident.text])
        prediction = model.predict(X_new)[0]
        return {"category": prediction}

    except Exception as e:
        metrics.FAILED_REQUESTS += 1
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "model_loaded": True
    }
@app.post("/ingest/servicenow")
def ingest_servicenow(ticket: ServiceNowTicket):
    combined_text = f"{ticket.short_description} {ticket.description}"

    X_new = vectorizer.transform([combined_text])
    prediction = model.predict(X_new)[0]
    confidence = max(model.predict_proba(X_new)[0])

    decision = "AUTO-CATEGORIZED"
    if confidence < 0.65:
        decision = "MANUAL_REVIEW_REQUIRED"

    return {
        "ticket_number": ticket.number,
        "predicted_category": prediction,
        "confidence": round(confidence, 2),
        "decision": decision,
        "priority": ticket.priority
    }
threading.Thread(target=monitor, daemon=True).start()
def slo_status():
    if metrics.TOTAL_REQUESTS == 0:
        return {
            "status": "NO DATA",
            "success_rate": 1.0,
            "error_budget_remaining": 1.0
        }

    success_rate = (metrics.TOTAL_REQUESTS - metrics.FAILED_REQUESTS) / metrics.TOTAL_REQUESTS
    error_budget = 1 - metrics.SLO_TARGET
    error_budget_used = max(0, metrics.SLO_TARGET - success_rate)
    error_budget_remaining = max(0, error_budget - error_budget_used)

    return {
        "status": "SLO BREACHED" if success_rate < metrics.SLO_TARGET else "SLO OK",
        "success_rate": round(success_rate, 4),
        "error_budget_remaining": round(error_budget_remaining, 4)
    }
@app.get("/slo")
def get_slo_status():
    return slo_status()
