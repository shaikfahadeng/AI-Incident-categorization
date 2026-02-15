from prometheus_fastapi_instrumentator import Instrumentator
app = FastAPI(title="AI Incident Categorization API")
Instrumentator().instrument(app).expose(app)
import csv
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

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

app = FastAPI(title="AI Incident Categorization API")

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
    X_new = vectorizer.transform([incident.text])

    prediction = model.predict(X_new)[0]
    confidence = max(model.predict_proba(X_new)[0])

    decision = "AUTO-CATEGORIZED"
    if confidence < 0.65:
        decision = "MANUAL_REVIEW_REQUIRED"

    return {
        "category": prediction,
        "confidence": round(confidence, 2),
        "decision": decision
    }

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

