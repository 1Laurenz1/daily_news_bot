from sqlalchemy import (
    func,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from datetime import datetime


class TimestampMixin:
    # def __init__(self):
    #     pass
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )