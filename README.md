# AI-powered support ticket system
What problem it solves? In a real company too many emails are sent everyday so use categorise emails automatically and sent them in different departments based on the context(crital to managers, billing to logistics, technical to developers?)
1. Διαβάζεις ένα μήνυμα (π.χ. πρόβλημα πελάτη)
2. Το AI αναλύει το μήνυμα
3. Κατηγοριοποιεί αυτόματα σε:
- Category (Technical Issue, Billing, Feature Request, κλπ)
- Urgency (Low, Medium, High, Critical)
- Sentiment (Positive, Neutral, Negative)
- Confidence (πόσο σίγουρο είναι το AI - 0-100%)

## Πώς το χρησιμοποιείς;
1. Γράψε ένα ticket στο αριστερό box:
Παράδειγμα:  URGENT! Our production server crashed and 1000 customers can't access the website! Need immediate help!
2. Πάτα "🚀 Submit & Classify"
3. Το AI αναλύει & δείχνει:
- Category → π.χ. "Technical Issue"
- Urgency → π.χ. "Critical" (κόκκινο badge)
- Sentiment → π.χ. "Negative" (frustrated customer)
- Confidence → π.χ. 92% (πόσο σίγουρο είναι)
- Model → "Groq/llama-3.1-8b-instant" (ποιο AI μοντέλο χρησιμοποίησε)

## Technology
Postgres
Maybe React
FastApi(Python v 3.12"stable")

## Features:
🔹DashBoard(React-Axios-Table view)
-Δείχνει tickets
-Φιλτράρει ανά category
-Δείχνει similarity matches
This will be very simple not UI Awesome!
🔹Add BackEnd..

## Done
Basic FastApi setup (main.py, requirements.txt)
PostgreSQL connection
Simple AI endpoint(mock response)
start doing features

## Versions & DeadLines 
### Each time i apply different concepts from AI agent Theory in project.
Version 1: AI Classification
(User στέλνει πρόβλημα → AI επιστρέφει structured JSON → Αποθήκευση στο DB.)
-API Endpoints
POST /tickets
GET /tickets
GET /tickets/{id}
-AI Layer
Prompt template
JSON structured output
Validation (Pydantic)
Retry on invalid JSON
Confidence score
-Database
Table: tickets
--id
--user_message
--category
--urgency
--sentiment
--confidence
--ai_raw_response
--model_version
--created_at
-Engineering Features
Logging prompt + response
Error handling
Async LLM call
Clean architecture (router → service → repository)
(Ερωτησεις που θα κανω στον εαυτο μου)
1. Ξέρεις structured extraction με σωστο τροπο η την εκανα λαθος εδω γιατι?
2. Ειναι αυτο το AI σε production-like flow η οχι?
3. Εμπιστεύετηκα τυφλά το LLM η οχι?

Version 2: Database Integration
(Ερωτησεις που θα κανω στον εαυτο μου)
Ειναι διαφορετικο αυτο για ΑΙ η το ιδιο οπως παντα?

Feature 3: RAG Implementation(AI + RAG)
-- Νέα Features
Embeddings
Δημιουργία embedding για κάθε ticket
Αποθήκευση σε pgvector
Similarity Search
Όταν έρχεται νέο ticket:
βρίσκεις 3 παρόμοια
τα βάζεις στο prompt
Context Injection
Prompt:
“Based on similar past issues: …”
Database
Νέος πίνακας:
ticket_embeddings
vector column
Endpoint
POST /tickets/with-context

(Ερωτησεις που θα κανω στον εαυτο μου)
Καταλαβαίνεις RAG σωστα η οχι?
Ξέρω embeddings πλεον η οχι? μηπως δεν τα κανω σωστα?
Ξέρεις vector search η οχι με το σωστο τροπο?
Ξέρεις knowledge grounding η οχι με το σωστο τροπο?

Version 4? vasika 3 einai  alla exw san 2 to DB integration
-- Νέα Features
Tool Definitions
get_similar_tickets
assign_priority
escalate_ticket
Agent Loop
LLM decides tool
Backend executes
Returns result
LLM continues reasoning
Conversation State
session table
message history
Guardrails
Strict JSON schema
Allowed categories only
Output validation
Cost Monitoring
Token usage logging
Model usage stats endpoint

(Ερωτησεις που θα κανω στον εαυτο μου αν τα ξερω καλα η οχι)
Agent orchestration
Tool calling
State machine thinking
Production AI backend

## AI Flow
Client → FastAPI Router → Service Layer → AI Service
                                    ↓
                                PostgreSQL
                                    ↓
                                pgvector

## Files

## URLs
Frontend: http://localhost:8000
API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/health

## Check if these are in project
Clean architecture
DTO separation
Logging strategy
Validation layer
RAG pipeline explanation
Error handling
Dockerized setup
README με architecture diagram

## Todo for production enviroment(from what i can understand for now...)
### Guardrails (Safety Layer)
Στο version1 πρέπει να έχω:
1. Strict JSON schema validation
Pydantic model
Αν αποτύχει → retry LLM call
Αν αποτύχει 2 φορές → fallback response
2. Allowed categories list 
Π.Χ ALLOWED_CATEGORIES = ["Hardware", "Software", "Billing"]
Αν LLM επιστρέψει: "Networking" → reject → retry with clarification prompt.

Στο version2 μπορείς να προσθέσεις:
Confidence threshold (π.χ. < 0.6 → flag for manual review)
Basic hallucination guard:
Αν category δεν υπάρχει στο DB → reject
Input length limits
Basic rate limiting

Στο version3 (serious level):
Output schema enforced via JSON mode
Content filtering
Moderation check
Rule-based override layer

### Cost Monitoring
Στο version1:
Απλά αποθήκευσε:
-model_name
-prompt_tokens
-completion_tokens
-total_tokens
-request_time_ms
Αυτά τα παίρνεις από το LLM API response.

Κάνε έναν πίνακα:
ai_usage_logs
- id
- ticket_id
- model
- prompt_tokens
- completion_tokens
- total_tokens
- cost_estimate
- created_at

Στο v2:
ndpoint: /metrics/usage
Συνολικό token usage
Cost estimate ανά ημέρα

Στο v3:
Rate limiting per user
Max tokens per request
Cost alert threshold

### Prompt Versioning
Αυτό είναι advanced αλλά όχι δύσκολο.
Μην κάνεις hardcode prompt string μέσα στον service.

Table: prompt_templates
- id
- name
- version
- template_text
- created_at
- is_active

Και στον ticket:
- prompt_version

Έτσι μπορείς να πεις: “Version 2 improved urgency detection by 18%”

## Engineering Decisions
Why structured JSON instead of free text?
Why pgvector instead of external vector DB?
Why retry logic limited to 2 attempts?
Why versioned prompts?
Do I need the following or not?
-Idempotency
-Failure modes
-LLM timeout handling
-Rate limiting strategy

## Test it
cd "e:\1.CodeProjects\AI Agent Assistant\nexus-ai"
python -m uvicorn main:app --reload
pws na testarw swsta ta endpoints?