import streamlit as st
from PyPDF2 import PdfReader
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import ollama
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

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
            text += extracted
    return text

def rel_text(text, text_size):
    words = text.split()
    texts = []
    for i in range(0, len(words), text_size):
        chunk = " ".join(words[i:i + text_size])
        texts.append(chunk)
    return texts

def embed_text(rel):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(rel)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    query = "Short definition based concepts"
    query_embd = model.encode([query])

    distance, indices = index.search(query_embd, 5)
    results = []
    for i in indices[0]:
        results.append(rel[i])

    return " ".join(results)

def generate_quest(context, duration, total_marks, num_questions):
    prompt = f"""
    Based on the following content:
    {context}

    Generate a question paper with:
    - Duration : {duration}
    - Total Marks: {total_marks}
    - Number of Questions: {num_questions}

    Divide the questions into:
    Section A 
    Section B 
    Section C 

    Instructions:
    - Section A → short definition-based questions
    - Section B → moderate explanation questions
    - Section C → long descriptive questions
    - Proper numbering (Q1, Q2...)
    - Maintain clean academic format
    """

    response = ollama.chat(
        model="llama3:latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def create_pdf(text, college):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{college}</b>", styles["Title"]))

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if "Section A" in line or "Section B" in line or "Section C" in line:
            story.append(Paragraph(f"<b>{line}</b>", styles["Normal"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)
    return temp_file.name

input_text = ""

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        input_text = extract_text_from_pdf(uploaded_file)

elif option == "Enter Text":
    input_text = st.text_area("Enter your text here")

if st.button("Generate Question Paper"):
    if input_text and college and duration:
        rel = rel_text(input_text, 50)
        context = embed_text(rel)
        result = generate_quest(context, duration, total_marks, num_questions)

        st.subheader("Generated Question Paper")
        st.text(result)

        pdf_path = create_pdf(result, college)

        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="question_paper.pdf")
    else:
        st.error("Please fill all inputs")