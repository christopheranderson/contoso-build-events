from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Column, Field, Relationship, SQLModel, String


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Shared properties
class UserBase(SQLModel):
    id: UUID = Field(
        default=UUID("00000000-0000-0000-0000-000000000000"), primary_key=True
    )
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


# Properties to return via API, id is always required
class UserPublic(UserBase):
    pass


class UsersPublic(SQLModel):
    data: Sequence[UserBase]
    count: int


# Enum for event type
class EventType(str, Enum):
    VIRTUAL = "virtual"
    IN_PERSON = "in_person"
    HYBRID = "hybrid"


# Shared properties
class EventBase(SQLModel):
    id: UUID = Field(default_factory=UUID, primary_key=True)
    name: str = Field(max_length=255)
    short_description: str | None = Field(
        default=None, max_length=100
    )  # New field for short description
    description: str | None = Field(default=None, max_length=255)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    event_type: EventType = Field(default=EventType.VIRTUAL)  # Add event type field
    is_private: bool = Field(
        default=False
    )  # Add field to indicate if the event is private
    organization_name: str | None = Field(
        default=None, max_length=255
    )  # Add organization name field
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    slug: str = Field(max_length=255, unique=True, regex=r"^[a-z0-9-]+$")  # Add slug field


# Properties to receive on event creation
class EventCreate(EventBase):
    pass


# Properties to receive on event update
class EventUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    short_description: str | None = Field(
        default=None, max_length=100
    )  # New field for short description
    description: str | None = Field(default=None, max_length=255)
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_type: EventType | None = None  # Add event type field
    is_private: bool | None = None  # Add field to indicate if the event is private
    organization_name: str | None = Field(
        default=None, max_length=255
    )  # Add organization name field
    slug: str | None = Field(default=None, max_length=255, regex=r"^[a-z0-9-]+$")  # Add slug field


# Enum for registration status
class EventRegistrationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELED = "canceled"


# Base model for EventRegistration
class EventRegistrationBase(SQLModel):
    event_id: UUID
    user_id: UUID
    status: EventRegistrationStatus = Field(default=EventRegistrationStatus.PENDING)
    cancellation_reason: str | None = Field(default=None, max_length=500)
    is_speaker: bool = Field(default=False)
    is_organizer: bool = Field(default=False)
    is_sponsor: bool = Field(default=False)
    is_student: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Properties to receive on event registration creation
class EventRegistrationCreate(EventRegistrationBase):
    pass


# Properties to receive on event registration update
class EventRegistrationUpdate(SQLModel):
    status: EventRegistrationStatus | None = None
    cancellation_reason: str | None = Field(default=None, max_length=500)
    is_speaker: bool | None = None
    is_organizer: bool | None = None
    is_sponsor: bool | None = None
    is_student: bool | None = None
    is_staff: bool | None = None


# Base model for EventDetails
class EventDetailsBase(SQLModel):
    readme: str | None = None  # Markdown-supported longer description
    code_of_conduct: str | None = None  # Markdown-supported code of conduct
    sponsors: str | None = None  # Markdown-supported sponsors info
    info_for_speakers: str | None = None  # Markdown-supported info for speakers
    info_for_sponsors: str | None = None  # Markdown-supported info for sponsors
    info_for_staff: str | None = None  # Markdown-supported info for staff
    contact_info: str | None = None  # Markdown-supported contact info
    resources: str | None = None  # Markdown-supported resources
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Properties to receive on event details creation
class EventDetailsCreate(EventDetailsBase):
    pass


# Properties to receive on event details update
class EventDetailsUpdate(SQLModel):
    readme: str | None = None
    code_of_conduct: str | None = None
    sponsors: str | None = None
    info_for_speakers: str | None = None
    info_for_sponsors: str | None = None
    info_for_staff: str | None = None
    contact_info: str | None = None
    resources: str | None = None


# Properties to return via API, id is always required
class EventPublic(EventBase):
    pass


# Properties to return via API for listing events
class Events(SQLModel):
    data: Sequence[EventBase]
    count: int


# Shared properties
class ItemBase(SQLModel):
    id: UUID
    owner_id: UUID
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    pass


class ItemsPublic(SQLModel):
    data: Sequence[ItemBase]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# Base model for Organization
class OrganizationBase(SQLModel):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
    )  # User-defined unique ID, such as microsoft
    name: str = Field(max_length=255)
    display_name: str | None = Field(
        default=None, max_length=255
    )  # Optional display name
    short_description: str = Field(max_length=500)
    profile_picture: str | None = None  # URL to profile picture
    profile_banner: str | None = None  # URL to profile banner
    contact_email: str | None = Field(default=None, max_length=255)
    linkedin_link: str | None = None  # URL to LinkedIn profile
    github_link: str | None = None  # URL to GitHub profile
    readme: str | None = None  # Markdown-supported longer description
    slug: str = Field(max_length=255, unique=True, regex=r"^[a-z0-9-]+$")  # Add slug field


# Properties to receive on organization creation
class OrganizationCreate(OrganizationBase):
    pass


# Properties to receive on organization update
class OrganizationUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    short_description: str | None = Field(default=None, max_length=500)
    profile_picture: str | None = None
    profile_banner: str | None = None
    contact_email: str | None = Field(default=None, max_length=255)
    linkedin_link: str | None = None
    github_link: str | None = None
    readme: str | None = None
    slug: str | None = Field(default=None, max_length=255, regex=r"^[a-z0-9-]+$")  # Add slug field


# Properties to return via API for listing organizations
class OrganizationList(SQLModel):
    data: Sequence[OrganizationBase]
    count: int


# Enum for session status
class SessionStatus(str, Enum):
    SUBMITTED = "submitted"
    APPROVED = "approved"
    CANCELLED = "cancelled"


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
    id: UUID
    title: str = Field(max_length=255)
    short_description: str | None = Field(
        default=None, max_length=255
    )  # Add short description
    abstract: str | None = Field(
        default=None, max_length=500
    )  # Rename description to abstract
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    status: SessionStatus = Field(default=SessionStatus.SUBMITTED)  # Add status field
    cancellation_reason: str | None = Field(
        default=None, max_length=500
    )  # Add cancellation reason field
    tags: list[str] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )  # Use JSON for list storage
    level: SessionLevel = Field(default=SessionLevel.LEVEL_100)  # Add level field
    session_type: SessionType = Field(
        default=SessionType.VIRTUAL
    )  # Add session type field
    location: str | None = Field(
        default=None, max_length=255
    )  # Add optional location field
    slug: str = Field(max_length=255, unique=True, regex=r"^[a-z0-9-]+$")  # Add slug field


# Properties to receive on session creation
class SessionCreate(SessionBase):
    event_id: UUID

class SessionSubmit(SQLModel):
    title: str = Field(max_length=255)
    short_description: str | None = Field(
        default=None, max_length=255
    )  # Add short description
    abstract: str | None = Field(
        default=None, max_length=500
    )
    level: SessionLevel = Field(default=SessionLevel.LEVEL_100)  # Add level field
    tags: list[str] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )  # Use JSON for list storage

# Properties to receive on session update
class SessionUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    short_description: str | None = Field(
        default=None, max_length=255
    )  # Add short description
    abstract: str | None = Field(
        default=None, max_length=500
    )  # Rename description to abstract
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: SessionStatus | None = None
    cancellation_reason: str | None = Field(
        default=None, max_length=500
    )  # Add cancellation reason field
    tags: list[str] | None = None  # Add tags field
    level: SessionLevel | None = None  # Add level field
    session_type: SessionType | None = None  # Add session type field
    location: str | None = Field(
        default=None, max_length=255
    )  # Add optional location field
    slug: str | None = Field(default=None, max_length=255, regex=r"^[a-z0-9-]+$")  # Add slug field


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
    session_registration_id: UUID = Field(
        foreign_key="sessionregistration.id", nullable=False
    )
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


# Association table for many-to-many relationship between Session and User
class SessionSpeakerLink(SQLModel, table=True):
    session_id: UUID = Field(foreign_key="session.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


# Association table for many-to-many relationship between Event and User
class EventOrganizerLink(SQLModel, table=True):
    event_id: UUID = Field(foreign_key="event.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


# Association table for many-to-many relationship between Organization and User (Admins)
class OrganizationAdminLink(SQLModel, table=True):
    organization_id: UUID = Field(foreign_key="organization.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


# Association table for many-to-many relationship between Organization and User (Members)
class OrganizationMemberLink(SQLModel, table=True):
    organization_id: UUID = Field(foreign_key="organization.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


# Address model for detailed location information


class AddressBase(SQLModel):
    friendly_name: str | None = Field(
        default=None, max_length=255
    )  # Optional friendly name
    description: str | None = Field(
        default=None, max_length=1000
    )  # Optional description
    street: str = Field(max_length=255)
    apt_suite: str | None = Field(
        default=None, max_length=255
    )  # Optional apartment/suite number
    city: str = Field(max_length=100)
    state: str = Field(max_length=100)
    postal_code: str = Field(max_length=20)
    country: str = Field(max_length=100)


class Address(AddressBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    events: list["Event"] = Relationship(
        back_populates="address"
    )  # One-to-many relationship with Event


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    profile: "UserProfile" = Relationship(
        back_populates="user"
    )  # Fix one-to-one relationship with UserProfile
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    organizer_for: list["Event"] = Relationship(
        back_populates="organizers", link_model=EventOrganizerLink
    )
    speaker_for: list["Session"] = Relationship(
        back_populates="speakers", link_model=SessionSpeakerLink
    )
    session_registrations: list["SessionRegistration"] = Relationship(
        back_populates="user"
    )  # Add relationship for session registrations
    event_registrations: list["EventRegistration"] = Relationship(
        back_populates="user"
    )  # Add relationship for event registrations
    admin_of: list["Organization"] = Relationship(
        back_populates="admins", link_model=OrganizationAdminLink
    )
    member_of: list["Organization"] = Relationship(
        back_populates="members", link_model=OrganizationMemberLink
    )


class UserProfile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, unique=True)
    username: str = Field(unique=True, index=True, max_length=50)
    profile_picture: str | None = Field(default=None, max_length=255)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=1000)
    current_position: str | None = Field(default=None, max_length=255)
    current_company: str | None = Field(default=None, max_length=255)
    skills: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=255)
    linkedin: str | None = Field(default=None, max_length=255)
    github: str | None = Field(default=None, max_length=255)
    twitter: str | None = Field(default=None, max_length=255)
    work_experience: str | None = Field(default=None, max_length=255)
    education: str | None = Field(default=None, max_length=255)
    projects: str | None = Field(default=None, max_length=255)
    certifications: str | None = Field(default=None, max_length=255)

    user: "User" = Relationship(back_populates="profile")


# Database model for SessionReview
class SessionReview(SessionReviewBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_registration_id: UUID = Field(
        foreign_key="sessionregistration.id", nullable=False
    )
    session_registration: "SessionRegistration" = Relationship(back_populates="reviews")


# Database model for SessionRegistration
class SessionRegistration(SessionRegistrationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    session_id: UUID = Field(foreign_key="session.id", nullable=False)
    session: "Session" = Relationship(back_populates="registrations")
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    user: User = Relationship(back_populates="session_registrations")
    reviews: SessionReview | None = Relationship(back_populates="session_registration")


# Database model for Session
class Session(SessionBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="event.id", nullable=False)
    event: "Event" = Relationship(back_populates="sessions")
    speakers: list[User] = Relationship(
        back_populates="speaker_for", link_model=SessionSpeakerLink
    )
    registrations: list[SessionRegistration] = Relationship(back_populates="session")


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    owner_id: UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="items")


# Database model for Organization
class Organization(OrganizationBase, table=True):
    admins: list["User"] = Relationship(
        back_populates="admin_of", link_model=OrganizationAdminLink
    )
    members: list["User"] = Relationship(
        back_populates="member_of", link_model=OrganizationMemberLink
    )
    events: list["Event"] = Relationship(back_populates="organization")


# Database model, database table inferred from class name
class Event(EventBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    details: Optional["EventDetails"] = Relationship(
        back_populates="event"
    )  # One-to-one relationship with EventDetails

    address_id: UUID = Field(
        foreign_key="address.id", nullable=True
    )  # Add foreign key to Address
    address: Address | None = Relationship(
        back_populates="events"
    )  # Add relationship to Address

    organizers: list[User] = Relationship(
        back_populates="organizer_for", link_model=EventOrganizerLink
    )
    sessions: list[Session] = Relationship(back_populates="event")
    registrations: list["EventRegistration"] = Relationship(back_populates="event")

    organization_id: UUID = Field(
        foreign_key="organization.id", nullable=True
    )  # Add foreign key to Organization
    organization: Organization = Relationship(
        back_populates="events"
    )  # Add relationship to Organization
    slug: str = Field(max_length=255, unique=True, regex=r"^[a-z0-9-]+$")  # Add slug field


# Database model for EventRegistration
class EventRegistration(EventRegistrationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    event_id: UUID = Field(foreign_key="event.id", nullable=False)
    event: "Event" = Relationship(back_populates="registrations")
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="event_registrations")


# Database model for EventDetails
class EventDetails(EventDetailsBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(
        foreign_key="event.id", unique=True, nullable=False
    )  # One-to-one relationship with Event
    event: "Event" = Relationship(
        back_populates="details", sa_relationship_kwargs={"cascade": "all, delete"}
    )
