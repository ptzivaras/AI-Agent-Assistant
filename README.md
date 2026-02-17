# 🤖 Nexus AI - Intelligent Ticket Classification System

AI-powered support ticket system that automatically categorizes, prioritizes, and analyzes customer support messages using real-time AI classification.

## 📸 Screenshots

### Frontend Dashboard
![Frontend UI](01.png)

### API Documentation
![FastAPI Docs](02.png)

---

## 🎯 Problem Statement

In real companies, **thousands of emails arrive daily**. Manual sorting is time-consuming and error-prone. This system:
- ✅ **Automatically categorizes** tickets (Technical, Billing, Feature Request, etc.)
- ✅ **Prioritizes urgency** (Critical → High → Medium → Low)
- ✅ **Analyzes sentiment** (Positive, Neutral, Negative)
- ✅ **Routes to correct teams** (Critical → Managers, Billing → Finance, Technical → Developers)

---

## 🚀 How It Works

1. **User submits** a support message (e.g., "URGENT! Server is down!")
2. **AI analyzes** the message using Groq/OpenAI
3. **System classifies** automatically:
   - **Category**: Technical Issue, Billing, Feature Request, Account, Bug Report, General Inquiry
   - **Urgency**: Low, Medium, High, Critical
   - **Sentiment**: Positive, Neutral, Negative
   - **Confidence**: 0-100% (how sure the AI is)
4. **Results saved** to database with full classification metadata

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.14** - Latest stable version
- **SQLAlchemy** - ORM for database management
- **Pydantic** - Data validation with type hints
- **SQLite** - Development database (PostgreSQL-ready)

### AI Layer
- **Groq API** - FREE ultra-fast LLM inference (llama-3.1-8b-instant)
- **OpenAI API** - Alternative provider support (gpt-3.5-turbo)
- **Structured Output** - JSON-validated AI responses

### Frontend
- **React 18** - Modern UI library (via CDN)
- **Vanilla CSS** - Custom gradient design
- **Babel Standalone** - In-browser JSX compilation
- **No build step required** - Direct browser usage

---

## ✨ Current Features

### ✅ Version 1: Mock AI System
- Basic FastAPI setup with clean architecture
- Mock keyword-based classifier (no API keys needed)
- PostgreSQL-compatible database schema
- CRUD operations (Create, Read, List, Statistics)
- Logging & error handling

### ✅ Version 2: Real AI Integration
- **Groq API integration** (FREE & ultra-fast)
- **OpenAI API support** (gpt-3.5-turbo)
- Provider switching via environment variable
- Automatic JSON extraction from AI responses
- Confidence scoring & model version tracking
- Configuration management with pydantic-settings

### ✅ React Frontend
- Beautiful gradient purple theme
- Real-time ticket submission & classification
- Live statistics dashboard
- Ticket history with color-coded badges
- Responsive design (mobile & desktop)
- No npm/build required - pure CDN

---

## 📂 Project Structure

```
AI-Agent-Assistant/
├── nexus-ai/                    # Backend (FastAPI)
│   ├── app/
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic validation
│   │   ├── services/            # Business logic (AI service)
│   │   ├── crud/                # Database operations
│   │   ├── routers/             # API endpoints
│   │   ├── logger.py            # Logging configuration
│   │   ├── config.py            # Settings management
│   │   └── database.py          # DB connection
│   ├── main.py                  # FastAPI app entry
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Configuration (API keys)
│
├── frontend/                    # React UI
│   ├── index.html               # Main HTML file
│   ├── app.jsx                  # React components
│   ├── style.css                # Gradient design
│   └── README.md                # Frontend docs
│
├── 01.png                       # Screenshot: Frontend UI
├── 02.png                       # Screenshot: API Docs
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+ installed
- Groq API key (FREE from https://groq.com)

### Backend Setup

1. **Navigate to backend folder:**
```bash
cd nexus-ai
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment (.env):**
```env
# AI Provider (groq or openai)
AI_PROVIDER=groq

# Groq API Key (FREE - get from https://groq.com)
GROQ_API_KEY=your-groq-key-here
GROQ_MODEL=llama-3.1-8b-instant

# Database
DATABASE_URL=sqlite:///./nexus.db
```

5. **Start backend server:**
```bash
uvicorn main:app --reload --port 8001
```

Backend running at: **http://localhost:8001**

### Frontend Setup

1. **Navigate to frontend folder:**
```bash
cd frontend
```

2. **Start HTTP server:**
```bash
python -m http.server 8080
```

Frontend running at: **http://localhost:8080**

---

## 🧪 Testing the System

### Example 1: Critical Technical Issue
**Input:**
```
URGENT! Our production server crashed and 1000 customers can't access the website! Need immediate help!
```

**Expected Output:**
- Category: `Technical Issue`
- Urgency: `Critical` (red badge)
- Sentiment: `Negative`
- Confidence: `~92%`

### Example 2: Billing Question
**Input:**
```
Hi, I was charged twice for my subscription last month. Can you please refund one charge? Thanks!
```

**Expected Output:**
- Category: `Billing`
- Urgency: `Medium`
- Sentiment: `Neutral`
- Confidence: `~87%`

### Example 3: Feature Request
**Input:**
```
It would be amazing if you could add dark mode to the app! I use it at night and it's too bright.
```

**Expected Output:**
- Category: `Feature Request`
- Urgency: `Low`
- Sentiment: `Positive`
- Confidence: `~95%`

---

## 📡 API Endpoints

### Create Ticket
```http
POST /tickets
Content-Type: application/json

{
  "user_message": "Your support message here (min 10 chars)"
}
```

### List All Tickets
```http
GET /tickets?page=1&page_size=10&category=Technical%20Issue&urgency=Critical
```

### Get Specific Ticket
```http
GET /tickets/{id}
```

### Get Statistics
```http
GET /tickets/stats
```

**Interactive API Docs:** http://localhost:8001/docs

---

## 📊 Database Schema

### Tickets Table
```sql
CREATE TABLE tickets (
    id              INTEGER PRIMARY KEY,
    user_message    TEXT NOT NULL,
    category        VARCHAR(50),
    urgency         VARCHAR(20),
    sentiment       VARCHAR(20),
    confidence      FLOAT,
    ai_raw_response TEXT,
    model_version   VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 Version Roadmap

### ✅ Version 1: Mock AI System (DONE)
**Goal:** Build foundation without external APIs

**Key Learnings:**
- ✅ Structured JSON extraction
- ✅ Clean architecture (router → service → crud)
- ✅ Production-like flow
- ✅ Validation & error handling

### ✅ Version 2: Real AI Integration (DONE)
**Goal:** Replace mock with real LLM APIs

**Key Learnings:**
- ✅ Multiple provider support (Groq + OpenAI)
- ✅ Configuration management
- ✅ JSON parsing strategies
- ✅ Confidence scoring

### 🔜 Version 3: RAG Implementation
**Goal:** Context-aware classification using similar past tickets

**Planned Features:**
- Generate embeddings for each ticket
- Store vectors in pgvector
- Similarity search (find 3 most similar tickets)
- Context injection into AI prompt
- New endpoint: `POST /tickets/with-context`

**Questions to Validate:**
- Do I understand RAG correctly?
- Do I implement embeddings properly?
- Is vector search done right?
- Do I understand knowledge grounding?

### 🔜 Version 4: Agent Orchestration
**Goal:** Multi-step reasoning with tool calling

**Planned Features:**
- Tool definitions (`get_similar_tickets`, `assign_priority`, `escalate_ticket`)
- Agent loop (LLM decides → Backend executes → Result → Continue)
- Conversation state management
- Guardrails (strict validation, allowed categories only)
- Cost monitoring (token usage logging)

**Questions to Validate:**
- Do I understand agent orchestration?
- Is tool calling implemented correctly?
- Do I handle state properly?
- Is this production-ready?

---

## 🔒 Production Considerations

### Guardrails (Safety Layer)

**Version 1 (Essential):**
- ✅ Strict JSON schema validation (Pydantic)
- ✅ Retry logic for failed LLM calls
- ✅ Allowed categories list validation
- ✅ Input length limits
- ✅ Basic rate limiting

**Version 2 (Recommended):**
- Confidence threshold (< 0.6 → manual review)
- Hallucination guard (reject invalid categories)
- Content filtering
- Moderation API check

**Version 3 (Advanced):**
- Output schema enforcement
- Rule-based override layer
- Multi-model consensus
- Human-in-the-loop for edge cases

### Cost Monitoring

**Current Implementation:**
- Model name tracking
- Token usage logging
- Request timing
- Provider selection

**Planned:**
```sql
CREATE TABLE ai_usage_logs (
    id              INTEGER PRIMARY KEY,
    ticket_id       INTEGER,
    model           VARCHAR(100),
    prompt_tokens   INTEGER,
    completion_tokens INTEGER,
    total_tokens    INTEGER,
    cost_estimate   FLOAT,
    created_at      TIMESTAMP
);
```

**Future Endpoints:**
- `GET /metrics/usage` - Total token usage
- `GET /metrics/cost` - Cost estimates per day
- `GET /metrics/performance` - Classification accuracy

### Prompt Versioning

**Strategy:**
```sql
CREATE TABLE prompt_templates (
    id              INTEGER PRIMARY KEY,
    name            VARCHAR(100),
    version         VARCHAR(20),
    template_text   TEXT,
    created_at      TIMESTAMP,
    is_active       BOOLEAN
);
```

**Benefits:**
- A/B testing different prompts
- Track which version performs better
- Rollback to previous versions
- Measure improvement over time

---

## 🏗️ Architecture & Design

### Clean Architecture Layers

```
┌─────────────────────────────────────┐
│         API Layer (Router)          │  ← FastAPI endpoints
├─────────────────────────────────────┤
│       Service Layer (Logic)         │  ← AI classification
├─────────────────────────────────────┤
│       CRUD Layer (Database)         │  ← SQLAlchemy queries
├─────────────────────────────────────┤
│        Data Layer (Models)          │  ← DB schema
└─────────────────────────────────────┘
```

### Data Flow

```
Client Request
     ↓
FastAPI Router (validates input)
     ↓
Service Layer (calls AI API)
     ↓
AI Provider (Groq/OpenAI)
     ↓
Response Parsing (extract JSON)
     ↓
CRUD Layer (save to database)
     ↓
Response to Client
```

---

## 🧪 Testing Strategy

### Current Status
- ✅ Manual testing via frontend
- ✅ API testing via FastAPI Docs (/docs)
- ✅ PowerShell integration tests

### Planned
- [ ] **Unit Tests** (pytest)
  - Test AI service mock
  - Test CRUD operations
  - Test schema validation
- [ ] **Integration Tests**
  - Test full API flow
  - Test database operations
  - Test AI provider switching
- [ ] **Load Tests**
  - Concurrent request handling
  - Token rate limiting
  - Database performance

---

## 🐳 Docker Setup (Planned)

### Planned Structure
```yaml
version: '3.8'
services:
  backend:
    build: ./nexus-ai
    ports:
      - "8001:8001"
    environment:
      - AI_PROVIDER=groq
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./nexus.db:/app/nexus.db
  
  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
```

---

## 📚 Learning Objectives

This project is built as a learning exercise to master:

### ✅ Completed
- Structured output extraction
- Multi-provider AI integration
- Clean architecture patterns
- RESTful API design
- React frontend basics
- Configuration management

### 🔄 In Progress
- RAG implementation
- Vector embeddings
- Semantic search
- Production guardrails

### 🔜 Next
- Agent orchestration
- Tool calling patterns
- State management
- Cost optimization

---

## 🤔 Engineering Questions to Validate

### Structured Extraction
- ✅ Do I validate JSON properly?
- ✅ Do I handle parsing failures gracefully?
- ✅ Is my schema flexible enough?

### Production Readiness
- ✅ Is error handling comprehensive?
- ✅ Are logs actionable?
- ⏳ Is rate limiting implemented?
- ⏳ Are costs tracked?

### AI Safety
- ✅ Do I validate LLM outputs?
- ⏳ Do I have hallucination guards?
- ⏳ Is confidence calibrated?
- ⏳ Human-in-the-loop for low confidence?

---

## 📝 URLs & Links

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs
- **Health Check:** http://localhost:8001/health

---

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome!

---

## 📄 License

MIT License - Feel free to use for learning purposes.

---

## 🙏 Acknowledgments

- **Groq** - For providing FREE ultra-fast LLM inference
- **FastAPI** - Amazing Python web framework
- **React** - Frontend library
- **Llama 3.1** - Open source LLM model

---

**Built with ❤️ as a learning project to master AI agent development**
