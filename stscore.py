import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

st.set_page_config(page_title="Resume Parser & Scorer", layout="wide")
st.title(" Resume Parser & Scorer")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("parsed_resumes.csv")
    except FileNotFoundError:
        return pd.DataFrame()

# Fuzzy Matching 
def fuzzy_match_score(text, keywords):
    if not isinstance(text, str) or not keywords:
        return 0.0
    scores = []
    for kw in keywords:
        best_score = max([fuzz.partial_ratio(kw, part) for part in text.lower().split()])
        scores.append(best_score)
    return sum(scores) / (len(keywords) * 100)

SKILL_WEIGHT = 0.45
EXP_WEIGHT = 0.20
EDU_WEIGHT = 0.35

skills_options = ["machine learning", "web development", "full stack", "python", "flask", "sql"]
exp_options = ["fresher", "1-2 years", "3-5 years", "5+ years"]
edu_options = ["b.e", "b.tech", "cse", "ai", "cybersecurity"]

df = load_data()

if df.empty:
    st.warning("⚠️ No parsed resumes found. Make sure 'parsed_resumes.csv' exists.")
    st.stop()

st.subheader(" Parsed Resume Data")
st.dataframe(df.head(3), use_container_width=True)

with st.expander("🔍 See full parsed data"):
    st.dataframe(df, use_container_width=True)

st.subheader(" Score Resumes")

with st.form("score_form"):
    st.markdown("### Select Criteria")
    skill_sel = st.multiselect("Choose Skills", skills_options)
    exp_sel = st.multiselect("Choose Experience", exp_options)
    edu_sel = st.multiselect("Choose Education", edu_options)
    submit = st.form_submit_button("Score Now")

if submit:
    results = []
    for _, row in df.iterrows():
        name = row.get("Name", "Unknown")
        filename = row.get("Filename", "Unknown")

        skill_score = fuzzy_match_score(row.get("Skills", ""), skill_sel)
        exp_score = fuzzy_match_score(row.get("Experience", ""), exp_sel)
        edu_score = fuzzy_match_score(row.get("Education", ""), edu_sel)

        final = round((skill_score * SKILL_WEIGHT + exp_score * EXP_WEIGHT + edu_score * EDU_WEIGHT) * 10, 2)

        results.append({
            "Name": name,
            "Filename": filename,
            "Skill Score (/10)": round(skill_score * 10, 2),
            "Experience Score (/10)": round(exp_score * 10, 2),
            "Education Score (/10)": round(edu_score * 10, 2),
            "Final Score (/10)": final
        })

    scored_df = pd.DataFrame(results)
    scored_df = scored_df.sort_values(by="Final Score (/10)", ascending=False).reset_index(drop=True)
    scored_df.insert(0, "Rank", scored_df.index + 1)

    st.success("Scoring Complete!")

    top = scored_df.iloc[0]
    st.markdown(f"""
    ### Top Applicant: **{top['Name']}**
    - **File:** {top['Filename']}
    - **Final Score:**  `{top['Final Score (/10)']}/10`
    """)

    with st.expander("See All Scores"):
        st.dataframe(scored_df, use_container_width=True)

    scored_df.to_csv("scored_resumes.csv", index=False)
