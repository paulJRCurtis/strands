from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .coordinator import CoordinatorAgent
from ..config import Config

app = FastAPI(title="Security Analysis Coordinator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = CoordinatorAgent()

@app.post("/analyze")
async def analyze_architecture(file: UploadFile = File(...)):
    return await coordinator.process_analysis(file)

@app.get("/status/{job_id}")
async def get_analysis_status(job_id: str):
    return await coordinator.get_job_status(job_id)

@app.get("/")
async def root():
    return {"message": "Security Analysis Coordinator", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)