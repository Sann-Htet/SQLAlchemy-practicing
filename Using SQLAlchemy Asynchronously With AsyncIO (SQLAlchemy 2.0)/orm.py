from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, select
from typing import List
import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(nullable=False)
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment by {self.user.username}>"
    
# insert data
async def insert_data(sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        async with session.begin():
            session.add_all(
                [
                    User(
                        username="sann123",
                        email="sann123@gmail.com",
                        bio="Really cool guy",
                        comments = [
                            Comment(comment_text="Please like me"),
                            Comment(comment_text="Please like me. I am handsome."),
                        ]
                    ),
                    User(
                        username="htet123",
                        email="htet123@gmail.com",
                        bio="Really cool guy I am",
                    )
                ]
            )
            session.commit()
    
# selecting, updating
async def select_update(sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        statement = select(User).where(
            User.username=="htet123"
        )
        
        result = await session.execute(statement)

        user = result.scalars().one()

        # user.username = "sann899"

        await session.delete(user)

        await session.commit()

async def async_main():
    # create the engine
    engine = create_async_engine(
        "sqlite+aiosqlite:///sample2.db",
        echo = True
    )

    # create a session
    session = async_sessionmaker(bind=engine,
                                 expire_on_commit=False)
    
    async with engine.begin():
        # create db tables
        # await conn.run_sync(Base.metadata.create_all)
        
        # await insert_data(session)

        await select_update(session)

asyncio.run(async_main())