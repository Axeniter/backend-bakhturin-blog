from pydantic import BaseModel, Field
from typing import Optional

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    is_published: bool = Field(False)

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = Field(None)

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    is_published: bool
