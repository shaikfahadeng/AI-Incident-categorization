import csv
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load and train model (simple & local)
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

# FastAPI app
app = FastAPI(title="AI Incident Categorization API")

class Incident(BaseModel):
    text: str

@app.post("/classify")
def classify_incident(incident: Incident):
    X_new = vectorizer.transform([incident.text])
    prediction = model.predict(X_new)
    return {"category": prediction[0]}
