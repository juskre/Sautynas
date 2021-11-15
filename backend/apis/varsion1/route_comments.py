from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.comments import CommentCreate,ShowComment
from db.session import get_db
from db.models.comments import Comment
from db.models.users import User
from db.repository.comments import (create_new_comment,
        delete_comment_by_id, 
        retreive_comment, 
        list_comment,
        update_comment_by_id)
from apis.varsion1.route_login import get_current_user_from_token

router = APIRouter()

@router.post("/create-comment", response_model=ShowComment)
def create_post(comment :CommentCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    comment = create_new_comment(comment=comment,db=db,owner_id=owner_id)
    return comment

@router.get("/get/{id}", response_model=ShowComment)
def retreive_comment_by_id(id:int, db: Session = Depends(get_db)):
    comment = retreive_comment(id=id,db=db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"comment with id {id} does nt exist")
    return comment

@router.get("/all", response_model=List[ShowComment])
def retreive_all_comment(db:Session=Depends(get_db)):
    comment = list_comment(db=db)
    return comment

@router.put("/update/{id}")
def update_comment(id:int, comment:CommentCreate, db:Session=Depends(get_db)):
    owner_id = 1
    message = update_comment_by_id(id=id, comment=comment, db=db,owner_id=owner_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"comment with {id} does not exist")
    return {"detail":"Successfully updated data."}

@router.delete("/delete/{id}")
def delete_comment(id:int, db:Session=Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    owner_id = 1
    comment = retreive_comment(id=id,db=db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"comment with id {id} does nt exist")
    if comment.owner_id == current_user.id or current_user.is_superuser:
        delete_comment_by_id(id=id,db=db,owner_id=current_user.id)
        return {"detail":"comment successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not permitted")
    