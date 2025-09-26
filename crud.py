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
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print(f"\nfound user {username}, {user}\n")
    return user


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="John")
        # await create_user(session=session, username="Sam")
        await get_user_by_username(session=session, username="Sam")
        await get_user_by_username(session=session, username="Bob")


if __name__ == "__main__":
    asyncio.run(main())