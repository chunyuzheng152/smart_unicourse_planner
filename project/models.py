from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from project import db

class User(db.Model):
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    username = so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email = so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash = so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    #__repr method created tells python how to print object, useful for debugging 
    def __repr__(self): 
        return '<User {}>'.format(self.username)

class Comment(db.Model):
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    content = so.Mapped[str] = so.mapped_column(sa.String(500))
    created_at = so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id = so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

class Survey(db.Model):
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    q1 = so.Mapped[int] = so.mapped_column(nullable=False)
    q2 = so.Mapped[int] = so.mapped_column(nullable=False)
    q3 = so.Mapped[int] = so.mapped_column(nullable=False)
    q4 = so.Mapped[int] = so.mapped_column(nullable=False)
    q5 = so.Mapped[int] = so.mapped_column(nullable=False)
    q6 = so.Mapped[int] = so.mapped_column(nullable=False)
    q7 = so.Mapped[int] = so.mapped_column(nullable=False)
    user_id = so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), nullable=False)