from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    BIGINT,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from typing import Optional, List
from datetime import datetime

from .mixins import TimestampMixin
from .create_base import Base



class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id: Mapped[BIGINT] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
        unique=False
    )
    user_id: Mapped[BIGINT] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True
    )
    
    interests: Mapped[List[str]] = mapped_column(
        ARRAY(String)
    )
    notification_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    digest_size: Mapped[int] = mapped_column(
        Integer,
        default=5
    )