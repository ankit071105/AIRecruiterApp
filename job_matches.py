# 📁 job_matches.py

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from faiss_engine import find_top_matches
from nlp_utils import count_categories


def show_job_matches(resume_text, jd_text):
    st.markdown("<h2 class='section-title'>🎯 Job Matching Insights</h2>", unsafe_allow_html=True)

    # jd_text is already passed as a list of job descriptions
    jd_list = jd_text
    if not jd_list:
        st.error("❌ No valid job descriptions found.")
        return

    # Get top matching JDs via FAISS
    top_matches = find_top_matches(resume_text, jd_list, top_k=3)
    # Display top match score
    if top_matches:
        # Clamp the top score to stay within [0, 1] for pie chart stability
        top_score_raw = top_matches[0]["score"]
        top_score = max(0.0, min(top_score_raw, 1.0))

        st.metric("🔍 Top Match Score", f"{top_score_raw * 100:.2f}%")

        if top_score_raw > 0.7:
            st.success("✅ Strong Match: Ready for screening")
        elif top_score_raw > 0.4:
            st.info("⚠️ Moderate Match: Consider improvements")
        else:
            st.warning("❌ Low Match: Needs significant revision")

        # Pie Chart: ATS match approximation
        with st.container():
            st.markdown("<div class='custom-card'><h4>📈 ATS Score (Approx)</h4>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots()
            ax1.pie(
                [top_score, 1 - top_score],
                labels=["Match", "Remaining"],
                autopct='%1.1f%%',
                colors=['#0B525B', '#CCCCCC'],
                startangle=90
            )
            ax1.axis('equal')
            st.pyplot(fig1)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No top matches found to visualize.")


    # Skill overlap percentage
    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    jd_words = set(re.findall(r"\w+", " ".join(jd_list).lower()))
    common = resume_words.intersection(jd_words)
    common_skills = [word for word in common if len(word) > 3]
    skill_overlap_pct = len(common_skills) / max(len(jd_words), 1) * 100

    with st.container():
        st.metric("🧠 Skill Overlap", f"{skill_overlap_pct:.2f}%")

    # 📊 Visualizations
    counts = count_categories(resume_text)

    with st.container():
        st.markdown("<div class='custom-card'><h4>📈 ATS Score (Top Match)</h4>", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots()
        ax1.pie([top_score, 1 - top_score], labels=["Match", "Remaining"], autopct='%1.1f%%',
                colors=['#0B525B', '#CCCCCC'], startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='custom-card'><h4>📊 Resume Breakdown (Skills & Education)</h4>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots()
        sns.barplot(
            x=["Technical Skills", "Soft Skills", "Education"],
            y=[counts["Technical Skills"], counts["Soft Skills"], counts["Education"]],
            palette="Blues_d", ax=ax2
        )
        ax2.set_ylabel("Count")
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='custom-card'><h4>📚 Projects, Achievements, Experience</h4>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots()
        sns.barplot(
            x=["Projects", "Achievements", "Experience"],
            y=[counts["Projects"], counts["Achievements"], counts["Experience"]],
            palette="Purples_d", ax=ax3
        )
        ax3.set_ylabel("Count")
        st.pyplot(fig3)
        st.markdown("</div>", unsafe_allow_html=True)

    # Matched keywords
    with st.expander("🧩 Matched Keywords (Click to Expand)"):
        st.write(", ".join(common_skills) or "No significant overlap found.")

    # Display Top JD Matches
    with st.expander("📋 Top Matching Job Descriptions (FAISS)"):
        for match in top_matches:
            jd_preview = match["job_description"][:150].replace("\n", " ").strip()
            st.markdown(f"**{match['score'] * 100:.2f}% match:** {jd_preview}...")

# for the summary logic

def get_resume_match_summary(resume_text, jd_text):
    jd_list = jd_text if isinstance(jd_text, list) else [jd_text]
    if not jd_list:
        return None

    top_matches = find_top_matches(resume_text, jd_list, top_k=3)
    top_score_raw = top_matches[0]["score"] if top_matches else 0.0
    top_score = max(0.0, min(top_score_raw, 1.0))

    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    jd_words = set(re.findall(r"\w+", " ".join(jd_list).lower()))
    common_skills = [word for word in resume_words.intersection(jd_words) if len(word) > 3]
    skill_overlap_pct = len(common_skills) / max(len(jd_words), 1) * 100

    counts = count_categories(resume_text)

    return {
        "top_score": top_score,
        "top_score_raw": top_score_raw,
        "skill_overlap_pct": skill_overlap_pct,
        "counts": counts,
    }
