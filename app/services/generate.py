import re, json
from typing import List
from app.kadalClient import get_chat_completion
from app.model import ClassModel
from app.services.plantuml_rules import (
    ERD_SPECIFIC_RULES, SEQUENCE_RULES, CLASS_RULES, COMPONENT_RULES, DATABASE_CODE_RULES, API_CONTRACT_RULES, USE_CASE_RULES,
    ERD_MERMAID_RULES, SEQUENCE_MERMAID_RULES, CLASS_MERMAID_RULES, USE_CASE_MERMAID_RULES, COMPONENT_MERMAID_RULES)
from app.services.prompts import getPromptMessage, getPromptDerivedArtifact

async def generate_derived_artifact(artifact_type: str, requirements: str, source_uml: str, classes: List[ClassModel]) -> str:
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
    messages = getPromptDerivedArtifact(
        extra_context,
        source_uml if artifact_key == "DATABASE" else "", 
        enriched_requirements
    )
    llm_response = await get_chat_completion(messages)
    print(llm_response)
    return llm_response

def clean_plantuml_code(raw_code: str) -> str:
    if not raw_code: return ""
    cleaned = re.sub(r'(?:plantuml|puml|text)?', '', raw_code)
    cleaned = cleaned.replace('', '').strip()
    return cleaned

async def generate_diagram(diagram_type: str, requirements: str, language: str, classes: List[ClassModel], flag: bool) -> str:
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
        },
        "MERMAID": {
            ("ERD", "ENTITY RELATIONSHIP"): ERD_MERMAID_RULES,
            ("SEQUENCE",): SEQUENCE_MERMAID_RULES,
            ("CLASS",): CLASS_MERMAID_RULES,
            ("USE CASE", "USE_CASE"): USE_CASE_MERMAID_RULES,
            ("COMPONENT",): COMPONENT_MERMAID_RULES,
        }
    }
    language_rules = MAPPING.get(language_key, MAPPING["PLANTUML"])
    extra_context = f"Generate a standard, clean {language_key} diagram."
    for keywords, context in language_rules.items():
        if any(key in diag_type_key for key in keywords):
            extra_context = context
            break
    extra_context = f"STRICT SCHEMA MAPPING: Transform the provided JSON into a {diag_type_key}. {extra_context}"
    messages = getPromptMessage(diagram_type, extra_context, final_requirements, language)
    raw_response = await get_chat_completion(messages)
    actual_response = clean_plantuml_code(raw_response) 
    if not flag:
        print(actual_response)
    return actual_response