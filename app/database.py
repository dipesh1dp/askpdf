from sqlalchemy import create_engine 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .config import settings

# Database URL
DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
 
# Create async engine
engine = create_async_engine(DATABASE_URL, 
                             echo=True, 
                             future=True
                             )

# Create a session maker to interact with the database
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# Create a base class for ORMs 
class Base(DeclarativeBase): 
    pass 


async def get_db():
    async with AsyncSessionLocal() as session: 
        try:
            yield session
            await session.commit()   # Commit the transaction
        except Exception:
            await session.rollback() # In case of error, rollback the transaction
            raise

# If not using alembic. 
# Call init_db() in lifespan in main.py
# async def init_db():
#     """Initialize database tables"""
#     from .models import Base
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


