import logging
import asyncio
import time
import json
from models.request_models import AnalyzeRequest
from models.response_models import AnalyzeResponse
from services.gemma_service import generate_response
from prompts.prompts import (
    INVESTOR_SYSTEM_PROMPT,
    CTO_SYSTEM_PROMPT,
    CUSTOMER_SYSTEM_PROMPT,
    COMPETITOR_SYSTEM_PROMPT,
    GROWTH_SYSTEM_PROMPT,
    FINAL_BOARD_SYSTEM_PROMPT,
    get_user_prompt,
    get_final_board_user_prompt
)

# Configure simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_investor_review(startup_name: str, startup_idea: str) -> str:
    logger.info("Investor Agent started.")
    res = await generate_response(INVESTOR_SYSTEM_PROMPT, get_user_prompt(startup_name, startup_idea))
    logger.info("Investor Agent completed.")
    return res

async def run_cto_review(startup_name: str, startup_idea: str) -> str:
    logger.info("CTO Agent started.")
    res = await generate_response(CTO_SYSTEM_PROMPT, get_user_prompt(startup_name, startup_idea))
    logger.info("CTO Agent completed.")
    return res

async def run_customer_review(startup_name: str, startup_idea: str) -> str:
    logger.info("Customer Agent started.")
    res = await generate_response(CUSTOMER_SYSTEM_PROMPT, get_user_prompt(startup_name, startup_idea))
    logger.info("Customer Agent completed.")
    return res

async def run_competitor_review(startup_name: str, startup_idea: str) -> str:
    logger.info("Competitor Agent started.")
    res = await generate_response(COMPETITOR_SYSTEM_PROMPT, get_user_prompt(startup_name, startup_idea))
    logger.info("Competitor Agent completed.")
    return res

async def run_growth_review(startup_name: str, startup_idea: str) -> str:
    logger.info("Growth Agent started.")
    res = await generate_response(GROWTH_SYSTEM_PROMPT, get_user_prompt(startup_name, startup_idea))
    logger.info("Growth Agent completed.")
    return res

async def run_final_board_review(investor: str, cto: str, customer: str, competitor: str, growth: str) -> dict:
    logger.info("Final Board Agent started.")
    user_prompt = get_final_board_user_prompt(investor, cto, customer, competitor, growth)
    res = await generate_response(FINAL_BOARD_SYSTEM_PROMPT, user_prompt)
    logger.info("Final Board Agent completed.")
    
    try:
        # Simple cleanup in case local LLMs ignore strict formatting instructions and append markdown
        clean_res = res.strip()
        if clean_res.startswith("```json"):
            clean_res = clean_res[7:]
        elif clean_res.startswith("```"):
            clean_res = clean_res[3:]
            
        if clean_res.endswith("```"):
            clean_res = clean_res[:-3]
            
        parsed = json.loads(clean_res.strip())
        return parsed
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Final Board JSON. Error: {e}. Raw response: {res}")
        return {
            "survival_score": 0,
            "market_score": 0,
            "technical_score": 0,
            "customer_score": 0,
            "competition_score": 0,
            "growth_score": 0,
            "biggest_risk": "Failed to parse Final Board response.",
            "biggest_opportunity": "Failed to parse Final Board response.",
            "recommended_pivot": "N/A",
            "verdict": "Build with Caution",
            "board_decision_confidence": 0,
            "action_plan": ["Review LLM raw output", "Fix JSON parsing error", "Retry evaluation", "N/A", "N/A", "N/A", "N/A"]
        }

class AnalysisService:
    @staticmethod
    async def process_idea(request: AnalyzeRequest) -> AnalyzeResponse:
        logger.info(f"Starting board analysis for startup: {request.startup_name}")
        start_time = time.time()
        
        # Phase 1: Run all 5 individual agent reviews concurrently
        (
            investor_review,
            cto_review,
            customer_review,
            competitor_review,
            growth_review
        ) = await asyncio.gather(
            run_investor_review(request.startup_name, request.startup_idea),
            run_cto_review(request.startup_name, request.startup_idea),
            run_customer_review(request.startup_name, request.startup_idea),
            run_competitor_review(request.startup_name, request.startup_idea),
            run_growth_review(request.startup_name, request.startup_idea)
        )
        
        # Phase 2: Feed all 5 reviews into the Final Board synthesis
        final_board_data = await run_final_board_review(
            investor=investor_review,
            cto=cto_review,
            customer=customer_review,
            competitor=competitor_review,
            growth=growth_review
        )
        
        execution_time = time.time() - start_time
        logger.info(f"Total execution time for all agents + board: {execution_time:.2f} seconds")
        
        # Returning real aggregated data!
        return AnalyzeResponse(
            investor_review=investor_review,
            cto_review=cto_review,
            customer_review=customer_review,
            competitor_review=competitor_review,
            growth_review=growth_review,
            survival_score=final_board_data.get("survival_score", 0),
            market_score=final_board_data.get("market_score", 0),
            technical_score=final_board_data.get("technical_score", 0),
            customer_score=final_board_data.get("customer_score", 0),
            competition_score=final_board_data.get("competition_score", 0),
            growth_score=final_board_data.get("growth_score", 0),
            biggest_risk=final_board_data.get("biggest_risk", "Unknown"),
            biggest_opportunity=final_board_data.get("biggest_opportunity", "Unknown"),
            recommended_pivot=final_board_data.get("recommended_pivot", "None"),
            verdict=final_board_data.get("verdict", "Do Not Build"),
            board_decision_confidence=final_board_data.get("board_decision_confidence", 0),
            action_plan=final_board_data.get("action_plan", [])
        )
