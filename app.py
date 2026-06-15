import streamlit as st
from groq import Groq
import fitz  # PyMuPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

st.title("📚 AI-Powered Study Buddy")
st.markdown("Your personal AI assistant — explain topics, summarize notes, generate quizzes & answer from your PDFs!")
st.divider()

# ─── Groq Client Setup ─────────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🔧 Choose Feature")
feature = st.sidebar.radio("Select a feature:", [
    "💡 Topic Explainer",
    "📝 Notes Summarizer",
    "❓ Quiz Generator",
    "📄 PDF Q&A"
])

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 1 — Topic Explainer
# ═══════════════════════════════════════════════════════════════════════════════
if feature == "💡 Topic Explainer":
    st.header("💡 Topic Explainer")
    st.write("Type any topic and get a simple, easy-to-understand explanation.")

    topic = st.text_input("Enter a topic:", placeholder="e.g., Photosynthesis, Newton's Laws, Machine Learning")

    if st.button("Explain"):
        if topic.strip() == "":
            st.warning("Please enter a topic!")
        else:
            with st.spinner("Generating explanation..."):
                prompt = f"Explain '{topic}' in very simple terms for a student. Keep it clear and easy to understand in 5-6 lines."
                result = ask_groq(prompt)
            st.success("✅ Explanation:")
            st.write(result)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 2 — Notes Summarizer
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "📝 Notes Summarizer":
    st.header("📝 Notes Summarizer")
    st.write("Paste your long study notes and get a concise summary.")

    notes = st.text_area("Paste your notes here:", height=250, placeholder="Paste your notes...")

    if st.button("Summarize"):
        if notes.strip() == "":
            st.warning("Please paste some notes!")
        elif len(notes.split()) < 20:
            st.warning("Notes too short! Please paste at least 20 words.")
        else:
            with st.spinner("Summarizing..."):
                prompt = f"Summarize the following study notes into 5 clear bullet points:\n\n{notes}"
                result = ask_groq(prompt)
            st.success("✅ Summary:")
            st.write(result)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 3 — Quiz Generator
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "❓ Quiz Generator":
    st.header("❓ Quiz Generator")
    st.write("Enter a topic and get 5 MCQ quiz questions!")

    topic = st.text_input("Enter a topic:", placeholder="e.g., Photosynthesis, Python basics, World War 2")

    if st.button("Generate Quiz"):
        if topic.strip() == "":
            st.warning("Please enter a topic!")
        else:
            with st.spinner("Generating quiz..."):
                prompt = f"""Generate 5 multiple choice questions about '{topic}'.
For each question provide:
- The question
- 4 options (A, B, C, D)
- The correct answer

Format each question clearly and number them 1-5."""
                result = ask_groq(prompt)
            st.success("✅ Quiz Generated!")
            st.write(result)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 4 — PDF Q&A
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "📄 PDF Q&A":
    st.header("📄 PDF Q&A")
    st.write("Upload your study PDF and ask questions from it!")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()

        st.success(f"✅ PDF loaded! ({len(full_text.split())} words extracted)")

        question = st.text_input("Ask a question from the PDF:", placeholder="e.g., What is the main topic?")

        if st.button("Get Answer"):
            if question.strip() == "":
                st.warning("Please enter a question!")
            else:
                with st.spinner("Finding answer..."):
                    context = full_text[:3000]
                    prompt = f"Based on the following text, answer this question: {question}\n\nText:\n{context}"
                    result = ask_groq(prompt)
                st.success("✅ Answer:")
                st.write(result)
