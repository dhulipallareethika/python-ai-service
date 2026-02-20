import json
from typing import List
from app.kadalclient import get_chat_completion
from app.model import ClassModel
from app.services.rules import DATABASE_CODE_RULES, API_CONTRACT_RULES
from app.services.prompts import (get_prompt_message, get_prompt_derived_artifact, strip_markdown, 
    get_prompt_refine_diagram, get_prompt_refine_artifact, MAPPING)
from app.logger import log

async def generate_derived_artifact(artifact_type: str, requirements: str, source_uml: str, classes: List[ClassModel], correlation_id: str) -> str:
    log.info(f"Process started for {artifact_type}")
    artifact_key = artifact_type.upper()
    if artifact_key == "DATABASE":
        extra_context = DATABASE_CODE_RULES
    elif artifact_key == "API":
        extra_context = API_CONTRACT_RULES
    else:
        raise ValueError("Invalid derived artifact type") 
    class_data = [cls.model_dump() for cls in classes]
    enriched_requirements = (
        f"Original User Requirements:\n{requirements}\n\n"
        f"STRICT STRUCTURED DATA MODEL (SOURCE OF TRUTH):\n"
        f"{json.dumps(class_data, indent=2)}"
    )
    messages = get_prompt_derived_artifact( extra_context, source_uml if artifact_key == "DATABASE" else "", enriched_requirements)
    llm_response = await get_chat_completion(messages, correlation_id=correlation_id)
    final_output = strip_markdown(llm_response)
    log.info(f"Derived artifact ({artifact_key}) generated", extra={'correlation_id': correlation_id})
    #print(final_output)
    return final_output

async def generate_diagram(diagram_type: str, requirements: str, language: str, classes: List[ClassModel], flag: bool, correlation_id: str) -> str:
    log.info(f"Process started for {diagram_type} using {language}")
    diag_type_key = diagram_type.upper()
    language_key = language.upper()
    class_data = [cls.model_dump() for cls in classes]
    final_requirements = (
        f"User Requirements Context: {requirements}\n\n"
        f"STRICT ARCHITECTURAL STRUCTURE TO FOLLOW:\n"
        f"{json.dumps(class_data, indent=2)}"
    )
    selected_language_rules = MAPPING.get(language_key, MAPPING.get("PLANTUML"))
    extra_context = f"Generate a standard, clean {language_key} diagram."
    for keywords, context in selected_language_rules.items():
        if any(key in diag_type_key for key in keywords):
            extra_context = context
            break    
    extra_context = f"STRICT SCHEMA MAPPING: Transform the provided JSON into a {diag_type_key}. {extra_context}"
    messages = get_prompt_message(diagram_type, extra_context, final_requirements, language)
    raw_response = await get_chat_completion(messages, correlation_id=correlation_id)
    actual_response = strip_markdown(raw_response) 
    if not flag:
        log.info(f"Successfully generated {diag_type_key} diagram code", extra={'correlation_id': correlation_id})
    print(actual_response)    
    return actual_response

async def refine_derived_artifact(artifact_type: str, existing_code: str, user_instruction: str, correlation_id: str) -> str:
    log.info(f"Process started for {artifact_type}")
    artifact_key = artifact_type.upper()
    if artifact_key == "DATABASE":
        extra_context = DATABASE_CODE_RULES
    elif artifact_key == "API":
        extra_context = API_CONTRACT_RULES
    else:
        raise ValueError("Invalid derived artifact type")
    messages = get_prompt_refine_artifact(extra_context, existing_code, user_instruction)
    llm_response = await get_chat_completion(messages, correlation_id=correlation_id)
    log.info(f"Refined {artifact_key} artifact", extra={'correlation_id': correlation_id})
    return strip_markdown(llm_response)

async def refine_diagram(diagram_type: str, existing_diagram_code: str, user_instruction: str, language: str, correlation_id: str) -> str:
    log.info(f"Process started for {diagram_type} using {language}")
    diag_type_key = diagram_type.upper()
    language_key = language.upper()
    selected_language_rules = MAPPING.get(language_key, MAPPING.get("PLANTUML"))
    rule_context = f"Maintain standard {language_key} syntax."
    for keywords, context in selected_language_rules.items():
        if any(key in diag_type_key for key in keywords):
            rule_context = context
            break
    extra_context = f"REFINEMENT MODE: {rule_context}"
    messages = get_prompt_refine_diagram(extra_context, existing_diagram_code, user_instruction, language)
    raw_response = await get_chat_completion(messages, correlation_id=correlation_id)
    log.info(f"Refined {diag_type_key} diagram code", extra={'correlation_id': correlation_id})
    #print(strip_markdown(raw_response))
    return strip_markdown(raw_response)