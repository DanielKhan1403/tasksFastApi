from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.db import get_async_db
from taskapp.models import User
from taskapp.schemas.auth import UserCreate, Token
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Хэширует пароль."""
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    """Проверяет пользователя по имени и паролю."""
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user

@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """Регистрация нового пользователя."""
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username}

@router.post("/login", response_model=Token)
async def login_for_access_token(username: str, password: str, db: AsyncSession = Depends(get_async_db)):
    """Логин и получение токена."""
    user = await authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": str(user.id), "token_type": "bearer"}
