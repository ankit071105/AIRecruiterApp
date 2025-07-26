# main.py
import streamlit as st
from resume_upload import handle_resume_upload
from jd_input import handle_jd_input
from analysis import show_analysis
from job_matches import show_job_matches
from screening import show_screening
from recommendation import show_recommendation
from faiss_engine import find_top_matches

st.set_page_config(page_title="AI Resume Recruiter", layout="wide")

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Persistent session state to track if "Next" is clicked
if "show_tabs" not in st.session_state:
    st.session_state.show_tabs = False

# Sidebar Inputs
st.sidebar.title("📂 Upload Inputs")
resume_text = handle_resume_upload()
jd_text = handle_jd_input()

# Prepare JD list for multi-match
if jd_text:
    if "jd_list" not in st.session_state:
        st.session_state.jd_list = jd_text.split("\n\n") if isinstance(jd_text, str) else jd_text

# Sidebar Next Button
if resume_text and jd_text:
    next_clicked = st.sidebar.button("➡️ Next", help="Click to proceed to screening & analysis")

    if next_clicked:
        st.session_state.show_tabs = True

# Conditional display of main sections
if st.session_state.show_tabs and resume_text and jd_text:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 1.5rem;'>
        <h1 style='
            font-family: "Georgia", serif;
            font-size: 3rem;
            color: #FFD700;
            margin-bottom: 0.2rem;
            text-shadow: 1px 1px 2px #00000050;
        '>
             NeuroHire
        </h1>
       
    </div>
    """, unsafe_allow_html=True)
    st.success("✅ Resume and JD loaded successfully!")

    tabs = st.tabs([
        "🔍 Fit Overview",
        "🎯 Role Matching",
        "📋 Comprehensive Screening",
        "🧭 Final Recommendation"
    ])

    with tabs[0]:
        with st.spinner("Fitting Overview..."):
            show_analysis(resume_text, jd_text)

    with tabs[1]:
        with st.spinner("Matching resume to job descriptions..."):
            show_job_matches(resume_text, st.session_state.jd_list)

    with tabs[2]:
        with st.spinner("Running screening analysis..."):
            screening_score = show_screening(resume_text, jd_text)
            # st.sidebar.metric("📊 Screening Score", f"{screening_score * 100:.1f}%")

    with tabs[3]:
        with st.spinner("Generating recommendation..."):
            show_recommendation(resume_text, jd_text)

else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 1.5rem;'>
        <h1 style='
            font-family: "Georgia", serif;
            font-size: 3rem;
            color: #FFD700;
            margin-bottom: 0.2rem;
            text-shadow: 1px 1px 2px #00000050;
        '>
    ZenResume
        </h1>
       
    </div>
""", unsafe_allow_html=True)
    st.info("📄 Please upload Resume and Job Description, then click **Next** in sidebar.")
