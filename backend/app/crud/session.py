from uuid import UUID

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    Event,  # Import Event model
    Session,
    SessionCreate,
    SessionRegistration,
    SessionRegistrationCreate,
    SessionRegistrations,
    SessionRegistrationUpdate,
    SessionReview,
    SessionReviewCreate,
    SessionReviews,
    SessionReviewUpdate,
    Sessions,
    SessionStatus,
    SessionSubmit,
    SessionUpdate,
)


# Session CRUD
async def get_session(db: AsyncSession, id: UUID) -> Session | None:
    result = await db.exec(select(Session).where(Session.id == id))
    return result.one_or_none()


async def create_session(db: AsyncSession, obj_in: SessionCreate) -> Session:
    db_obj = Session(**obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_session(
    db: AsyncSession, db_obj: Session, obj_in: SessionUpdate
) -> Session:
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_session(db: AsyncSession, id: UUID) -> None:
    db_obj = await get_session(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


async def get_sessions(db: AsyncSession, skip: int = 0, limit: int = 10) -> Sessions:
    result = await db.exec(select(Session).offset(skip).limit(limit))
    sessions = result.all()
    count_result = await db.exec(select(func.count()).select_from(Session))
    count = count_result.one_or_none() or 0  # Directly use scalar value or default to 0
    return Sessions(data=sessions, count=count)


# Add get_session_by_slug
async def get_session_by_slug(
    db: AsyncSession, organization_slug: str, event_slug: str, session_slug: str
) -> Session | None:
    result = await db.exec(
        select(Session).where(
            Session.event.organization.slug == organization_slug,
            Session.event.slug == event_slug,
            Session.slug == session_slug,
        )
    )
    return result.one_or_none()


# Add update_session_by_slug
async def update_session_by_slug(
    db: AsyncSession,
    organization_slug: str,
    event_slug: str,
    session_slug: str,
    obj_in: SessionUpdate,
) -> Session:
    db_obj = await get_session_by_slug(db, organization_slug, event_slug, session_slug)
    if not db_obj:
        raise ValueError("Session not found")
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


# Add delete_session_by_slug
async def delete_session_by_slug(
    db: AsyncSession, organization_slug: str, event_slug: str, session_slug: str
) -> None:
    db_obj = await get_session_by_slug(db, organization_slug, event_slug, session_slug)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


# Add list_sessions_by_event_slug
async def list_sessions_by_event_slug(
    db: AsyncSession,
    organization_slug: str,
    event_slug: str,
    skip: int = 0,
    limit: int = 10,
) -> Sessions:
    result = await db.exec(
        select(Session)
        .where(
            Session.event.organization.slug == organization_slug,
            Session.event.slug == event_slug,
        )
        .offset(skip)
        .limit(limit)
    )
    sessions = result.all()
    count_result = await db.exec(
        select(func.count())
        .select_from(Session)
        .where(
            Session.event.organization.slug == organization_slug,
            Session.event.slug == event_slug,
        )
    )
    count = count_result.one_or_none() or 0
    return Sessions(data=sessions, count=count)


# SessionRegistration CRUD
async def get_session_registration(
    db: AsyncSession, id: UUID
) -> SessionRegistration | None:
    result = await db.exec(
        select(SessionRegistration).where(SessionRegistration.id == id)
    )
    return result.one_or_none()


async def create_session_registration(
    db: AsyncSession, obj_in: SessionRegistrationCreate
) -> SessionRegistration:
    db_obj = SessionRegistration(**obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_session_registration(
    db: AsyncSession, db_obj: SessionRegistration, obj_in: SessionRegistrationUpdate
) -> SessionRegistration:
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_session_registration(db: AsyncSession, id: UUID) -> None:
    db_obj = await get_session_registration(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


async def get_session_registrations(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> SessionRegistrations:
    result = await db.exec(select(SessionRegistration).offset(skip).limit(limit))
    registrations = result.all()
    count_result = await db.exec(select(func.count()).select_from(SessionRegistration))
    count = count_result.one_or_none() or 0  # Directly use scalar value or default to 0
    return SessionRegistrations(data=registrations, count=count)


# SessionReview CRUD
async def get_session_review(db: AsyncSession, id: UUID) -> SessionReview | None:
    result = await db.exec(select(SessionReview).where(SessionReview.id == id))
    return result.one_or_none()


async def create_session_review(
    db: AsyncSession, obj_in: SessionReviewCreate
) -> SessionReview:
    db_obj = SessionReview(**obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_session_review(
    db: AsyncSession, db_obj: SessionReview, obj_in: SessionReviewUpdate
) -> SessionReview:
    obj_data = db_obj.dict()
    update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_session_review(db: AsyncSession, id: UUID) -> None:
    db_obj = await get_session_review(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


async def get_session_reviews(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> SessionReviews:
    result = await db.exec(select(SessionReview).offset(skip).limit(limit))
    reviews = result.all()
    count_result = await db.exec(select(func.count()).select_from(SessionReview))
    count = count_result.one_or_none() or 0  # Directly use scalar value or default to 0
    return SessionReviews(data=reviews, count=count)


# Add submit_session method
async def submit_session(
    db: AsyncSession, organization_slug: str, event_slug: str, session_in: SessionSubmit
) -> Session:
    # Fetch the event by organization and event slug
    event = await db.exec(
        select(Event).where(
            Event.organization.slug == organization_slug, Event.slug == event_slug
        )
    )
    event = event.one_or_none()
    if not event:
        raise ValueError("Event not found")

    # Create the session
    db_obj = Session(
        title=session_in.title,
        short_description=session_in.short_description,
        abstract=session_in.abstract,
        level=session_in.level,
        tags=session_in.tags,
        event_id=event.id,
        status=SessionStatus.SUBMITTED,
        slug=session_in.title.replace(" ", "-").lower(),
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
