import json
import psycopg2
from psycopg2.extras import RealDictCursor

fixture_path = "game/fixtures/initial_questions.json"

# Connect to Postgres
conn = psycopg2.connect(
    dbname="anxiety_db",
    user="postgres",
    password="your_password",  # <-- change to your real password
    host="localhost",
    port=5432
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Fetch all questions (ID + text)
cursor.execute("SELECT id, text FROM game_question;")
questions = cursor.fetchall()

# Create a map of question text -> UUID
question_map = {q["text"].strip().lower(): str(q["id"]) for q in questions}

# Load fixture
with open(fixture_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Clean and fix references
for obj in data:
    if "fields" in obj:
        # Remove disorder_type
        # obj["fields"].pop("disorder_type", None)

        # Fix question_id
        if "question_id" in obj["fields"]:
            original_id = obj["fields"]["question_id"]
            question_text = obj["fields"].get("question_text", "").strip().lower()

            if question_text in question_map:
                obj["fields"]["question_id"] = question_map[question_text]
            else:
                print(f"⚠ No match found for question: {question_text}")
                obj["fields"]["question_id"] = None  # or placeholder

# Save cleaned fixture
with open(fixture_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Fixture cleaned & question_id linked to real DB UUIDs.")

cursor.close()
conn.close()
