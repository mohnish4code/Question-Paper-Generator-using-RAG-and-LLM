import streamlit as st
from PyPDF2 import PdfReader
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("AI Question Paper Generator")

college = st.text_input("Enter College Name")
duration = st.text_input("Enter Time Duration (e.g., 3 Hours)")
total_marks = st.number_input("Enter Total Marks", min_value=1, step=1)
num_questions = st.number_input("Enter Number of Questions", min_value=1, step=1)

option = st.radio("Choose Input Type", ["Upload PDF", "Enter Text"])

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "

    return text

def rel_text(text, text_size):
    words = text.split()
    texts = []

    for i in range(0, len(words), text_size):
        chunk = " ".join(words[i:i + text_size])
        texts.append(chunk)

    return texts

def embed_text(rel):
    embeddings = embedding_model.encode(rel)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))

    query = "Important topics for examination questions"
    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding, dtype=np.float32),
        min(5, len(rel))
    )

    results = [rel[i] for i in indices[0]]

    return " ".join(results)

def generate_quest(context, duration, total_marks, num_questions):
    prompt = f"""
Based on the following content:

{context}

Generate a professional university-level question paper.

Requirements:
- Duration: {duration}
- Total Marks: {total_marks}
- Number of Questions: {num_questions}

Structure:

SECTION A
- Short definition-based questions

SECTION B
- Medium-length explanation questions

SECTION C
- Long descriptive and analytical questions

Instructions:
- Use proper academic formatting
- Use question numbering
- Distribute questions appropriately across sections
- Ensure questions are relevant to the provided content
- Include marks allocation where appropriate
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating question paper: {str(e)}"

def create_pdf(text, college):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph(f"<b>{college}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if (
            "SECTION A" in line.upper()
            or "SECTION B" in line.upper()
            or "SECTION C" in line.upper()
        ):
            story.append(Paragraph(f"<b>{line}</b>", styles["Heading2"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))

        story.append(Spacer(1, 6))

    doc.build(story)

    return temp_file.name

input_text = ""

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        input_text = extract_text_from_pdf(uploaded_file)

else:
    input_text = st.text_area("Enter your text here")

if st.button("Generate Question Paper"):
    if input_text and college and duration:

        rel = rel_text(input_text, 50)

        context = embed_text(rel)

        with st.spinner("Generating Question Paper..."):
            result = generate_quest(
                context,
                duration,
                total_marks,
                num_questions
            )

        st.subheader("Generated Question Paper")
        st.markdown(result)

        pdf_path = create_pdf(result, college)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="question_paper.pdf",
                mime="application/pdf"
            )

    else:
        st.error("Please fill all inputs and provide content.")