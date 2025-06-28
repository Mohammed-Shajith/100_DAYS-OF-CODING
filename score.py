import pandas as pd

# --- Weight configuration ---
SKILL_WEIGHT = 0.45
EXPERIENCE_WEIGHT = 0.20
EDUCATION_WEIGHT = 0.35

# --- User input options ---
skills_options = [
    "machine learning", "web development", "full stack",
    "python", "flask", "sql", "html", "css", "javascript"
]

experience_options = [
    "fresher", "1-2 years", "3-5 years", "5+ years"
]

education_options = [
    "b.e", "b.tech", "computer science", "artificial intelligence",
    "cybersecurity", "cse", "information technology"
]

# --- Get user input ---
print("\nSelect relevant SKILLS from below (comma-separated numbers):")
for i, skill in enumerate(skills_options, 1):
    print(f"{i}. {skill}")
skill_input = input("Enter choices (e.g., 1,3,5): ")
selected_skills = [skills_options[int(i)-1].lower() for i in skill_input.split(',') if i.strip().isdigit()]

print("\nSelect EXPERIENCE level:")
for i, exp in enumerate(experience_options, 1):
    print(f"{i}. {exp}")
exp_input = input("Enter choice (e.g., 2): ")
selected_exp = experience_options[int(exp_input.strip())-1].lower()

print("\nSelect EDUCATION keywords (comma-separated numbers):")
for i, edu in enumerate(education_options, 1):
    print(f"{i}. {edu}")
edu_input = input("Enter choices (e.g., 1,3,5): ")
selected_edu = [education_options[int(i)-1].lower() for i in edu_input.split(',') if i.strip().isdigit()]

# --- Load parsed resumes ---
try:
    df = pd.read_csv("parsed_resumes.csv")
except FileNotFoundError:
    print("parsed_resumes.csv not found.")
    exit()

# --- Function to calculate match ratio ---
def match_score(field_text, selected_keywords):
    if not isinstance(field_text, str):
        return 0
    field_text = field_text.lower()
    matches = sum(1 for kw in selected_keywords if kw in field_text)
    return matches / len(selected_keywords) if selected_keywords else 0

# --- Score each resume ---
scores = []
for _, row in df.iterrows():
    skill_score = match_score(row.get("Skills", ""), selected_skills)
    exp_score = match_score(row.get("Experience", ""), [selected_exp])
    edu_score = match_score(row.get("Education", ""), selected_edu)

    final_score = (skill_score * SKILL_WEIGHT + 
                   exp_score * EXPERIENCE_WEIGHT + 
                   edu_score * EDUCATION_WEIGHT) * 10  # scale to 10

    scores.append({
        "Filename": row.get("Filename", "Unknown"),
        "Name": row.get("Name", "Unknown"),
        "Score (/10)": round(final_score, 2)
    })

# --- Save results ---
score_df = pd.DataFrame(scores)
score_df.to_csv("scored_resumes.csv", index=False)
print("\n✅ Resume scores saved to 'scored_resumes.csv'")
