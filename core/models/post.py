from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from .base import Base
from .mixins import UserRelationMixin


class Post(Base, UserRelationMixin):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(128))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
