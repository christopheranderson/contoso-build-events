from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional, Sequence
from . import User, Event

# Base model for Organization
class OrganizationBase(SQLModel):
    id: str = Field(primary_key=True, max_length=50)  # User-defined unique ID, such as microsoft
    name: str = Field(max_length=255)
    display_name: Optional[str] = Field(default=None, max_length=255)  # Optional display name
    short_description: str = Field(max_length=500)
    profile_picture: Optional[str] = None  # URL to profile picture
    profile_banner: Optional[str] = None  # URL to profile banner
    contact_email: Optional[str] = Field(default=None, max_length=255)
    linkedin_link: Optional[str] = None  # URL to LinkedIn profile
    github_link: Optional[str] = None  # URL to GitHub profile
    readme: Optional[str] = None  # Markdown-supported longer description

# Properties to receive on organization creation
class OrganizationCreate(OrganizationBase):
    pass

# Properties to receive on organization update
class OrganizationUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)
    short_description: Optional[str] = Field(default=None, max_length=500)
    profile_picture: Optional[str] = None
    profile_banner: Optional[str] = None
    contact_email: Optional[str] = Field(default=None, max_length=255)
    linkedin_link: Optional[str] = None
    github_link: Optional[str] = None
    readme: Optional[str] = None

# Database model for Organization
class Organization(OrganizationBase, table=True):
    admins: List["User"] = Relationship(back_populates="admin_of")
    members: List["User"] = Relationship(back_populates="member_of")
    events: List["Event"] = Relationship(back_populates="organization")

# Properties to return via API for listing organizations
class OrganizationList(SQLModel):
    data: Sequence[OrganizationBase]
    count: int
