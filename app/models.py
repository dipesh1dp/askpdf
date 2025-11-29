from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Optional
from .database import Base 


class User(Base):
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=False, nullable=False) 
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    documents: Mapped[List["Document"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    chats: Mapped[List["ChatMemory"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Document(Base): 
    __tablename__ = "documents" 

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(nullable=False) 
    file_path: Mapped[str] = mapped_column(nullable=False) 
    uploade_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) 

    owner: Mapped[User] = relationship(back_populates="documents")
