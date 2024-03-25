from sqlalchemy import Table, Column, Integer, MetaData, String, Text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
import asyncio


meta = MetaData()

users_table = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=True),
    Column('email', String, nullable=False),
    Column('bio', Text, nullable=False)    
)

async def async_main():
    engine = create_async_engine(
        "sqlite+aiosqlite:///simple.db",
        echo = True
    )

    # connected
    async with engine.begin() as conn:
        # create db
        await conn.run_sync(meta.create_all)

        # insert data into table
        await conn.execute(
            users_table.insert(), [
                {'username': 'sann123',
                 'email': 'sann123@gmail.com',
                 'bio': 'Really cool guy'},
                 {'username': 'htet123',
                 'email': 'htet123@gmail.com',
                 'bio': 'ML Engineer'}
                ]
        )

    # select
    async with engine.connect() as conn:
        statement = select(users_table).where(
            users_table.c.username == 'sann123'
        )

        result = await conn.execute(statement)

        print(result.all())


asyncio.run(async_main())