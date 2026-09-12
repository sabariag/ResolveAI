from fastapi import APIRouter
from backend.models.request_models import ResolveRequest
from backend.services.agent_service import agent_service

router = APIRouter(
    prefix="/api/resolve",
    tags=["Resolve"]
)

@router.get("/health")
async def health():
    return {
        "status": "ok"
    }

@router.post("")
async def resolve_issue(request: ResolveRequest):

    result = await agent_service.process_query(
        request.model_dump()
    )

    return {
        "success": True,
        "request": request.model_dump(),
        "result": result
    }