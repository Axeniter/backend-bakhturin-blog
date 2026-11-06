from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src import models, schemas
from src.database import get_db

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("", status_code=201, response_model=schemas.PostResponse)
async def create_post(data: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    post = models.Post(**data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get("/stats", response_model=schemas.PostStats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    total_posts = (await db.execute(select(func.count(models.Post.id)))).scalar() or 0
    total_comments = (await db.execute(select(func.count(models.Comment.id)))).scalar() or 0
    published = (
        await db.execute(
            select(func.count(models.Post.id)).where(models.Post.is_published == True)
        )
    ).scalar() or 0

    avg_subq = (
        select(func.avg(func.coalesce(func.count(models.Comment.id), 0)))
        .select_from(models.Post)
        .outerjoin(models.Comment)
        .group_by(models.Post.id)
    )
    avg_comments = (await db.execute(avg_subq)).scalar() or 0.0

    return schemas.PostStats(
        total_posts=total_posts,
        total_comments=total_comments,
        avg_comments_per_post=round(float(avg_comments), 2),
        published_posts=published,
    )


@router.get("", response_model=List[schemas.PostResponse])
async def get_posts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    author: Optional[str] = None,
    q: Optional[str] = Query(None, description="Поиск по заголовку без учёта регистра"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Post)
    if author:
        stmt = stmt.where(models.Post.author == author)
    if q:
        stmt = stmt.where(models.Post.title.ilike(f"%{q}%"))
    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, data: schemas.PostUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return None
