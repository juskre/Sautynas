from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.users import UserCreate,ShowUser
from db.session import get_db
from db.models.users import User
from db.repository.users import create_new_user,retreive_user,delete_user_by_id
from apis.varsion1.route_login import get_current_user_from_token
router = APIRouter()


@router.post("/",response_model=ShowUser)
def create_user(user: UserCreate,db: Session=Depends(get_db)):
    user = create_new_user(user, db)
    return user

@router.delete("/delete/{id}")
def delete_user(id:int, db:Session=Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    owner_id = 1
    user = retreive_user(id=id,db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does nt exist")
    if user.id == current_user.id or current_user.is_superuser:
        delete_user_by_id(id=id,db=db,owner_id=current_user.id)
        return {"detail":"Post successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not permitted")