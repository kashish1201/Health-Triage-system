import streamlit as st
import pandas as pd
from triage_agent import get_triage_decision, calculate_risk, save_patient_record
from nlp_summary import extract_symptoms
from condition_predictor import predict_condition  # new file

st.set_page_config(page_title="AI Village Triage", layout="centered")
st.title("🏥 AI-Based Village Health Triage Assistant")

# ⬇️ Tabs for Triage and History
tab1, tab2 = st.tabs(["🩺 Triage Assistant", "📊 Patient History"])

# ==============================
# TAB 1: TRIAGE ASSISTANT
# ==============================
with tab1:
    # Expander for patient info
    with st.expander("📋 Patient Information", expanded=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("👤 Patient Name")
        village = col2.text_input("🌍 Village/State")

    # Input Method Selection
    input_method = st.radio("📝 Input Method", ["Select from list", "Free text description"])

    symptoms = []
    duration = 1
    fever_severity = "Low"

    # Dynamic input
    if input_method == "Free text description":
        condition_text = st.text_area("🗣️ Describe the patient's condition")
        if condition_text:
            nlp_result = extract_symptoms(condition_text)
            symptoms = nlp_result["symptoms"]
            duration_text = nlp_result["duration"]
            severity_text = nlp_result["severity"]

            # Show extracted info
            st.markdown("#### 🔍 Extracted from text:")
            st.write(f"Symptoms: {symptoms}")
            st.write(f"Duration: {duration_text}")
            st.write(f"Severity: {severity_text}")

            # Parse duration if it's like "3 days"
            import re
            match = re.search(r"\d+", duration_text)
            if match:
                duration = int(match.group())
            fever_severity = severity_text.capitalize() if severity_text in ["low", "medium", "high"] else "Low"
    else:
        symptoms = st.multiselect("🔽 Select Symptoms", [
            "fever", "diarrhea", "cough", "vomiting", "rash", "cold",
            "dehydration", "breathing difficulty", "weakness", "body pain", "unconscious"
        ])
        with st.expander("⚙️ Symptom Details"):
            duration = st.slider("🕒 Duration of symptoms (in days)", 0, 10, 1)
            fever_severity = st.radio("🌡️ Fever severity", ["Low", "Medium", "High"])

    # Analyze Button
    if st.button("🔍 Analyze Patient"):
        if not name or not village or not symptoms:
            st.warning("Please complete all fields.")
        else:
            decision = get_triage_decision(symptoms, duration, fever_severity)
            score, risk_level = calculate_risk(symptoms, duration, fever_severity)

            st.success(f"Triage Decision: {decision}")
            st.info(f"Risk Level: {risk_level} | Score: {score}")

            # Predict condition using dummy ML
            condition, confidence = predict_condition(symptoms)
            st.write(f"🤖 Possible Condition: **{condition}** ({confidence}% confidence)")

            # Save to patient history
            save_patient_record(name, village, symptoms, decision, score, risk_level)

            st.download_button("📄 Download PDF Report", "Feature coming soon!", file_name=f"{name}_report.txt")

# ==============================
# TAB 2: PATIENT HISTORY
# ==============================
with tab2:
    st.header("📊 Patient History Log")

    try:
        history_df = pd.read_csv("patient_history.csv")
        st.dataframe(history_df, use_container_width=True)
    except FileNotFoundError:
        st.warning("No patient history available yet. Triage a patient to start recording data.")
