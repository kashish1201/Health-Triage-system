import datetime
import csv
import os

# Risk scoring system
SYMPTOM_WEIGHTS = {
    "fever": 1,
    "rash": 2,
    "cough": 1,
    "cold": 1,
    "vomiting": 2,
    "dehydration": 2,
    "diarrhea": 2,
    "breathing difficulty": 4,
    "weakness": 1,
    "body pain": 1,
    "unconscious": 5
}

# Risk scoring function (symptoms + new params)
def calculate_risk(symptoms, duration=0, fever_severity="Low"):
    base_score = sum(SYMPTOM_WEIGHTS.get(sym.lower().strip(), 0) for sym in symptoms)

    # Add modifiers
    if duration >= 3:
        base_score += 2
    elif duration == 2:
        base_score += 1

    if "fever" in [s.lower().strip() for s in symptoms]:
        if fever_severity == "High":
            base_score += 2
        elif fever_severity == "Medium":
            base_score += 1

    # Risk level
    if base_score >= 7:
        level = "🔴 High"
    elif base_score >= 4:
        level = "🟡 Moderate"
    else:
        level = "🟢 Low"
    return base_score, level

# Enhanced triage logic
def get_triage_decision(symptoms, duration=0, fever_severity="Low"):
    symptoms = [s.lower().strip() for s in symptoms]
    symptom_set = set(symptoms)

    # Priority emergency cases
    if 'breathing difficulty' in symptom_set or 'unconscious' in symptom_set:
        return "🚨 Emergency! Refer to doctor immediately"

    # High-risk combinations
    if 'fever' in symptom_set and 'rash' in symptom_set:
        return "Refer to doctor (Possible dengue/measles)"
    if 'vomiting' in symptom_set and 'diarrhea' in symptom_set and 'dehydration' in symptom_set:
        return "Give ORS and Refer to doctor"
    if 'fever' in symptom_set and 'weakness' in symptom_set and 'vomiting' in symptom_set:
        return "Refer to doctor (Possible infection)"
    
    # Duration-specific concern
    if 'fever' in symptom_set and duration >= 4:
        return "Refer to doctor (Persistent fever)"
    
    # Severity-specific concern
    if 'fever' in symptom_set and fever_severity == "High":
        return "Refer to doctor (High fever)"

    # Moderate risk
    if 'cough' in symptom_set and 'cold' in symptom_set:
        return "Monitor at home (Common cold)"
    if 'fever' in symptom_set and 'body pain' in symptom_set:
        return "Give paracetamol and Monitor"
    if 'diarrhea' in symptom_set and 'dehydration' in symptom_set:
        return "Give ORS and Monitor"

    # Low risk single symptoms
    if 'vomiting' in symptom_set or 'diarrhea' in symptom_set:
        return "Give ORS and Monitor at home"
    if 'fever' in symptom_set:
        return "Monitor and check temperature regularly"
    if 'cold' in symptom_set or 'cough' in symptom_set:
        return "Monitor at home"

    return "Monitor at home (No serious symptoms detected)"

# Optional: save session to CSV
def save_patient_record(name, location, symptoms, decision, score, level):
    filepath = "patient_history.csv"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now, name, location, ', '.join(symptoms), decision, score, level]
    header = ["Timestamp", "Name", "Location", "Symptoms", "Triage Decision", "Risk Score", "Risk Level"]

    write_header = not os.path.exists(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)

# CLI Test (still works!)
if __name__ == "__main__":
    print("Enter patient name:")
    name = input()
    print("Enter location/state:")
    location = input()
    print("Enter patient symptoms separated by commas:")
    symptoms = input().split(',')
    print("Enter duration of symptoms (in days):")
    duration = int(input())
    print("Fever severity (Low/Medium/High):")
    severity = input().capitalize()

    score, level = calculate_risk(symptoms, duration, severity)
    decision = get_triage_decision(symptoms, duration, severity)
    save_patient_record(name, location, symptoms, decision, score, level)

    print(f"\nRisk Level: {level} | Score: {score}")
    print(f"Triage Decision: {decision}")
