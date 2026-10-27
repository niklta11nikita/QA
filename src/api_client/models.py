from pydantic import BaseModel

class PostRequest(BaseModel):
    title: str
    body: str
    userId: int

class PostResponse(BaseModel):
    title: str
    body: str
    userId: int
    id: int