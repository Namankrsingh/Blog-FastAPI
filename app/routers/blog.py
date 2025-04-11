from fastapi import APIRouter, Depends, status, HTTPException,File, UploadFile, Form
from sqlalchemy.orm import Session
from app import models, schemas, oauth2, database
from app.database import get_db
from app.routers import auth
from fastapi import Query
from typing import List

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

@router.post("/", response_model=schemas.BlogResponse)
def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    media_path = None
    if file:
        file_location = f"media/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        media_path = f"http://localhost:8000/media/{file.filename}"

    new_blog = models.Blog(
        title=title,
        content=content,
        media_url=media_path,
        user_id=current_user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/my", response_model=list[schemas.BlogResponse])
def get_my_blogs(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).filter(models.Blog.user_id == current_user.id).all()
    return blogs

# @router.get("/", response_model=list[schemas.BlogResponse])
# def get_all_blogs(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
#     blogs = db.query(models.Blog).offset(skip).limit(limit).all()
#     return blogs

@router.get("/public", response_model=List[schemas.BlogWithCommentsAndLikes])
def public_blog_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 10, 
                     search: str = Query("", description="Filter blogs by title or content")):
    blogs = db.query(models.Blog).filter(
        (models.Blog.title.ilike(f"%{search}%")) | (models.Blog.content.ilike(f"%{search}%"))
    ).offset(skip).limit(limit).all()
    return blogs


@router.get("/{id}", response_model=schemas.BlogResponse)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.post("/{blog_id}/like")
def like_blog(blog_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if current_user in blog.liked_by:
        blog.liked_by.remove(current_user)
    else:
        blog.liked_by.append(current_user)
    db.commit()
    return {"message": "Like toggled"}

@router.put("/{blog_id}/comments/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(blog_id: int, comment_id: int, updated: schemas.CommentCreate,
                   db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.blog_id == blog_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    comment.text = updated.text
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{blog_id}/comments/{comment_id}", status_code=204)
def delete_comment(blog_id: int, comment_id: int,
                   db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.blog_id == blog_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(comment)
    db.commit()


