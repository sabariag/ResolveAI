from pydantic import BaseModel

class ResolveRequest(BaseModel):
    query: str
    user_id: str | None = None