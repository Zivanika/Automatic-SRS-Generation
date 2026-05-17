# SRS Generator - Interview Cheatsheet

This document provides a technical overview of the SRS (Software Requirements Specification) generation project. Use this to prepare for interview questions regarding architecture, specific technologies, and implementation details.

## 1. Project Overview
A web application that generates comprehensive SRS documents from user inputs using AI (LangChain + OpenAI), providing real-time progress updates via Server-Sent Events (SSE), and exporting results to PDF and Word formats.

- **Frontend**: Next.js, Tailwind CSS, TypeScript
- **Backend**: Python (FastAPI), LangChain, ReportLab
- **Database**: MongoDB (User data & SRS records)
- **Auth**: NextAuth.js

---

## 2. Authentication (NextAuth.js)
**File**: `Frontend/src/app/api/auth/[...nextauth]/options.ts`

The project uses **NextAuth.js** to handle authentication with a hybrid approach supporting both **OAuth providers** and **Credentials** (Email/Password).

### Key Features:
- **Multiple Providers**: GitHub, Google, Twitter, Facebook, Apple, and Credentials.
- **JWT Strategy**: Sessions are stateless and stored in JSON Web Tokens (JWT).
- **Custom Callbacks**:
  - **`jwt()`**: 
    - Handles "Just-In-Time" user creation for OAuth logins (if a user logs in with Google for the first time, a MongoDB record is created).
    - Customizes the token to include the user's MongoDB `_id` and `username`.
  - **`session()`**: 
    - Passes the custom token fields (`_id`, `username`) to the client-side session, making them accessible via the `useSession()` hook.

**Interview Talking Point**: "I implemented a custom JWT callback to sync social login users with my MongoDB database, ensuring that every authenticated user, regardless of provider, has a consistent user profile in my system."

---

## 3. Real-Time Updates (Server-Sent Events - SSE)
**Files**: `Backend Python/app.py` (Server), `Frontend/src/app/workspace/[identifier]/page.tsx` (Client)

Instead of simple HTTP requests or WebSockets, the app uses **Server-Sent Events (SSE)** to stream the long-running generation process to the client.

### Backend Implementation (`app.py`):
- Endpoint: `/generate-srs-stream`
- Implementation: Uses FastAPI's `StreamingResponse` with `media_type="text/event-stream"`.
- It defines a Python generator function `srs_generation_stream` that `yields` data in the format `data: {...}\n\n`.
- **Workflow**:
  1.  Yield "initiated" status.
  2.  Yield "processing" updates as it calls the AI model.
  3.  Yield "completed" status with file paths once finished.

### Frontend Integration (`page.tsx`):
- Uses the native `fetch` API with `response.body.getReader()` to read the stream chunk-by-chunk.
- A `while(true)` loop decodes the binary chunks into text and parses the JSON messages.
- Updates the progress bar and status text in real-time based on the received "message" field.

**Interview Talking Point**: "I chose SSE over WebSockets because communication is unidirectional (server-to-client updates) and it's lighter/easier to implement than full duplex sockets for this specific use case."

---

## 4. AI Pipeline & Prompt Engineering (LangChain)
**File**: `Backend Python/app.py`

The core logic uses **LangChain** to interface with OpenAI's `gpt-4o-mini` model.

### Pipeline Steps:
1.  **Input Collection**: Receives structured inputs (Purpose, Target Audience, Tech Stack, etc.) from the frontend.
2.  **Prompt Construction**: A dynamic f-string injects all user inputs into a structured prompt.
    - *Key constraints in prompt*: "Follow IEEE 830 standards", "No markdown hash symbols", "Specific section numbering".
3.  **Model Invocation**:
    - **System Message**: Sets the persona ("Expert technical writer").
    - **Human Message**: Contains the actual request.
4.  **Output Parsing**: Uses `StrOutputParser` to get raw string output.

**Interview Talking Point**: "I used LangChain to structure the interaction with GPT-4, defining a strict System Prompt to ensure the output valid IEEE 830 compliant technical documentation rather than generic text."

---

## 5. Document Post-Processing & Generation
**File**: `Backend Python/app.py`

Raw text from the AI is not enough; it needs to be cleaned and formatted into professional files.

### Text Cleaning (Regex):
- Extracts the generated Title using `re.search(r'Title:\s*(.*)', generated_text)`.
- Removes the internal title line from the body to avoid duplication.
- Sanitizes the title for use as a filename (removes special chars).

### PDF Generation (`reportlab`):
- **Library**: `reportlab` (Python).
- **Logic**: 
  - Iterates through text lines.
  - Detects headings using Regex (`^\d+\.` matches "1.", "1.1", etc.) and applies a **Bold/Larger** style.
  - Applies standard body styles to other text.
  - Saves file to `storage/[username]/pdfs/`.

### Word Generation (`python-docx`):
- **Library**: `python-docx`.
- **Logic**: Similar logic to PDF, mapping detected headings to Word's `add_heading(level=1)` and body text to `add_paragraph()`.

**Interview Talking Point**: "I successfully bridged the gap between unstructured AI text and structured documents by implementing a parser that recognizes numbering patterns (e.g., '1. Introduction') and applies defining styles in the final PDF/Docx output."

---

## 6. Access Control & Storage
**Files**: `app.py` & `models.py`

- **Storage**: Files are saved locally in a `storage/` directory, organized by username.
- **Security Functions**: 
  - `sanitize_filename()`: Prevents directory traversal attacks (e.g., `../../etc/passwd`).
  - `get_user_directories()`: Ensures isolation between user files.
- **Download Endpoints**: `/download-pdf/{username}/{filename}` checks if the file exists and streams it back using `FileResponse`.

## 7. Client-Side PDF Viewing
**File**: `Frontend/src/app/view-pdf/[pdfPath]/page.tsx`

The application features an in-browser PDF viewer so users can review the document without downloading it first.

- **Library**: `react-pdf`
- **Mechanism**:
  - The URL parameter `pdfPath` is decoded.
  - `axios` fetches the PDF as a `blob` from the backend.
  - `window.URL.createObjectURL(blob)` creates a local URL for the PDF data.
  - Failure handling ensures a smooth UI even if the file is missing or the backend is down.

