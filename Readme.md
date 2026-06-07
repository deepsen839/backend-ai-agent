# Persistent Sales Assistant Agent

A production-style AI Sales Assistant built with FastAPI, React, Groq, SQLite, FAISS, and Sentence Transformers.

The assistant:

* Understands a SaaS product catalog
* Maintains persistent memory across sessions
* Uses real tools instead of relying on raw LLM knowledge
* Generates a self-evaluation score for every response
* Provides REST APIs for frontend integration
* Is deployed on Railway

---

# Live Deployment

## Frontend

https://blissful-elegance-production-bb99.up.railway.app/

## Backend

https://selfless-growth-production-aa22.up.railway.app/

## API Documentation

https://selfless-growth-production-aa22.up.railway.app/docs

## Health Check

https://selfless-growth-production-aa22.up.railway.app/health

---

# Architecture Diagram

```text
User
 │
 ▼
POST /chat/{user_id}
 │
 ▼
FastAPI Route
 │
 ▼
Chat Service
 │
 ▼
Sales Agent
 │
 ├── search_catalog(query)
 │
 ├── get_user_memory(user_id)
 │
 └── flag_for_human(user_id, reason)
 │
 ▼
Groq LLM
 │
 ▼
Response Generation
 │
 ▼
Evaluation Service
 │
 ├── Groundedness
 │
 ├── Relevance
 │
 ├── Confidence
 │
 └── Flagging
 │
 ▼
SQLite Memory Layer
 │
 ▼
Response Returned
```

---

# Project Structure

```text
app/
├── api/
│   ├── chat.py
│   ├── catalog.py
│   └── health.py
│
├── agents/
│   ├── sales_agent.py
│   └── evaluator.py
│
├── memory/
│   ├── base.py
│   └── sqlite_memory.py
│
├── tools/
│   ├── search_catalog.py
│   ├── get_user_memory.py
│   └── flag_for_human.py
│
├── services/
│   ├── chat_service.py
│   └── eval_service.py
│
├── models/
│   ├── requests.py
│   └── responses.py
│
├── db/
│   ├── database.py
│   └── models.py
│
├── catalog.json
├── main.py
└── requirements.txt
```

---

# Memory Design Decision

## Requirement

The assignment requires:

* Persistent cross-session memory
* Database-backed storage
* No in-memory dictionaries

## Implementation

Conversation history is stored in SQLite using SQLAlchemy.

Each message stores:

* user_id
* role
* content
* session_id
* created_at

Example:

```text
user_id      role        content
------------------------------------------------
demo-user    user        What is Enterprise pricing?
demo-user    assistant   Enterprise costs $499/mo
demo-user    user        Does that include SSO?
```

Before generating a response, the agent retrieves previous messages using:

```python
get_user_memory(user_id)
```

This allows the assistant to maintain context even after browser refreshes or separate API calls.

## Why This Design?

The memory layer is abstracted:

```text
memory/
├── base.py
└── sqlite_memory.py
```

This means switching from SQLite to:

* PostgreSQL
* Redis
* Mem0
* Vector databases

requires changing only the memory implementation rather than the entire application.

## What I Would Use At Scale

For production systems I would use:

* PostgreSQL for persistence
* Redis for hot memory caching
* Mem0 or vector memory for long-term retrieval
* Conversation summarization for large histories

---

# Tool Design

The assistant uses real callable tools.

## search_catalog(query)

Purpose:

* Searches pricing plans
* Searches features
* Prevents hallucination

Implementation:

* Sentence Transformers embeddings
* FAISS vector search
* Catalog JSON retrieval

Example:

```python
search_catalog(
    "Enterprise pricing"
)
```

---

## get_user_memory(user_id)

Purpose:

* Retrieves previous user conversations
* Maintains context across sessions

Example:

```python
get_user_memory(
    "demo-user"
)
```

---

## flag_for_human(user_id, reason)

Purpose:

* Escalates low-confidence responses
* Supports future human review workflows

Example:

```python
flag_for_human(
    user_id,
    "confidence below threshold"
)
```

---

# Evaluation Design

Every response includes a structured evaluation block.

Example:

```json
{
  "response": "Enterprise costs $499/month and includes SSO.",
  "eval": {
    "groundedness": 0.95,
    "relevance": 0.92,
    "confidence": 0.91,
    "flagged": false,
    "reasoning": "Response sourced from catalog and user memory."
  }
}
```

## Metrics

### Groundedness

Measures how well the response is supported by catalog data.

### Relevance

Measures how well the response answers the user question.

### Confidence

Measures model confidence in correctness.

### Flagged

Triggers escalation when confidence falls below threshold.

---

# Evaluation Limitations

Current implementation uses LLM self-evaluation.

Limitations:

* Not fully independent
* Can be optimistic
* May overestimate quality

For production I would replace this with:

* RAGAS
* DeepEval
* TruLens
* Dedicated evaluator models

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

# API Endpoints

## POST /chat/{user_id}

Send a message and receive:

* Response
* Evaluation block
* Tools called
* Session ID

---

## GET /chat/{user_id}/history

Retrieve full conversation history.

---

## DELETE /chat/{user_id}/memory

Delete all user memory.

---

## GET /catalog

Retrieve product catalog.

---

## GET /health

Health check endpoint.

---

# Example Chat Response

```json
{
  "response": "Enterprise costs $499/month and includes unlimited users, SSO, audit logs, and SLA.",
  "eval": {
    "groundedness": 0.95,
    "relevance": 0.93,
    "confidence": 0.91,
    "flagged": false,
    "reasoning": "Response grounded in catalog data and user memory."
  },
  "tools_called": [
    "search_catalog",
    "get_user_memory"
  ],
  "session_id": "9f59c74c-7f8f-4f5c-87cf-b18d4a0f0e13"
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
Enterprise costs $499/month and includes unlimited users, SSO, audit logs, and SLA.
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
Yes. The Enterprise plan includes SSO.
```

The second request demonstrates persistent cross-session memory because the user does not repeat the Enterprise plan name.

---

# Local Development

## Backend

```bash
cd app

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Deployment

## Backend

Railway

https://selfless-growth-production-aa22.up.railway.app/

## Frontend

Railway

https://blissful-elegance-production-bb99.up.railway.app/

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* SQLite
* Groq
* Sentence Transformers
* FAISS

## Frontend

* React
* Vite
* Axios

## Infrastructure

* Docker
* Railway
* GitHub Actions

---

# Future Improvements

* PostgreSQL production database
* Redis caching
* Memory summarization
* Human review dashboard
* RAGAS-based evaluation
* Multi-agent architecture
* Streaming responses
* Observability and tracing
