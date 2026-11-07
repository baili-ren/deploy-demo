from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = (CheckConstraint('length(trim(content)) > 0', name='ck_messages_content_nonempty'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
