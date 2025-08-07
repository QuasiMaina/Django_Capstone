import json
from pathlib import Path

NARRATIVE_PATH = Path(__file__).resolve().parent / "narrative.json"

def load_narrative():
    with open(NARRATIVE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
