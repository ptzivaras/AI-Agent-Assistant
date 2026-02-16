from fastapi import FastAPI
from app.app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nexus API")

@app.get("/")
def root():
    return {"message": "Nexus API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
