from fastapi import FastAPI
from app.app.database import engine, Base
from app.app.models import Ticket  # Import models to register with Base

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nexus AI - Ticket Classification System",
    description="AI-powered ticket classification with structured output",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Nexus API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
