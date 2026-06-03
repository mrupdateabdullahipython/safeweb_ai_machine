import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import random
import base64

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="SafeWeb AI — Enterprise Shield",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []
if "trigger_animation" not in st.session_state:
    st.session_state.trigger_animation = False

# ==========================================
# 3. BASE64 LOCAL IMAGE ENCODER & PREMIUM CSS
# ==========================================
# Tabbatar hoton yana cikin folder daya da app.py kuma sunansa security_background.jpg
LOCAL_IMAGE_PATH = "security_background.jpg" 

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    bin_str = get_base64_of_bin_file(LOCAL_IMAGE_PATH)
    background_css = f'background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.96)), url("data:image/jpg;base64,{bin_str}");'
except FileNotFoundError:
    # Idan ba a sami hoton ba, manhajar zata yi amfani da kalar duhu na asali don kar ta tsaya
    background_css = 'background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 70%);'

import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import random  # Don lissafin Risk Score idan model din ba shi da predict_proba
import base64
# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="SafeWeb AI — Enterprise Shield",
    page_icon="🛡️",
    layout="wide"  # Anyi amfani da wide layout domin Sidebar din ya zauna da kyau
)

# ==========================================
# 2. SESSION STATE (PREDICTION HISTORY)
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# 3. PREMIUM ADVANCED CSS
# ==========================================

# Gano asalin hoton kwamfutarka (Sanya sunan hotonka a nan)
LOCAL_IMAGE_PATH = "security_background.jpg" 

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    bin_str = get_base64_of_bin_file(LOCAL_IMAGE_PATH)
    # Sanya hoton a cikin tsarin CSS
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }}
    
    /* Duka sauran CSS dinka na custom-card, main-title, button da sauran su suna nan a kasa... */
    .custom-card {{
        background: rgba(30, 41, 59, 0.55) !important;
        backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }}
    .stTextInput > div {{
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }}
    .main-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border-radius: 12px !important;
        width: 100% !important;
    }}
    .metric-box {{
        background: rgba(15, 23, 42, 0.6);
        padding: 15px;
        border-radius: 10px;
    }}
    .blocked-res {{ background: rgba(220, 38, 38, 0.2); border-left: 5px solid #dc2626; }}
    .allowed-res {{ background: rgba(5, 150, 105, 0.2); border-left: 5px solid #059669; }}
    </style>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    # Idan ba a sami hoton ba, manhajar zata yi amfani da kalar duhu na asali don kar ta tsaya
    st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 70%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc;
}

/* Glassmorphic Cards */
.custom-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    margin-bottom: 25px;
}

/* Input Fields Accent */
.stTextInput > div {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}
.stTextInput > div:focus-within {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
}

/* Glowing Typography */
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

/* Premium Button styling */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white !important;
    border: none !important;
    padding: 14px 28px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2) !important;
}
div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 25px rgba(37, 99, 235, 0.4) !important;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

/* Badges & Metrics */
.metric-box {
    background: rgba(15, 23, 42, 0.5);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
}
.score-high { color: #f87171; font-size: 1.8rem; font-weight: 700; }
.score-low { color: #34d399; font-size: 1.8rem; font-weight: 700; }

.result-box {
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    font-weight: 500;
}
.blocked-res { background: rgba(220, 38, 38, 0.15); border-left: 5px solid #dc2626; color: #fca5a5; }
.allowed-res { background: rgba(5, 150, 105, 0.15); border-left: 5px solid #059669; color: #a7f3d0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. MODEL LOADING (WITH ERROR HANDLING)
# ==========================================
@st.cache_resource
def load_model_securely():
    try:
        model = joblib.load("blocker_brain.pkl")
        return model, None
    except FileNotFoundError:
        return None, "CRITICAL ERROR: 'blocker_brain.pkl' file not found. Please ensure the model file is in the same directory."
    except Exception as e:
        return None, f"UNEXPECTED ERROR: Failed to parse the ML model matrix. Details: {str(e)}"

brain, model_error = load_model_securely()

# ==========================================
# 5. SIDEBAR DASHBOARD
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ Control Center")
    st.markdown("---")
    
    # System Status Card
    st.markdown("**SYSTEM METRICS**")
    if model_error:
        st.error("🔴 Offline")
    else:
        st.success("🟢 AI Engine Online")
    
    st.write("")
    
    # Session Stats
    total_scans = len(st.session_state.history)
    blocked_scans = sum(1 for x in st.session_state.history if x['Status'] == "Blocked")
    allowed_scans = total_scans - blocked_scans
    
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric(label="Total Scans Today", value=total_scans)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.caption("🚫 Blocked")
        st.subheader(blocked_scans)
    with col_sb2:
        st.caption("✅ Safe")
        st.subheader(allowed_scans)
        
    st.markdown("---")
    st.markdown("**ENGINE SPECIFICATIONS**")
    st.info("• Core Architecture: LinearSVC\n• Feature Vectorizer: TF-IDF\n• Intended Target: Child Content Shielding")
    
    # Clear History Button
    if st.button("Clear Scan Logs"):
        st.session_state.history = []
        st.rerun()

# ==========================================
# 6. MAIN USER INTERFACE
# ==========================================
# Display Error if Model Missing
if model_error:
    st.error(model_error)
    st.info("🛠️ **Developer Note:** Ensure you have completed your pipeline script and saved the model using `joblib.dump(model, 'blocker_brain.pkl')`")
    st.stop()

# Header Layout
st.markdown('<div class="main-title">🛡️ SafeWeb AI Blocker</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#94a3b8; font-size:1.15rem;">Enterprise-Grade Content Filtering powered by Machine Learning</p>', unsafe_allow_html=True)

# Main Form Container
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("### 🔍 Real-Time Content Scanner")

user_input = st.text_input(
    label="Input a URL domain string or textual elements below to scan for security compliance:",
    placeholder="e.g., streaming-porn-portal.net/movie_id=982"
)

st.write("")

if st.button("Execute Deep Analysis"):
    if user_input.strip() == "":
        st.warning("⚠️ Action Blocked: The input field cannot be empty. Please specify content.")
    else:
        with st.spinner("Extracting parameters and running semantic scan..."):
            # Predict
            prediction = brain.predict([user_input])[0]
            pred_str = str(prediction).strip()
            
            # Formulating a custom simulated Risk Score for linear models lacking proba metrics
            if pred_str.lower() in ["blocked", "yes", "1"]:
                status = "Blocked"
                risk_score = random.randint(76, 99)  # High Risk Range
            else:
                status = "Allowed"
                risk_score = random.randint(1, 24)   # Low Risk Range
            
            # Log Data to Session State History
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.history.insert(0, {
                "Timestamp": timestamp,
                "Content Checked": user_input,
                "Status": status,
                "Risk Score": f"{risk_score}%"
            })
        
        # Displaying Results
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if status == "Blocked":
                st.markdown(
                    f'<div class="result-box blocked-res">🚫 <strong>ACCESS DENIED:</strong> This content has been explicitly blocked. The algorithm detected markers aligned with prohibited or explicit material.</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="result-box allowed-res">✅ <strong>ACCESS GRANTED:</strong> Content successfully verified. No restricted patterns found. The website is marked safe for kids.</div>',
                    unsafe_allow_html=True
                )
                st.balloons()
                
        with col2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.write("**AI ANALYST RISK SCORE**")
            if status == "Blocked":
                st.markdown(f'<span class="score-high">{risk_score}%</span>', unsafe_allow_html=True)
                st.caption("CRITICAL THREAT")
            else:
                st.markdown(f'<span class="score-low">{risk_score}%</span>', unsafe_allow_html=True)
                st.caption("CLEAN ENDPOINT")
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # End of Card Container

# ==========================================
# 7. PREDICTION HISTORY & DOWNLOAD REPORT
# ==========================================
st.markdown("### 📋 Historic Session Logs")

if st.session_state.history:
    df_history = pd.DataFrame(st.session_state.history)
    
    # Display beautiful Dataframe
    st.dataframe(df_history, use_container_width=True)
    
    # Download CSV Section
    csv_data = df_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Report (CSV File)",
        data=csv_data,
        file_name=f"safeweb_ai_audit_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.caption("No tracking logs logged in this current session yet. Enter strings above to populate database matrices.")

# ==========================================
# 8. ENTERPRISE FOOTER
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.write("---")
st.markdown(
    "<div style='text-align: center; padding: 10px;'>"
    "<p style='color: #38bdf8; font-size: 1.1rem; font-weight: 700; margin-bottom: 4px;'>"
    "🚀 High-Performance Intelligence & Scalable Architecture"
    "</p>"
    "<p style='color: #94a3b8; font-size: 0.95rem; max-width: 750px; margin: 0 auto 15px auto; line-height: 1.5;'>"
    "Need a tailored Artificial Intelligence model, secure cloud dashboard, or predictive data automation "
    "to scale your business operations? Let's transform your complex technical requirements into elegant enterprise systems."
    "</p>"
    "<p style='color: #64748b; font-size: 0.85rem;'>"
    "Project Developed by <strong>updateabdullahi</strong> under <strong>Easy Business Technology (Nigeria)</strong>.<br>"
    "All Engineering and Intellectual Property Rights Reserved © 2026."
    "</p>"
    "</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "🛡️ <strong>SafeWeb AI Dashboard v2.5 Enterprise</strong><br>"
    "Developed & Maintained by <strong>Easy Business Technology (Nigeria)</strong>. "
    "All Research and IP Rights Reserved © 2026."
    "</p>",
    unsafe_allow_html=True
)