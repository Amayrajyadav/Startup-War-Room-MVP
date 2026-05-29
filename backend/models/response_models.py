from pydantic import BaseModel
from typing import List, Optional

class AnalyzeResponse(BaseModel):
    investor_review: str
    cto_review: str
    customer_review: str
    competitor_review: str
    growth_review: str
    survival_score: int
    market_score: int
    technical_score: int
    customer_score: int
    competition_score: int
    growth_score: int
    biggest_risk: str
    biggest_opportunity: str
    recommended_pivot: str
    verdict: str
    board_decision_confidence: Optional[int] = 0
    action_plan: List[str]
