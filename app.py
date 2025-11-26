import streamlit as st
import tempfile, os
import pandas as pd

from parsers import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, clean_text
from skill_extraction import simple_keyword_skills, spacy_candidate_skills, load_skills_list
from similarity import compute_similarity, compare_skills
from report import export_csv_jd_resume

import matplotlib.pyplot as plt
import plotly.express as px


# ----------- Streamlit UI Setup -----------
st.set_page_config(layout="wide", page_title="AI-Powered Skill Gap Analyzer")
st.title("AI-Powered Skill Gap Analyzer")

col1, col2 = st.columns(2)

with col1:
    st.header("Upload Resume")
    resume_file = st.file_uploader("Upload resume (PDF/DOCX/TXT)", type=["pdf","docx","txt"], key="resume")

with col2:
    st.header("Upload Job Description")
    jd_file = st.file_uploader("Upload job description (PDF/DOCX/TXT)", type=["pdf","docx","txt"], key="jd")


# ----------- Run Analysis Button -----------
if st.button("Run Analysis"):

    if not resume_file or not jd_file:
        st.error("Please upload both resume and job description.")
    else:
        tmp_res = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{resume_file.name}")
        tmp_res.write(resume_file.getvalue())
        tmp_res.flush()

        tmp_jd = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{jd_file.name}")
        tmp_jd.write(jd_file.getvalue())
        tmp_jd.flush()

        def parse_file(path):
            ext = path.split(".")[-1].lower()
            if ext == "pdf":
                return extract_text_from_pdf(path)
            elif ext == "docx":
                return extract_text_from_docx(path)
            else:
                return extract_text_from_txt(path)

        resume_text = clean_text(parse_file(tmp_res.name))
        jd_text = clean_text(parse_file(tmp_jd.name))

        st.subheader("Parsed Preview")
        st.text_area("Resume preview", resume_text[:5000], height=200)
        st.text_area("JD preview", jd_text[:5000], height=200)

        try:
            skill_list = load_skills_list("data/skills_list.txt")
        except:
            skill_list = []

        st.subheader("Extracted Skills")
        if skill_list:
            resume_skills = simple_keyword_skills(resume_text, skill_list)
            jd_skills = simple_keyword_skills(jd_text, skill_list)
        else:
            resume_skills = spacy_candidate_skills(resume_text)[:50]
            jd_skills = spacy_candidate_skills(jd_text)[:50]

        st.write("**Resume Skills:**", resume_skills)
        st.write("**JD Skills:**", jd_skills)

        st.subheader("Similarity & Skill Gaps")
        results, similarity_matrix = compare_skills(resume_skills, jd_skills)
        similarity_score = compute_similarity(resume_skills, jd_skills)

        st.metric("Overall Skill Match Score", f"{similarity_score}%")

        r_df = pd.DataFrame(results)
        st.session_state["r_df"] = r_df  # save state after creation
        st.session_state["jd_df"] = pd.DataFrame({"JD Skill": jd_skills})

        if not r_df.empty:
            st.dataframe(r_df.sort_values("Similarity Score", ascending=False), use_container_width=True)

            matched = r_df[r_df["Status"] == "Matched"]["Resume Skill"].tolist()
            weak = r_df[r_df["Status"] == "Weak Match"]["Resume Skill"].tolist()
            missing = list(set(jd_skills) - set(matched) - set(weak))

            st.markdown("### Gap Summary")
            st.write(f"**Matched skills:** {matched}")
            st.write(f"**Weak skills:** {weak}")
            st.write(f"**Missing skills:** {missing}")

            st.markdown("### Visualization")
            colA, colB = st.columns(2)

            labels = ["Matched", "Weak", "Missing"]
            sizes = [len(matched), len(weak), len(missing)]

            if sum(sizes) > 0:
                with colA:
                    fig1, ax1 = plt.subplots(figsize=(2.2, 2.2))
                    ax1.pie(
                        sizes, labels=labels, autopct='%1.1f%%',
                        startangle=90, textprops={'fontsize': 6}
                    )
                    ax1.axis("equal")
                    st.pyplot(fig1)

                with colB:
                    bar_fig = px.bar(
                        r_df, x="Resume Skill", y="Similarity Score",
                        color="Status", text="Similarity Score", height=250
                    )
                    st.plotly_chart(bar_fig, use_container_width=True)


# ----------- Export Outside Run Analysis -----------
if "jd_df" in st.session_state and "r_df" in st.session_state:
    st.subheader("Export Report")
    if st.button("Download"):
        out_path = export_csv_jd_resume(
            st.session_state["jd_df"].to_dict(orient="records"),
            st.session_state["r_df"].to_dict(orient="records"),
            path="skill_gap_report.csv"
        )
        with open(out_path, "rb") as f:
            st.download_button("Download File", f, file_name="skill_gap_report.csv")
