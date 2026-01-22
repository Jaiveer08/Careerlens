import streamlit as st
import json
import time
from backend.resume_parser import extract_text
from backend.skill_extractor import extract_skills
from backend.scorer import calculate_score
from ai.role_predictor import predict_role
from frontend.styles import load_css
from frontend.ui_components import card, skill_list

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="CareerLens",
    page_icon="🔍",
    layout="wide",  # Changed to wide for a more dashboard-like feel
    initial_sidebar_state="expanded"
)

# ---------------- Session State Initialization ----------------
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# ---------------- CSS Styling ----------------
st.markdown("""
<style>
    /* Global Styles */
    .main { background-color: #0e1117; color: #ffffff; }
    
    /* Custom Card Style */
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #374151;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .score-big { font-size: 3rem; font-weight: bold; }
    .score-green { color: #10b981; }
    .score-yellow { color: #f59e0b; }
    .score-red { color: #ef4444; }
    
    /* Headers */
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background-color: #374151;
        padding: 5px 10px;
        margin: 3px;
        border-radius: 15px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Load Data ----------------
@st.cache_data
def load_role_skills():
    with open("data/role_skills.json") as f:
        return json.load(f)

ROLE_SKILLS = load_role_skills()

# ---------------- Sidebar (Inputs) ----------------
with st.sidebar:
    #st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("CareerLens 🔎")
    st.markdown("Optimization Toolkit")
    
    st.divider()
    
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("PDF or DOCX", type=["pdf", "docx"])

    st.subheader("Target Role")
    # Add 'Auto-Detect' as the first option
    role_options = ["Auto-Detect (AI)"] + list(ROLE_SKILLS.keys())
    selected_role_option = st.selectbox("Select Role to Analyze", role_options)

    analyze_btn = st.button("🚀 Run Analysis", use_container_width=True, type="primary")
    
    st.markdown("---")
    st.caption("© 2026 CareerLens| Crafted by REXA")

# ---------------- Main Logic ----------------
def process_resume():
    """Handles the heavy lifting of processing and stores in session state"""
    try:
        # 1. Extract Text
        resume_text = extract_text(uploaded_file)
        
        # 2. AI Role Prediction (Always run this to show insights)
        predicted_role, confidence = predict_role(resume_text, ROLE_SKILLS)
        
        # 3. Determine Final Target Role
        if selected_role_option == "Auto-Detect (AI)":
            final_target_role = predicted_role
            role_source = "AI_AUTO"
        else:
            final_target_role = selected_role_option
            role_source = "MANUAL"

        # 4. Extract Skills & Score
        skills_found = extract_skills(resume_text, ROLE_SKILLS[final_target_role])
        score, missing_skills = calculate_score(skills_found, ROLE_SKILLS[final_target_role])

        # 5. Store in Session State
        st.session_state.analysis_results = {
            "text": resume_text,
            "predicted_role": predicted_role,
            "predicted_conf": confidence,
            "target_role": final_target_role,
            "role_source": role_source,
            "skills_found": skills_found,
            "missing_skills": missing_skills,
            "score": score
        }
    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")

# ---------------- Execution Trigger ----------------
if analyze_btn:
    if not uploaded_file:
        st.toast(" Please upload a resume first!", icon="⚠️")
    else:
        with st.spinner("Parsing resume and matching AI patterns..."):
            # Simulate a tiny delay for UX (users trust 'work' that takes a second)
            time.sleep(0.8) 
            process_resume()

# ---------------- Results Display ----------------
# We check session_state, not the button, so results persist on interaction
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # 
    
    # --- Header Section ---
    st.subheader(f"Analysis for: {results['target_role']}")
    
    # Show AI Insight if the user manually selected a role that differs from AI
    if results['role_source'] == "MANUAL" and results['predicted_role'] != results['target_role']:
        st.info(f"💡 **AI Insight:** While you selected **{results['target_role']}**, our AI analysis suggests your profile strongly matches **{results['predicted_role']}** ({results['predicted_conf']} match).")
    
    elif results['role_source'] == "AI_AUTO":
        st.success(f"🤖 **Auto-Detected:** Analyzed profile as **{results['target_role']}** based on your content.")

    st.divider()

    # --- Score Dashboard ---
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        # Determine Color
        score = results['score']
        color_class = "score-green" if score >= 80 else "score-yellow" if score >= 50 else "score-red"
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:14px; color:#9ca3af;">Resume Score</div>
            <div class="score-big {color_class}">{score}</div>
            <div style="font-size:12px;">out of 100</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("**Skill Match Progress**")
        st.progress(score / 100)
        st.caption(f"You have {len(results['skills_found'])} matching skills out of {len(ROLE_SKILLS[results['target_role']])} required.")

    with col3:
        # Guidance Logic
        if score > 80:
            guidance = "🌟 **Ready for Apply!** Your resume is well-optimized."
        elif score > 50:
            guidance = "🛠 **Needs Polish.** Focus on adding the missing keywords."
        else:
            guidance = "⚠️ **Gap Identified.** Significant skill acquisition needed."
        
        st.info(guidance)

    # --- Detailed Skill Analysis ---
    st.subheader("Skill Breakdown")
    
    tab1, tab2, tab3 = st.tabs(["✅ Present Skills", "❌ Missing Skills", "🚀 Improvement Plan"])

    with tab1:
        if results['skills_found']:
            # Using formatting tool to create tags
            html_tags = "".join([f"<span class='skill-tag'>{s}</span>" for s in results['skills_found']])
            st.markdown(html_tags, unsafe_allow_html=True)
        else:
            st.warning("No relevant skills found for this role.")

    with tab2:
        if results['missing_skills']:
            html_tags = "".join([f"<span class='skill-tag' style='background-color:#4b2c2c; border:1px solid #ef4444'>{s}</span>" for s in results['missing_skills']])
            st.markdown(html_tags, unsafe_allow_html=True)
        else:
            st.balloons()
            st.success("No missing skills! You are a perfect match.")

    with tab3:
        st.markdown("### Actionable Steps")
        st.markdown(f"""
        1. **Project Work:** Build a project specifically using **{', '.join(results['missing_skills'][:3])}**.
        2. **Certification:** Consider a certification in {results['target_role']} to validate your knowledge.
        3. **Resume Formatting:** Ensure these keywords appear in your "Skills" and "Experience" sections.
        """)

else:
    # Empty State (Before Upload)
    st.markdown("""
    <div style="text-align:center; margin-top:50px;">
        <h2>👋 Welcome to CareerLens</h2>
        <p style="color:#9ca3af; max-width:600px; margin:auto;">
            Upload your resume on the left sidebar to get a detailed AI analysis, 
            ATS score, and personalized improvement roadmap.
        </p>
    </div>
    """, unsafe_allow_html=True)
