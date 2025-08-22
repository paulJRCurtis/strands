from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .coordinator import CoordinatorAgent
from .models import AnalysisRequest, AnalysisResult
from ..logging_config import setup_logging
from ..middleware.logging_middleware import LoggingMiddleware
from ..config import Config
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Security Analysis Coordinator")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
coordinator = CoordinatorAgent()

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_architecture(file: UploadFile = File(...)):
    """Analyze uploaded architecture for security issues"""
    logger.info(f"Starting analysis for file: {file.filename} ({file.content_type})")
    try:
        result = await coordinator.process_analysis(file)
        logger.info(f"Analysis completed for {file.filename} - Risk Score: {result.get('risk_score', 'N/A')}")
        return result
    except Exception as e:
        logger.error(f"Analysis failed for {file.filename}: {str(e)}")
        raise

@app.get("/status/{job_id}")
async def get_analysis_status(job_id: str):
    """Get analysis job status"""
    logger.info(f"Status check for job: {job_id}")
    return await coordinator.get_job_status(job_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)