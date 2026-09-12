from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.routes.resolve import router

app = FastAPI(title="ResolveAI API")

app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        }
    )


@app.get("/")
def home():
    return {
        "message": "ResolveAI Backend Running"
    }