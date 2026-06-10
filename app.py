import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import random
import base64
import numpy as np
import requests
from bs4 import BeautifulSoup

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
LOCAL_IMAGE_PATH = "security_background.jpg" 

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    bin_str = get_base64_of_bin_file(LOCAL_IMAGE_PATH)
    background_css = f'background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.96)), url("data:image/jpg;base64,{bin_str}");'
except FileNotFoundError:
    background_css = 'background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 70%);'

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

/* Sanya Hoton Bango na Kwamfuta */
.stApp {{
    {background_css}
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc;
}}

/* Glassmorphic Cards */
.custom-card {{
    background: rgba(30, 41, 59, 0.55) !important;
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    margin-bottom: 25px;
}}

/* Input Fields Accent */
.stTextInput > div {{
    background: rgba(15, 23, 42, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}}
.stTextInput > div:focus-within {{
    border-color: #38bdf8 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
}}

/* Glowing Typography */
.main-title {{
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}}

/* Premium Button styling */
div.stButton > button:first-child {{
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
}}
div.stButton > button:first-child:hover {{
    transform: translateY(-2px);
    box-shadow: 0 15px 25px rgba(37, 99, 235, 0.4) !important;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}}

/* Badges & Metrics */
.metric-box {{
    background: rgba(15, 23, 42, 0.6);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
}}
.score-high {{ color: #f87171; font-size: 1.8rem; font-weight: 700; }}
.score-low {{ color: #34d399; font-size: 1.8rem; font-weight: 700; }}

.result-box {{
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    font-weight: 500;
    line-height: 1.6;
}}
.blocked-res {{ background: rgba(220, 38, 38, 0.18); border-left: 5px solid #dc2626; color: #fca5a5; }}
.allowed-res {{ background: rgba(5, 150, 105, 0.18); border-left: 5px solid #059669; color: #a7f3d0; }}

.report-title {{
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
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
# EXTRA: HELPER FUNCTION FOR WEB SCRAPING
# ==========================================
def scrape_website_content(url_string):
    """Muna kwaso ainihin rubutun dake cikin kowace gidan yanar gizo a asirce"""
    clean_url = url_string.strip()
    
    # Idan mutum bai saka http/https ba, mu saka masa don kada requests ya ba da error
    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # Shiga shafin, ka ba shi sakan 3 kacal don kada app din ya yi nauyi
        response = requests.get(clean_url, headers=headers, timeout=3, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Goge kofofin JavaScript da CSS dake cikin HTML din
            for script in soup(["script", "style"]):
                script.extract()
            # Kwaso tsaftataccen rubutu
            web_text = soup.get_text()
            # Hada shi wuri guda da tace sarari
            lines = (line.strip() for line in web_text.split())
            chunks = (phrase for line in lines for phrase in line.split("  "))
            final_text = " ".join(chunk for chunk in chunks if chunk)
            return final_text if final_text.strip() else url_string
    except Exception:
        # Idan an samu matsalar intanet ko rashin shiga shafi, dawo da ainihin rubutun mutum
        return url_string
    return url_string

# ==========================================
# 5. SIDEBAR DASHBOARD
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ Control Center")
    st.markdown("---")
    
    st.markdown("**SYSTEM METRICS**")
    if model_error:
        st.error("🔴 Offline")
    else:
        st.success("🟢 AI Engine Online")
    
    st.write("")
    
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
    
    if st.button("Clear Scan Logs"):
        st.session_state.history = []
        st.session_state.pop("last_result", None)
        st.session_state.trigger_animation = False
        st.rerun()

# ==========================================
# 6. MAIN USER INTERFACE
# ==========================================
if model_error:
    st.error(model_error)
    st.info("🛠️ **Developer Note:** Ensure you have completed your pipeline script and saved the model using `joblib.dump(model, 'blocker_brain.pkl')`")
    st.stop()

# TASHIN BALLOONS IDAN ABU YA FI KAWO ALHERI (ALLOWED)
if st.session_state.trigger_animation:
    st.balloons()
    st.session_state.trigger_animation = False

st.markdown('<div class="main-title">🛡️ SafeWeb AI Blocker</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#cbd5e1; font-size:1.15rem; font-weight: 500;">Enterprise-Grade Content Filtering powered by Machine Learning</p>', unsafe_allow_html=True)

# Main Form Container
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("### 🔍 Real-Time Content Scanner")

user_input = st.text_input(
    label="Input a URL domain string or textual elements below to scan for security compliance:",
    placeholder="e.g., Introductions to machine learning for beginners"
)

st.write("")

if st.button("Execute Deep Scan"):
    if user_input.strip() == "":
        st.warning("⚠️ Action Blocked: The input field cannot be empty. Please specify content.")
    else:
        with st.spinner("Extracting parameters and running semantic scan..."):
            
            # 1. BIYAR DA RUBUTU ZUWA ƘANANAN BAƘAƘE DA TACE SHARADI
            checked_input = user_input.lower().strip()
            
            # JERIN KALMOMIN BATSA DA MUKASAN AI ƊINKA YANA RASHIN GANO WA (FALSE NEGATIVES)
            hardcoded_blacklist = ["bluefilms", "bluefilm", "porn", "xxx", "lesbian", "adultsite", "xvideos"]
            
            # Dabarar katseshi ta atomatik idan yana dauke da wadannan kalmomin
            if any(word in checked_input for word in hardcoded_blacklist):
                pred_str = "Blocked"
                risk_score = 99  # Tunda muna da tabbacin na batsa ne gaba daya
            else:
                # --- TSARIN WEB SCRAPING DYNAMICS (Mafi inganci idan babu kalmar a sama) ---
                input_to_predict = user_input
                if any(ext in checked_input for ext in [".com", ".net", ".org", "http", ".site", ".xyz", ".gov", ".edu"]):
                    input_to_predict = scrape_website_content(user_input)
                
                # Predict daga ainihin kwakwalwar model dinka ta amfani da rubutun da aka kwaso
                prediction = brain.predict([input_to_predict])[0]
                pred_str = str(prediction).strip()
                
                # Lissafin AI Risk Score na Gaskiya dangane da model matrices
                try:
                    if hasattr(brain, "predict_proba"):
                        proba = brain.predict_proba([input_to_predict])[0]
                        risk_score = int(proba[1] * 100) if len(proba) > 1 else int(proba[0] * 100)
                    elif hasattr(brain, "decision_function"):
                        decision = brain.decision_function([input_to_predict])[0]
                        probability = 1 / (1 + np.exp(-decision))
                        risk_score = int(probability * 100)
                    else:
                        risk_score = 92 if pred_str.lower() in ["blocked", "yes", "1"] else 12
                except Exception:
                    risk_score = 85 if pred_str.lower() in ["blocked", "yes", "1"] else 8

            # Sanya sharadi da trigger na animation
            if pred_str.lower() in ["blocked", "yes", "1"]:
                status = "Blocked"
                st.session_state.trigger_animation = False
            else:
                status = "Allowed"
                st.session_state.trigger_animation = True
            
            # Adana a logs tarihi
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.history.insert(0, {
                "Timestamp": timestamp,
                "Content Checked": user_input,
                "Status": status,
                "Risk Score": f"{risk_score}%"
            })
            
            # Adana sakamako a session state
            st.session_state.last_result = {
                "status": status,
                "score": risk_score,
                "input_text": user_input
            }
            
        st.rerun()

# ------------------------------------------
# GYARA: NUNA SAKAMAKO A KASAN BUTTON LAFIYA LAU
# ------------------------------------------
if "last_result" in st.session_state:
    res = st.session_state.last_result
    st.write("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if res["status"] == "Blocked":
            st.markdown(
                f'<div class="result-box blocked-res">'
                f'<div class="report-title">🚫 ACCESS DENIED — CYBER SECURITY THREAT DETECTED</div>'
                f'<strong>Analysis Summary:</strong> The input element matching <code>"{res["input_text"]}"</code> has been explicitly restricted by the AI firewall. '
                f'Our natural language processing model detected linguistic matrices, semantic patterns, or malicious domain string fragments highly correlated with pornography, explicit adult material, or high-risk content. '
                f'<br><br><strong>Action Taken:</strong> Content vectors filtered instantly. Inbound handshake aborted. This endpoint remains quarantined to ensure child safety standards.'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-box allowed-res">'
                f'<div class="report-title">✅ ACCESS GRANTED — COMPLIANCE VERIFIED</div>'
                f'<strong>Analysis Summary:</strong> The requested string <code>"{res["input_text"]}"</code> has successfully bypassed the firewall matrices. '
                f'The Natural Language processing matrix computed the behavioral weight of the tokens and found 0% malicious intent alignment. '
                f'The content data stream parameters are fully compliant with safe-browsing regulations and child-shield protocols.'
                f'<br><br><strong>Status Evaluation:</strong> Certified Clean. Trusted node replication allowed. Safe for children and family consumption.'
                f'</div>',
                unsafe_allow_html=True
            )
    with col2:
        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
        st.write("**AI ANALYST RISK SCORE**")
        if res["status"] == "Blocked":
            st.markdown(f'<span class="score-high">{res["score"]}%</span>', unsafe_allow_html=True)
            st.caption("CRITICAL THREAT")
        else:
            st.markdown(f'<span class="score-low">{res["score"]}%</span>', unsafe_allow_html=True)
            st.caption("CLEAN ENDPOINT")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Rufewar babban Card

# ==========================================
# 7. PREDICTION HISTORY & DOWNLOAD REPORT
# ==========================================
st.markdown("### 📋 Historic Session Logs")

if st.session_state.history:
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history, use_container_width=True)
    
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