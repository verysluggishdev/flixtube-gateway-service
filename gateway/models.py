from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    channelID = Column(String, nullable=False, unique=True)
    channelName = Column(String, nullable=False)
    avatar = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    thumbnail = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    video = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    post_metrics = relationship("PostMetrics", back_populates="post")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class PostMetrics(Base):
    __tablename__ = 'post_metrics'
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    post = relationship("Post", back_populates='post_metrics')
    user = relationship("User")
    liked = Column(Boolean, index=True, nullable=False, server_default='false')
    disliked = Column(Boolean, index=True, nullable=False, server_default='false')
    shared = Column(Boolean, index=True, nullable=False, server_default='false')