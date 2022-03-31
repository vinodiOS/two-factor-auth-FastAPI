import email
from db.models.users import User
from sqlalchemy.orm import Session


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user