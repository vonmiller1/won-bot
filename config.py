"""
Configuration module for Gemma Medical Scribe
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

MODEL_NAME = os.getenv("MODEL_NAME", "gemma4:e4b")
MODEL_VERSION = "4.0.0"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

TESSERACT_CMD = os.getenv("TESSERACT_CMD", "tesseract")
TESSERACT_LANG = os.getenv("TESSERACT_LANG", "eng")

STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")

MEDICAL_DB_PATH = BASE_DIR / "data" / "medical_terms.json"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

SYSTEM_PROMPT = """You are a professional medical scribe. Structure notes clearly 
and flag any urgent findings. Always maintain patient confidentiality."""

SOAP_TEMPLATE = """
SUBJECTIVE:
{subjective}

OBJECTIVE:
{objective}

ASSESSMENT:
{assessment}

PLAN:
{plan}
"""
