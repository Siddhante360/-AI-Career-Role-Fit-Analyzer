import re
import fitz
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from role_database import ROLE_DATABASE

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(uploaded_file):
    text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills(text, skill_list):
    matched = []
    text = text.lower()

    for skill in skill_list:
        skill_lower = skill.lower()
        pattern = r'\b' + re.escape(skill_lower) + r'\b'

        if re.search(pattern, text):
            matched.append(skill)
        elif fuzz.token_set_ratio(skill_lower, text) > 85:
            matched.append(skill)

    return list(set(matched))


def analyze_resume(uploaded_file, selected_role):

    resume_text = extract_text_from_pdf(uploaded_file)
    clean_resume = clean_text(resume_text)

    role_data = ROLE_DATABASE[selected_role]
    core_skills = role_data["core_skills"]
    bonus_skills = role_data["bonus_skills"]

    core_matches = extract_skills(clean_resume, core_skills)
    bonus_matches = extract_skills(clean_resume, bonus_skills)

    missing_core = list(set(core_skills) - set(core_matches))
    missing_bonus = list(set(bonus_skills) - set(bonus_matches))

    core_ratio = len(core_matches) / len(core_skills)
    bonus_ratio = len(bonus_matches) / len(bonus_skills)

    role_text = " ".join(core_skills + bonus_skills)

    resume_emb = model.encode(clean_resume)
    role_emb = model.encode(role_text)

    similarity = cosine_similarity(
        resume_emb.reshape(1, -1),
        role_emb.reshape(1, -1)
    )[0][0]

    semantic_score = (similarity + 1) / 2

    final_score = (
        0.5 * semantic_score +
        0.35 * core_ratio +
        0.15 * bonus_ratio
    ) * 100

    final_score = round(final_score, 2)

    if final_score >= 75:
        verdict = "Strong Fit ✅"
    elif final_score >= 50:
        verdict = "Moderate Fit ⚖️"
    else:
        verdict = "Low Fit ❌"

    return {
        "score": final_score,
        "verdict": verdict,
        "core_matches": core_matches,
        "bonus_matches": bonus_matches,
        "missing_core": missing_core,
        "missing_bonus": missing_bonus
    }