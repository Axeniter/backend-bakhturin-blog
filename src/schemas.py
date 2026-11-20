from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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
    created_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    id: int
    text: str
    author: str
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostStats(BaseModel):
    total_posts: int
    total_comments: int
    avg_comments_per_post: float
    published_posts: int
