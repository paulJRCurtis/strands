from pydantic import BaseModel
from typing import List, Dict, Optional

class SecurityFinding(BaseModel):
    severity: str
    category: str
    description: str
    recommendation: str
    affected_component: str

class AnalysisRequest(BaseModel):
    architecture_type: str
    metadata: Optional[Dict] = None

class AnalysisResult(BaseModel):
    job_id: str
    status: str
    findings: List[SecurityFinding] = []
    risk_score: Optional[int] = None
    report: Optional[Dict] = None