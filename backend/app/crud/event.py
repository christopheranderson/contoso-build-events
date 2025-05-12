from uuid import UUID

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    Event,
    EventCreate,
    EventDetails,
    EventDetailsCreate,
    EventDetailsUpdate,
    EventRegistration,
    EventRegistrationCreate,
    EventRegistrationUpdate,
    Events,
    EventUpdate,
)


# Event CRUD
async def get_event(db: AsyncSession, id: UUID) -> Event | None:
    result = await db.exec(select(Event).where(Event.id == id))
    return result.one_or_none()


async def create_event(db: AsyncSession, obj_in: EventCreate) -> Event:
    db_obj = Event(**obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_event(db: AsyncSession, db_obj: Event, obj_in: EventUpdate) -> Event:
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_event(db: AsyncSession, id: UUID) -> None:
    db_obj = await get_event(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 10) -> Events:
    result = await db.exec(select(Event).offset(skip).limit(limit))
    events = result.all()
    count_result = await db.exec(select(func.count()).select_from(Event))
    count = count_result.one_or_none() or 0
    return Events(data=events, count=count)


# Add get_event_by_slug
async def get_event_by_slug(
    db: AsyncSession, organization_slug: str, slug: str
) -> Event | None:
    result = await db.exec(
        select(Event).where(
            Event.organization.slug == organization_slug, Event.slug == slug
        )
    )
    return result.one_or_none()


# Add update_event_by_slug
async def update_event_by_slug(
    db: AsyncSession, organization_slug: str, slug: str, obj_in: EventUpdate
) -> Event:
    db_obj = await get_event_by_slug(db, organization_slug, slug)
    if not db_obj:
        raise ValueError("Event not found")
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


# Add delete_event_by_slug
async def delete_event_by_slug(
    db: AsyncSession, organization_slug: str, slug: str
) -> None:
    db_obj = await get_event_by_slug(db, organization_slug, slug)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


# EventDetails CRUD
async def get_event_details(db: AsyncSession, event_id: UUID) -> EventDetails | None:
    result = await db.exec(
        select(EventDetails).where(EventDetails.event_id == event_id)
    )
    return result.one_or_none()


async def create_event_details(
    db: AsyncSession, obj_in: EventDetailsCreate, event_id: UUID
) -> EventDetails:
    db_obj = EventDetails(event_id=event_id, **obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_event_details(
    db: AsyncSession, db_obj: EventDetails, obj_in: EventDetailsUpdate
) -> EventDetails:
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_event_details(db: AsyncSession, event_id: UUID) -> None:
    db_obj = await get_event_details(db, event_id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


# EventRegistration CRUD
async def get_event_registration(
    db: AsyncSession, id: UUID
) -> EventRegistration | None:
    result = await db.exec(select(EventRegistration).where(EventRegistration.id == id))
    return result.one_or_none()


async def create_event_registration(
    db: AsyncSession, obj_in: EventRegistrationCreate
) -> EventRegistration:
    db_obj = EventRegistration(**obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_event_registration(
    db: AsyncSession, db_obj: EventRegistration, obj_in: EventRegistrationUpdate
) -> EventRegistration:
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_event_registration(db: AsyncSession, id: UUID) -> None:
    db_obj = await get_event_registration(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


# Add get_event_details_by_slug
async def get_event_details_by_slug(
    db: AsyncSession, organization_slug: str, event_slug: str
) -> EventDetails | None:
    result = await db.exec(
        select(EventDetails)
        .join(Event)
        .where(Event.organization.slug == organization_slug, Event.slug == event_slug)
    )
    return result.one_or_none()


# Function to fetch events by organization slug
async def get_events_by_organization_slug(
    db: AsyncSession, organization_slug: str, skip: int = 0, limit: int = 10
) -> list[Event]:
    result = await db.exec(
        select(Event)
        .where(Event.organization.slug == organization_slug)
        .offset(skip)
        .limit(limit)
    )
    return list(result.all())
