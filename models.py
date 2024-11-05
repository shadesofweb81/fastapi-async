# app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


# app/enums.py
from enum import Enum

class RoleName(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# app/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: RoleName = Field(sa_column_kwargs={"unique": True})  # Enum field for role name

    # Relationship to User
    users: list["User"] = Relationship(back_populates="role")


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    address: Optional[str] = Field(default=None)

    # Foreign key to User
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="profile")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    # Foreign key to Role
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")

    # Relationship to Role
    role: Optional[Role] = Relationship(back_populates="users")

    # Relationship to UserProfile
    profile: Optional[UserProfile] = Relationship(back_populates="user")
