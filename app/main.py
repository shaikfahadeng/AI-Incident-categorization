# imports
import csv
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# data loading + model training
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

# FastAPI app MUST be here
app = FastAPI(title="AI Incident Categorization API")

# request model
class Incident(BaseModel):
    text: str

# classify endpoint
@app.post("/classify")
def classify_incident(incident: Incident):
    X_new = vectorizer.transform([incident.text])
    prediction = model.predict(X_new)[0]
    return {"category": prediction}

# health endpoint (IMPORTANT: must be AFTER app definition)
@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "model_loaded": True
    }
