from app.services.rules import (
    ERD_SPECIFIC_RULES, SEQUENCE_RULES, CLASS_RULES, COMPONENT_RULES, USE_CASE_RULES, 
    ERD_MERMAID_RULES, SEQUENCE_MERMAID_RULES, CLASS_MERMAID_RULES, USE_CASE_MERMAID_RULES, COMPONENT_MERMAID_RULES
    )
import re

def get_prompt_message(diagram_type:  str, extra_context: str, requirements: str,language:str):
    lang = language.upper()
    if lang == "MERMAID":
        syntax_header = "appropriate Mermaid header (e.g., erDiagram, sequenceDiagram, graph TD, etc.)"
        constraint_text = f"""
        Constraint: Return ONLY raw Mermaid.js code. 
        NO markdown (```), NO introductory text. 
        Ensure the code starts with the {syntax_header}.
        NEVER use @startuml or @enduml tags."""
    else:
        constraint_text = """
        Constraint: Return ONLY raw PlantUML code. 
        NO markdown (```), NO introductory text. 
        Ensure code starts with @startuml and ends with @enduml."""
    prompt = f"""
    Task: Generate a {diagram_type} in {language}.
    Critical Formatting Rules:
    {extra_context}
    User Requirements:
    {requirements}
    {constraint_text}
    """
    messages = [
        {"role": "system", "content": f"You are a software architect expert in {language}. You output ONLY valid, error-free {language} code without markdown decoration."},
        {"role": "user", "content": prompt}
    ]
    return messages

def get_prompt_derived_artifact(extra_context, source_uml, requirements):
    prompt = f"""
    {extra_context}
    ### STRUCTURED DATA MODEL (SOURCE OF TRUTH)
    {requirements}
    ### UML CONTEXT (ONLY FOR DATABASE, EMPTY FOR API)
    {source_uml}
    ### FINAL RULES
    You are a CODE GENERATOR ONLY.
    - API → Output ONLY OpenAPI YAML
    - DATABASE → Output ONLY SQL + MongoDB
    - NO UML
    - NO PlantUML
    - NO @startuml
    - NO diagrams
    - NO markdown
    """
    messages = [
        {
            "role": "system",
            "content": "You are a strict code generator. You never output UML, diagrams, markdown, or explanations."
        },
        {"role": "user", "content": prompt}
    ]
    return messages

def get_prompt_extract_structure(requirements: str, project_name: str):
    prompt = f"""
    Task: Analyze the requirements and extract a structured Class Diagram JSON.
    Rules for Enums:
    - Attribute "nature": Must be one of ["Identifying", "Descriptive", "Optional"]
    - Relationship "nature": Must be one of ["Association", "Aggregation", "Composition"]
    - Relationship "sourcetype"/"targettype": Must be one of ["One", "Many"]
    Constraint: Return ONLY a raw JSON object. No markdown, no triple backticks (```).
    Structure:
    {{
        "projectName": "{project_name}",
        "classes": [
            {{
                "className": "Name",
                "attributes": [
                    {{ "name": "attrName", "type": "String", "nature": "Identifying", "required": true }}
                ],
                "relationships": [
                    {{ "source": "ClassA", "target": "ClassB", "nature": "Association", "sourcetype": "One", "targettype": "Many", "label": "has" }}
                ]
            }}
        ]
    }}
    User Requirements:
    {requirements}
    """
    messages = [
        {"role": "system", "content": "You are a software architect that outputs ONLY valid JSON based on class structures."},
        {"role": "user", "content": prompt}
    ]
    return messages

def get_prompt_refine_diagram(extra_context, existing_code, instruction,language):
    lang = language.upper()
    if lang == "MERMAID":
        header_instruction = "appropriate Mermaid header (e.g., erDiagram, sequenceDiagram, graph TD)"
        constraint_text = f"""
        Constraint: Return ONLY raw Mermaid.js code. 
        NO markdown (```), NO introductory text. 
        Ensure the code starts with the {header_instruction}.
        NEVER use @startuml or @enduml tags."""
    else:
        constraint_text = """
        Constraint: Return ONLY raw PlantUML code. 
        NO markdown (```), NO introductory text. 
        Ensure code starts with @startuml and ends with @enduml."""
    prompt = f"""
    Task: Refine the following {language} diagram based on the user instructions.
    Critical Formatting Rules:
    {extra_context}
    [Existing {language} Code]:
    {existing_code}
    [User Instructions]:
    {instruction}
    {constraint_text}
    """
    messages = [
        {"role": "system", "content": f"You are a software architect expert in {language} refinement. You output ONLY valid, error-free raw code without markdown decoration."},
        {"role": "user", "content": prompt}
    ]
    return messages

def get_prompt_refine_artifact(extra_context, existing_code, instruction):
    prompt = f"""
    Task: Refine the following technical artifact (JSON/SQL/Code).
    Rules for this artifact type:
    {extra_context}
    [Existing Code]:
    {existing_code}
    [Refinement Instructions]:
    {instruction}
    Constraint: Return ONLY the raw code or JSON. No markdown blocks or explanations.
    """
    messages = [
        {"role": "system", "content": "You are a technical expert. Refine the provided artifact strictly following instructions."},
        {"role": "user", "content": prompt}
    ]
    return messages

def strip_markdown(text: str) -> str:
    if not text: return ""
    cleaned = re.sub(r'```(?:\w+)?', '', text)
    return cleaned.replace('```', '').strip()

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