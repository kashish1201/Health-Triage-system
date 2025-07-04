# nlp_summary.py
import re
import spacy

nlp = spacy.load("en_core_web_sm")

SYMPTOM_SYNONYMS = {
    "fever": ["temperature", "feverish", "hot", "high temp", "body heat"],
    "cough": ["dry cough", "wet cough", "coughing"],
    "cold": ["runny nose", "nasal", "sneeze"],
    "vomiting": ["nausea", "throwing up", "puke", "retching"],
    "diarrhea": ["loose motion", "frequent stools", "watery stool"],
    "dehydration": ["dry mouth", "less urine", "very thirsty", "sunken eyes"],
    "rash": ["red spots", "itchy", "skin rash", "bumps"],
    "headache": ["migraine", "head pain"],
    "fatigue": ["tired", "no energy", "lethargic"],
    "body pain": ["body ache", "joint pain"],
    "breathing difficulty": ["shortness of breath", "can't breathe"],
    "dizziness": ["lightheaded", "giddy"],
    "unconscious": ["fainted", "not responding"],
    "chest pain": ["tight chest", "heart pain"],
    "abdominal pain": ["stomach ache", "cramps"],
    "sore throat": ["throat pain", "irritated throat"],
    "burning sensation": ["burning while urinating", "burning skin"],
    "back pain": ["lower back pain", "upper back ache"],
    "urine issues": ["painful urination", "frequent urination", "less urine"],
    "eye redness": ["red eye", "itchy eyes"],
    "ear pain": ["earache", "pain in ear"]
}

REVERSE_SYMPTOM_MAP = {}
for canonical, variants in SYMPTOM_SYNONYMS.items():
    for variant in variants:
        REVERSE_SYMPTOM_MAP[variant] = canonical
    REVERSE_SYMPTOM_MAP[canonical] = canonical

# 🔍 Patterns for severity & duration
SEVERITY_WORDS = ["mild", "moderate", "severe", "high", "intense","low"]
DURATION_PATTERNS = [
    r"\bfor (\d+ days?)\b",
    r"\bsince (yesterday|last night|this morning)\b",
    r"\bfor (a week|two days|three days)\b"
]

def extract_symptoms(text):
    text = text.lower()
    doc = nlp(text)
    detected_symptoms = set()
    detected_severity = None
    detected_duration = None

    # 1. Symptom matching
    for phrase, mapped_symptom in REVERSE_SYMPTOM_MAP.items():
        if phrase in text:
            detected_symptoms.add(mapped_symptom)

    # 2. Severity detection
    for word in doc:
        if word.text in SEVERITY_WORDS:
            detected_severity = word.text
            break

    # 3. Duration detection
    for pattern in DURATION_PATTERNS:
        match = re.search(pattern, text)
        if match:
            detected_duration = match.group(1)
            break

    return {
        "symptoms": list(detected_symptoms) if detected_symptoms else ["unknown"],
        "severity": detected_severity or "unspecified",
        "duration": detected_duration or "unspecified"
    }
