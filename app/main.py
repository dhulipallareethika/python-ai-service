import uuid
from fastapi import FastAPI, Request, Body
from app.model import *
from app.services.generate import generate_diagram, generate_derived_artifact
from app.handlers import global_exception_handler, global_response_middleware
from fastapi.exceptions import RequestValidationError
from app.services.extract import extract_project_structure
from app.logger import log
from app.services.generate import refine_diagram, refine_derived_artifact

app = FastAPI(title="Archie AI Service", openapi_version="3.0.2")
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = corr_id
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = corr_id
    return response

@app.middleware("http")
async def wrap_response(request: Request, call_next):
    return await global_response_middleware(request, call_next)

@app.post("/generate")
async def generate(request: Request, gen_req: GenerateRequest = Body(...)):
    c_id = request.state.correlation_id
    log.info(f"Process started for {gen_req.diagramType}", extra={'correlation_id': c_id})
    diagramType = gen_req.diagramType
    if diagramType == DiagramType.DATABASE:
        uml_context = await generate_diagram(
            "ERD",
            gen_req.requirementsText,
            "PLANTUML",
            gen_req.classes,
            flag=True,
            correlation_id=c_id
        )
        final_output = await generate_derived_artifact(
            "DATABASE",
            gen_req.requirementsText,
            uml_context,
            gen_req.classes,
            correlation_id=c_id
        )
        return {
            "diagramType": diagramType,
            "diagramLanguage": "SQL/NoSQL",
            "diagramCode": final_output,
            "isRenderable": False,
            "correlation_id": c_id
        }
    if diagramType == DiagramType.API:
        final_output = await generate_derived_artifact(
            "API",
            gen_req.requirementsText,
            "",  
            gen_req.classes,
            correlation_id=c_id
        )
        return {
            "diagramType": diagramType,
            "diagramLanguage": "OPENAPI",
            "diagramCode": final_output,
            "isRenderable": False,
            "correlation_id": c_id
        }
    diagram_code = await generate_diagram(
        diagramType.value,
        gen_req.requirementsText,
        gen_req.diagramLanguage,
        gen_req.classes,
        flag=False,
        correlation_id=c_id
    )
    return {
        "diagramType": diagramType,
        "diagramLanguage": gen_req.diagramLanguage,
        "diagramCode": diagram_code,
        "isRenderable": True,
        "correlation_id": c_id
    }

@app.post("/extract", response_model=ProjectResponse)
async def extract_structure(request: Request, ext_req: ExtractionRequest = Body(...)):
    c_id = request.state.correlation_id
    log.info(f"Extracting structure for project: {ext_req.projectName}", extra={'correlation_id': c_id})
    structured_data = await extract_project_structure(
        ext_req.requirementsText, 
        ext_req.projectName,
        correlation_id=c_id
    )
    return structured_data

@app.post("/refine")
async def refine(request: Request, ref_req: RefineRequest = Body(...)):
    c_id = request.state.correlation_id # Corrected: Extracting from state
    diagramType = ref_req.diagramType
    if diagramType in [DiagramType.DATABASE, DiagramType.API]:
        is_db = (diagramType == DiagramType.DATABASE)
        refined_output = await refine_derived_artifact(diagramType.value, ref_req.existingDiagramCode, ref_req.userInstruction, correlation_id=c_id)
        return {
            "diagramType": diagramType,
            "diagramLanguage": "JSON/SQL" if is_db else "OPENAPI",
            "diagramCode": refined_output,
            "isRenderable": False,
            "correlation_id": c_id
        }
    refined_code = await refine_diagram(diagramType.value, ref_req.existingDiagramCode, ref_req.userInstruction, ref_req.diagramLanguage, correlation_id=c_id)
    return {
        "diagramType": diagramType,
        "diagramLanguage": ref_req.diagramLanguage,
        "diagramCode": refined_code,
        "isRenderable": True,
        "correlation_id": c_id
    }