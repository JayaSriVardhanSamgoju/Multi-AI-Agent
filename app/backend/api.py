from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings 
from app.common.logger import get_logger 
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="Multi AI agent")


class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: list[str]
    allow_search: bool


class ErrorResponse(BaseModel):
    detail: str


class ChatResponse(BaseModel):
    response: str


@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid model name"
        },
        500: {
            "model": ErrorResponse,
            "description": "Error during generating the response"
        }
    }
)
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model {request.model_name}")
    
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model name")

    try:
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )
        logger.info(f"Successfully got the response from the AI agent {request.model_name}")
        return {"response": response}
    except Exception as e:
        logger.exception("Exception caught during generating response")
        raise HTTPException(status_code=500, detail=str(CustomException("Error during generating the response", e)))
