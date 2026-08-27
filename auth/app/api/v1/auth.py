from fastapi import  APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...schemas.user import UserCreate, UserResponse
from ...services.user_service import UserService
from ...tasks import send_welcome_email_task

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED,)
def register(data:UserCreate,db: Session = Depends(get_db)):
    service = UserService(db)

    try:
        user = service.create_user(
            email = data.email,
            password= data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
        )

        # Send email asynchronously
        send_welcome_email_task.delay(
            user.email,
            user.first_name,
        )

        return user

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )