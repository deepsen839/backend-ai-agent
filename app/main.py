from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware
)
from app.tools.search_catalog import (
    initialize_catalog_search
)
from app.db.database import (
    Base,
    engine
)

from app.api.chat import (
    router as chat_router
)

from app.api.catalog import (
    router as catalog_router
)

from app.api.health import (
    router as health_router
)

from app.api.evals import (
    router as eval_router
)

# Create tables on startup
Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Persistent Sales Assistant",
    version="1.0.0",
    description="""
Persistent AI Sales Assistant

Features:
- Cross-session memory
- Tool calling
- Catalog search
- Self evaluation
- Human escalation
"""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    chat_router
)

app.include_router(
    catalog_router
)

app.include_router(
    health_router
)

app.include_router(
    eval_router
)


@app.get("/")
def root():
    return {
        "service": "Persistent Sales Assistant",
        "status": "running",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():

    initialize_catalog_search()