from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str = Field(
        min_length=2,
        max_length=100,
    )

    phone_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
    )


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str | None
    role: str
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True
    )