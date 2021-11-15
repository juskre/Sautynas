from sqlalchemy.orm import Session
from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher

def create_new_user(user: UserCreate, db:Session):
    user = User(username=user.username,
                email = user.email,
                hashed_password = Hasher.get_password_hash(user.password),
                is_active=True,
                is_superuser=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def retreive_user(id:int, db:Session):
    user = db.query(User).filter(User.id==id).first()
    return user

def list_user(db :Session):
    user = db.query(User).all()
    return user


def delete_user_by_id(id:int, db:Session,owner_id):
    existing_user = db.query(User).filter(User.id==id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1