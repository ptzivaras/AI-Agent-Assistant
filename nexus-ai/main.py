from fastapi import FastAPI
from app.app.database import engine, Base
from app.app.models import Ticket  # Import models to register with Base
from app.app.routers import tickets_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nexus AI - Ticket Classification System",
    description="AI-powered ticket classification with structured output",
    version="1.0.0"
)

# Include routers
app.include_router(tickets_router)

@app.get("/")
def root():
    return {
        "message": "Nexus AI - Ticket Classification System",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "create_ticket": "POST /tickets",
            "list_tickets": "GET /tickets",
            "get_ticket": "GET /tickets/{id}",
            "statistics": "GET /tickets/stats"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
