from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    media_url: Optional[str] = None

class BlogAuthor(BaseModel):
    username: str

    class Config:
        from_attributes = True

class BlogResponse(BlogBase):
    id: int
    author: BlogAuthor  
    media_url: Optional[str] = None

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str

class CommentUser(BaseModel):
    username: str

    class Config:
        from_attributes = True

class LikeUser(BaseModel):
    username: str

    class Config:
        from_attributes = True

class CommentResponse(BaseModel):
    id: int
    text: str
    user: CommentUser
    liked_by: List[LikeUser] = []

    class Config:
        from_attributes = True

class BlogWithComments(BlogBase):
    id: int
    author: BlogAuthor
    comments: List[CommentResponse]

    class Config:
        from_attributes = True

class BlogWithCommentsAndLikes(BlogBase):
    id: int
    author: BlogAuthor
    media_url: Optional[str] = None
    comments: List[CommentResponse] = []
    liked_by: List[LikeUser] = []

    class Config:
        from_attributes = True
