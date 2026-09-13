import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ResolveAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(99,102,241,0.20), transparent 30%),
        radial-gradient(circle at 85% 15%, rgba(168,85,247,0.18), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(59,130,246,0.15), transparent 30%),
        #070914;
    color: white;
}

/* Hide Streamlit header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main container */
.block-container {
    max-width: 1100px;
    padding-top: 4rem;
    padding-bottom: 4rem;
}

/* Hero */
.hero {
    text-align: center;
    margin-bottom: 35px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 50px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    color: #c4b5fd;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 18px;
    box-shadow: 0 0 30px rgba(139,92,246,0.18);
}

.hero-title {
    font-size: 58px;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0;
    background: linear-gradient(90deg, #ffffff, #c4b5fd, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 12px;
    color: #a1a1aa;
    font-size: 18px;
}

/* Floating card */
.glass-card {
    background: rgba(17, 24, 39, 0.72);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 28px;
    padding: 32px;
    box-shadow:
        0 25px 80px rgba(0,0,0,0.45),
        0 0 60px rgba(99,102,241,0.10);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    margin-top: 20px;
}

/* Agent status */
.agent-status {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 25px;
}

.status-dot {
    width: 11px;
    height: 11px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 15px #22c55e;
}

.status-text {
    color: #d4d4d8;
    font-size: 14px;
    font-weight: 600;
}

/* Labels */
label {
    color: #d4d4d8 !important;
    font-weight: 600 !important;
}

/* Text area */
textarea {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 18px !important;
    color: white !important;
    font-size: 16px !important;
}

textarea:focus {
    border: 1px solid rgba(139,92,246,0.8) !important;
    box-shadow: 0 0 25px rgba(139,92,246,0.18) !important;
}

/* Text input */
input {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    color: white !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 58px;
    border-radius: 17px;
    border: 1px solid rgba(255,255,255,0.18);
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 17px;
    font-weight: 700;
    box-shadow:
        0 10px 35px rgba(99,102,241,0.35),
        inset 0 1px rgba(255,255,255,0.25);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow:
        0 15px 45px rgba(139,92,246,0.45),
        0 0 30px rgba(99,102,241,0.25);
}

/* Result card */
.result-card {
    margin-top: 25px;
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
}

.result-title {
    font-size: 13px;
    color: #a1a1aa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.result-status {
    font-size: 26px;
    font-weight: 800;
    margin-top: 5px;
    color: #c4b5fd;
}

.result-message {
    margin-top: 10px;
    color: #d4d4d8;
    line-height: 1.6;
}

/* Floating decorative circles */
.float-one,
.float-two,
.float-three {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}

.float-one {
    width: 180px;
    height: 180px;
    top: 18%;
    left: 4%;
    background: rgba(99,102,241,0.08);
    filter: blur(10px);
}

.float-two {
    width: 230px;
    height: 230px;
    bottom: 8%;
    right: 3%;
    background: rgba(168,85,247,0.08);
    filter: blur(15px);
}

.float-three {
    width: 90px;
    height: 90px;
    top: 55%;
    right: 12%;
    background: rgba(59,130,246,0.08);
    filter: blur(8px);
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 35px;
    color: #71717a;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- FLOATING BACKGROUND ----------------
st.markdown("""
<div class="float-one"></div>
<div class="float-two"></div>
<div class="float-three"></div>
""", unsafe_allow_html=True)


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">

<div class="hero-badge">
✦ AI-POWERED CUSTOMER RESOLUTION
</div>

<div class="hero-title">
🤖 ResolveAI
</div>

<div class="hero-subtitle">
Autonomous Customer Resolution Agent
</div>

</div>
""", unsafe_allow_html=True)


# ---------------- MAIN CARD ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("""
<div class="agent-status">
<div class="status-dot"></div>
<div class="status-text">ResolveAI Agent Online</div>
</div>
""", unsafe_allow_html=True)


query = st.text_area(
    "Customer Issue",
    placeholder="Describe your problem... Example: My headphones arrived damaged. I want a replacement.",
    height=170
)

user_id = st.text_input(
    "User ID",
    placeholder="Optional • e.g. user123"
)

st.write("")

# ---------------- RESOLVE ----------------
if st.button("🚀 Resolve Issue", type="primary"):

    if not query.strip():

        st.warning("Please describe your customer issue.")

    else:

        with st.spinner("ResolveAI is investigating your issue..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/api/resolve",
                    json={
                        "query": query,
                        "user_id": user_id
                    },
                    timeout=30
                )

                if response.status_code == 200:

                    data = response.json()

                    status = data["result"]["status"]
                    message = data["result"].get(
                        "message",
                         data["result"].get(
                             "final_response",
                              "Resolution completed successfully."
                             )
                        )

                    st.markdown(
                        f"""
                        <div class="result-card">

                        <div class="result-title">
                        Resolution Status
                        </div>

                        <div class="result-status">
                        {status.upper()}
                        </div>

                        <div class="result-message">
                        {message}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"Backend returned status code {response.status_code}"
                    )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to ResolveAI backend: {e}"
                )


st.markdown('</div>', unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
ResolveAI • Autonomous Customer Support • AI Resolution Engine
</div>
""", unsafe_allow_html=True)
