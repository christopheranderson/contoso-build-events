from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.event import (
    create_event,
    create_event_details,
    create_event_registration,
    delete_event_by_slug,
    delete_event_registration,
    get_event_by_slug,
    get_event_details_by_slug,
    get_event_registration,
    get_events_by_organization_slug,
    update_event_by_slug,
    update_event_details,
    update_event_registration,
)
from app.crud.organization import get_organization, get_organization_by_slug
from app.models import (
    Event,
    EventCreate,
    EventDetails,
    EventDetailsCreate,
    EventDetailsUpdate,
    EventRegistration,
    EventRegistrationCreate,
    EventRegistrationUpdate,
    EventUpdate,
    User,
)

router = APIRouter(tags=["events"])


# Event Routes
@router.get("/orgs/{organization_slug}/e/", response_model=list[Event])
async def read_events(
    organization_slug: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await get_events_by_organization_slug(
        db, organization_slug, skip=skip, limit=limit
    )


@router.get("/orgs/{organization_slug}/e/{event_slug}", response_model=Event)
async def read_event(
    organization_slug: str,
    event_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.is_private:
        organization = await get_organization(db, event.organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        if current_user.id not in [
            admin.id for admin in organization.admins
        ] and current_user.id not in [member.id for member in organization.members]:
            raise HTTPException(
                status_code=403,
                detail="User is not authorized to view this private event",
            )

    return event


@router.post("/orgs/{organization_slug}/e/", response_model=Event)
async def create_new_event(
    organization_slug: str,
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    organization = await get_organization_by_slug(db, organization_slug)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    if current_user.id not in [
        admin.id for admin in organization.admins
    ] and current_user.id not in [member.id for member in organization.members]:
        raise HTTPException(
            status_code=403, detail="User is not an admin or member of the organization"
        )

    return await create_event(db, event_in)


@router.put("/orgs/{organization_slug}/e/{event_slug}", response_model=Event)
async def update_existing_event(
    organization_slug: str,
    event_slug: str,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    organization = await get_organization(db, event.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    if current_user.id not in [
        admin.id for admin in organization.admins
    ] and current_user.id not in [admin.id for admin in event.organizers]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to update this event"
        )

    return await update_event_by_slug(db, organization_slug, event_slug, event_in)


@router.delete("/orgs/{organization_slug}/e/{event_slug}", status_code=204)
async def delete_existing_event(
    organization_slug: str,
    event_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    organization = await get_organization(db, event.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    if current_user.id not in [
        admin.id for admin in organization.admins
    ] and current_user.id not in [admin.id for admin in event.organizers]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to delete this event"
        )

    await delete_event_by_slug(db, organization_slug, event_slug)


# EventDetails Routes
@router.get(
    "/orgs/{organization_slug}/e/{event_slug}/details", response_model=EventDetails
)
async def read_event_details(
    organization_slug: str, event_slug: str, db: AsyncSession = Depends(get_db)
):
    details = await get_event_details_by_slug(db, organization_slug, event_slug)
    if not details:
        raise HTTPException(status_code=404, detail="Event details not found")
    return details


@router.post(
    "/orgs/{organization_slug}/e/{event_slug}/details", response_model=EventDetails
)
async def create_event_details_route(
    organization_slug: str,
    event_slug: str,
    details_in: EventDetailsCreate,
    db: AsyncSession = Depends(get_db),
):
    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return await create_event_details(db, details_in, event.id)


@router.put(
    "/orgs/{organization_slug}/e/{event_slug}/details", response_model=EventDetails
)
async def update_event_details_route(
    organization_slug: str,
    event_slug: str,
    details_in: EventDetailsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    details = await get_event_details_by_slug(db, organization_slug, event_slug)
    if not details:
        raise HTTPException(status_code=404, detail="Event details not found")

    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_user.id not in [
        admin.id for admin in event.organization.admins
    ] and current_user.id not in [admin.id for admin in event.organizers]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to update event details"
        )

    return await update_event_details(db, details, details_in)


# EventRegistration Routes
@router.get(
    "/orgs/{organization_slug}/e/{event_slug}/registrations/{registration_id}",
    response_model=EventRegistration,
)
async def read_event_registration(
    organization_slug: str,
    event_slug: str,
    registration_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registration = await get_event_registration(db, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Event registration not found")

    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event or event.id != registration.event_id:
        raise HTTPException(status_code=404, detail="Event not found")

    if (
        current_user.id != registration.user_id
        and current_user.id not in [admin.id for admin in event.organization.admins]
        and current_user.id not in [owner.id for owner in event.organizers]
    ):
        raise HTTPException(
            status_code=403, detail="User is not authorized to view this registration"
        )

    return registration


@router.post(
    "/orgs/{organization_slug}/e/{event_slug}/registrations/",
    response_model=EventRegistration,
)
async def create_event_registration_route(
    organization_slug: str,
    event_slug: str,
    registration_in: EventRegistrationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.is_private:
        organization = await get_organization(db, event.organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        if current_user.id not in [
            admin.id for admin in organization.admins
        ] and current_user.id not in [member.id for member in organization.members]:
            raise HTTPException(
                status_code=403,
                detail="User is not authorized to register for this private event",
            )

    if registration_in.event_id != event.id:
        raise HTTPException(
            status_code=400, detail="Event ID in registration does not match event slug"
        )
    if (
        current_user.id not in [admin.id for admin in event.organization.admins]
        and registration_in.user_id != current_user.id
    ):  # Ensure the registration is for the current user or the user is an event admin
        raise HTTPException(
            status_code=400,
            detail="User ID in registration does not match current user",
        )

    return await create_event_registration(db, registration_in)


@router.put(
    "/orgs/{organization_slug}/e/{event_slug}/registrations/{registration_id}",
    response_model=EventRegistration,
)
async def update_event_registration_route(
    organization_slug: str,
    event_slug: str,
    registration_id: UUID,
    registration_in: EventRegistrationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registration = await get_event_registration(db, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Event registration not found")

    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event or event.id != registration.event_id:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_user.id != registration.user_id and current_user.id not in [
        admin.id for admin in event.organization.admins
    ]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to update this registration"
        )

    return await update_event_registration(db, registration, registration_in)


@router.delete(
    "/orgs/{organization_slug}/e/{event_slug}/registrations/{registration_id}",
    status_code=204,
)
async def delete_event_registration_route(
    organization_slug: str,
    event_slug: str,
    registration_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registration = await get_event_registration(db, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Event registration not found")

    event = await get_event_by_slug(db, organization_slug, event_slug)
    if not event or event.id != registration.event_id:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_user.id != registration.user_id and current_user.id not in [
        admin.id for admin in event.organization.admins
    ]:
        raise HTTPException(
            status_code=403, detail="User is not authorized to delete this registration"
        )

    await delete_event_registration(db, registration_id)
