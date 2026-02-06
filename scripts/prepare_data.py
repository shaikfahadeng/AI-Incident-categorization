import csv

texts = []
labels = []

with open("data/incidents.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        texts.append(row["text"])
        labels.append(row["category"])

print("Sample incident text:", texts[0])
print("Corresponding category:", labels[0])
print("Total incidents loaded:", len(texts))
