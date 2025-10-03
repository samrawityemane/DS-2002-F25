import csv
import json
from pathlib import Path
import pandas as pd

BASE = Path(".")

raw_csv_path = BASE / "raw_survey_data.csv"

rows = [
    [1001, "Computer Science", 2.9, "Yes", "16.0"],
    [1002, "Economics", 3.5, "No", "14.5"],
    [1003, "Chemistry", 3, "No", "10.5"],
    [1004, "Statistics", 3.92, "No", "18"],
    [1005, "Cognitive Science", 3, "No", "20.0"],
]

with raw_csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "major", "GPA", "is_cs_major", "credits_taken"])
    writer.writerows(rows)

print(f"Wrote {raw_csv_path.name}")

raw_json_path = BASE / "raw_course_catalog.json"

courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 2000,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "CS3205",
        "section": "001",
        "title": "HCI in Software Development",
        "level": 3000,
        "instructors": [
            {"name": "Panagiotis Apostolellis", "role": "Primary"}
        ]
    },
    {
        "course_id": "DRAM1020",
        "section": "002",
        "title": "Speaking in Public",
        "level": 1000,
        "instructors": [
            {"name": "Tovah Close", "role": "Primary"}
        ]
    },
    {
        "course_id": "CS3140",
        "section": "002",
        "title": "Software Development Essentials",
        "level": 3000,
        "instructors": [
            {"name": "Rich Nguyen", "role": "Primary"}
        ]
    },
    {
        "course_id": "CS3120",
        "section": "002",
        "title": "Discrete Math and Theory 2",
        "level": 3000,
        "instructors": [
            {"name": "Ray Pettit", "role": "Primary"}
        ]
    },
    {
        "course_id": "PSYC2150",
        "section": "001",
        "title": "Introduction to Cognition",
        "level": 2000,
        "instructors": [
            {"name": "Mariana Teles", "role": "Primary"}
        ]
    }
]

with raw_json_path.open("w", encoding="utf-8") as f:
    json.dump(courses, f, indent=2)

print(f"Wrote {raw_json_path.name}")

df = pd.read_csv(raw_csv_path)

bool_map = {"Yes": True, "No": False, "yes": True, "no": False, True: True, False: False}
df["is_cs_major"] = df["is_cs_major"].map(bool_map)

df = df.astype({"GPA": "float64"})
df["credits_taken"] = df["credits_taken"].astype("float64")

clean_csv_path = BASE / "clean_survey_data.csv"
df.to_csv(clean_csv_path, index=False)
print(f"Wrote {clean_csv_path.name}")

with raw_json_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

normalized = pd.json_normalize(
    data,
    record_path=["instructors"],
    meta=["course_id", "title", "level", "section"],
    errors="ignore"
)

clean_json_csv_path = BASE / "clean_course_catalog.csv"
normalized.to_csv(clean_json_csv_path, index=False)
print(f"Wrote {clean_json_csv_path.name}")

print("\nDone. Generated:")
print(" - raw_survey_data.csv")
print(" - raw_course_catalog.json")
print(" - clean_survey_data.csv")
print(" - clean_course_catalog.csv")