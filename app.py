import streamlit as st
from groq import Groq
import fitz  # PyMuPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%); }
    
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-sub {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #1e1e3a, #2d2d5e);
        border: 1px solid #4a4a8a;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .feature-card:hover { border-color: #00d4ff; }
    .result-box {
        background: linear-gradient(135deg, #0d2137, #0d3726);
        border-left: 4px solid #00d4ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        color: #e2e8f0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #7b2ff7, #00d4ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 4px 20px rgba(123, 47, 247, 0.5);
    }
    .stTextInput > div > input, .stTextArea > div > textarea {
        background-color: #1e1e3a;
        color: #e2e8f0;
        border: 1px solid #4a4a8a;
        border-radius: 10px;
    }
    .stRadio > div { color: #e2e8f0; }
    .sidebar .sidebar-content { background: #1a1a2e; }
    h1, h2, h3 { color: #e2e8f0; }
    .stat-box {
        background: linear-gradient(135deg, #2d1b69, #11998e);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">📚 AI Study Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Your personal AI-powered assistant for smarter studying 🚀</div>', unsafe_allow_html=True)

# ─── Stats Row ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-box">💡<br><b>Topic Explainer</b><br>Instant AI explanations</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-box">📝<br><b>Summarizer</b><br>Condense your notes</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box">❓<br><b>Quiz Generator</b><br>Auto MCQ creation</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-box">📄<br><b>PDF Q&A</b><br>Ask from your PDFs</div>', unsafe_allow_html=True)

st.divider()

# ─── Groq Client Setup ─────────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🎯 Choose Feature")
st.sidebar.markdown("---")
feature = st.sidebar.radio("", [
    "💡 Topic Explainer",
    "📝 Notes Summarizer",
    "❓ Quiz Generator",
    "📄 PDF Q&A"
])
st.sidebar.markdown("---")
st.sidebar.markdown("**🤖 Powered by**")
st.sidebar.markdown("Groq API + LLaMA 3.3 70B")
st.sidebar.markdown("**⚡ Ultra-fast AI responses**")

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 1 — Topic Explainer
# ═══════════════════════════════════════════════════════════════════════════════
if feature == "💡 Topic Explainer":
    st.markdown("## 💡 Topic Explainer")
    st.markdown('<div class="feature-card">Type any topic and get a simple, clear AI-powered explanation instantly!</div>', unsafe_allow_html=True)
    st.markdown("")

    topic = st.text_input("🔍 Enter a topic:", placeholder="e.g., Photosynthesis, Newton's Laws, Machine Learning, Blockchain...")

    if st.button("✨ Explain Now"):
        if topic.strip() == "":
            st.warning("⚠️ Please enter a topic!")
        else:
            with st.spinner("🤖 AI is thinking..."):
                prompt = f"Explain '{topic}' in very simple terms for a student. Use easy language, give a real-life example, and keep it within 6-8 lines."
                result = ask_groq(prompt)
            st.markdown(f'<div class="result-box">✅ <b>Explanation:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 2 — Notes Summarizer
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "📝 Notes Summarizer":
    st.markdown("## 📝 Notes Summarizer")
    st.markdown('<div class="feature-card">Paste your long study notes and get a crisp, bullet-point summary in seconds!</div>', unsafe_allow_html=True)
    st.markdown("")

    notes = st.text_area("📋 Paste your notes here:", height=200, placeholder="Paste your study notes here...")

    if st.button("⚡ Summarize Now"):
        if notes.strip() == "":
            st.warning("⚠️ Please paste some notes!")
        elif len(notes.split()) < 20:
            st.warning("⚠️ Notes too short! Please paste at least 20 words.")
        else:
            with st.spinner("🤖 Summarizing your notes..."):
                prompt = f"Summarize the following study notes into 5 clear bullet points. Make it concise and easy to remember:\n\n{notes}"
                result = ask_groq(prompt)
            st.markdown(f'<div class="result-box">✅ <b>Summary:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 3 — Quiz Generator
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "❓ Quiz Generator":
    st.markdown("## ❓ Quiz Generator")
    st.markdown('<div class="feature-card">Enter any topic and get 5 MCQ questions to test your knowledge instantly!</div>', unsafe_allow_html=True)
    st.markdown("")

    topic = st.text_input("🎯 Enter a topic for the quiz:", placeholder="e.g., Photosynthesis, Python basics, World War 2...")

    if st.button("🎲 Generate Quiz"):
        if topic.strip() == "":
            st.warning("⚠️ Please enter a topic!")
        else:
            with st.spinner("🤖 Creating your quiz..."):
                prompt = f"""Generate 5 multiple choice questions about '{topic}'.
For each question:
- Write the question clearly
- Give 4 options (A, B, C, D)
- Mention the correct answer at the end

Number them 1 to 5. Make questions educational and interesting."""
                result = ask_groq(prompt)
            st.markdown(f'<div class="result-box">✅ <b>Your Quiz:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 4 — PDF Q&A
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "📄 PDF Q&A":
    st.markdown("## 📄 PDF Q&A")
    st.markdown('<div class="feature-card">Upload your study PDF and ask any question — AI will answer from your document!</div>', unsafe_allow_html=True)
    st.markdown("")

    uploaded_file = st.file_uploader("📁 Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("📖 Reading your PDF..."):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()

        st.success(f"✅ PDF loaded successfully! ({len(full_text.split())} words extracted)")

        question = st.text_input("❓ Ask a question from the PDF:", placeholder="e.g., What is the main topic? Summarize chapter 1...")

        if st.button("🔍 Get Answer"):
            if question.strip() == "":
                st.warning("⚠️ Please enter a question!")
            else:
                with st.spinner("🤖 Finding your answer..."):
                    context = full_text[:3000]
                    prompt = f"Based on the following text, answer this question clearly: {question}\n\nText:\n{context}"
                    result = ask_groq(prompt)
                st.markdown(f'<div class="result-box">✅ <b>Answer:</b><br><br>{result}</div>', unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown('<p style="text-align:center; color:#4a4a8a;">Made with ❤️ by Chellingi Kanaka Durga MahaLakshmi | BVCITS | IBM Edunet Internship 2024</p>', unsafe_allow_html=True)
  
