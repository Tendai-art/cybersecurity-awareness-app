import streamlit as st
import pandas as pd
import altair as alt

# -------------------------
# LOGIN SYSTEM
# -------------------------
USER_CREDENTIALS = {
    "admin": "password123",
    "tenda": "securepass"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# -------------------------
# MAIN APP
# -------------------------
def main_app():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Add Risk", "HIPAA Assessment", "Dashboard", "Simulation Training"])

    # Initialize session state
    if "risks" not in st.session_state:
        st.session_state["risks"] = []
    if "hipaa_scores" not in st.session_state:
        st.session_state["hipaa_scores"] = {"Admin": 0, "Technical": 0, "Physical": 0, "Notes": ""}

    # -------------------------
    # ADD RISK PAGE
    # -------------------------
    if page == "Add Risk":
        st.header("Add a Risk / Awareness Gap")

        risk_description = st.text_input("Risk description")
        domain = st.selectbox("Awareness gap domain", ["Phishing Awareness", "Password Hygiene", "Incident Response", "Policy Knowledge"])
        severity = st.slider("Cognitive gap severity (0–10)", 0, 10, 5)
        likelihood = st.slider("Likelihood (1–5)", 1, 5, 3)
        impact = st.slider("Impact (1–5)", 1, 5, 3)

        risk_score = severity * likelihood * impact
        st.write(f"Calculated Risk Score: {risk_score}")

        if st.button("Add Risk"):
            st.session_state["risks"].append({
                "Description": risk_description,
                "Domain": domain,
                "Severity": severity,
                "Likelihood": likelihood,
                "Impact": impact,
                "Score": risk_score
            })
            st.success("Risk added!")

    # -------------------------
    # HIPAA ASSESSMENT PAGE
    # -------------------------
    elif page == "HIPAA Assessment":
        st.header("HIPAA Safeguard Assessment")

        admin = st.slider("Administrative safeguards (0–100)", 0, 100, 50)
        technical = st.slider("Technical safeguards (0–100)", 0, 100, 50)
        physical = st.slider("Physical safeguards (0–100)", 0, 100, 50)
        notes = st.text_area("Notes / observations")

        if st.button("Save HIPAA Assessment"):
            st.session_state["hipaa_scores"] = {
                "Admin": admin,
                "Technical": technical,
                "Physical": physical,
                "Notes": notes
            }
            st.success("HIPAA assessment saved!")

    # -------------------------
    # DASHBOARD PAGE
    # -------------------------
    elif page == "Dashboard":
        st.header("Dashboard")

        st.subheader("Aggregated Risks")
        if st.session_state["risks"]:
            df = pd.DataFrame(st.session_state["risks"])
            st.table(df)
        else:
            st.write("No risks added yet.")

        st.subheader("HIPAA Safeguard Scores")
        hipaa = st.session_state["hipaa_scores"]
        st.write(f"Administrative: {hipaa['Admin']}")
        st.write(f"Technical: {hipaa['Technical']}")
        st.write(f"Physical: {hipaa['Physical']}")
        st.write(f"Notes: {hipaa['Notes']}")

        # Simple overall score
        if st.session_state["risks"]:
            avg_risk = sum(r["Score"] for r in st.session_state["risks"]) / len(st.session_state["risks"])
        else:
            avg_risk = 0
        hipaa_avg = (hipaa["Admin"] + hipaa["Technical"] + hipaa["Physical"]) / 3
        st.metric("Overall Risk Score", f"{avg_risk:.1f}")
        st.metric("HIPAA Compliance Score", f"{hipaa_avg:.1f}")

    # -------------------------
    # SIMULATION TRAINING PAGE
    # -------------------------
    elif page == "Simulation Training":
        st.header("Awareness Training Simulation")

        trainings_per_year = st.slider("Trainings per year", 1, 12, 4)
        training_effect = st.slider("Training effect per event (%)", 1, 50, 20)
        monthly_decay = st.slider("Monthly decay (%)", 0, 20, 2)
        months = st.slider("Months to simulate", 1, 24, 12)

        if st.button("Run Simulation"):
            # Start with average risk score as baseline awareness gap
            if st.session_state["risks"]:
                baseline = sum(r["Severity"] for r in st.session_state["risks"]) / len(st.session_state["risks"])
            else:
                baseline = 5  # default baseline

            awareness = []
            score = baseline
            for m in range(1, months + 1):
                # decay
                score -= (monthly_decay / 100) * score
                # training boost
                if m % (12 // trainings_per_year) == 0:
                    score += (training_effect / 100) * (10 - score)
                awareness.append({"Month": m, "Awareness": score})

            df = pd.DataFrame(awareness)
            chart = alt.Chart(df).mark_line(point=True).encode(
                x="Month",
                y="Awareness"
            ).properties(title="Awareness Growth Over Time")
            st.altair_chart(chart, use_container_width=True)

# -------------------------
# APP ENTRY POINT
# -------------------------
if not st.session_state.authenticated:
    login()
else:
    main_app()

