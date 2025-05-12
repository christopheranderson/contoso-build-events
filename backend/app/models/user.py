from typing import Sequence
from uuid import UUID, uuid4

from .item import Item
from .event import Event, EventOrganizerLink, EventRegistration  # Import EventRegistration
from .session import Session, SessionSpeakerLink  # Import Session and SessionSpeakerLink
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    id: UUID = Field(default=UUID('00000000-0000-0000-000-000000000000'), primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    organizer_for: list["Event"] = Relationship(back_populates="organizers", link_model=EventOrganizerLink)
    speaker_for: list[Session] = Relationship(back_populates="speakers", link_model=SessionSpeakerLink)
    registered_for: list[Session] = Relationship(back_populates="user")  # Add relationship for session registrations
    event_registrations: list["EventRegistration"] = Relationship(back_populates="user")  # Add relationship for event registrations
    profile: "UserProfile" = Relationship(back_populates="user")  # Fix one-to-one relationship with UserProfile


class UserProfile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, unique=True)
    username: str = Field(unique=True, index=True, max_length=50)
    profile_picture: str | None = Field(default=None, max_length=255)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=1000)
    current_position: str | None = Field(default=None, max_length=255)
    current_company: str | None = Field(default=None, max_length=255)
    skills: list[str] = Field(default_factory=list)
    website: str | None = Field(default=None, max_length=255)
    linkedin: str | None = Field(default=None, max_length=255)
    github: str | None = Field(default=None, max_length=255)
    twitter: str | None = Field(default=None, max_length=255)
    work_experience: list[dict] = Field(default_factory=list)  # Example: [{"title": "Software Engineer", "company": "XYZ", "duration": "2 years"}]
    education: list[dict] = Field(default_factory=list)  # Example: [{"degree": "B.Sc. Computer Science", "institution": "ABC University", "year": "2020"}]
    projects: list[dict] = Field(default_factory=list)  # Example: [{"name": "Project A", "description": "A cool project"}]
    certifications: list[dict] = Field(default_factory=list)  # Example: [{"name": "AWS Certified", "year": "2021"}]

    user: "User" = Relationship(back_populates="profile")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    pass


class UsersPublic(SQLModel):
    data: Sequence[UserBase]
    count: int