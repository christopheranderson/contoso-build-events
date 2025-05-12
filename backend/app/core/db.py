from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, SQLModel, create_engine, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.core.config import settings
from app.models import Organization, OrganizationCreate, User, UserCreate

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

fake = Faker()

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


async def init_db(session: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    print("Creating database tables...")
    # SQLModel.metadata.create_all(engine)

    user = (await session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    )).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    await initialize_with_sample_data(session=session)


async def initialize_with_sample_data(session: AsyncSession) -> None:
    org_count = (await session.exec(
        select(func.count()).select_from(Organization)
    )).one()

    if org_count > 9:
        print("Sample data already exists. Skipping creation.")
        return
    else:
        print(f"Only saw {org_count} sample organizations. Creating more...")

    org_in = OrganizationCreate(
        name="Contoso",
        display_name="Contoso Inc",
        short_description="Contoso is a leading provider of business solutions.",
        slug="contoso",
    )

    await crud.organization.create_organization(db=session, obj_in=org_in)

    # Create 10 sample organizations
    for i in range(1, 11):
        company_name = fake.company()
        org_in = OrganizationCreate(
            name=company_name,
            display_name=company_name,
            short_description=fake.catch_phrase(),
            slug=company_name.lower().replace(" ", "-"),
        )
        await crud.organization.create_organization(db=session, obj_in=org_in)
