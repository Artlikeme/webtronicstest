import redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PostLike


async def update_redis_likes_dislikes(post_id: int, session: AsyncSession):
    r = redis.Redis(host='localhost', port=6379)
    query_postlike = select(PostLike).where(
        (PostLike.post_id == post_id) & (PostLike.like == True))
    query_postdislike = select(PostLike).where(
        (PostLike.post_id == post_id) & (PostLike.like == False))

    postLike = await session.execute(query_postlike)
    postDisLike = await session.execute(query_postdislike)
    r.set(post_id, f"Likes: {len(postLike.all())} / Dislikes: {len(postDisLike.all())}")
