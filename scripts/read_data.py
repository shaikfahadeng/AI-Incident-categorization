import csv

print("Reading incident dataset...")

with open("data/incidents.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print("Incident:", row["text"], "| Category:", row["category"])
