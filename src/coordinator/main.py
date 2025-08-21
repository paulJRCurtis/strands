from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .coordinator import CoordinatorAgent
from .models import AnalysisRequest, AnalysisResult

app = FastAPI(title="Security Analysis Coordinator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
coordinator = CoordinatorAgent()

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_architecture(file: UploadFile = File(...)):
    """Analyze uploaded architecture for security issues"""
    return await coordinator.process_analysis(file)

@app.get("/status/{job_id}")
async def get_analysis_status(job_id: str):
    """Get analysis job status"""
    return await coordinator.get_job_status(job_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)