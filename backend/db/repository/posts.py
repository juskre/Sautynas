from sqlalchemy.orm import Session

from schemas.posts import PostCreate
from db.models.posts import Post

def create_new_post(post:PostCreate, db:Session,owner_id:int):
    post = Post(**post.dict(),owner_id = owner_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def retreive_post(id:int, db:Session):
    post = db.query(Post).filter(Post.id==id).first()
    return post

def list_post(db :Session):
    post = db.query(Post).all()
    return post

def update_post_by_id(id:int, post:PostCreate, db:Session, owner_id:int):
    existing_post = db.query(Post).filter(Post.id==id)
    if not existing_post.first():
        return 0
    post.__dict__.update(owner_id=owner_id)
    existing_post.update(post.__dict__)
    db.commit()
    return 1

def delete_post_by_id(id:int, db:Session,owner_id):
    existing_post = db.query(Post).filter(Post.id==id)
    if not existing_post.first():
        return 0
    existing_post.delete(synchronize_session=False)
    db.commit()
    return 1