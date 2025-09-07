# main.py
import streamlit as st
from resume_upload import handle_resume_upload
from jd_input import handle_jd_input
from analysis import show_analysis
from job_matches import show_job_matches
from screening import show_screening
from recommendation import show_recommendation
from faiss_engine import find_top_matches
import random

st.set_page_config(page_title="ZenResume - Space Edition", layout="wide")

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add stars background
stars_js = """
<script>
function createStars() {
    const container = document.querySelector('.stars');
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = Math.random() * 3 + 2 + 's';
        star.style.opacity = Math.random();
        container.appendChild(star);
    }
}
createStars();
</script>
<div class="stars"></div>
"""
st.components.v1.html(stars_js, height=0)

# Persistent session state to track if "Next" is clicked
if "show_tabs" not in st.session_state:
    st.session_state.show_tabs = False

# Sidebar Inputs
st.sidebar.title("🌌 Upload Inputs")
resume_text = handle_resume_upload()
jd_text = handle_jd_input()

# Prepare JD list for multi-match
if jd_text:
    if "jd_list" not in st.session_state:
        st.session_state.jd_list = jd_text.split("\n\n") if isinstance(jd_text, str) else jd_text

# Sidebar Next Button
if resume_text and jd_text:
    next_clicked = st.sidebar.button("🚀 Next", help="Click to launch analysis")

    if next_clicked:
        st.session_state.show_tabs = True

# Conditional display of main sections
if st.session_state.show_tabs and resume_text and jd_text:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;' class="floating">
        <h1 style='
            font-family: "Orbitron", sans-serif;
            font-size: 3.5rem;
            color: #3498db;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 15px rgba(52, 152, 219, 0.7);
            letter-spacing: 2px;
        '>
            ZenResume<span style="color: #f1c40f;">⦿</span>
        </h1>
        <p style='color: #bdc3c7; font-size: 1.2rem; margin-top: 0;'>
            Interstellar Resume Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.success("✅ Resume and JD successfully uploaded! Launching analysis...")

    tabs = st.tabs([
        "🔭 Fit Overview",
        "🛸 Role Matching",
        "📡 Comprehensive Screening",
        "🚀 Final Recommendation"
    ])

    with tabs[0]:
        with st.spinner("Scanning resume dimensions..."):
            show_analysis(resume_text, jd_text)

    with tabs[1]:
        with st.spinner("Calculating orbital matches..."):
            show_job_matches(resume_text, st.session_state.jd_list)

    with tabs[2]:
        with st.spinner("Running deep space screening..."):
            screening_score = show_screening(resume_text, jd_text)

    with tabs[3]:
        with st.spinner("Generating cosmic recommendation..."):
            show_recommendation(resume_text, jd_text)

else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;' class="floating">
        <h1 style='
            font-family: "Orbitron", sans-serif;
            font-size: 3.5rem;
            color: #3498db;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 15px rgba(52, 152, 219, 0.7);
            letter-spacing: 2px;
        '>
            ZenResume<span style="color: #f1c40f;">⦿</span>
        </h1>
        <p style='color: #bdc3c7; font-size: 1.2rem; margin-top: 0;'>
            Interstellar Resume Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some space-themed placeholder content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; border-radius: 12px; 
                    background: rgba(18, 25, 40, 0.7); border: 1px solid rgba(52, 152, 219, 0.3);'>
            <h3 style='color: #3498db;'>🌠 Welcome to ZenResume Space Edition</h3>
            <p style='color: #bdc3c7;'>Upload your resume and job description to begin your cosmic career journey</p>
            <div style='font-size: 4rem; margin: 1rem 0;'>👨‍🚀 → 🪐 → 💼</div>
            <p style='color: #7f8c8d; font-size: 0.9rem;'>Navigate to the sidebar to upload your documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("📄 Please upload Resume and Job Description, then click **Next** in sidebar.")