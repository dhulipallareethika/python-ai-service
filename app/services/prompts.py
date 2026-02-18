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

def getPromptDerivedArtifact(extraContext, sourceUML, requirements):

    prompt = f"""
    {extraContext}
     ### STRUCTURED DATA MODEL (SOURCE OF TRUTH)
    {requirements}
     ### UML CONTEXT (ONLY FOR DATABASE, EMPTY FOR API)
    {sourceUML}
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

def getPromptExtractStructure(requirements: str, project_name: str):
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


def getPromptRefineArtifact(extraContext, existingCode, instruction):
    prompt = f"""
    Task: Refine the following technical artifact (JSON/SQL/Code).
    Rules for this artifact type:
    {extraContext}
    [Existing Code]:
    {existingCode}
    [Refinement Instructions]:
    {instruction}
    Constraint: Return ONLY the raw code or JSON. No markdown blocks or explanations.
    """
    messages = [
        {"role": "system", "content": "You are a technical expert. Refine the provided artifact strictly following instructions."},
        {"role": "user", "content": prompt}
    ]
    return messages