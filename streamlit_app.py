import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Resume-Job Matcher", page_icon="🎯")
st.title("🎯 AI Resume-Job Matcher")
st.caption("Embeddings-based fit score + skill-gap analysis")

resume = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd = st.text_area("Paste the job description", height=250)

if st.button("Analyze", type="primary", disabled=not (resume and len(jd) >= 50)):
    with st.spinner("Analyzing..."):
        try:
            r = requests.post(
                f"{API_URL}/match",
                files={"resume": (resume.name, resume.getvalue(), "application/pdf")},
                data={"job_description": jd},
                timeout=120,
            )
            r.raise_for_status()
            res = r.json()
        except requests.RequestException as e:
            st.error(f"API error: {e}")
            st.stop()

    st.subheader(f"{res['score']}% — {res['verdict']}")
    st.progress(min(int(res["score"]), 100))
    c1, c2 = st.columns(2)
    c1.metric("Semantic similarity", f"{res['semantic_score']}%")
    c2.metric("Skill coverage", f"{res['skill_score']}%")

    st.success("✅ Matched skills: " + (", ".join(res["matched_skills"]) or "none"))
    if res["missing_skills"]:
        st.warning("⚠️ Missing skills: " + ", ".join(res["missing_skills"]))
        st.info("Tip: add these to your resume only if you genuinely have them — "
                "otherwise, build a small project to learn them.")
