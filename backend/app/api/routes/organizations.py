from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.models.organization import Organization, OrganizationCreate, OrganizationUpdate, OrganizationList
from app.crud.organization import (
    get_organization, create_organization, update_organization, delete_organization, list_organizations
)
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

# Dependency to check if the user is an admin of the organization
def check_admin(user: User, organization: Organization):
    if user.id not in [admin.id for admin in organization.admins]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )

# List organizations (public)
@router.get("/organizations", response_model=OrganizationList)
async def list_organizations_route(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await list_organizations(db=db, skip=skip, limit=limit)

# Get organization by ID (public)
@router.get("/organizations/{organization_id}", response_model=Organization)
async def get_organization_route(
    organization_id: str, db: AsyncSession = Depends(get_db)
):
    organization = await get_organization(db=db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    return organization

# Create organization (admin only)
@router.post("/organizations", response_model=Organization)
async def create_organization_route(
    organization_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization = await create_organization(db=db, obj_in=organization_in)
    organization.admins.append(current_user)  # Add the creator as an admin
    return organization

# Update organization (admin only)
@router.put("/organizations/{organization_id}", response_model=Organization)
async def update_organization_route(
    organization_id: str,
    organization_in: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization = await get_organization(db=db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    check_admin(current_user, organization)
    return await update_organization(db=db, db_obj=organization, obj_in=organization_in)

# Delete organization (admin only)
@router.delete("/organizations/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization_route(
    organization_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization = await get_organization(db=db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    check_admin(current_user, organization)
    await delete_organization(db=db, id=organization_id)
