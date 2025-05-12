from typing import Sequence, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

from .user import User
from .session import Session  
from .organization import Organization  
from sqlmodel import Field, Relationship, SQLModel


# Enum for event type
class EventType(str, Enum):
    VIRTUAL = "virtual"
    IN_PERSON = "in_person"
    HYBRID = "hybrid"


# Association table for many-to-many relationship between Event and User
class EventOrganizerLink(SQLModel, table=True):
    event_id: UUID = Field(foreign_key="event.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)


# Address model for detailed location information
class Address(SQLModel):
    friendly_name: str | None = Field(default=None, max_length=255)  # Optional friendly name
    description: str | None = Field(default=None, max_length=1000)  # Optional description
    street: str = Field(max_length=255)
    city: str = Field(max_length=100)
    state: str = Field(max_length=100)
    postal_code: str = Field(max_length=20)
    country: str = Field(max_length=100)


# Shared properties
class EventBase(SQLModel):
    id: UUID = Field(default_factory=UUID, primary_key=True)
    name: str = Field(max_length=255)
    short_description: str | None = Field(default=None, max_length=100)  # New field for short description
    description: str | None = Field(default=None, max_length=255)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)
    event_type: EventType = Field(default=EventType.VIRTUAL)  # Add event type field
    location: Address | None = None  # Use Address model for location
    is_private: bool = Field(default=False)  # Add field to indicate if the event is private
    organization_name: str | None = Field(default=None, max_length=255)  # Add organization name field
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Properties to receive on event creation
class EventCreate(EventBase):
    pass

# Properties to receive on event update
class EventUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    short_description: str | None = Field(default=None, max_length=100)  # New field for short description
    description: str | None = Field(default=None, max_length=255)
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_type: EventType | None = None  # Add event type field
    location: Address | None = None  # Use Address model for location
    is_private: bool | None = None  # Add field to indicate if the event is private
    organization_name: str | None = Field(default=None, max_length=255)  # Add organization name field


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


# Database model for EventRegistration
class EventRegistration(EventRegistrationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    event: "Event" = Relationship(back_populates="registrations")
    user: "User" = Relationship(back_populates="event_registrations")


# Base model for EventDetails
class EventDetailsBase(SQLModel):
    readme: Optional[str] = None  # Markdown-supported longer description
    code_of_conduct: Optional[str] = None  # Markdown-supported code of conduct
    sponsors: Optional[str] = None  # Markdown-supported sponsors info
    info_for_speakers: Optional[str] = None  # Markdown-supported info for speakers
    info_for_sponsors: Optional[str] = None  # Markdown-supported info for sponsors
    info_for_staff: Optional[str] = None  # Markdown-supported info for staff
    contact_info: Optional[str] = None  # Markdown-supported contact info
    resources: Optional[str] = None  # Markdown-supported resources
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Properties to receive on event details creation
class EventDetailsCreate(EventDetailsBase):
    pass

# Properties to receive on event details update
class EventDetailsUpdate(SQLModel):
    readme: Optional[str] = None
    code_of_conduct: Optional[str] = None
    sponsors: Optional[str] = None
    info_for_speakers: Optional[str] = None
    info_for_sponsors: Optional[str] = None
    info_for_staff: Optional[str] = None
    contact_info: Optional[str] = None
    resources: Optional[str] = None


# Database model for EventDetails
class EventDetails(EventDetailsBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="event.id", unique=True, nullable=False)  # One-to-one relationship with Event
    event: "Event" = Relationship(back_populates="details", sa_relationship_kwargs={"cascade": "all, delete"})


# Database model, database table inferred from class name
class Event(EventBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    organizers: list[User] = Relationship(back_populates="organized_events", link_model=EventOrganizerLink)
    sessions: list[Session] = Relationship(back_populates="event")
    registrations: list[EventRegistration] = Relationship(back_populates="event")
    organization_id: UUID = Field(foreign_key="organization.id", nullable=True)  # Add foreign key to Organization
    organization: Organization = Relationship(back_populates="events")  # Add relationship to Organization
    details: Optional[EventDetails] = Relationship(back_populates="event")  # One-to-one relationship with EventDetails


# Properties to return via API, id is always required
class EventPublic(EventBase):
    pass


# Properties to return via API for listing events
class Events(SQLModel):
    data: Sequence[EventBase]
    count: int

