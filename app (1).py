import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

st.title("📚 AI-Powered Study Buddy")
st.markdown("Your personal AI assistant — explain topics, summarize notes, generate quizzes & answer from your PDFs!")
st.divider()

# ─── Load Models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_explainer():
    return pipeline("text2text-generation", model="google/flan-t5-small")

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")

explainer  = load_explainer()
summarizer = load_summarizer()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🔧 Choose Feature")
feature = st.sidebar.radio("Select a feature:", [
    "💡 Topic Explainer",
    "📝 Notes Summarizer",
    "❓ Quiz Generator",
    "📄 PDF Summarizer"
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
                prompt = f"Explain {topic} in simple terms:"
                result = explainer(prompt, max_new_tokens=200)
                explanation = result[0]["generated_text"]
            st.success("✅ Explanation:")
            st.write(explanation)

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
        elif len(notes.split()) < 30:
            st.warning("Notes are too short. Please paste at least 30 words.")
        else:
            with st.spinner("Summarizing..."):
                result = summarizer(notes, max_length=130, min_length=30, do_sample=False)
                summary = result[0]["summary_text"]
            st.success("✅ Summary:")
            st.write(summary)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 3 — Quiz Generator
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "❓ Quiz Generator":
    st.header("❓ Quiz Generator")
    st.write("Enter a topic and get 5 MCQ quiz questions!")

    topic = st.text_input("Enter a topic:", placeholder="e.g., Photosynthesis, Python basics")

    if st.button("Generate Quiz"):
        if topic.strip() == "":
            st.warning("Please enter a topic!")
        else:
            with st.spinner("Generating quiz..."):
                questions = []
                for i in range(1, 6):
                    prompt = f"Generate a multiple choice question about {topic} with 4 options A B C D and the answer:"
                    result = explainer(prompt, max_new_tokens=150)
                    questions.append(result[0]["generated_text"])

            st.success("✅ Quiz Generated!")
            for i, q in enumerate(questions, 1):
                with st.expander(f"Question {i}"):
                    st.write(q)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 4 — PDF Summarizer
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "📄 PDF Summarizer":
    st.header("📄 PDF Summarizer")
    st.write("Upload your study PDF and get a summary of the content!")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()

        st.success(f"✅ PDF loaded! ({len(full_text.split())} words extracted)")

        if st.button("Summarize PDF"):
            with st.spinner("Summarizing PDF..."):
                # Take first 800 words only (model limit)
                words = full_text.split()[:800]
                text_chunk = " ".join(words)
                result = summarizer(text_chunk, max_length=150, min_length=40, do_sample=False)
                summary = result[0]["summary_text"]
            st.success("✅ PDF Summary:")
            st.write(summary)
