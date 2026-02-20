from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import json
from starlette.concurrency import iterate_in_threadpool
from app.logger import log

class LLMServiceError(Exception):
    def __init__(self, message: str):
        self.message = message

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        error_details = exc.errors()
        log.error(f"Validation Error occurred: {error_details}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "FAILURE",
                "data": None,
                "error": {
                    "message": "Invalid request parameters",
                    "details": error_details,
                    "code": "VALIDATION_ERROR"
                }
            }
        )
    if isinstance(exc, LLMServiceError):
        log.error(f"LLM Service Error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "status": "FAILURE",
                "data": None,
                "error": {"message": exc.message, "code": "LLM_PROVIDER_ERROR"}
            }
        )
    log.exception(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "FAILURE",
            "data": None,
            "error": {"message": "Internal Server Error", "code": "INTERNAL_ERROR"}
        }
    )

async def global_response_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 200 and "application/json" in response.headers.get("content-type", ""):
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))  
        try:
            body_json = json.loads(response_body[0].decode())
            if isinstance(body_json, dict) and "status" in body_json:
                return response
            wrapped_content = {
                "status": "SUCCESS",
                "data": body_json,
                "error": None
            }
            return JSONResponse(content=wrapped_content, status_code=200)
        except :
            pass
    return response