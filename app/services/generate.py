import re
import json
from typing import List
from app.kadalClient import get_chat_completion
from app.model import ClassModel
from app.logger import log
from app.services.rules import ( ERD_SPECIFIC_RULES, SEQUENCE_RULES, CLASS_RULES, COMPONENT_RULES, DATABASE_CODE_RULES, API_CONTRACT_RULES, USE_CASE_RULES,
    ERD_MERMAID_RULES, SEQUENCE_MERMAID_RULES, CLASS_MERMAID_RULES, USE_CASE_MERMAID_RULES, COMPONENT_MERMAID_RULES)
from app.services.prompts import ( getPromptMessage, getPromptDerivedArtifact, getPromptRefineArtifact)

def clean_plantuml_code(raw_code: str) -> str:
    """Strips markdown and unnecessary text to ensure clean Diagram-as-Code."""
    if not raw_code: 
        return ""
    cleaned = re.sub(r'```(?:plantuml|puml|text|mermaid)?', '', raw_code)
    cleaned = cleaned.replace('```', '').strip()
    return cleaned

def get_language_rules(diagram_type: str, language: str) -> str:
    """Helper to fetch specific rules based on diagram type and language."""
    diag_type_key = diagram_type.upper()
    language_key = language.upper()
    mapping = {
        "PLANTUML": {
            ("ERD", "ENTITY RELATIONSHIP"): ERD_SPECIFIC_RULES,
            ("SEQUENCE",): SEQUENCE_RULES,
            ("CLASS",): CLASS_RULES,
            ("USE CASE", "USE_CASE"): USE_CASE_RULES,
            ("COMPONENT",): COMPONENT_RULES,
        },
        "MERMAID": {
            ("ERD", "ENTITY RELATIONSHIP"): ERD_MERMAID_RULES,
            ("SEQUENCE",): SEQUENCE_MERMAID_RULES,
            ("CLASS",): CLASS_MERMAID_RULES,
            ("USE CASE", "USE_CASE"): USE_CASE_MERMAID_RULES,
            ("COMPONENT",): COMPONENT_MERMAID_RULES,
        }
    }
    language_rules = mapping.get(language_key, mapping["PLANTUML"])
    for keywords, context in language_rules.items():
        if any(key in diag_type_key for key in keywords):
            return context
    return f"Generate a standard, clean {language_key} diagram."

async def generate_diagram( diagram_type: str, requirements: str, language: str, classes: List[ClassModel], flag: bool, correlation_id: str) -> str:
    log.info(f"Generating {language} {diagram_type}", extra={'correlation_id': correlation_id})
    class_data = [cls.model_dump() for cls in classes]
    final_requirements = (
        f"User Requirements Context: {requirements}\n\n"
        f"STRICT ARCHITECTURAL STRUCTURE TO FOLLOW:\n"
        f"{json.dumps(class_data, indent=2)}"
    )
    extra_context = get_language_rules(diagram_type, language)
    extra_context = f"STRICT SCHEMA MAPPING: Transform the provided JSON into a {diagram_type.upper()}. {extra_context}"
    messages = getPromptMessage(diagram_type, extra_context, final_requirements, language)
    raw_response = await get_chat_completion(messages, correlation_id=correlation_id)
    actual_response = clean_plantuml_code(raw_response) 
    if not flag:
        log.info(f"Diagram created and cleaned", extra={'correlation_id': correlation_id})
        print(actual_response)
    return actual_response

async def generate_derived_artifact( artifact_type: str, requirements: str, source_uml: str, classes: List[ClassModel], correlation_id: str) -> str:
    artifact_key = artifact_type.upper()
    log.info(f"Generating artifact: {artifact_key}", extra={'correlation_id': correlation_id})
    extra_context = DATABASE_CODE_RULES if artifact_key == "DATABASE" else API_CONTRACT_RULES
    class_data = [cls.model_dump() for cls in classes]
    enriched_requirements = (
        f"Original User Requirements:\n{requirements}\n\n"
        f"STRICT STRUCTURED DATA MODEL (SOURCE OF TRUTH):\n"
        f"{json.dumps(class_data, indent=2)}"
    )
    messages = getPromptDerivedArtifact( extra_context, source_uml if artifact_key == "DATABASE" else "", enriched_requirements)
    llm_response = await get_chat_completion(messages, correlation_id=correlation_id)
    log.info(f"Artifact {artifact_key} generated successfully", extra={'correlation_id': correlation_id})
    return llm_response

async def refine_diagram( diagram_type: str, existing_diagram_code: str, user_instruction: str, language: str, correlation_id: str) -> str:
    log.info(f"Refining {language} {diagram_type}", extra={'correlation_id': correlation_id})
    extra_context = get_language_rules(diagram_type, language)
    messages = getPromptRefineArtifact(extra_context, existing_diagram_code, user_instruction)
    raw_response = await get_chat_completion(messages, correlation_id=correlation_id)
    refined_code = clean_plantuml_code(raw_response)
    log.info("Diagram refinement complete", extra={'correlation_id': correlation_id})
    print(refined_code)
    return refined_code

async def refine_derived_artifact( artifact_type: str, existing_code: str, user_instruction: str, correlation_id: str) -> str:
    log.info(f"Refining artifact: {artifact_type}", extra={'correlation_id': correlation_id})
    extra_context = DATABASE_CODE_RULES if "DATABASE" in artifact_type.upper() else API_CONTRACT_RULES
    messages = getPromptRefineArtifact(extra_context, existing_code, user_instruction)
    llm_response = await get_chat_completion(messages, correlation_id=correlation_id)
    return llm_response