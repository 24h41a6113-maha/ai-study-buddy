import streamlit as st
from groq import Groq
import fitz
import time

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

# ─── Custom CSS + Animations ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.stApp {
    background: #000011;
    background-image: 
        radial-gradient(ellipse at 20% 50%, rgba(120, 40, 200, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 200, 255, 0.1) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(255, 50, 100, 0.08) 0%, transparent 50%);
}

.hero-container {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00ffff, #bf00ff, #ff0066, #00ffff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 4s ease infinite;
    text-shadow: none;
    letter-spacing: 2px;
}

.hero-sub {
    color: #8892b0;
    font-size: 1.15rem;
    margin-top: 0.5rem;
    letter-spacing: 1px;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 255, 0.3); }
    50% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 0 60px rgba(191, 0, 255, 0.4); }
}

@keyframes borderGlow {
    0%, 100% { border-color: #00ffff; }
    33% { border-color: #bf00ff; }
    66% { border-color: #ff0066; }
}

.stat-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    color: white;
    animation: fadeInUp 0.6s ease forwards, pulse 3s ease infinite;
    transition: all 0.3s;
    backdrop-filter: blur(10px);
}
.stat-card:hover {
    transform: translateY(-5px) scale(1.03);
    border-color: #bf00ff;
    box-shadow: 0 10px 40px rgba(191, 0, 255, 0.4);
}
.stat-card .icon { font-size: 2rem; }
.stat-card .title { font-weight: 700; color: #00ffff; font-size: 1.1rem; }
.stat-card .desc { color: #8892b0; font-size: 0.85rem; }

.feature-header {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00ffff;
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    margin-bottom: 1rem;
    animation: fadeInUp 0.4s ease;
}

.feature-desc {
    background: linear-gradient(135deg, rgba(0,255,255,0.05), rgba(191,0,255,0.05));
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #ccd6f6;
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
    animation: fadeInUp 0.5s ease;
    animation: borderGlow 3s ease infinite;
}

.result-box {
    background: linear-gradient(135deg, rgba(0,20,40,0.9), rgba(20,0,40,0.9));
    border: 1px solid #00ffff;
    border-radius: 16px;
    padding: 1.8rem;
    color: #ccd6f6;
    font-size: 1.05rem;
    line-height: 1.8;
    animation: fadeInUp 0.5s ease;
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.15), inset 0 0 30px rgba(0,0,0,0.5);
    white-space: pre-wrap;
}

.stButton > button {
    background: linear-gradient(90deg, #bf00ff, #00ffff, #ff0066);
    background-size: 200% 200%;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 0.7rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 1px;
    transition: all 0.3s !important;
    animation: gradientShift 3s ease infinite;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 30px rgba(191, 0, 255, 0.7), 0 0 60px rgba(0, 255, 255, 0.3) !important;
}

.stTextInput > div > input, .stTextArea > div > textarea {
    background: rgba(0, 20, 40, 0.8) !important;
    color: #ccd6f6 !important;
    border: 1px solid rgba(0, 255, 255, 0.3) !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
}
.stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
    border-color: #00ffff !important;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #000022, #0a0015) !important;
    border-right: 1px solid rgba(0, 255, 255, 0.2);
}

.sidebar-title {
    font-family: 'Orbitron', monospace;
    color: #00ffff;
    font-size: 1.1rem;
    text-align: center;
    padding: 0.5rem;
    text-shadow: 0 0 10px rgba(0,255,255,0.5);
}

.footer {
    text-align: center;
    color: #495670;
    font-size: 0.9rem;
    padding: 1rem;
    border-top: 1px solid rgba(0,255,255,0.1);
    margin-top: 2rem;
}


.mascot-body {
    font-size: 5rem;
    animation: mascotFloat 3s ease-in-out infinite;
    filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.8));
    display: inline-block;
}

.mascot-bubble {
    background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(191,0,255,0.1));
    border: 1px solid rgba(0,255,255,0.4);
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    color: #00ffff;
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.5rem;
    animation: bubblePulse 2s ease-in-out infinite;
    display: inline-block;
}

@keyframes mascotFloat {
    0%, 100% { transform: translateY(0px) rotate(-3deg); }
    25% { transform: translateY(-15px) rotate(3deg); }
    50% { transform: translateY(-8px) rotate(-2deg); }
    75% { transform: translateY(-18px) rotate(4deg); }
}

@keyframes bubblePulse {
    0%, 100% { opacity: 0.8; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}

div[data-baseweb="radio"] label {
    color: #8892b0 !important;
    font-size: 1rem !important;
}

.success-badge {
    display: inline-block;
    background: linear-gradient(90deg, #00ffff20, #bf00ff20);
    border: 1px solid #00ffff;
    border-radius: 20px;
    padding: 0.3rem 1rem;
    color: #00ffff;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚡ AI STUDY BUDDY ⚡</div>
    <div class="hero-sub">🚀 Your intelligent study companion powered by LLaMA 3.3 70B</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin: 0.5rem 0 1.5rem 0;">
    <div class="mascot-body">🦉</div><br>
    <div class="mascot-bubble">✨ Hoot! I am Owly — your wise AI Study Buddy!</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Stat Cards ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-card"><div class="icon">💡</div><div class="title">EXPLAINER</div><div class="desc">Instant topic explanations</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-card"><div class="icon">📝</div><div class="title">SUMMARIZER</div><div class="desc">Condense your notes</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat-card"><div class="icon">❓</div><div class="title">QUIZ GEN</div><div class="desc">Auto MCQ creation</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="stat-card"><div class="icon">📄</div><div class="title">PDF Q&A</div><div class="desc">Ask from your PDFs</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Clickable Feature Selector ────────────────────────────────────────────────
st.markdown('<div style="text-align:center; color:#00ffff; font-size:1.1rem; font-weight:700; margin-bottom:1rem; letter-spacing:1px;">👇 SELECT A FEATURE TO GET STARTED</div>', unsafe_allow_html=True)

if "feature" not in st.session_state:
    st.session_state.feature = "💡 Topic Explainer"

btn1, btn2, btn3, btn4 = st.columns(4)
with btn1:
    if st.button("💡 Topic Explainer"):
        st.session_state.feature = "💡 Topic Explainer"
with btn2:
    if st.button("📝 Notes Summarizer"):
        st.session_state.feature = "📝 Notes Summarizer"
with btn3:
    if st.button("❓ Quiz Generator"):
        st.session_state.feature = "❓ Quiz Generator"
with btn4:
    if st.button("📄 PDF Q&A"):
        st.session_state.feature = "📄 PDF Q&A"

feature = st.session_state.feature

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ─── Groq ──────────────────────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content

def type_writer(text, placeholder):
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(f'<div class="result-box">{displayed}▌</div>', unsafe_allow_html=True)
        time.sleep(0.008)
    placeholder.markdown(f'<div class="result-box">{displayed}</div>', unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎯 FEATURES</div>', unsafe_allow_html=True)
    st.markdown("---")
    feature = st.radio("", [
        "💡 Topic Explainer",
        "📝 Notes Summarizer",
        "❓ Quiz Generator",
        "📄 PDF Q&A"
    ])
    st.markdown("---")
    st.markdown('<div style="color:#00ffff; font-weight:700; font-size:1rem;">📖 How to Use</div>', unsafe_allow_html=True)
    if feature == "💡 Topic Explainer":
        st.markdown('<div style="color:#8892b0; font-size:0.9rem;">1️⃣ Type any topic in the box<br><br>2️⃣ Click <b style="color:#00ffff;">EXPLAIN NOW</b><br><br>3️⃣ Read your AI explanation!</div>', unsafe_allow_html=True)
    elif feature == "📝 Notes Summarizer":
        st.markdown('<div style="color:#8892b0; font-size:0.9rem;">1️⃣ Paste your study notes in the text box<br><br>2️⃣ Click <b style="color:#00ffff;">SUMMARIZE NOW</b><br><br>3️⃣ Get 5 bullet point summary!</div>', unsafe_allow_html=True)
    elif feature == "❓ Quiz Generator":
        st.markdown('<div style="color:#8892b0; font-size:0.9rem;">1️⃣ Type a topic you want to practice<br><br>2️⃣ Click <b style="color:#00ffff;">GENERATE QUIZ</b><br><br>3️⃣ Answer 5 MCQ questions!</div>', unsafe_allow_html=True)
    elif feature == "📄 PDF Q&A":
        st.markdown('<div style="color:#8892b0; font-size:0.9rem;">1️⃣ Upload your PDF file<br><br>2️⃣ Type your question<br><br>3️⃣ Click <b style="color:#00ffff;">GET ANSWER</b><br><br>4️⃣ AI answers from your PDF!</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="color:#495670; font-size:0.85rem; text-align:center;">🤖 Groq API<br>⚡ LLaMA 3.3 70B<br>🌐 Streamlit Cloud</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
if feature == "💡 Topic Explainer":
    st.markdown('<div class="feature-header">💡 TOPIC EXPLAINER</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">🔍 Type any topic — get a simple, student-friendly AI explanation with real-life examples!</div>', unsafe_allow_html=True)
    topic = st.text_input("", placeholder="e.g., Photosynthesis, Machine Learning, Quantum Physics, Blockchain...")
    if st.button("⚡ EXPLAIN NOW"):
        if topic.strip() == "":
            st.warning("⚠️ Please enter a topic!")
        else:
            with st.spinner("🤖 AI is generating explanation..."):
                result = ask_groq(f"Explain '{topic}' in simple terms for a student. Use easy language, give a real-life example, and keep it 6-8 lines.")
            st.markdown('<div class="success-badge">✅ Explanation Ready!</div>', unsafe_allow_html=True)
            placeholder = st.empty()
            type_writer(result, placeholder)

elif feature == "📝 Notes Summarizer":
    st.markdown('<div class="feature-header">📝 NOTES SUMMARIZER</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">📋 Paste your long notes — get crisp bullet-point summary in seconds!</div>', unsafe_allow_html=True)
    notes = st.text_area("", height=200, placeholder="Paste your study notes here...")
    if st.button("⚡ SUMMARIZE NOW"):
        if notes.strip() == "":
            st.warning("⚠️ Please paste some notes!")
        elif len(notes.split()) < 20:
            st.warning("⚠️ Too short! Please paste at least 20 words.")
        else:
            with st.spinner("🤖 AI is summarizing..."):
                result = ask_groq(f"Summarize these study notes into 5 clear bullet points. Be concise:\n\n{notes}")
            st.markdown('<div class="success-badge">✅ Summary Ready!</div>', unsafe_allow_html=True)
            placeholder = st.empty()
            type_writer(result, placeholder)

elif feature == "❓ Quiz Generator":
    st.markdown('<div class="feature-header">❓ QUIZ GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">🎯 Enter any topic — get 5 MCQ questions to test your knowledge!</div>', unsafe_allow_html=True)
    topic = st.text_input("", placeholder="e.g., Photosynthesis, Python basics, Indian History...")
    if st.button("🎲 GENERATE QUIZ"):
        if topic.strip() == "":
            st.warning("⚠️ Please enter a topic!")
        else:
            with st.spinner("🤖 AI is creating your quiz..."):
                result = ask_groq(f"Generate 5 MCQ questions about '{topic}'. For each: question, 4 options (A B C D), correct answer. Number 1-5.")
            st.markdown('<div class="success-badge">✅ Quiz Ready! Good Luck! 🍀</div>', unsafe_allow_html=True)
            st.balloons()
            placeholder = st.empty()
            type_writer(result, placeholder)

elif feature == "📄 PDF Q&A":
    st.markdown('<div class="feature-header">📄 PDF Q&A</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">📁 Upload your study PDF — ask any question and AI answers from your document!</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("📖 Reading PDF..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            full_text = "".join([page.get_text() for page in doc])
        st.markdown(f'<div class="success-badge">✅ PDF Loaded! {len(full_text.split())} words extracted</div>', unsafe_allow_html=True)
        question = st.text_input("", placeholder="Ask anything from your PDF...")
        if st.button("🔍 GET ANSWER"):
            if question.strip() == "":
                st.warning("⚠️ Please enter a question!")
            else:
                with st.spinner("🤖 Finding answer from your PDF..."):
                    result = ask_groq(f"Based on this text, answer: {question}\n\nText:\n{full_text[:3000]}")
                st.markdown('<div class="success-badge">✅ Answer Found!</div>', unsafe_allow_html=True)
                placeholder = st.empty()
                type_writer(result, placeholder)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">⚡ Made with ❤️ by <b>Chellingi Kanaka Durga MahaLakshmi</b> | Bonam Venkata Chalamayya Institute of Technology and Science | IBM Edunet Internship 2024</div>', unsafe_allow_html=True)
