# 🐱 Meow – Cat Assistant Chatbot  
**A cute, intelligent RAG-powered assistant for answering veterinary questions**

Meow is a cat-themed intelligent chatbot that uses **Retrieval-Augmented Generation (RAG)**, **vector search**, and **LLMs** to answer user questions in English or Arabic.  
The chatbot is trained on veterinary resources (such as *Veterinary Toxicology and Pharmacy*) to help answer animal-health-related questions accurately.

It supports a simple and friendly web interface built with **Flask**, stores conversation history in SQLite, and retrieves information from uploaded documents using FAISS vector search.

---

## 🧩 Features

### 🔍 **RAG-Based Q&A**
- Extracts text from PDFs, PPTX, notebooks, and Python files.
- Splits content into searchable chunks.
- Retrieves the most relevant information before generating answers.

### 🌍 **Multilingual Support**
- Detects English or Arabic automatically.
- Responds in the same language as the user.

### 💬 **Chat History**
- Uses an SQLite database to store questions, answers, and timestamps.
- Displays the latest 20 interactions in the interface.

### 🐱 **Cute Cat-Themed UI**
- Pastel colors and a cat logo.
- Simple, clean HTML layout for enjoyable interaction.

### 🧠 **Multiple Model Options**
- OpenAI GPT-4o-mini
- OpenRouter models
- HuggingFace transformers  
(Fallbacks applied if one model fails.)

---

## 📁 Project Structure


project_root/
│
├── data/ # Knowledge base files (PDFs, PPTX...)
│ └── VETERINARY TOXICOLOGY AND PHARMACY.pdf
│
├── model/
│ ├── core.py # Core logic: loaders, splitters, prompts, models, RAG pipeline
│ ├── app.ipynb # Main backend: embeddings, FAISS, Flask app, chat history logic
│ ├── chat_history.db # SQLite database for previous chats
│
├── templates/
│ └── index.html # Web UI (Cat-themed chat page)

---

<img width="1366" height="768" alt="Screenshot (577)" src="https://github.com/user-attachments/assets/1bca5042-074d-4a25-9353-a832c032c344" />


## ⚙️ How It Works

### 1️⃣ **Data Loading**
- Files inside the `data/` folder are read (PDF/PowerPoint/Python/etc.).
- Text is extracted via custom readers in `core.py`.

### 2️⃣ **Chunking & Embeddings**
- Text is split using **RecursiveCharacterTextSplitter**.
- Embeddings created using **HuggingFace all-MiniLM-L6-v2**.
- Stored inside **FAISS** for fast vector search.

### 3️⃣ **Answer Generation**
When a user asks a question:
- FAISS retrieves similar text chunks.
- The LLM uses retrieved context + prompt rules.
- The response is generated in the same language as the user.

### 4️⃣ **Chat History**
- Saved using an SQLite database.
- Displayed on the front-end using Jinja2 templates.

### 5️⃣ **Frontend**
- Flask serves a minimal HTML page.
- Shows chat messages + input box.

---

## 🚀 Running the Project

### **Prerequisites**
- Python 3.10+
- Virtual environment recommended
- API key for OpenAI (if using GPT models)

### **Steps**
1. Install dependencies inside the notebook:
2. Run all cells in `app.ipynb`.
3. Open the local server:
http://127.0.0.1:5000/

<img width="1366" height="768" alt="Screenshot (578)" src="https://github.com/user-attachments/assets/23783823-6953-49b3-bd2d-5857747526fe" />
