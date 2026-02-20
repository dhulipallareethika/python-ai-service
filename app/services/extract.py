import json
import re
from app.services.prompts import get_prompt_extract_structure
from app.kadalclient import get_chat_completion 
from app.logger import log

async def extract_project_structure(requirements_text: str, project_name: str, correlation_id: str) -> dict:
    messages = get_prompt_extract_structure(requirements_text, project_name)
    try:
        raw_response = await get_chat_completion(messages, correlation_id=correlation_id)
        clean_json = re.sub(r'```(?:json)?', '', raw_response).strip()
        clean_json = clean_json.replace('```', '') 
        structured_data = json.loads(clean_json)
        log.info(f"Structure extracted successfully for {project_name}", extra={'correlation_id': correlation_id})
        return structured_data
    except json.JSONDecodeError as e:
        log.error(f"JSON Parsing Error: {str(e)}", extra={'correlation_id': correlation_id})
        return {
            "projectName": project_name,
            "classes": [],
            "error": "Failed to parse AI response into JSON",
            "raw_snippet": raw_response[:200] if raw_response else ""
        }
    except Exception as e:
        log.error(f"Unexpected error in extraction: {str(e)}", extra={'correlation_id': correlation_id})
        raise e