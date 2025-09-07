# main.py
import streamlit as st
from resume_upload import handle_resume_upload
from jd_input import handle_jd_input
from analysis import show_analysis
from job_matches import show_job_matches
from screening import show_screening
from recommendation import show_recommendation
from faiss_engine import find_top_matches

st.set_page_config(
    page_title="ZenResume - Space Edition", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Persistent session state to track if "Next" is clicked
if "show_tabs" not in st.session_state:
    st.session_state.show_tabs = False

# Sidebar with space theme
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="stars"></div>
        <div class="twinkling"></div>
        <h2>🚀 ZenResume</h2>
        <p>Navigate your career galaxy</p>
    </div>
    """, unsafe_allow_html=True)
    
    resume_text = handle_resume_upload()
    jd_text = handle_jd_input()

# Prepare JD list for multi-match
if jd_text:
    if "jd_list" not in st.session_state:
        st.session_state.jd_list = jd_text.split("\n\n") if isinstance(jd_text, str) else jd_text

# Sidebar Next Button
if resume_text and jd_text:
    next_clicked = st.sidebar.button("🌌 Launch Analysis", help="Click to proceed to screening & analysis", use_container_width=True)

    if next_clicked:
        st.session_state.show_tabs = True

# Conditional display of main sections
if st.session_state.show_tabs and resume_text and jd_text:
    # Space-themed header
    st.markdown("""
    <div class="space-header">
        <div class="stars"></div>
        <div class="twinkling"></div>
        <div class="content">
            <h1>ZenResume</h1>
            <p>Exploring the career cosmos</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Resume and JD loaded successfully!")

    tabs = st.tabs([
        "🌠 Fit Overview",
        "🪐 Role Matching",
        "🔭 Comprehensive Screening",
        "🚀 Final Recommendation"
    ])

    with tabs[0]:
        with st.spinner("Analyzing cosmic compatibility..."):
            show_analysis(resume_text, jd_text)

    with tabs[1]:
        with st.spinner("Scanning the job galaxy..."):
            show_job_matches(resume_text, st.session_state.jd_list)

    with tabs[2]:
        with st.spinner("Running deep space screening..."):
            screening_score = show_screening(resume_text, jd_text)

    with tabs[3]:
        with st.spinner("Calculating trajectory..."):
            show_recommendation(resume_text, jd_text)

else:
    # Landing page with space theme
    st.markdown("""
    <div class="space-landing">
        <div class="stars"></div>
        <div class="twinkling"></div>
        <div class="content">
            <h1>ZenResume</h1>
            <p>Navigate the cosmos of career opportunities</p>
            <div class="planet"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📄 Please upload Resume and Job Description, then click **Launch Analysis** in sidebar.")
