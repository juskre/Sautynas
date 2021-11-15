from sqlalchemy.orm import Session

from schemas.comments import CommentCreate
from db.models.comments import Comment

def create_new_comment(comment:CommentCreate, db:Session,owner_id:int):
    comment = Comment(**comment.dict(),owner_id = owner_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def retreive_comment(id:int, db:Session):
    comment = db.query(Comment).filter(Comment.id==id).first()
    return comment

def list_comment(db :Session):
    comment = db.query(Comment).all()
    return comment

def update_comment_by_id(id:int, comment:CommentCreate, db:Session, owner_id:int):
    existing_comment = db.query(Comment).filter(Comment.id==id)
    if not existing_comment.first():
        return 0
    comment.__dict__.update(owner_id=owner_id)
    existing_comment.update(comment.__dict__)
    db.commit()
    return 1

def delete_comment_by_id(id:int, db:Session,owner_id):
    existing_comment = db.query(Comment).filter(Comment.id==id)
    if not existing_comment.first():
        return 0
    existing_comment.delete(synchronize_session=False)
    db.commit()
    return 1