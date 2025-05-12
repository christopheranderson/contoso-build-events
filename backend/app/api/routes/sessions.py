from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.event import get_event, get_event_by_slug
from app.crud.session import (
    delete_session_by_slug,
    get_session_by_slug,
    list_sessions_by_event_slug,
    submit_session,
    update_session_by_slug,
)
from app.models import (
    Session,
    SessionStatus,
    SessionSubmit,
    SessionUpdate,
    User,
)

router = APIRouter(tags=["sessions"])


# Session Routes
# Update read_sessions to take in organization_slug and event_slug
@router.get("/orgs/{organization_slug}/e/{event_slug}", response_model=list[Session])
async def read_sessions(
    organization_slug: str,
    event_slug: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await list_sessions_by_event_slug(
        db, organization_slug, event_slug, skip=skip, limit=limit
    )


# Refactor read_session to use organization, event, and session slugs
@router.get(
    "/orgs/{organization_slug}/e/{event_slug}/s/{session_slug}", response_model=Session
)
async def read_session(
    organization_slug: str,
    event_slug: str,
    session_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await get_session_by_slug(db, organization_slug, event_slug, session_slug)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != SessionStatus.SUBMITTED:
        event = await get_event(db, session.event_id)
        if (
            event is not None
            and current_user.id not in [owner.id for owner in event.organizers]
            and current_user.id not in [speaker.id for speaker in session.speakers]
        ):
            raise HTTPException(
                status_code=403, detail="User is not authorized to view this session"
            )

    return session


# Update submit_session route to use the submit_session CRUD method
@router.post("/orgs/{organization_slug}/e/{event_slug}/submit", response_model=Session)
async def submit_session_route(
    organization_slug: str,
    event_slug: str,
    session_in: SessionSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the user is authorized to submit a session for the event
    event = await get_event_by_slug(db, organization_slug, slug=event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.is_private and current_user.id not in [
        owner.id for owner in event.organizers
    ]:
        raise HTTPException(
            status_code=403,
            detail="User is not authorized to submit a session for this event",
        )

    return await submit_session(db, organization_slug, event_slug, session_in)


# Refactor update_session_route to use organization, event, and session slugs
@router.put(
    "/orgs/{organization_slug}/e/{event_slug}/s/{session_slug}", response_model=Session
)
async def update_session_route(
    organization_slug: str,
    event_slug: str,
    session_slug: str,
    session_in: SessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await get_session_by_slug(db, organization_slug, event_slug, session_slug)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    event = await get_event(db, session.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_user.id not in [owner.id for owner in event.organizers]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to update this session"
        )

    return await update_session_by_slug(
        db, organization_slug, event_slug, session_slug, session_in
    )


# Refactor delete_session_route to use organization, event, and session slugs
@router.delete(
    "/orgs/{organization_slug}/e/{event_slug}/s/{session_slug}", status_code=204
)
async def delete_session_route(
    organization_slug: str,
    event_slug: str,
    session_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await get_session_by_slug(db, organization_slug, event_slug, session_slug)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    event = await get_event(db, session.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_user.id not in [owner.id for owner in event.organizers]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to delete this session"
        )

    await delete_session_by_slug(db, organization_slug, event_slug, session_slug)
