from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src import models, schemas
from src.database import get_db

router = APIRouter(prefix="/api/posts/{post_id}/comments", tags=["comments"])


@router.post("", status_code=201, response_model=schemas.CommentResponse)
async def create_comment(
    post_id: int, data: schemas.CommentCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if not post.is_published:
        raise HTTPException(
            status_code=409,
            detail="You can comment only published post",
        )

    comment = models.Comment(**data.model_dump(), post_id=post_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("", response_model=List[schemas.CommentResponse])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Post not found")

    stmt = select(models.Comment).where(models.Comment.post_id == post_id)
    result = await db.execute(stmt)
    return result.scalars().all()
