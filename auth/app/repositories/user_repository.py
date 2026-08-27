from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user import User

class UserRepository:

    @staticmethod
    def get_by_email(db:Session,email:str) -> User | None:
        statement = select(User).where(User.email==email)
        return db.scalar(statement)

    @staticmethod
    def create(db:Session,user:User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user