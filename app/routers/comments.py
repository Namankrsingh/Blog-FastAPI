from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, oauth2

router = APIRouter(prefix="/blogs/{blog_id}/comments", tags=["Comments"])

@router.post("/", response_model=schemas.CommentResponse)
def create_comment(blog_id: int, comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    new_comment = models.Comment(text=comment.text, blog_id=blog_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/", response_model=list[schemas.CommentResponse])
def get_comments(blog_id: int, db: Session = Depends(database.get_db), skip: int = 0, limit: int = 10):
    comments = db.query(models.Comment).filter(models.Comment.blog_id == blog_id).offset(skip).limit(limit).all()
    return comments

@router.post("/{comment_id}/like")
def like_comment(blog_id: int, comment_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter_by(id=comment_id, blog_id=blog_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if current_user in comment.liked_by:
        comment.liked_by.remove(current_user)
    else:
        comment.liked_by.append(current_user)
    db.commit()
    return {"message": "Like toggled"}