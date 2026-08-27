from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class UserRole(str, Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    # =========================
    # ID
    # =========================

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # =========================
    # BASIC INFORMATION
    # =========================

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    # =========================
    # AUTHORIZATION
    # =========================

    role: Mapped[UserRole] = mapped_column(
        default=UserRole.CUSTOMER,
        nullable=False,
    )

    # =========================
    # ACCOUNT STATUS
    # =========================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )