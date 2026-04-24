📄 AI Question Paper Generator

This project generates a structured academic question paper from either a PDF or user-provided text using RAG and LLMs. It automatically extracts relevant content, identifies important concepts, and formats questions into different sections.

🚀 Features

Upload a PDF or enter text manually
Extracts and processes content intelligently
Uses embeddings to find important topics
Generates a complete question paper using LLM
Divides questions into:
Section A (Short questions)
Section B (Moderate questions)
Section C (Descriptive questions)
Download the generated question paper as a PDF
Simple Streamlit-based UI

🛠️ Tech Stack

Python
Streamlit
PyPDF2
Sentence Transformers
FAISS / Similarity Search
Ollama (LLM - Llama3)
ReportLab

📂 Project Structure
├── app.py                # Streamlit application
├── requirements.txt     # Dependencies
├── README.md            # Project documentation

⚙️ How It Works
User uploads a PDF or enters text
Text is split into smaller chunks
Each chunk is converted into embeddings
Relevant chunks are retrieved using similarity search
A prompt is generated using this context
LLM (Llama3 via Ollama) generates the question paper
Output is displayed and can be downloaded as a PDF

📌 Notes
Works best with Python 3.10 / 3.11
Requires Ollama running locally
FAISS may have compatibility issues on Windows, alternative similarity methods can be used

🔮 Future Improvements

Better question difficulty control
Multiple subject support
Export in different formats (DOCX, TXT)
Deployment on cloud

👨‍💻 Author
Mohnish Shandilya