# <h1 align="center">Blueprint.AI Backend — Fast, Intelligent SRS Generation Engine</h1>

<p>
The powerhouse behind Blueprint.AI — this FastAPI backend transforms simple project inputs into complete, professional Software Requirements Specification (SRS) documents. From AI-driven content generation to seamless PDF/Word export, the backend is designed for reliability, speed, and a smooth developer experience.  
Built with modern tooling and optimized for real-time responsiveness, it ensures that users receive high-quality SRS documents in seconds.
</p>

---

## 🧠 What This Backend Does

* 🤖 **AI-Powered SRS Generation**
  Automatically creates structured, detailed SRS documents using LangChain + OpenAI.

* ⚡ **Real-Time Streaming (SSE)**
  Watch your SRS come to life step-by-step with Server-Sent Events—no polling required.

* 📄 **PDF & DOCX Export**
  Instantly produces polished PDFs and Word documents using ReportLab & python-docx.

* 🔒 **Secure by Design**
  Validation, safe filename handling, and organized folder structure keep everything clean and safe.

* 🚀 **Blazing-Fast FastAPI Server**
  Lightweight, async, production-ready backend.

---

## 🧰 Tech Stack

**Backend Core:**
![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white) 
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white) 
![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge\&logo=openai\&logoColor=white) 
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge) 

**Document Generation:**
![ReportLab](https://img.shields.io/badge/ReportLab-FF6F00?style=for-the-badge) 
![Docx](https://img.shields.io/badge/python--docx-02569B?style=for-the-badge) 

**Server:**
![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge) 

---

## 🏁 Getting Started

### 1️⃣ Install dependencies

```sh
pip install -r requirements.txt
```

### 2️⃣ Configure environment variables

```sh
cp .env.example .env
```

Inside `.env`, add:

```
OPENAI_API_KEY=sk-xxxx
PORT=5000
```

### 3️⃣ Run the server

**Development (auto-reload):**

```sh
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

**Production:**

```sh
uvicorn app:app --host 0.0.0.0 --port 5000
```

Server runs at:

```
http://localhost:5000
```

---

## 🔌 API Overview

### ✅ Health Check

```
GET /
```

Returns:

```json
{
  "message": "[+] Server up and running..."
}
```

---

## 🔥 Real-Time SRS Generation (SSE)

### `POST /generate-srs-stream`

Your best option. Generates SRS + PDF + Word with **live streaming updates**:

* AI initialization
* Content generation
* PDF creation
* Word creation
* Final file paths + SRS content

No polling, no waiting blindly.

---

## 🧾 Legacy SRS Generation (non-stream)

### `POST /generate-srs`

Returns only the generated SRS text.

---

## 📄 Document Generation

### `POST /generate-pdf`

Input text → Output PDF + DOCX
Organized into user-specific folders.

---

## ⬇️ File Downloads

### Download PDF

```
GET /download-pdf/{username}/{filename}
```

### Download Word

```
GET /download-word/{username}/{filename}
```

---

## 🎯 Why This Backend Matters

* Built for **scalability**
* Designed for **smooth user experience**
* Optimized for **fast AI processing**
* Production-ready **document architecture**

From taking user data to delivering downloadable professional SRS files, the backend ensures a frictionless workflow.

---

## 📬 Contact

Want to connect or collaborate?

[![linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/harshita-barnwal-17a732234)

© 2025 Harshita Barnwal

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
