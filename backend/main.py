from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import companies, recommendations
app = FastAPI(
    title="WorkSphere API",
    description="AI-driven Career Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(companies.router)
app.include_router(recommendations.router)
@app.get("/")
def home():
    return {"message": "Welcome to WorkSphere API"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "WorkSphere"}
