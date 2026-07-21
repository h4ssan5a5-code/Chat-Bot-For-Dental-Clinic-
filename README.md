# 🦷 Rashid Dental AI Assistant

An AI-powered dental clinic assistant built with **FastAPI**, **Google Gemini**, and **RAG (Retrieval-Augmented Generation)**. It answers patient questions using the clinic's own knowledge base, detects appointment-booking intent in natural language, extracts appointment details automatically, and stores bookings in a database — all through a single conversational `/chat` endpoint.

---

## ✨ Features

- **Conversational chatbot** powered by Google Gemini (`gemini-flash-latest`)
- **RAG pipeline** — clinic knowledge (services, FAQs, hours, emergencies) is chunked, embedded, and retrieved with FAISS so answers are grounded in real clinic data instead of hallucinated
- **Automatic appointment booking** — detects booking intent from free-text messages, extracts structured details (name, phone, email, date, time) via Gemini, and asks for anything missing
- **Safety guardrails** — blocks diagnosis requests, medication/prescription advice, and flags emergency language with a clear escalation message
- **Persistent storage** — appointments are saved to a SQL database via SQLAlchemy
- **Session-aware conversation memory** (in-memory, per session/user)

---

## 🏗️ Tech Stack

| Layer            | Technology |
|-------------------|------------|
| API Framework      | FastAPI + Uvicorn |
| LLM                | Google Gemini (`google-genai`) |
| Embeddings         | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector Search      | FAISS (`faiss-cpu`) |
| Database ORM       | SQLAlchemy |
| DB Driver          | `psycopg2-binary` (PostgreSQL) |
| Config Management  | `pydantic-settings` |
| Validation         | Pydantic v2 (`EmailStr`, etc.) |

---

## 📁 Project Structure

```
rashid-dental-ai/
├── app/
│   ├── main.py                  # FastAPI app entrypoint, registers routers
│   ├── config.py                # Settings loaded from .env (Gemini key, DB URL)
│   ├── safety.py                # Diagnosis / medication / emergency keyword guardrails
│   ├── api/
│   │   ├── chat.py              # POST /chat — main conversational endpoint
│   │   └── appointment.py       # POST /appointments/ — direct appointment creation
│   ├── services/
│   │   ├── chatbot.py           # Core orchestration: intent → extraction → RAG → answer
│   │   ├── intent_detector.py   # Keyword-based booking intent detection
│   │   ├── extract_details.py   # Uses Gemini to pull structured JSON from a message
│   │   ├── appointment_service.py # Saves appointment to the database
│   │   ├── gemini_service.py    # Thin wrapper around the Gemini client
│   │   └── session.py           # In-memory per-session conversation history
│   ├── rag/
│   │   ├── loader.py            # Loads all .md files from knowledge_base/
│   │   ├── chunker.py           # Splits markdown into chunks by headings
│   │   ├── embeddings.py        # Encodes text with SentenceTransformer
│   │   ├── vectorstore.py       # FAISS index build + similarity search
│   │   └── prompt.py            # System prompt / assistant rules
│   ├── database/
│   │   ├── database.py          # Engine, session factory, Base, get_db() (used by main.py)
│   │   ├── connection.py        # Alternate engine setup (env-based, unused by main flow)
│   │   ├── session.py           # Alternate session factory (unused by main flow)
│   │   ├── models.py            # SQLAlchemy `Appointment` model
│   │   └── schemas.py           # (currently empty)
│   ├── schemas/
│   │   ├── chat.py              # ChatRequest / ChatResponse pydantic models
│   │   └── appointment.py       # AppointmentRequest / AppointmentCreate pydantic models
│   ├── crud/
│   │   └── appointment.py       # Alternate create_appointment() CRUD helper
│   └── memory/
│       └── conversation.py      # Alternate in-memory conversation store
├── knowledge_base/
│   ├── clinic.md                # Address, phone, opening hours
│   ├── services.md              # Teeth cleaning, root canal, braces
│   ├── faq.md                   # (empty — to be filled in)
│   ├── emergency.md             # (empty — to be filled in)
│   ├── appointment.md           # (empty — to be filled in)
│   └── chatbot_rules.md         # (empty — to be filled in)
├── frontend/                    # (currently empty — placeholder for a UI)
├── tests/                       # (currently empty — placeholder for test suite)
└── .env                         # Local secrets (not committed)
```

> **Note:** The `database/` and `services/` folders each contain two parallel implementations (e.g. `database.py` vs `connection.py`/`session.py`, and `services/appointment_service.py` vs `crud/appointment.py`). Only `database/database.py` and `services/appointment_service.py` are currently wired into `main.py` / the API routers — the others appear to be earlier drafts kept in the repo.

---

## ⚙️ Setup & Installation

### 1. Clone and enter the project
```bash
git clone <your-repo-url>
cd rashid-dental-ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
The repo's `requirements.txt` is currently empty. Based on the packages actually used in the code, install:

```bash
pip install fastapi uvicorn[standard] pydantic pydantic-settings \
            sqlalchemy psycopg2-binary python-dotenv \
            google-genai sentence-transformers faiss-cpu \
            numpy email-validator
```

> 💡 Tip: run `pip freeze > requirements.txt` after installing to lock these versions for the repo.

### 4. Configure environment variables
Copy `env.example` to `.env` and fill in your own values:

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

- `GEMINI_API_KEY` — API key from Google AI Studio
- `DATABASE_URL` — SQLAlchemy connection string, e.g. `postgresql://user:password@localhost:5432/rashid_dental`

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

---

## 📡 API Endpoints

### `POST /chat`
Main conversational endpoint. Handles both general Q&A and appointment booking in one flow.

**Request:**
```json
{
  "message": "I'd like to book an appointment for teeth cleaning tomorrow at 5pm, my name is Ali, phone 03001234567",
  "session_id": "user-123"
}
```

**Response:**
```json
{
  "response": "✅ Appointment booked successfully!\n\nName: Ali\nDate: 2026-07-22\nTime: 17:00"
}
```

If required details are missing, the assistant asks for them instead of booking. If the message isn't about booking, it answers using RAG over the clinic's knowledge base.

### `POST /appointments/`
Direct appointment creation endpoint (bypasses the chatbot/NLU flow).

**Request:**
```json
{
  "name": "Ali Raza",
  "phone": "03001234567",
  "email": "ali@example.com",
  "appointment_date": "2026-07-22",
  "appointment_time": "17:00",
  "message": "Teeth cleaning"
}
```

**Response:**
```json
{
  "message": "Appointment booked successfully!",
  "id": 1
}
```

---

## 🧠 How the RAG Pipeline Works

1. **Load** — `loader.py` reads every `.md` file in `knowledge_base/`
2. **Chunk** — `chunker.py` splits each document by markdown headings (`#`, `##`, `###`)
3. **Embed** — `embeddings.py` encodes chunks with `all-MiniLM-L6-v2`
4. **Index** — `vectorstore.py` builds a FAISS `IndexFlatL2` index at startup
5. **Retrieve** — on each non-booking question, the top-k (default 3) most relevant chunks are retrieved
6. **Generate** — the retrieved context + the user's question are passed to Gemini, which is instructed to answer only from the given context

---

## 🛡️ Safety Guardrails

`app/safety.py` and the RAG system prompt (`app/rag/prompt.py`) enforce that the assistant:
- Never diagnoses medical/dental conditions
- Never recommends or prescribes medication
- Flags likely emergencies (bleeding, swelling, difficulty breathing, etc.) and tells the user to seek immediate care
- Answers only from the clinic's knowledge base, and says so explicitly when information isn't available

---

## 🚧 Known Gaps / TODO

- `knowledge_base/faq.md`, `emergency.md`, `appointment.md`, and `chatbot_rules.md` are empty placeholders
- you can make .md files according to your requirements
- `frontend/` has no UI yet
- `tests/` has no test files yet
- Duplicate/unused modules (`database/connection.py`, `database/session.py`, `crud/appointment.py`, `memory/conversation.py`) could be removed once confirmed unused, to avoid confusion
- `app/database/schemas.py` is empty

---

## 👤 Author

**Muhammad Hassan Tariq**
AI/ML Engineer
- GitHub: [github.com/h4ssan5a5-code](https://github.com/h4ssan5a5-code)
- LinkedIn: [linkedin.com/in/hassan-tariq-21844b401](https://linkedin.com/in/hassan-tariq-21844b401/)
- Portfolio: [hassantariqportfolio.vercel.app](https://hassantariqportfolio.vercel.app)
