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

## 🏗️ Architecture Principles

- **Clean separation**: Router → Service → Repository
- **AI logic isolated** in AI Service layer
- **No blind trust** in LLM output
- **Full request/response logging**
- **Prompt version traceability**
- **Cost observability**

---

## 🗺️ Version Roadmap

### Version 1 → AI Classification (with DB)
**User στέλνει πρόβλημα → AI επιστρέφει structured JSON → Αποθήκευση στο DB**

**Features:**
- ✅ API Endpoints (POST, GET, LIST)
- ✅ AI Layer
  - Prompt template with structured output
  - JSON validation (Pydantic schemas)
  - Retry mechanism (max 2 attempts)
  - Confidence score calculation
- ✅ Database (SQLite → PostgreSQL ready)
  - Table: `tickets` with full classification metadata
  - Columns: id, user_message, category, urgency, sentiment, confidence, ai_raw_response, model_version, created_at
- ✅ Engineering
  - Async LLM calls
  - Request/response logging
  - Error handling with fallbacks
  - Clean architecture (router → service → repository)

**React Frontend:**
- ✅ Gradient purple theme with responsive design
- ✅ Real-time ticket submission & classification
- ✅ Live statistics dashboard
- ✅ Color-coded badges (urgency levels)
- ✅ No build step (CDN-based React)

**Ερωτησεις που θα κανω στον εαυτο μου:**
1. Ξέρω structured extraction σωστά ή την έκανα λάθος;
2. Είναι αυτό production-like flow ή όχι;
3. Εμπιστεύτηκα τυφλά το LLM ή όχι;

---

### Version 2 → RAG (Retrieval-Augmented Generation)
**Όταν έρχεται νέο ticket → βρίσκω παρόμοια → context injection στο prompt**

**Features:**
- 🔲 Embeddings
  - Generate embedding για κάθε ticket
  - Store in pgvector column
- 🔲 Similarity Search
  - Query vector database
  - Retrieve top-3 similar tickets
  - Context injection: "Based on similar past issues: ..."
- 🔲 Database
  - New table: `ticket_embeddings`
  - Vector column (pgvector extension)
- 🔲 Endpoint: `POST /tickets/with-context`

**Ερωτησεις που θα κανω στον εαυτο μου:**
- Καταλαβαίνω RAG σωστά ή όχι;
- Ξέρω embeddings πλέον ή μήπως δεν τα κάνω σωστά;
- Ξέρω vector search με το σωστό τρόπο;
- Ξέρω knowledge grounding με το σωστό τρόπο;

---

### Version 3 → Agent Orchestration
**LLM αποφασίζει ποιο tool να χρησιμοποιήσει → Backend εκτελεί → Loop**

**Features:**
- 🔲 Tool Definitions
  - `get_similar_tickets(query)` - RAG retrieval
  - `assign_priority(ticket_id, level)` - Business logic
  - `escalate_ticket(ticket_id, team)` - Routing
- 🔲 Agent Loop
  - LLM decides which tool to call
  - Backend executes tool
  - Returns result to LLM
  - LLM continues reasoning (max 5 iterations)
- 🔲 Conversation State
  - Table: `sessions` with message history
  - State persistence across requests
  - Context window management

**Ερωτησεις που θα κανω στον εαυτο μου:**
- Agent orchestration σωστά ή όχι;
- Tool calling σωστά ή όχι;
- State machine thinking σωστά ή όχι;
- Production AI backend σωστά ή όχι;

---

## 🧪 Testing Examples

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

## 🔒 Production Requirements

### 1. Business Rule Override Layer

**Business rules can override AI classification when predefined deterministic conditions are met.**

This is a core AI production principle: **never trust the model blindly**.

**Examples:**
```python
# Rule 1: Keyword-based urgency override
if "server down" in message.lower() or "production crash" in message.lower():
    urgency = "Critical"  # Override AI decision
    override_reason = "Contains critical keywords"

# Rule 2: Confidence threshold
if classification.confidence < 0.7:
    status = "pending_review"  # Flag for manual review
    assigned_to = "human_queue"

# Rule 3: Business hours enforcement
if is_after_hours() and category == "Billing":
    priority = "Low"  # Defer non-urgent billing to next day
    override_reason = "After hours billing inquiry"

# Rule 4: VIP customer detection
if customer.tier == "Enterprise":
    urgency = max(urgency, "High")  # Elevate priority
    sla_hours = 4  # Strict SLA
```

**Implementation:**
- Apply rules **after** AI classification
- Log all overrides with reason
- Track override frequency (% of tickets)
- A/B test rule effectiveness

---

### 2. Hard Boundaries (Bounded AI)

**AI systems without boundaries = unstable systems.**

These limits prevent runaway costs, infinite loops, and unpredictable behavior.

| Resource | Limit | Rationale |
|----------|-------|-----------|
| **Max tokens per request** | 1500 input + 500 output | Cost control & latency |
| **Max retries** | 2 attempts | Prevent retry storms |
| **Request timeout** | 10 seconds | User experience threshold |
| **Max agent loop iterations** | 5 steps | No infinite reasoning |
| **Embedding dimensions** | 1536 (OpenAI) / 768 (local) | Memory & performance |
| **Vector search results** | Top 3 | Context window optimization |
| **Confidence threshold** | 0.6 minimum | Below → manual review |

**Enforcement:**
```python
# Example: Timeout decorator
@timeout(seconds=10)
async def classify_ticket(message: str):
    response = await ai_provider.call(message)
    return response

# Example: Bounded agent loop
for iteration in range(MAX_ITERATIONS):  # Hard stop at 5
    if agent.is_done():
        break
    action = agent.decide_next_action()
    result = execute_tool(action)
    agent.update_state(result)
```

---

### 3. Failure Handling Strategy

**What happens when AI fails?**

Real production systems need graceful degradation, not crashes.

| Failure Scenario | Strategy | Fallback Behavior |
|------------------|----------|-------------------|
| **Provider timeout** | Switch to OpenAI if Groq fails | 5s timeout → fallback |
| **Invalid JSON response** | Retry with explicit schema (max 2x) | Default classification if still fails |
| **Embedding API fails** | Proceed without RAG context | Classification works, no context injection |
| **Vector search returns empty** | Use base prompt (no similar tickets) | Degrade gracefully |
| **All providers down** | Return 503 + queue ticket | Manual classification later |
| **Confidence < threshold** | Flag for human review | No automatic action |
| **Database connection lost** | Cache in Redis, persist later | Temporary in-memory storage |

**Implementation:**
```python
async def classify_with_fallback(message: str):
    try:
        # Primary: Groq
        return await groq_provider.classify(message)
    except TimeoutError:
        logger.warning("Groq timeout, falling back to OpenAI")
        try:
            return await openai_provider.classify(message)
        except Exception as e:
            logger.error(f"All providers failed: {e}")
            return default_classification(message)  # Mock classifier
```

---

### 4. Guardrails

- ✅ **Strict JSON schema** - Structured output validation (Pydantic)
- ✅ **Allowed categories only** - Enum constraints (no arbitrary values)
- ✅ **Output validation** - Reject invalid classifications
- ✅ **Retry mechanism** - Max 2 attempts with exponential backoff
- ✅ **Error logging** - Complete request/response tracking

---

### 5. AI Observability & Metrics

**Beyond token counting - track AI behavior.**

| Metric | Purpose | Alert Threshold |
|--------|---------|-----------------|
| **Classification distribution** | Detect category bias | >40% in one category |
| **Low-confidence ratio** | Model uncertainty | >20% below 0.7 |
| **AI error rate** | Provider failures | >5% errors |
| **P95/P99 latency** | Performance monitoring | >3s / >5s |
| **Override frequency** | Business rule usage | Track trend over time |
| **Token usage** | Cost tracking | Daily budget limit |
| **Confidence calibration** | Accuracy vs confidence | Weekly analysis |

**Implementation:**
```python
# Metrics endpoint
@app.get("/metrics/ai")
async def ai_metrics():
    return {
        "classification_distribution": {
            "Technical Issue": 35.2,
            "Billing": 22.1,
            "Feature Request": 18.5,
            ...
        },
        "low_confidence_ratio": 12.4,  # % below 0.7
        "ai_error_rate": 2.1,  # % failed requests
        "avg_latency_ms": 847,
        "p95_latency_ms": 1420,
        "token_usage_24h": {
            "input": 12450,
            "output": 8920,
            "estimated_cost_usd": 0.34
        }
    }
```

---

### 6. Cost Monitoring

- 📊 **Token usage logging** - Track input/output tokens per request
- 📊 **Model usage stats** - Endpoint for usage analytics
- 📊 **Provider comparison** - Groq (free) vs OpenAI cost tracking
- 📊 **Daily budget alerts** - Notify when approaching limit
- 📊 **Per-user cost tracking** - Identify expensive usage patterns

---

### 7. Prompt Versioning

All prompts are versioned and logged:
- **v1.0**: Basic classification template
- **v2.0**: RAG-enhanced context injection
- **v3.0**: Agent orchestration with tool calls

Each ticket stores the `model_version` used for classification, enabling:
- A/B testing of prompt variations
- Rollback to previous prompt versions
- Performance comparison across versions
- Reproducible classification decisions

---

## 🎓 Learning Progress

### ✅ Completed Concepts
- ✅ Structured output extraction (Pydantic validation)
- ✅ Multi-provider AI integration (Groq + OpenAI)
- ✅ Clean architecture patterns (Router → Service → Repository)
- ✅ RESTful API design with FastAPI
- ✅ React frontend basics (CDN-based, no build)
- ✅ Configuration management (pydantic-settings)
- ✅ Prompt versioning & logging  
- ✅ Token usage tracking

### 🔄 Working On
- 🔄 RAG implementation (embeddings + vector search)
- 🔄 Production guardrails (business rules, boundaries)
- 🔄 Failure handling strategies
- 🔄 AI observability metrics

### 📋 Todo
- Agent orchestration with tool calling
- State management across requests
- Cost optimization strategies
- Load testing & performance tuning
- Docker containerization
- Human-in-the-Loop (HITL) Workflow
- LLM Security (Prompt Injection Defense)
- Caching Strategy (Redis architecture)
- Feedback Loop & Model Improvement
- Data Privacy & Compliance (GDPR, PII masking)
- Async Processing (message queues, workers)
---

## 📊 Data Flow

```
Client Request
     ↓
FastAPI Router (validates input)
     ↓
Service Layer (applies business rules)
     ↓
AI Provider (Groq/OpenAI with fallback)
     ↓
Response Parsing (extract + validate JSON)
     ↓
Business Rule Check (override if needed)
     ↓
CRUD Layer (save to database)
     ↓
Metrics Logging (tokens, latency, confidence)
     ↓
Response to Client
```

---

## 🧪 Testing Strategy 

### Unit Tests
- ✅ AI service with mocked LLM responses
- ✅ CRUD operations with in-memory SQLite
- ✅ Schema validation (Pydantic)
- ✅ Business rule logic (override scenarios)
- ✅ Confidence threshold handling

### Integration Tests
- 🔄 Full API flow (submit → classify → retrieve)
- 🔄 Database operations with real PostgreSQL
- 🔄 AI provider switching (Groq ↔ OpenAI fallback)
- 🔄 Failure scenarios (timeouts, invalid JSON)

### Load Tests
- 🔲 Concurrent ticket submission (100 req/s)
- 🔲 Rate limiting validation
- 🔲 Token usage under load
- 🔲 Database connection pooling

---

## 🤔 Engineering Self-Assessment

### Structured Extraction
- ❓ Do I validate JSON properly?
- ❓ Do I handle parsing failures gracefully?
- ❓ Is my schema flexible enough for future changes?

### Production Readiness
- ✅ Is error handling comprehensive? → **Yes** (retry + fallback)
- ✅ Are logs actionable? → **Yes** (full request/response tracking)
- ⚠️ Is rate limiting implemented? → **Partially** (planned)
- ✅ Are costs tracked? → **Yes** (token usage per request)

### AI Safety
- ✅ Do I validate LLM outputs? → **Yes** (Pydantic + retry)
- ⚠️ Do I have hallucination guards? → **Partially** (confidence threshold)
- ❓ Is confidence calibrated? → **Need to test accuracy vs confidence**
- ✅ Human-in-the-loop for low confidence? → **Yes** (manual review queue)

---

## 🏗️ Engineering Decisions

### Why Groq?
- ⚡ **FREE tier** with generous limits
- ⚡ **Ultra-fast inference** (sub-second responses)
- ⚡ **Production-ready** structured outputs

### Why SQLite → PostgreSQL?
- 🗄️ **Development simplicity** (no setup required)
- 🗄️ **PostgreSQL-ready** (pgvector for embeddings)
- 🗄️ **Easy migration** path for production

### Why React via CDN?
- 🚀 **Zero build complexity**
- 🚀 **Instant prototyping**
- 🚀 **Easy hosting** (no webpack/vite needed)

---

## 🐳 Docker Setup (Planned)

```yaml
services:
  backend:
    build: ./nexus-ai
    ports:
      - "8001:8001"
    env_file: .env
    environment:
      - DATABASE_URL=postgresql://admin:secret@db:5432/nexus_ai
      - AI_PROVIDER=groq
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
  
  db:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: nexus_ai
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 📝 Next Steps for Production

### Infrastructure
- [ ] Migrate SQLite → PostgreSQL with pgvector
- [ ] Set up Redis for caching/session storage
- [ ] Configure environment variables (secrets manager)
- [ ] Set up reverse proxy (Nginx/Caddy)
- [ ] SSL/TLS certificates (Let's Encrypt)

### Security
- [ ] API key authentication (Bearer tokens)
- [ ] Rate limiting per user/IP (Redis-based)
- [ ] Input sanitization (prevent injection)
- [ ] CORS configuration (whitelist domains)
- [ ] Security headers (CSP, HSTS, X-Frame-Options)

### Monitoring
- [ ] Centralized logging (ELK/Loki)
- [ ] Metrics collection (Prometheus/Grafana)
- [ ] Error tracking (Sentry/Rollbar)
- [ ] Health check endpoints
- [ ] AI metrics dashboard

### CI/CD
- [ ] GitHub Actions pipeline
- [ ] Automated tests (pytest)
- [ ] Docker image builds
- [ ] Blue-green deployments
- [ ] Rollback strategy
