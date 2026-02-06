import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load data
texts = []
labels = []

with open("data/incidents.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        texts.append(row["text"])
        labels.append(row["category"])

print("Training data loaded:", len(texts), "incidents")

# Convert text to numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train model
model = LogisticRegression()
model.fit(X, labels)

print("Model training completed")

# Test with a new incident
new_incident = ["Application crashes after deployment"]
new_X = vectorizer.transform(new_incident)

prediction = model.predict(new_X)

print("New Incident:", new_incident[0])
print("Predicted Category:", prediction[0])
