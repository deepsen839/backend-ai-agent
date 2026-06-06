# Persistent Sales Assistant Agent

A production-style AI Sales Assistant built with FastAPI, React, Groq, SQLite, FAISS, and Sentence Transformers.

The assistant:

* Answers questions using a product catalog
* Maintains persistent memory across sessions
* Uses tools instead of relying solely on LLM knowledge
* Produces a self-evaluation score for every response
* Exposes REST APIs for frontend integration
* Supports deployment on Railway

---

# Live Deployment

## Frontend

https://blissful-elegance-production-bb99.up.railway.app

## Backend

https://selfless-growth-production-aa22.up.railway.app

---

# Architecture

```text
User
 │
 ▼
POST /chat/{user_id}
 │
 ▼
Chat Service
 │
 ▼
Sales Agent
 │
 ├── get_user_memory(user_id)
 │
 ├── search_catalog(query)
 │
 └── flag_for_human(reason)
 │
 ▼
Groq LLM
 │
 ▼
Response Generation
 │
 ▼
Eval Service
 │
 ├── Groundedness Score
 │
 ├── Relevance Score
 │
 ├── Confidence Score
 │
 └── Flag Decision
 │
 ▼
Persist Conversation
 │
 ▼
SQLite Database
 │
 ▼
API Response
```

---

# Memory Design

The application stores conversation history in SQLite using SQLAlchemy.

Each message is stored with:

* user_id
* role
* content
* timestamp
* session_id

This allows the assistant to retrieve previous interactions for a user even after browser refreshes, application restarts, or separate API calls.

Memory is abstracted behind a dedicated memory layer:

```text
memory/
├── base.py
└── sqlite_memory.py
```

This design allows future migration to:

* PostgreSQL
* Redis
* Mem0
* Vector Databases

by replacing a single implementation file.

---

# Tool Design

The assistant uses real callable tools.

## search_catalog(query)

Searches the SaaS catalog using Sentence Transformers embeddings and FAISS similarity search.

Used to answer pricing and feature questions.

## get_user_memory(user_id)

Retrieves previous user conversations from the database.

Provides cross-session context.

## flag_for_human(user_id, reason)

Triggers escalation when confidence falls below a threshold.

---

# Evaluation Design

Every response is evaluated before being returned.

Example:

```json
{
  "response": "Enterprise costs $499/month and includes SSO.",
  "eval": {
    "groundedness": 0.95,
    "relevance": 0.92,
    "confidence": 0.91,
    "flagged": false,
    "reasoning": "Response grounded in catalog data."
  }
}
```

Metrics:

* Groundedness
* Relevance
* Confidence
* Flagged Status

Limitations:

* Uses LLM self-evaluation
* Scores may be optimistic
* Not fully independent

At scale this would be replaced with:

* RAGAS
* DeepEval
* TruLens
* Dedicated evaluator models

---

# API Endpoints

## Chat

```http
POST /chat/{user_id}
```

Send a message and receive a response with evaluation.

---

## History

```http
GET /chat/{user_id}/history
```

Retrieve full conversation history.

---

## Memory Reset

```http
DELETE /chat/{user_id}/memory
```

Delete all user memory.

---

## Catalog

```http
GET /catalog
```

Retrieve pricing catalog.

---

## Health

```http
GET /health
```

Service health check.

---

# Product Catalog

```json
{
  "plans": [
    {
      "name": "Starter",
      "price": "$49/mo",
      "features": [
        "5 users",
        "API access",
        "email support"
      ]
    },
    {
      "name": "Growth",
      "price": "$199/mo",
      "features": [
        "25 users",
        "webhooks",
        "priority support"
      ]
    },
    {
      "name": "Enterprise",
      "price": "$499/mo",
      "features": [
        "unlimited users",
        "SSO",
        "audit logs",
        "SLA"
      ]
    }
  ]
}
```

---

# Cross-Session Memory Demonstration

## Call 1

```bash
curl -X POST \
"https://selfless-growth-production-aa22.up.railway.app/chat/demo-user" \
-H "Content-Type: application/json" \
-d '{
  "message":"What is Enterprise pricing?"
}'
```

Expected response:

```text
Enterprise costs $499/month and includes SSO, audit logs, SLA, and unlimited users.
```

---

## Call 2

```bash
curl -X POST \
"https://selfless-growth-production-aa22.up.railway.app/chat/demo-user" \
-H "Content-Type: application/json" \
-d '{
  "message":"Does that include SSO?"
}'
```

Expected response:

```text
Yes, the Enterprise plan includes SSO.
```

The second request demonstrates memory continuity because the plan name is not repeated by the user.

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* Groq
* FAISS
* Sentence Transformers
* SQLite

## Frontend

* React
* Vite
* Axios

## DevOps

* Docker
* GitHub Actions
* Railway

---

# Future Improvements

* PostgreSQL production database
* Redis caching
* Streaming responses
* Human review dashboard
* Memory summarization
* Multi-agent architecture
* RAGAS based evaluation
* OpenTelemetry observability
