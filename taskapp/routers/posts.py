from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from taskapp.models import Post, User
from taskapp.schemas.posts import PostCreate, PostResponse
from core.db import get_async_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/posts", tags=["posts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_user_id_from_token(token: str = Depends(oauth2_scheme)) -> int:
    return int(token)

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(get_user_id_from_token),  # Преобразуем user_id из токена
):
    new_post = Post(title=post.title, content=post.content, owner_id=user_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Post))
    return result.scalars().all()


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostCreate,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(get_user_id_from_token),  # Преобразуем user_id из токена
):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = result.scalar_one_or_none()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    db_post.title = post.title
    db_post.content = post.content
    await db.commit()
    await db.refresh(db_post)
    return db_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(get_user_id_from_token),
):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = result.scalar_one_or_none()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    await db.delete(db_post)
    await db.commit()
