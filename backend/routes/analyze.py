from fastapi import APIRouter, HTTPException
from models.request_models import AnalyzeRequest
from models.response_models import AnalyzeResponse
from services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_startup(request: AnalyzeRequest):
    try:
        response = await AnalysisService.process_idea(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
