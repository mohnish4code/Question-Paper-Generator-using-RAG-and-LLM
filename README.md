# AI Question Paper Generator using RAG and LLM

## Overview

The AI Question Paper Generator is a Retrieval-Augmented Generation (RAG) based application that automatically generates academic question papers from study materials. Users can either upload PDF documents or provide textual content directly. The system retrieves the most relevant information from the provided content using semantic search and generates a structured question paper using a Large Language Model (LLM).

The generated question paper is organized into multiple sections based on question difficulty levels and can be downloaded as a PDF.

---

## Features

* Upload PDF documents or enter text manually.
* Automatic text extraction from PDF files.
* Semantic search using Sentence Transformers and FAISS.
* Retrieval-Augmented Generation (RAG) pipeline.
* AI-powered question generation using Google Gemini.
* Customizable duration, total marks, and number of questions.
* Automatic division into:

  * Section A – Short Answer Questions
  * Section B – Medium Answer Questions
  * Section C – Long Descriptive Questions
* Download generated question papers as PDF files.
* Interactive web interface built using Streamlit.

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Retrieval System

* Sentence Transformers
* FAISS

### Large Language Model

* Google Gemini 2.5 Flash

### PDF Processing

* PyPDF2
* ReportLab

### Numerical Computation

* NumPy

---

## Project Workflow

1. User uploads a PDF or enters text manually.
2. Text is extracted and divided into smaller chunks.
3. Sentence Transformer converts text chunks into embeddings.
4. FAISS performs similarity search to retrieve relevant content.
5. Retrieved content is passed to Gemini through a structured prompt.
6. Gemini generates a complete academic question paper.
7. The generated paper is displayed and exported as a PDF.

---

## System Architecture

Input Document/Text

↓

Text Chunking

↓

Sentence Transformer Embeddings

↓

FAISS Vector Search

↓

Relevant Context Retrieval

↓

Gemini LLM

↓

Question Paper Generation

↓

PDF Export

## Example Use Cases

* University Question Paper Generation
* Assignment Creation
* Practice Test Generation
* Faculty Assessment Preparation
* Educational Content Automation

---

## Future Enhancements

* Bloom's Taxonomy based question generation.
* Difficulty-level customization.
* Subject-wise question categorization.
* Question bank creation and management.
* Multi-language support.
* Automatic answer key generation.

---

## Author

Mohnish Shandilya

B.Tech Electronics and Computer Engineering

Machine Learning | Deep Learning | Generative AI | Computer Vision

---