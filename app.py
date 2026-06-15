import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

st.title("📚 AI-Powered Study Buddy")
st.markdown("Your personal AI assistant for studying — explain topics, summarize notes, generate quizzes & answer from your PDFs!")
st.divider()

# ─── Load Models (cached so they load only once) ───────────────────────────────
@st.cache_resource
def load_explainer():
    return pipeline("text2text-generation", model="google/flan-t5-base")

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

explainer   = load_explainer()
summarizer  = load_summarizer()
embedder    = load_embedder()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🔧 Choose Feature")
feature = st.sidebar.radio("Select a feature:", [
    "💡 Topic Explainer",
    "📝 Notes Summarizer",
    "❓ Quiz Generator",
    "📄 PDF Q&A (RAG)"
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
                prompt = f"Explain the topic '{topic}' in simple terms for a student:"
                result = explainer(prompt, max_new_tokens=300)
                explanation = result[0]["generated_text"]
            st.success("✅ Here's your explanation:")
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
                result = summarizer(notes, max_length=150, min_length=40, do_sample=False)
                summary = result[0]["summary_text"]
            st.success("✅ Summary:")
            st.write(summary)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 3 — Quiz Generator
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "❓ Quiz Generator":
    st.header("❓ Quiz Generator")
    st.write("Enter a topic and get 5 MCQ quiz questions to test yourself!")

    topic = st.text_input("Enter a topic for the quiz:", placeholder="e.g., Photosynthesis, World War 2, Python basics")

    if st.button("Generate Quiz"):
        if topic.strip() == "":
            st.warning("Please enter a topic!")
        else:
            with st.spinner("Generating quiz questions..."):
                questions = []
                for i in range(1, 6):
                    prompt = (
                        f"Generate MCQ question number {i} about '{topic}' with 4 options (A, B, C, D) "
                        f"and mention the correct answer at the end. Format: Question, A), B), C), D), Answer:"
                    )
                    result = explainer(prompt, max_new_tokens=200)
                    questions.append(result[0]["generated_text"])

            st.success("✅ Quiz Generated!")
            for i, q in enumerate(questions, 1):
                with st.expander(f"Question {i}"):
                    st.write(q)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 4 — PDF Q&A using RAG
# ═══════════════════════════════════════════════════════════════════════════════
elif feature == "📄 PDF Q&A (RAG)":
    st.header("📄 PDF Q&A — Ask Questions from Your Notes")
    st.write("Upload your study PDF and ask questions. The AI will answer based on your document!")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Extract text from PDF
        with st.spinner("Reading PDF..."):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()

        st.success(f"✅ PDF loaded! ({len(full_text.split())} words extracted)")

        # Chunk text
        def chunk_text(text, chunk_size=200):
            words = text.split()
            return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

        chunks = chunk_text(full_text)

        # Embed chunks and store in FAISS
        with st.spinner("Building knowledge base..."):
            embeddings = embedder.encode(chunks, convert_to_numpy=True)
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)

        st.info("📖 Knowledge base ready! Ask your question below.")

        question = st.text_input("Ask a question from the PDF:", placeholder="e.g., What is the main topic discussed?")

        if st.button("Get Answer"):
            if question.strip() == "":
                st.warning("Please enter a question!")
            else:
                with st.spinner("Finding answer..."):
                    # Retrieve top 3 relevant chunks
                    q_embedding = embedder.encode([question], convert_to_numpy=True)
                    distances, indices = index.search(q_embedding, k=3)
                    context = " ".join([chunks[i] for i in indices[0]])

                    # Generate answer
                    prompt = f"Based on the following context, answer the question:\nContext: {context}\nQuestion: {question}\nAnswer:"
                    result = explainer(prompt, max_new_tokens=200)
                    answer = result[0]["generated_text"]

                st.success("✅ Answer:")
                st.write(answer)

                with st.expander("📌 Context used to answer"):
                    st.write(context)
