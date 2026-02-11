import re, json
from typing import List
from app.kadalClient import get_chat_completion
from app.model import ClassModel
from app.services.plantuml_rules import (ERD_SPECIFIC_RULES, SEQUENCE_RULES, CLASS_RULES, COMPONENT_RULES, DATABASE_CODE_RULES, API_CONTRACT_RULES, USE_CASE_RULES)
from app.services.prompts import getPromptMessage, getPromptDerivedArtifact

async def generate_derived_artifact(artifact_type: str, requirements: str, source_uml: str, classes: List[ClassModel]) -> str:
    diag_type_key = artifact_type.upper()
    if "DATABASE" in diag_type_key:
        extra_context = DATABASE_CODE_RULES
    else:
        extra_context = API_CONTRACT_RULES
    class_data = [cls.model_dump() for cls in classes]
    enriched_requirements = (
        f"Original User Requirements: {requirements}\n\n"
        f"STRICT ARCHITECTURAL STRUCTURE (Use these entities and fields only):\n"
        f"{json.dumps(class_data, indent=2)}"
    )
    messages = getPromptDerivedArtifact(extra_context, source_uml, enriched_requirements)
    llm_response = await get_chat_completion(messages)
    return llm_response

def clean_plantuml_code(raw_code: str) -> str:
    if not raw_code: return ""
    cleaned = re.sub(r'```(?:plantuml|puml|text)?', '', raw_code)
    cleaned = cleaned.replace('```', '').strip()
    return cleaned

async def generate_diagram(diagram_type: str, requirements: str, language: str, classes: List[ClassModel]) -> str:
    diag_type_key = diagram_type.upper()
    language_key = language.upper()
    class_data = [cls.model_dump() for cls in classes]
    final_requirements = (
        f"User Requirements Context: {requirements}\n\n"
        f"STRICT ARCHITECTURAL STRUCTURE TO FOLLOW:\n"
        f"{json.dumps(class_data, indent=2)}"
    )
    MAPPING = {
        "PLANTUML": {
            ("ERD", "ENTITY RELATIONSHIP"): ERD_SPECIFIC_RULES,
            ("SEQUENCE",): SEQUENCE_RULES,
            ("CLASS",): CLASS_RULES,
            ("USE CASE", "USE_CASE"): USE_CASE_RULES,
            ("COMPONENT",): COMPONENT_RULES,
        }
    }
    selected_language_rules = MAPPING.get(language_key, MAPPING["PLANTUML"])
    extra_context = f"Generate a standard, clean {language_key} diagram."
    for keywords, context in selected_language_rules.items():
        if any(key in diag_type_key for key in keywords):
            extra_context = context
            break
    extra_context = f"STRICT SCHEMA MAPPING: Transform the provided JSON into a {diag_type_key}. {extra_context}"
    messages = getPromptMessage(diagram_type, extra_context, final_requirements, language)
    raw_response = await get_chat_completion(messages)
    actual_response = clean_plantuml_code(raw_response) 
    print(actual_response)
    return actual_response