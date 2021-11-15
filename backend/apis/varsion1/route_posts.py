from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.posts import PostCreate,ShowPost
from db.session import get_db
from db.models.posts import Post
from db.models.users import User
from db.repository.posts import (create_new_post,
        delete_post_by_id, 
        retreive_post, 
        list_post,
        update_post_by_id)
from apis.varsion1.route_login import get_current_user_from_token

router = APIRouter()

@router.post("/create-post", response_model=ShowPost)
def create_post(post :PostCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    post = create_new_post(post=post,db=db,owner_id=owner_id)
    return post

@router.get("/get/{id}", response_model=ShowPost)
def retreive_post_by_id(id:int, db: Session = Depends(get_db)):
    post = retreive_post(id=id,db=db)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does nt exist")
    return post

@router.get("/all", response_model=List[ShowPost])
def retreive_all_post(db:Session=Depends(get_db)):
    post = list_post(db=db)
    return post

@router.put("/update/{id}")
def update_post(id:int, post:PostCreate, db:Session=Depends(get_db)):
    owner_id = 1
    message = update_post_by_id(id=id, post=post, db=db,owner_id=owner_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} does not exist")
    return {"detail":"Successfully updated data."}

@router.delete("/delete/{id}")
def delete_post(id:int, db:Session=Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    owner_id = 1
    post = retreive_post(id=id,db=db)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does nt exist")
    if post.owner_id == current_user.id or current_user.is_superuser:
        delete_post_by_id(id=id,db=db,owner_id=current_user.id)
        return {"detail":"Post successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not permitted")
    
    