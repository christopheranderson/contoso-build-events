from uuid import UUID, uuid4
from datetime import datetime
from typing import List, TYPE_CHECKING, Sequence
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel
from .event import Event
from .user import User

# Enum for session status
class SessionStatus(str, Enum):
    SUBMITTED = "submitted"
    APPROVED = "approved"
    CANCELLED = "cancelled"

# Association table for many-to-many relationship between Session and User
class SessionSpeakerLink(SQLModel, table=True):
    session_id: UUID = Field(foreign_key="session.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)

# Enum for session level
class SessionLevel(int, Enum):
    LEVEL_100 = 100
    LEVEL_200 = 200
    LEVEL_300 = 300
    LEVEL_400 = 400

# Enum for session type
class SessionType(str, Enum):
    VIRTUAL = "virtual"
    IN_PERSON = "in_person"
    HYBRID = "hybrid"

# Shared properties for Session
class SessionBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=255)
    short_description: str | None = Field(default=None, max_length=255)  # Add short description
    abstract: str | None = Field(default=None, max_length=500)  # Rename description to abstract
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    status: SessionStatus = Field(default=SessionStatus.SUBMITTED)  # Add status field
    cancellation_reason: str | None = Field(default=None, max_length=500)  # Add cancellation reason field
    tags: list[str] = Field(default_factory=list)  # Add tags field
    level: SessionLevel = Field(default=SessionLevel.LEVEL_100)  # Add level field
    session_type: SessionType = Field(default=SessionType.VIRTUAL)  # Add session type field
    location: str | None = Field(default=None, max_length=255)  # Add optional location field

# Properties to receive on session creation
class SessionCreate(SessionBase):
    event_id: UUID

# Properties to receive on session update
class SessionUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    short_description: str | None = Field(default=None, max_length=255)  # Add short description
    abstract: str | None = Field(default=None, max_length=500)  # Rename description to abstract
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: SessionStatus | None = None
    cancellation_reason: str | None = Field(default=None, max_length=500)  # Add cancellation reason field
    tags: list[str] | None = None  # Add tags field
    level: SessionLevel | None = None  # Add level field
    session_type: SessionType | None = None  # Add session type field
    location: str | None = Field(default=None, max_length=255)  # Add optional location field

# Enum for registration status
class SessionRegistrationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELED = "canceled"

# Base model for SessionRegistration
class SessionRegistrationBase(SQLModel):
    session_id: UUID
    user_id: UUID
    status: SessionRegistrationStatus = Field(default=SessionRegistrationStatus.PENDING)
    cancelation_reason: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Properties to receive on session registration creation
class SessionRegistrationCreate(SessionRegistrationBase):
    pass

# Properties to receive on session registration update
class SessionRegistrationUpdate(SQLModel):
    status: SessionRegistrationStatus | None = None
    cancelation_reason: str | None = Field(default=None, max_length=500)

# Base model for SessionReview
class SessionReviewBase(SQLModel):
    session_registration_id: UUID = Field(foreign_key="sessionregistration.id", nullable=False)
    title: str = Field(max_length=255)
    body: str = Field(max_length=1000)
    is_hidden: bool = Field(default=False)  # Marked as hidden by an event organizer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Properties to receive on session review creation
class SessionReviewCreate(SessionReviewBase):
    pass

# Properties to receive on session review update
class SessionReviewUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    body: str | None = Field(default=None, max_length=1000)
    is_hidden: bool | None = None

# Database model for SessionReview
class SessionReview(SessionReviewBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    session_registration: "SessionRegistration" = Relationship(back_populates="reviews")

# Database model for SessionRegistration
class SessionRegistration(SessionRegistrationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    session: "Session" = Relationship(back_populates="registrations")
    user: User = Relationship(back_populates="registered_for")
    reviews: list[SessionReview] = Relationship(back_populates="session_registration")  # Add relationship for reviews

# Database model for Session
class Session(SessionBase, table=True):
    event_id: UUID = Field(foreign_key="event.id", nullable=False)
    event: Event = Relationship(back_populates="sessions")
    speakers: List[User] = Relationship(back_populates="speaker_for", link_model=SessionSpeakerLink)
    registrations: List[SessionRegistration] = Relationship(back_populates="session")

# Properties to return via API for listing sessions
class Sessions(SQLModel):
    data: Sequence[SessionBase]
    count: int

# Properties to return via API for listing session registrations
class SessionRegistrations(SQLModel):
    data: Sequence[SessionRegistrationBase]
    count: int

# Properties to return via API for listing session reviews
class SessionReviews(SQLModel):
    data: Sequence[SessionReviewBase]
    count: int
