"""
Unit tests for Gemma Medical Scribe
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    extract_medical_terms,
    format_soap_note,
    sanitize_input,
    validate_patient_id,
    chunk_text,
)
from scribe_agent import medical_lookup, run_agent


class TestMedicalLookup:
    def test_known_term(self):
        result = medical_lookup("dyspnea")
        assert "Difficult or labored breathing" in result

    def test_unknown_term(self):
        result = medical_lookup("xyzunknown")
        assert "Retrieved from local medical database" in result

    def test_case_insensitive(self):
        result = medical_lookup("DYSPNEA")
        assert "Difficult or labored breathing" in result


class TestExtractMedicalTerms:
    def test_single_term(self):
        text = "Patient presents with dyspnea on exertion."
        terms = extract_medical_terms(text)
        assert "dyspnea" in terms

    def test_multiple_terms(self):
        text = "Patient has tachycardia and hypertension with mild edema."
        terms = extract_medical_terms(text)
        assert "tachycardia" in terms
        assert "hypertension" in terms
        assert "edema" in terms

    def test_no_terms(self):
        text = "The weather is nice today."
        terms = extract_medical_terms(text)
        assert len(terms) == 0


class TestFormatSoapNote:
    def test_complete_note(self):
        note = format_soap_note(
            subjective="Patient reports chest pain",
            objective="BP 140/90, HR 92",
            assessment="Possible angina",
            plan="ECG, cardiology consult",
        )
        assert "SUBJECTIVE:" in note
        assert "OBJECTIVE:" in note
        assert "ASSESSMENT:" in note
        assert "PLAN:" in note
        assert "chest pain" in note


class TestSanitizeInput:
    def test_removes_html_tags(self):
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result

    def test_preserves_normal_text(self):
        result = sanitize_input("Patient has fever and cough")
        assert result == "Patient has fever and cough"


class TestValidatePatientId:
    def test_valid_id(self):
        assert validate_patient_id("PT12345") is True

    def test_too_short(self):
        assert validate_patient_id("PT1") is False

    def test_special_chars(self):
        assert validate_patient_id("PT-123") is False


class TestChunkText:
    def test_short_text(self):
        result = chunk_text("Short text", max_length=100)
        assert len(result) == 1

    def test_long_text(self):
        long_text = "word " * 500
        result = chunk_text(long_text, max_length=100)
        assert len(result) > 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
