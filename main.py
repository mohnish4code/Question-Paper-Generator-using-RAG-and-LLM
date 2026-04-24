from PyPDF2 import PdfReader
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import ollama
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def credentials():
    college = input("Enter College Name: ")
    duration = input("Enter Time Duration (e.g., 3 Hours): ")
    total_marks = int(input("Enter Total Marks: "))
    num_questions = int(input("Enter Number of Questions: "))
    return college, duration, total_marks, num_questions

def enter_choices():
    e = input("Enter the choice for the format(pdf(1)/text(2)) : ")
    if e == "1":
        file_name = input("Enter PDF file path: ")
        return extract_text_from_pdf(file_name)
    elif e == "2":
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

def question_paper(t, filename, college):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{college}</b>", styles["Title"]))

    lines = t.split("\n")
    for line in lines:
        line = line.strip()
        if "Section A" in line or "Section B" in line or "Section C" in line:
            story.append(Paragraph(f"<b>{line}</b>", styles["Normal"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)
    print("Your pdf is saved")

college, duration, total_marks, num_questions = credentials()
text = enter_choices()
rel = rel_text(text, 50)
context = embed_text(rel)

result = generate_quest(context, duration, total_marks, num_questions)
print(result)

output_file = input("Enter filename to save (e.g., qp.pdf): ")
question_paper(result, output_file, college)