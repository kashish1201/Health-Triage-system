# condition_predictor.py
def predict_condition(symptoms):
    rules = {
        frozenset(["fever", "cough"]): ("Flu", 80),
        frozenset(["diarrhea", "vomiting"]): ("Gastroenteritis", 85),
        frozenset(["fever", "rash"]): ("Measles", 75),
    }
    
    symptom_set = frozenset(symptoms)
    for rule, (cond, conf) in rules.items():
        if rule.issubset(symptom_set):
            return cond, conf

    return "Uncertain", 60
