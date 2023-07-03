import redis
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post, PostLike
from .schemas import PostRead, PostCreate, PostBase, LikeBase
from .services import update_redis_likes_dislikes
from src.auth.auth import current_active_user
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(tags=["post"])


@router.post("/post/")
async def create_post(post: PostCreate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user),
                      ):
    try:
        post.owner_id = user.id
        stmt = insert(Post).values(**post.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except Exception:
        raise HTTPException(status_code=403, detail={
            "status": "ERROR",
            "data": None,
            "details": None
        })


@router.get("/post/list", response_model=list[PostRead])
async def read_list_posts(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()


@router.get("/post/{post_id}", response_model=PostRead)
async def read_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    return result.scalars().first()


@router.put("/post/{post_id}")
async def update_post(post_id: int,
                      post: PostBase,
                      session: AsyncSession = Depends(get_async_session)
                      ):
    try:
        stmt = update(Post).where(Post.id == post_id).values(**post.dict())
        await session.execute(stmt)
        await session.commit()
    except Exception:
        raise HTTPException(status_code=403, detail={
            "status": "ERROR",
            "data": None,
            "details": None
        })


@router.delete("/post/{post_id}")
async def delete_post(post_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)
                      ):
    stmt = delete(Post).where(Post.id == post_id, Post.owner_id == user.id)
    await session.execute(stmt)
    await session.commit()


@router.post("/like/post")
async def like_post(like: LikeBase,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user),
                    ):
    try:
        post = await session.execute(select(Post).where(Post.id == like.post_id))
        post_first = post.scalars().first()
        if not post_first:
            raise HTTPException(status_code=404, detail="Post not found")
        if post_first.owner_id == user.id:
            raise HTTPException(status_code=403, detail="This post is yours")

        like.owner_id = user.id

        query_postlike = select(PostLike).where(
            (PostLike.post_id == like.post_id) & (PostLike.owner_id == like.owner_id))
        postLike = await session.execute(query_postlike)
        if not postLike.all():
            await session.execute(insert(PostLike).values(**like.dict()))
        else:
            await session.execute(update(PostLike).
                                  where((PostLike.post_id == like.post_id) & (PostLike.owner_id == like.owner_id)).
                                  values(like=like.like))

        await update_redis_likes_dislikes(like.post_id, session)  # redis update
        await session.commit()
        return {"status": "success"}
    except Exception:
        raise HTTPException(status_code=403, detail={
            "status": "ERROR",
            "data": None,
            "details": None
        })


@router.post("/like/post/{post_id}")
async def view_post_likes(post_id: int,
                          session: AsyncSession = Depends(get_async_session),
                          ):
    r = redis.Redis(host='localhost', port=6379)

    likes = r.get(post_id)

    if not likes:
        query_postlike = select(PostLike).where(
            (PostLike.post_id == post_id) & (PostLike.like == True))
        query_postdislike = select(PostLike).where(
            (PostLike.post_id == post_id) & (PostLike.like == False))
        postLike = await session.execute(query_postlike)
        postDisLike = await session.execute(query_postdislike)

        r.set(post_id, f"Likes: {len(postLike.all())} / Dislikes: {len(postDisLike.all())}")
        return r.get(post_id)
    else:
        return likes
