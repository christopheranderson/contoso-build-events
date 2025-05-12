from sqlmodel import func as sqlmodel_func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    Organization,
    OrganizationCreate,
    OrganizationList,
    OrganizationUpdate,
)


async def get_organization(db: AsyncSession, id: str) -> Organization | None:
    result = await db.exec(select(Organization).where(Organization.id == id))
    return result.one_or_none()


async def create_organization(
    db: AsyncSession, obj_in: OrganizationCreate
) -> Organization:
    db_obj = Organization(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_organization(
    db: AsyncSession, db_obj: Organization, obj_in: OrganizationUpdate
) -> Organization:
    obj_data = db_obj.model_dump()
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_organization(db: AsyncSession, id: str) -> None:
    db_obj = await get_organization(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()


async def list_organizations(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> OrganizationList:
    result = await db.exec(select(Organization).offset(skip).limit(limit))
    organizations = result.all()
    count_result = await db.exec(
        select(sqlmodel_func.count()).select_from(Organization)
    )
    count = count_result.one()
    return OrganizationList(data=organizations, count=count)


# Add get_organization_by_slug
async def get_organization_by_slug(db: AsyncSession, slug: str) -> Organization | None:
    result = await db.exec(select(Organization).where(Organization.slug == slug))
    return result.one_or_none()


# Add update_organization_by_slug
async def update_organization_by_slug(
    db: AsyncSession, slug: str, obj_in: OrganizationUpdate
) -> Organization:
    db_obj = await get_organization_by_slug(db, slug)
    if not db_obj:
        raise ValueError("Organization not found")
    obj_data = db_obj.model_dump()
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


# Add delete_organization_by_slug
async def delete_organization_by_slug(db: AsyncSession, slug: str) -> None:
    db_obj = await get_organization_by_slug(db, slug)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
