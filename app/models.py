from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

blog_likes = Table(
    "blog_likes", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("blog_id", Integer, ForeignKey("blogs.id"))
)

comment_likes = Table(
    "comment_likes", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("comment_id", Integer, ForeignKey("comments.id"))
)

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    media_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="blogs")  
    comments = relationship("Comment", back_populates="blog", cascade="all, delete")
    liked_by = relationship("User", secondary=blog_likes, backref="liked_blogs")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    blogs = relationship("Blog", back_populates="author")  
    comments = relationship("Comment", back_populates="user", cascade="all, delete")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    blog = relationship("Blog", back_populates="comments")
    user = relationship("User", back_populates="comments")
    liked_by = relationship("User", secondary=comment_likes, backref="liked_comments")

