
# AI-Based Village Health Triage Agent

## Description
This tool supports ASHA/ANM workers in Indian villages to make informed health triage decisions using a basic AI model.

## Features
- 📋 Rule-based logic for healthcare triage
- 🔤 Optional basic NLP keyword extraction from symptom text
- 🌐 Easy-to-use **Streamlit GUI**
- 🚑 Suggests next steps:
  - "Give ORS"
  - "Refer to doctor"
  - "Monitor at home"

## How to Run

### Option 1: CLI (Command Line)
```bash
python triage_agent.py
python nlp_summary.py
```

### Option 2: GUI (Recommended)
Make sure `streamlit` is installed:
```bash
pip install streamlit
```

Then run the app:
```bash
streamlit run app.py
```

## SDG Alignment
Aligned with **SDG 3 – Good Health and Well-being**, enabling rural health workers with decision support tools.

---
