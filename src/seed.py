import asyncio
from sqlalchemy import select, func
from src.database import AsyncSessionLocal
from src import models


async def seed():
    async with AsyncSessionLocal() as db:
        existing = (await db.execute(select(func.count(models.Post.id)))).scalar()
        if existing > 0:
            print("Database already seeded")
            return

        p1 = models.Post(
            title="Hello world", content="hi everyone)", author="Alex", is_published=True
        )
        p2 = models.Post(
            title="Bye World", content="bye everyone(", author="Alex", is_published=False
        )
        db.add_all([p1, p2])
        await db.commit()
        await db.refresh(p1)

        db.add_all([
            models.Comment(text="hello", author="Max", post_id=p1.id),
            models.Comment(text="it's cool", author="Ivan", post_id=p1.id),
        ])
        await db.commit()
        print("Database seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed())
