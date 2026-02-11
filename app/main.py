from fastapi import FastAPI, Request
from app.model import *
from app.services.generate import generate_diagram, generate_derived_artifact
from app.handlers import global_exception_handler, global_response_middleware
from fastapi.exceptions import RequestValidationError
from app.services.extract import extract_project_structure

app = FastAPI(title="Archie AI Service", openapi_version="3.0.2")

# Global Error Handlers for robust validation and exception catching
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

@app.middleware("http")
async def wrap_response(request: Request, call_next):
    """
    Standardizes the API response format globally.
    """
    return await global_response_middleware(request, call_next)

@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generates either a visual diagram or a code-based artifact (SQL/OpenAPI).
    """
    diagramType = request.diagramType
    diagramLanguage = request.diagramLanguage
    
    # 1. Handle Derived Artifacts (DATABASE -> SQL, API -> OpenAPI)
    if diagramType in [DiagramType.DATABASE, DiagramType.API]:
        is_db = (diagramType == DiagramType.DATABASE)
        # Use ERD logic for Database and Sequence logic for API as the base UML context
        base_uml_type = "ERD" if is_db else "SEQUENCE" 
        
        # Step A: Generate the intermediate UML context (PlantUML)
        uml_context = await generate_diagram(
            base_uml_type, 
            request.requirementsText, 
            "PLANTUML", 
            request.classes 
        )
        
        # Step B: Transform the UML and Classes into the final code-based artifact
        final_output = await generate_derived_artifact(
            diagramType.value, 
            request.requirementsText, 
            uml_context,
            request.classes  
        )
        
        return {
            "diagramType": diagramType,
            "diagramLanguage": "SQL/NoSQL" if is_db else "OPENAPI",
            "diagramCode": final_output,  # The YAML or SQL code
            "isRenderable": False         # These are code snippets, not images
        }
    
    # 2. Handle Standard Visual Diagrams (CLASS, SEQUENCE, USE_CASE, etc.)
    diagram_code = await generate_diagram(
        diagramType.value, 
        request.requirementsText, 
        request.diagramLanguage,
        request.classes  
    )
    
    return {
        "diagramType": diagramType,
        "diagramLanguage": diagramLanguage,
        "diagramCode": diagram_code,
        "isRenderable": True
    }

@app.post("/extract", response_model=ProjectResponse)
async def extract_structure(request: ExtractionRequest):
    """
    Analyzes raw text requirements and extracts the structured JSON classes 
    required for the /generate endpoint.
    """
    structured_data = await extract_project_structure(
        request.requirementsText, 
        request.project_id
    )
    return structured_data