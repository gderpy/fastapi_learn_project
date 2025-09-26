import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)

    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()

    user: User | None = await session.scalar(stmt)
    print(f"\nfound user {username}, {user}\n")
    return user


async def create_user_profile(
        session: AsyncSession, 
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="John")
        # await create_user(session=session, username="Sam")
        user_sam = await get_user_by_username(session=session, username="Sam")
        user_john = await get_user_by_username(session=session, username="John")
        # await get_user_by_username(session=session, username="Bob")

        await create_user_profile(
            session=session, 
            user_id=user_john.id,
            first_name="John"
        )

        await create_user_profile(
            session=session, 
            user_id=user_sam.id,
            first_name="Sam",
            last_name="White"
        )


if __name__ == "__main__":
    asyncio.run(main())