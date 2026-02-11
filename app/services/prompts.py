def getPromptMessage(diagramType:  str, extraContext: str, requirements: str,language:str):
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
    Task: Generate a {diagramType} in {language}.
    Critical Formatting Rules:
    {extraContext}
    User Requirements:
    {requirements}
    {constraint_text}
    """
    messages = [
        {"role": "system", "content": f"You are a software architect expert in {language}. You output ONLY valid, error-free {language} code without markdown decoration."},
        {"role": "user", "content": prompt}
    ]
    return messages

# app/services/prompts.py

def getPromptDerivedArtifact(extraContext, sourceUML, requirements):
    # We add a 'STRICT NO-UML' instruction here
    prompt = f"""
    {extraContext}

    ### DATA SOURCE
    Based on this Architecture Design:
    {sourceUML}

    And this Structured Data Model:
    {requirements}

    ### FINAL INSTRUCTION
    You are a Code Generator, NOT a diagram generator. 
    - If this is API: Return ONLY valid YAML.
    - If this is DATABASE: Return ONLY valid SQL and MongoDB commands.
    - REJECT all PlantUML tags. If you output '@startuml', the system will fail.
    """
    messages = [
        {
            "role": "system", 
            "content": "You are a specialized bot that converts UML designs into raw code (YAML/SQL). You never use markdown, never use conversational filler, and never use PlantUML tags."
        },
        {"role": "user", "content": prompt}
    ]
    return messages

def getPromptExtractStructure(requirements: str, project_id: str):
    prompt = f"""
    Task: Analyze the requirements and extract a structured Class Diagram JSON.
    
    Rules for Enums:
    - Attribute "nature": Must be one of ["Identifying", "Descriptive", "Optional"]
    - Relationship "nature": Must be one of ["Association", "Aggregation", "Composition"]
    - Relationship "sourcetype"/"targettype": Must be one of ["One", "Many"]

    Constraint: Return ONLY a raw JSON object. No markdown, no triple backticks (```).
    
    Structure:
    {{
        "project_id": "{project_id}",
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