from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()

    def get_user_by_email(self,email: str) -> User | None:
        return self.repository.get_by_email(self.db,email,)

    def create_user(self,email: str,password: str,) -> User:

        existing_user  = self.repository.get_by_email(self.db,email)

        if existing_user:
            raise ValueError("email already registered")

        hashed_password = hash_password(password)

        user = User(email=email,password=hashed_password,)

        return self.repository.create(self.db,user)