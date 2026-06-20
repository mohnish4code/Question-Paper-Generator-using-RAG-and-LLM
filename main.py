from PyPDF2 import PdfReader
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def credentials():
    college = input("Enter College Name: ")
    duration = input("Enter Time Duration (e.g., 3 Hours): ")
    total_marks = int(input("Enter Total Marks: "))
    num_questions = int(input("Enter Number of Questions: "))
    return college, duration, total_marks, num_questions

def enter_choices():
    choice = input("Enter the choice for the format(pdf(1)/text(2)): ")

    if choice == "1":
        file_name = input("Enter PDF file path: ")
        return extract_text_from_pdf(file_name)

    elif choice == "2":
        return input("Enter text: ")

    else:
        print("Enter a valid choice")
        return enter_choices()

def extract_text_from_pdf(file_name):
    reader = PdfReader(file_name)

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

def question_paper(text, filename, college):

    doc = SimpleDocTemplate(filename)

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
            story.append(
                Paragraph(
                    f"<b>{line}</b>",
                    styles["Heading2"]
                )
            )

        else:
            story.append(
                Paragraph(
                    line,
                    styles["Normal"]
                )
            )

        story.append(Spacer(1, 6))

    doc.build(story)

    print("Question paper PDF saved successfully.")

college, duration, total_marks, num_questions = credentials()

text = enter_choices()

rel = rel_text(text, 50)

context = embed_text(rel)

result = generate_quest(
    context,
    duration,
    total_marks,
    num_questions
)

print("\nGenerated Question Paper:\n")
print(result)

output_file = input(
    "\nEnter filename to save (e.g., qp.pdf): "
)

question_paper(
    result,
    output_file,
    college
)