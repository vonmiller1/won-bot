"""
Utility functions for Gemma Medical Scribe
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


def load_medical_database(path: Path) -> Dict[str, str]:
    """Load medical terms database from JSON file."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_medical_terms(text: str) -> List[str]:
    """Extract potential medical terms from input text."""
    pattern = r"\b(?:dyspnea|tachycardia|hypertension|bradycardia|edema|"
    pattern += r"arrhythmia|hypotension|fever|nausea|vomiting|diarrhea|"
    pattern += r"constipation|headache|dizziness|fatigue|insomnia|anemia|"
    pattern += r"pneumonia|bronchitis|asthma|copd|diabetes|seizure|stroke)\b"
    matches = re.findall(pattern, text.lower())
    return list(set(matches))


def format_soap_note(subjective: str, objective: str, assessment: str, plan: str) -> str:
    """Format a SOAP note from components."""
    return f"""
SUBJECTIVE:
{subjective}

OBJECTIVE:
{objective}

ASSESSMENT:
{assessment}

PLAN:
{plan}
""".strip()


def sanitize_input(text: str) -> str:
    """Sanitize user input by removing potentially harmful characters."""
    text = re.sub(r"[<>{}]", "", text)
    return text.strip()


def validate_patient_id(patient_id: str) -> bool:
    """Validate patient ID format (alphanumeric, 4-20 chars)."""
    pattern = r"^[A-Za-z0-9]{4,20}$"
    return bool(re.match(pattern, patient_id))


def chunk_text(text: str, max_length: int = 2000) -> List[str]:
    """Split text into chunks for processing."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
