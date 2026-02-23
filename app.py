import streamlit as st
from engine import analyze_resume
from role_database import ROLE_DATABASE

st.set_page_config(
    page_title="AI Career Role Fit Analyzer",
    layout="wide"
)

st.title("🚀 AI Career Role Fit Analyzer")
st.write("Upload your resume and evaluate your compatibility with predefined job roles.")

# Dropdown for 30 roles
selected_role = st.selectbox(
    "Select Job Role",
    list(ROLE_DATABASE.keys())
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF only)",
    type=["pdf"]
)

if st.button("Analyze Resume"):

    if uploaded_file is not None:

        with st.spinner("Analyzing... Please wait."):
            result = analyze_resume(uploaded_file, selected_role)

        st.markdown("## 📊 Role Fit Score")
        st.progress(float(result["score"]) / 100.0)
        st.metric("Match Percentage", f"{result['score']}%")

        st.markdown("## 📌 Verdict")
        if result["score"] >= 75:
            st.success(result["verdict"])
        elif result["score"] >= 50:
            st.warning(result["verdict"])
        else:
            st.error(result["verdict"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Matched Skills")
            st.write("Core Skills:", result["core_matches"])
            st.write("Bonus Skills:", result["bonus_matches"])

        with col2:
            st.markdown("### ❌ Missing Skills")
            st.write("Core Skills:", result["missing_core"])
            st.write("Bonus Skills:", result["missing_bonus"])

        if result["score"] < 75:
            st.markdown("## 🔎 Recommended Focus Areas")

            if result["missing_core"]:
                st.write("**Priority Skills to Learn:**")
                for skill in result["missing_core"][:3]:
                    st.write("-", skill)

            if result["missing_bonus"]:
                st.write("**Optional Improvements:**")
                for skill in result["missing_bonus"][:2]:
                    st.write("-", skill)

    else:
        st.warning("Please upload a resume file.")