from sqlalchemy.orm import Session

from ..core.security import hash_password,verify_password
from ..models.user import User
from ..repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()

    def get_user_by_email(self,email: str) -> User | None:
        return self.repository.get_by_email(self.db,email,)

    def create_user(self,email: str,password: str,
        first_name:  str,last_name: str,
        phone_number: str) -> User:

        existing_user  = self.repository.get_by_email(self.db,email)

        if existing_user:
            raise ValueError("email already registered")

        hashed_password = hash_password(password)

        user = User(email=email,
                    password=hashed_password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    )

        return self.repository.create(self.db,user)

    def authenticate_user(self,email: str,password: str,) -> User:

        user = self.repository.get_by_email(self.db,email,)

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(password,user.password,):

            raise ValueError(
                "Invalid email or password"
            )

        return user